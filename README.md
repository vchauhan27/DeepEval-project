# DeepEval RAG Project

This repository contains an intelligent Agentic Retrieval-Augmented Generation (RAG) system built with LangChain and LangGraph, paired with a comprehensive evaluation suite powered by DeepEval.

The project is structured into two main components:
1. **Research Agent (`research-agent/`)**: A conversational agent that uses tools to fetch internal knowledge (via ChromaDB), search the web (via Tavily), and maintain long-term memory across interactions.
2. **LLM Evaluation (`llm-eval/`)**: A suite of automated evaluation scripts that use `deepeval` to test the agent's performance, memory consistency, and reasoning capabilities using various metrics (GEval, DAG, etc.).

## 📁 Project Structure

- `research-agent/`: Contains the core agent implementation (`agent.py`), data ingestion pipeline (`ingest.py`), and prompts.
- `llm-eval/`: Contains different evaluation approaches for testing the agent:
  - `ARENA/`: Arena-style evaluations.
  - `DAG/`: Directed Acyclic Graph evaluations (e.g., `ConversationalDAGMetric`).
  - `GEval/`: GEval-based metrics (e.g., `ConversationalGEval`).
  - `rag-eval/`: Specific evaluations for RAG retrieval and generation.
  - `agent-eval/`: General agent evaluations.
  - `MCP_Eval/`: Model Context Protocol evaluations (Work in progress).
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
   ```
   *Note: OpenRouter is used for the LLMs, and Tavily is used for web search.*

## 🤖 Running the Research Agent

To interact with the research agent via the command line:

```bash
cd research-agent
python agent.py
```

The agent will prompt you for questions. It decides whether to query the internal Chroma database, search the web, or use its memory based on your input.

*Note: For populating the internal knowledge base, you may need to run `python ingest.py` before querying.*

## 🧪 Running Evaluations

The `llm-eval` directory contains various scripts to automatically test the agent. The evaluation models are configured in `config.py` at the root.

For example, to run the Conversational GEval metric (which tests memory consistency across turns):

```bash
cd llm-eval/GEval
python conversational_GEval.py
```

To run the Directed Acyclic Graph (DAG) metric:

```bash
cd llm-eval/DAG
python conversational_DAG.py
```

These scripts simulate a conversation with the `research-agent` and then use DeepEval to judge the agent's responses based on custom criteria (e.g., whether it correctly remembered and used facts from earlier in the conversation).

## ⚙️ Configuration

The root `config.py` file centralizes settings like:
- Model selection for the evaluator (e.g., DeepEval Judge model).
- Other potential model settings for the agent and embeddings.

Ensure this is set to the model you intend to use via OpenRouter.
