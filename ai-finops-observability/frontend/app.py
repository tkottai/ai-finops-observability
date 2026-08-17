import streamlit as st
import requests

st.set_page_config(
    page_title="AI FinOps Observability",
    page_icon="📊",
    layout="centered"
)

st.title("AI FinOps Observability")
st.markdown("Local LLM Observability + Cost Tracking on Apple Silicon")

# Sidebar
st.sidebar.header("Settings")

model = st.sidebar.selectbox(
    "LLM Model",
    ["llama3.2", "llama3.2:3b", "mistral", "phi3"],
    index=0
)

pricing_model = st.sidebar.selectbox(
    "Pricing Model",
    [
        "local",
        "openai_luna",
        "openai_sol",
        "anthropic_haiku",
        "anthropic_opus",
        "kimi_k3"
    ],
    format_func=lambda x: {
        "local": "Local (Mac)",
        "openai_luna": "OpenAI GPT-5.6 Luna",
        "openai_sol": "OpenAI GPT-5.6 Sol",
        "anthropic_haiku": "Claude Haiku 4.5",
        "anthropic_opus": "Claude Opus 4.8",
        "kimi_k3": "Kimi K3"
    }[x],
    index=0
)

api_url = st.sidebar.text_input("API URL", value="http://localhost:8000/generate")

# Main area
prompt = st.text_area(
    "Enter your prompt:",
    height=150,
    placeholder="e.g. Explain observability in simple terms..."
)

if st.button("Generate", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating response..."):
            try:
                response = requests.post(
                    api_url,
                    json={
                        "prompt": prompt,
                        "model": model,
                        "pricing_model": pricing_model
                    },
                    timeout=120
                )
                response.raise_for_status()
                data = response.json()

                st.subheader("Response")
                st.write(data.get("response", "No response received."))

                st.subheader("Request Metrics")
                tokens = data.get("tokens", {})
                cost = data.get("cost", {})

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Prompt Tokens", tokens.get("prompt", 0))
                col2.metric("Completion Tokens", tokens.get("completion", 0))
                col3.metric("Total Tokens", tokens.get("total", 0))
                col4.metric("Duration (s)", data.get("duration_sec", 0))

                st.subheader("Cost Breakdown")
                st.caption(f"Pricing Model: **{cost.get('pricing_model', 'N/A')}**")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("GPU Power (W)", cost.get("gpu_power_watts", 0))
                col2.metric("Token Cost", f"${cost.get('token_cost_usd', 0):.6f}")
                col3.metric("Energy Cost", f"${cost.get('energy_cost_usd', 0):.6f}")
                col4.metric("Total Cost", f"${cost.get('total_cost_usd', 0):.6f}")

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("AI FinOps Observability • Running locally on Apple Silicon")
