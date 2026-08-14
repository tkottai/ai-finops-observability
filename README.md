Overview:


For large enterprises that are building out Agentic AI use cases, one of the most important elements is the AI costing, observability and performance. There are a lot of strategies you can use to build out a better architecture to integrate all of the layers in the technical stack. Building a stack that will track everything at the chip level to inference level is very important to not only observe the costs, but also the uptime / upkeep. In this example, i've built out a simulated Finops + Observability solutions:


Instrumentation: OpenTelemetry
Metrics Storage: Prometheus
Visualization: Grafana
CPU/Host Metrics: Prometheus Node Explorer
GPU Metrics: Macmon - Prometheus endpoint
Tracing - Grafana Tempo - Full journey of a request
Logs - Loki - Searches application logs
Orchestration - Docker Compose
Inference Engine - Ollama
LLM Observability - Langfuse - Deep observability for LLM prompts, costs, and quality
RAG Evaluation - RAGAS - Helps automatically test and score whether your RAG system is giving accurate, grounded, and useful answers.
Cost / FinOps - Custom Tool
Frontend - Streamlit


Functional Flow:

1) Send a prompt request via Streamlit
2) OpenTelemetry starts a trace
3) RAG retrieves context
4) Request goes to Ollama (LLM)
5) Ollama runs the model on GPU/Neural Engine
6) Metrics collected in parallel-
      Token usage & latency → OpenTelemetry + Langfuse
      CPU / Memory → Node Exporter
      GPU usage %, power (watts), temperature → macmon
7) Cost service calculates token costs and estimated energy cost (using GPU power draw × time)
8) Everything appears in Grafana dashboards (and Langfuse UI).




Appendix:

Important Ports-
FastAPI App 
TCP 8000
http://localhost:8000

Prometheus 
TCP 9090
http://localhost:9090

Grafana 
TCP 3000
http://localhost:3000
Colima VM -> Docker Container -> Grafana container TCP listens to port 3000 .YML -> Grafana application
The VM recieves the HTTPS/TCP connection coming from your Mac and routes it into the correct container (speaks HTTPS/TCP).

macmon - not in docker 
TCP 9101
http://localhost:9101/metrics

Node Exporter
TCP 9100

---
Estimated Cost = (Token Cost) + (GPU Power × Duration × Electricity Rate) + (Memory Pressure Factor)
--
Key files-
docker-compose.yml
Dockerfile
requirements.txt
.env
monitoring/prometheus.yml
app/main.py
app/otel_setup.py
app/cost_calculator.py
frontend/app .py
---
YAML - Configuration data format

---
<img width="430" height="585" alt="Screenshot 2026-08-14 at 6 11 22 PM" src="https://github.com/user-attachments/assets/e1970ff8-b010-4110-9cc8-5c5fa385440a" />

---
Token - Small piece of text
Embedding - Numerical representation of meaning
Vector - List of numbers
Similarity - How close two vectors are (cosine)
Embedding model - AI model that creates the vectors

