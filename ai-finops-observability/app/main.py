from fastapi import FastAPI, Response
from pydantic import BaseModel
import httpx
import time
import os
from otel_setup import setup_otel
from cost_calculator import calculate_cost
from dotenv import load_dotenv
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST") or os.getenv("LANGFUSE_BASE_URL")
)

app = FastAPI(title="AI FinOps Observability", version="0.4.7")
setup_otel(app)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")


class Query(BaseModel):
    prompt: str
    model: str = "llama3.2"
    pricing_model: str = "local"


@app.get("/")
def root():
    return {"message": "AI FinOps Observability is running"}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/generate")
async def generate(query: Query):
    start_time = time.time()

    trace = langfuse.trace(
        name="ollama-generate",
        input={"prompt": query.prompt},
        metadata={
            "model": query.model,
            "pricing_model": query.pricing_model
        }
    )

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": query.model,
                    "prompt": query.prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            data = response.json()

        duration = time.time() - start_time
        prompt_tokens = data.get("prompt_eval_count", 0)
        completion_tokens = data.get("eval_count", 0)
        output_text = data.get("response", "")

        cost = calculate_cost(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            duration_sec=duration,
            pricing_model=query.pricing_model
        )

        trace.generation(
            name="ollama-completion",
            model=query.model,
            input=query.prompt,
            output=output_text,
            usage={
                "input": prompt_tokens,
                "output": completion_tokens,
                "total": prompt_tokens + completion_tokens
            },
            metadata={
                "duration_sec": round(duration, 3),
                "total_cost_usd": cost["total_cost_usd"],
                "gpu_power_watts": cost.get("gpu_power_watts")
            }
        )

        trace.update(output=output_text)

        return {
            "model": query.model,
            "response": output_text,
            "tokens": {
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": prompt_tokens + completion_tokens
            },
            "cost": cost,
            "duration_sec": round(duration, 3)
        }

    finally:
        langfuse.flush()


@app.get("/health")
def health():
    return {"status": "healthy"}
