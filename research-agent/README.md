# Research Agent

                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │ Research Agent  │
                  │   LangChain     │
                  └────────┬────────┘
                           │
                 decides which tool
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
      ┌───────────────┐ ┌──────────────┐ ┌──────────────┐
      │ RAG Tool      │ │ Web Tool     │ │ Memory Tool  │
      │               │ │              │ │              │
      │ BGE-M3        │ │ Tavily       │ │ LangGraph    │
      │      ↓        │ │      ↓       │ │    Store     │
      │    Chroma     │ │    Web       │ │              │
      └───────┬───────┘ └──────┬───────┘ └──────┬───────┘
              │                │                │
              └────────────┬───┴────────────────┘
                           ▼
                  ┌─────────────────┐
                  │    OpenRouter   │
                  │   Chat Model    │
                  └────────┬────────┘
                           │
                           ▼
                         ANSWER

This directory contains the `research-agent`, an intelligent Agentic RAG implementation built using LangChain and LangGraph. It is designed to evaluate both internal knowledge base documents and external web sources to formulate well-reasoned answers to user queries.

## Architecture & Tools

The agent is driven by a chat model via OpenRouter and acts as a central decision-maker. It is equipped with several tools:

- **RAG Tool (`retrieve_documents`)**: Queries an internal knowledge base stored in a Chroma vector database using BGE-M3 embeddings.
- **Web Tool (`search_web`)**: Queries the public internet using Tavily Search when the question requires current or external information.
- **Memory Tools (`remember_fact` & `recall_facts`)**: Utilizes LangGraph's `InMemoryStore` to store and retrieve long-term facts about the user across conversations.

## How It Works

1. The user asks a research question.
2. The agent interprets the query and decides which tools to invoke based on its system prompt.
3. It may retrieve internal documents, perform web searches, or both.
4. It synthesizes the retrieved information to provide a comprehensive answer, maintaining context (via memory checkpoints) across multiple interactions.

## Usage

To run the agent interactively via the CLI:

```bash
python agent.py
```
You will be prompted to enter research questions in a loop. Type `exit` or `quit` to end the session.

## Configuration

Make sure your `.env` file is properly configured with the necessary API keys:
- `OPENROUTER_API_KEY`
- `TAVILY_API_KEY`

Model selection for the agent and embeddings is managed centrally in the `config.py` file located at the project root.