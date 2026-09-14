# DeepEval RAG & Agent Project

This repository contains an intelligent Agentic Retrieval-Augmented Generation (RAG) system built with LangChain and LangGraph, paired with a comprehensive evaluation suite powered by DeepEval.

The project is structured into two main components:
1. **Research Agent (`research-agent/`)**: A conversational agent that uses tools to fetch internal knowledge (via ChromaDB), search the web (via Tavily), maintain long-term memory across interactions, and an MCP (Model Context Protocol) server for tool integration.
2. **LLM Evaluation (`llm-eval/`)**: A suite of automated evaluation scripts that use `deepeval` to test the agent's performance, memory consistency, safety, MCP tool usage, and reasoning capabilities using various metrics.

## 📁 Project Structure

- `research-agent/`: Contains the core agent implementation (`agent.py`), data ingestion pipeline (`ingest.py`), system prompts, and a FastMCP server (`mcp_server.py`).
- `llm-eval/`: Contains different evaluation approaches for testing the agent:
  - `agent-eval/`: Evaluates the agent's step-by-step trace, Tool Correctness, Plan Adherence, and Task Completion.
  - `ARENA/`: Arena-style side-by-side model evaluations.
  - `DAG/`: Directed Acyclic Graph evaluations (e.g., `ConversationalDAGMetric`).
  - `Data_Generation/`: Scripts for synthetically generating test cases and goldens.
  - `GEval/`: GEval-based custom criteria metrics (e.g., `ConversationalGEval`).
  - `MCP-Eval/`: Evaluates single-turn and multi-turn MCP tool usage and task completion.
  - `rag-eval/`: Specific evaluations for RAG retrieval and generation.
  - `safety-eval/`: Adversarial safety testing measuring Bias, Toxicity, Misuse, PII Leakage, Role Violation, and Non-Advice.
- `config.py`: Centralized configuration for model selection (for both the agent and evaluator).
- `pyproject.toml` / `requirements.txt`: Project dependencies.

## 🚀 Prerequisites and Installation

The project requires **Python 3.12+**.

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd DeepEval-project
   ```

2. **Install dependencies:**
   You can install the required packages using pip (or `uv` since `uv.lock` is present):
   ```bash
   pip install -r requirements.txt
   # OR
   pip install .
   ```

3. **Environment Setup:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key
   TAVILY_API_KEY=your_tavily_api_key
   CONFIDENTAI_API_KEY=your_confident_ai_api_key
   ```
   *Note: OpenRouter is used for the LLMs, Tavily for web search, and ConfidentAI for DeepEval metrics logging.*

## 🤖 Running the Research Agent

To interact with the research agent via the command line:

```bash
cd research-agent
python agent.py
```

The agent will prompt you for questions. It decides whether to query the internal Chroma database, search the web, use its memory, or use MCP tools based on your input.

*Note: For populating the internal knowledge base, you may need to run `python ingest.py` before querying.*

You can also run the bundled FastMCP server to expose utilities to external agents:
```bash
python mcp_server.py
```

## 🧪 Running Evaluations

The `llm-eval` directory contains various scripts to automatically test the agent. The evaluation models are configured in `config.py` at the root.

For example, to run the Safety Evaluation pipeline:
```bash
cd llm-eval/safety-eval
python safety-eval.py
```

To run the MCP Server evaluation:
```bash
cd llm-eval/MCP-Eval
python mcp-eval.py
```

These scripts simulate a conversation or a single-turn prompt with the `research-agent` (or its MCP server) and then use DeepEval to judge the agent's responses based on rigorous criteria, logging the results to Confident AI.

## ⚙️ Configuration

The root `config.py` file centralizes settings like:
- Model selection for the evaluator (e.g., DeepEval Judge model).
- Other potential model settings for the agent and embeddings.

Ensure this is set to the model you intend to use via OpenRouter.
