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
<img width="2270" height="1210" alt="image" src="https://github.com/user-attachments/assets/41161bc8-d472-4d05-8d40-464f2ad2d45e" />
<img width="2514" height="1262" alt="image" src="https://github.com/user-attachments/assets/cdaf2399-a618-4b6e-b094-6550d7adf42c" />



































Appendix:

Important Ports-
- FastAPI App TCP 8000
- Prometheus TCP 9090
- Grafana TCP 3000
Colima VM -> Docker Container -> Grafana container TCP listens to port 3000 .YML -> Grafana application
The VM recieves the HTTPS/TCP connection coming from your Mac and routes it into the correct container (speaks HTTPS/TCP).
- macmon - not in docker -TCP 9101
- Node Exporter - TCP 9100

Calculations - 
Estimated Cost = (Token Cost) + (GPU Power × Duration × Electricity Rate) + (Memory Pressure Factor)

YAML - Configuration data format

Sample token costs for input and outputs - 
<img width="430" height="585" alt="Screenshot 2026-08-14 at 6 11 22 PM" src="https://github.com/user-attachments/assets/e1970ff8-b010-4110-9cc8-5c5fa385440a" />


Token - Small piece of text
Embedding - Numerical representation of meaning
Vector - List of numbers
Similarity - How close two vectors are (cosine)
Embedding model - AI model that creates the vectors

Below are the tools I'm using - 
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
