import requests
from typing import Optional, Dict

# Realistic pricing models (per 1K tokens)
PRICING_MODELS = {
    "local": {
        "input": 0.00015,
        "output": 0.0006,
        "name": "Local (Mac)"
    },
    "openai_luna": {
        "input": 0.0002,      # $0.20 per 1M = $0.0002 per 1K
        "output": 0.0012,     # $1.20 per 1M
        "name": "OpenAI GPT-5.6 Luna"
    },
    "openai_sol": {
        "input": 0.005,       # $5.00 per 1M
        "output": 0.030,      # $30.00 per 1M
        "name": "OpenAI GPT-5.6 Sol"
    },
    "anthropic_haiku": {
        "input": 0.001,       # $1.00 per 1M
        "output": 0.005,      # $5.00 per 1M
        "name": "Claude Haiku 4.5"
    },
    "anthropic_opus": {
        "input": 0.005,       # $5.00 per 1M
        "output": 0.025,      # $25.00 per 1M
        "name": "Claude Opus 4.8"
    },
    "kimi_k3": {
        "input": 0.003,       # $3.00 per 1M
        "output": 0.015,      # $15.00 per 1M
        "name": "Kimi K3"
    }
}


def get_current_gpu_power() -> float:
    """Fetch real GPU power from Prometheus (macmon)."""
    try:
        response = requests.get(
            "http://prometheus:9090/api/v1/query",
            params={"query": "macmon_gpu_power_watts"},
            timeout=2
        )
        data = response.json()
        if data["status"] == "success" and data["data"]["result"]:
            return float(data["data"]["result"][0]["value"][1])
    except Exception as e:
        print(f"Could not fetch GPU power: {e}")
    return 7.5  # fallback


def calculate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    duration_sec: float = 0.0,
    pricing_model: str = "local",
    gpu_power_watts: Optional[float] = None
) -> Dict:
    """
    Calculate cost using different pricing models + real GPU power.
    """

    model = PRICING_MODELS.get(pricing_model, PRICING_MODELS["local"])

    # Token cost
    token_cost = (prompt_tokens / 1000 * model["input"]) + \
                 (completion_tokens / 1000 * model["output"])

    # Real GPU power
    if gpu_power_watts is None:
        gpu_power_watts = get_current_gpu_power()

    # Energy cost ($0.15 per kWh example)
    energy_kwh = (gpu_power_watts * duration_sec) / 3600
    energy_cost = energy_kwh * 0.15

    total_cost = token_cost + energy_cost

    return {
        "pricing_model": model["name"],
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "gpu_power_watts": round(gpu_power_watts, 2),
        "token_cost_usd": round(token_cost, 6),
        "energy_cost_usd": round(energy_cost, 6),
        "total_cost_usd": round(total_cost, 6)
    }
