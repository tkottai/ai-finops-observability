Overview:


Here is a simulated Finops + Observability solution for tracking AI workloads. The purpose of this solution is to build a cost and workload tracking dashboard for AI deployments in your organization. As soon as you run this solution, a trace will start tracking all your AI deployments. It will track every step your AI is making + calculating the costs of tokens by drilling down to the workloads happening in your datacenter. 


Here is the functional flow of how each of these data points is being collected - 

1) Start by using your AI, submit a prompt or run an Agent
2) A trace has begun, with details about every action your AI or Agent is taking
3) Retrieves context, request goes to LLM, LLM runs the model on GPU/Neural Engine
4) An AI generation or Agentic AI action is presented as the output, either user can submit an additional prompt or the next step in Agentic chain is auto executed
5) Metrics collected in parallel -
      Token usage & latency → OpenTelemetry + Langfuse
      CPU / Memory → Node Exporter
      GPU usage %, power (watts), temperature → macmon
7) Cost service calculates token costs and estimated energy cost (using GPU power draw × time)
8) Everything appears in FinOps Dashboard

<img width="1458" height="1278" alt="image" src="https://github.com/user-attachments/assets/2259ad3d-984e-4833-b8ec-0e6a768c90a7" />
<img width="2270" height="1210" alt="image" src="https://github.com/user-attachments/assets/f44a7c0d-ae47-4094-986e-dcc2313a181a" />
<img width="2514" height="1262" alt="image" src="https://github.com/user-attachments/assets/6b4478fe-b848-4b58-85a5-759fc609ee84" />





































Calculations:

Estimated Cost = (Token Cost) + (GPU Power × Duration × Electricity Rate) + (Memory Pressure Factor)


Sample token costs for input and outputs - 
<img width="430" height="585" alt="Screenshot 2026-08-14 at 6 11 22 PM" src="https://github.com/user-attachments/assets/e1970ff8-b010-4110-9cc8-5c5fa385440a" />


Below are the tools I'm using:
1) Instrumentation - OpenTelemetry
2) Metrics Storage - Prometheus
3) Visualization - Grafana
4) CPU/Host Metrics - Prometheus Node Explorer
5) GPU Metrics: Macmon - Prometheus endpoint
6) Tracing - Grafana Tempo - Full journey of a request
7) Logs - Loki - Searches application logs
8) Orchestration - Docker Compose
9) Inference Engine - Ollama
10) LLM Observability - Langfuse - Deep observability for LLM prompts, costs, and quality
11) RAG Evaluation - RAGAS - Helps automatically test and score whether your RAG system is giving accurate, grounded, and useful answers.
12) Cost / FinOps - Custom Tool
13) Frontend - Streamlit

## Baseline Architecture

This repository currently documents a simulated reference architecture. The diagram below separates the AI workload, telemetry pipeline, cost calculation, and visualization layers that a full implementation would connect.

```mermaid
flowchart TB
    User["User or agent trigger"] --> App["AI application or agent"]
    App --> RAG["Retrieval and tool calls"]
    RAG --> Ollama["Ollama inference"]

    App -. traces .-> OTel["OpenTelemetry"]
    App -. LLM events .-> Langfuse["Langfuse"]
    Host["Host CPU and memory"] -. metrics .-> Node["Node Exporter"]
    GPU["GPU power and utilization"] -. metrics .-> Macmon["macmon exporter"]

    OTel --> Tempo["Grafana Tempo"]
    App -. logs .-> Loki["Grafana Loki"]
    Node --> Prom["Prometheus"]
    Macmon --> Prom
    Langfuse --> Cost["Custom cost calculator"]
    Prom --> Cost

    Tempo --> Grafana["Grafana FinOps dashboard"]
    Loki --> Grafana
    Prom --> Grafana
    Cost --> Grafana
```

Architectural Flow:

```mermaid
sequenceDiagram
    actor User
    participant App as AI Application
    participant LLM as Ollama
    participant Telemetry as Telemetry Stack
    participant Cost as Cost Service
    participant Dash as Grafana

    User->>App: Submit prompt or start agent
    App->>Telemetry: Start trace and record metadata
    App->>LLM: Send prompt and retrieved context
    LLM-->>App: Return generation or tool decision
    App->>Telemetry: Record tokens, latency, logs and spans
    LLM->>Telemetry: Export host and GPU metrics
    Telemetry->>Cost: Supply usage and duration measurements
    Cost->>Cost: Calculate token and estimated energy cost
    Cost-->>Dash: Publish cost metrics
    Telemetry-->>Dash: Publish traces, logs and infrastructure metrics
    Dash-->>User: Display workload and cost views
```

Control and Deployment Boundaries

- Docker Compose is the proposed local orchestration boundary for Prometheus, Grafana, Tempo, Loki, Langfuse, Ollama, and supporting services.
- `macmon` remains outside Docker and exposes GPU-related metrics on TCP 9101.
- Node Exporter exposes host metrics on TCP 9100; Prometheus scrapes the configured exporters on TCP 9090.
- The cost formula is an estimate and should be labeled separately from provider-billed cost.
- No executable observability stack is currently checked into this repository; configuration files and application instrumentation remain implementation work.
