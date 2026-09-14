# DeepEval Agentic RAG — Research Agent & Evaluation Suite

An end-to-end implementation of an **Agentic RAG (Retrieval-Augmented Generation)** system built with **LangChain** and **LangGraph**, paired with a comprehensive evaluation suite powered by **[DeepEval](https://github.com/confident-ai/deepeval)**.

The project covers two things simultaneously:
1. **A production-style research agent** — with RAG, web search, MCP tools, short-term and long-term memory, and a structured system prompt.
2. **A full evaluation layer** — that tests whether the agent is behaving correctly across every capability: retrieval quality, tool use, safety, memory, planning, and conversational coherence.

---

## 📐 Architecture Overview

```
DeepEval-project/
│
├── research-agent/          # The agent itself
│   ├── agent.py             # Core agent: LLM + tools + memory + prompts
│   ├── ingest.py            # Chunk & embed documents → Chroma DB
│   ├── mcp_server.py        # FastMCP server (word_count, format_citation)
│   ├── prompt1.txt          # System prompt v1 (baseline)
│   ├── prompt2.txt          # System prompt v2 (explicit planning step)
│   └── data/                # Source documents for the knowledge base
│
├── llm-eval/                # Evaluation suite (8 sub-evals)
│   ├── rag-eval/            # RAG retrieval & generation quality
│   ├── agent-eval/          # Agentic trace metrics (planning, tool selection)
│   ├── DAG/                 # Deterministic DAG-based groundedness gates
│   ├── GEval/               # LLM-as-judge custom criteria
│   ├── safety-eval/         # Adversarial safety & guardrail testing
│   ├── MCP-Eval/            # MCP tool invocation correctness
│   ├── ARENA/               # A/B comparison between prompt variants
│   └── multi-turn-eval/     # All 11 DeepEval conversational metrics
│
├── Data-Generation/         # Synthetic test case & golden generation
│   ├── golden_synthesis.py  # Generate goldens from the knowledge base
│   └── conversation_simulator.py  # Simulate full conversations with the agent
│
└── config.py                # Centralized model & judge configuration
```

---

## 🤖 Research Agent (`research-agent/`)

### What it does

The agent is a **loop-based decision maker** — at each step, the LLM reads the conversation history and decides which tool to call next (or whether to stop and answer). It is built with `langchain.agents.create_agent` on top of a LangGraph runtime.

### Tools available to the agent

| Tool | Type | Purpose |
|------|------|---------|
| `retrieve_documents` | RAG | Query the internal Chroma vector DB (BGE-M3 embeddings, top-5 chunks) |
| `search_web` | Web | Tavily web search for current / external information |
| `word_count` | MCP | Count words, characters, and reading time in a passage |
| `format_citation` | MCP | Format APA or MLA citations |
| `remember_fact` | Memory | Persist a user preference or fact to long-term store |
| `recall_facts` | Memory | Retrieve previously saved facts about the user |

### Memory model

- **Short-term (conversation)**: `InMemorySaver` checkpointer — the agent recalls all prior turns within the same `thread_id`.
- **Long-term (cross-session)**: `InMemoryStore` — facts saved via `remember_fact` are keyed by `user_id` and survive across threads.

### MCP server (`mcp_server.py`)

A **FastMCP** server (stdio transport) that exposes `word_count` and `format_citation` as MCP-protocol tools. `agent.py` connects to it via `MultiServerMCPClient`, which spawns the server as a subprocess and loads its tools dynamically at startup.

### System prompts

| File | Purpose |
|------|---------|
| `prompt1.txt` | Baseline prompt — role definition, tool-use rules, format rules |
| `prompt2.txt` | Extended prompt — adds an explicit "state your plan first" instruction used for `Plan Quality` evaluation |

---

## 🧪 Evaluation Suite (`llm-eval/`)

All eval scripts share a common pattern:
- Import `agent` and `Context` from `research-agent/agent.py`
- Invoke the agent with a real question using a **unique `thread_id` per test case** (prevents cross-contamination of conversation history)
- Score the output using a DeepEval metric with the **Gemini judge** (`gemini-flash-lite-latest`) configured in `config.py`

### 1. RAG Evaluation (`rag-eval/`)

**Script:** `rag-eval.py`

Tests the quality of the retrieval and generation pipeline using five standard RAG metrics:

| Metric | What it checks |
|--------|---------------|
| Answer Relevancy | Does the answer address the question? |
| Faithfulness | Are all claims grounded in retrieved documents? |
| Contextual Relevancy | Are the retrieved chunks relevant to the question? |
| Contextual Precision | Are relevant chunks ranked above irrelevant ones? |
| Contextual Recall | Do the retrieved chunks cover the expected answer? |

```bash
cd llm-eval/rag-eval
python rag-eval.py
```

---

### 2. Agentic Evaluation (`agent-eval/`)

**Script:** `agent-eval.py`

Evaluates the agent's full **execution trace** — not just the final answer, but every step the agent took to get there. Uses DeepEval's trace-based metrics:

| Metric | What it checks |
|--------|---------------|
| Task Completion | Did the agent complete the user's goal? |
| Step Efficiency | Did the agent avoid unnecessary steps/tool calls? |
| Plan Adherence | Did the agent follow its stated plan? |
| Plan Quality | Was the plan specific, complete, and well-structured? |
| Tool Correctness | Did the agent call the right tools? |
| Argument Correctness | Were the tool arguments correct? |

The `invoke_with_tracing()` helper in `agent.py` attaches a DeepEval `CallbackHandler` so the full trace is captured.

```bash
cd llm-eval/agent-eval
python agent-eval.py
```

---

### 3. DAG Evaluation (`DAG/`)

**Scripts:** `DAG.py`, `conversational_DAG.py`

Uses **Directed Acyclic Graph (DAG) metrics** to encode multi-step evaluation logic as a decision tree. The root node makes a deterministic check on `RETRIEVAL_CONTEXT` (not the output text), which avoids false failures when the agent correctly reports that the KB was empty.

**DAG.py** — Single-turn:
- `Internal Knowledge Groundedness Gate`: Checks if the agent's answer is grounded in retrieved KB documents (skips the LLM judge automatically for web-search-only answers).

**conversational_DAG.py** — Multi-turn:
- `Memory Recall Gate`: Checks if the agent correctly recalled information from an earlier turn.

```bash
cd llm-eval/DAG
python DAG.py
python conversational_DAG.py
```

---

### 4. GEval Evaluation (`GEval/`)

**Scripts:** `GEval.py`, `conversational_GEval.py`

Uses **LLM-as-judge GEval** with custom natural-language criteria to evaluate subjective quality dimensions:

**GEval.py** — Single-turn:
- `Format Adherence`: Answer-first structure, clear evidence labeling, tool attribution.

**conversational_GEval.py** — Multi-turn:
- `Memory Consistency`: Agent correctly attributes user context from earlier turns.

```bash
cd llm-eval/GEval
python GEval.py
python conversational_GEval.py
```

---

### 5. Safety Evaluation (`safety-eval/`)

**Script:** `safety-eval.py`

Tests adversarial inputs — prompts designed to make the agent misbehave or leak information. Uses DeepEval's built-in safety metrics:

| Metric | What it checks |
|--------|---------------|
| Bias | Does the agent produce biased responses? |
| Toxicity | Does the agent produce toxic or harmful content? |
| Misuse | Does the agent comply with out-of-scope requests? |
| PII Leakage | Does the agent expose personal identifiable information? |
| Role Violation | Does the agent stay within its defined academic research role? |
| Non-Advice Compliance | Does the agent avoid giving medical/legal/financial advice? |

The PII test case includes an `expected_output` (ideal refusal) so the judge evaluates the agent's actual refusal against the gold standard.

```bash
cd llm-eval/safety-eval
python safety-eval.py
```

---

### 6. MCP Evaluation (`MCP-Eval/`)

**Script:** `mcp-eval.py`

Tests whether the agent correctly invokes MCP tools (`word_count`, `format_citation`) in both single-turn and multi-turn scenarios.

| Metric | What it checks |
|--------|---------------|
| MCP Use | Did the agent call the correct MCP tool? |
| Multi-Turn MCP Use | Did the agent invoke MCP tools correctly across turns? |
| MCP Task Completion | Did the agent complete the MCP-dependent task? |

The script also connects directly to the MCP server to fetch its tool primitives and validates them.

```bash
cd llm-eval/MCP-Eval
python mcp-eval.py
```

---

### 7. Arena Evaluation (`ARENA/`)

**Script:** `arena-GEval.py`

Runs an **A/B comparison** between two agent variants — one using `prompt1.txt` and one using `prompt2.txt` — on the same question. A judge LLM picks the winner based on quality, completeness, and evidence use.

```bash
cd llm-eval/ARENA
python arena-GEval.py
```

---

### 8. Multi-Turn Evaluation (`multi-turn-eval/`)

**Script:** `multi_turn_metrics.py`

Runs all **11 DeepEval conversational metrics** against the live agent, one per golden question, each on an isolated `thread_id`:

| Metric | Focus |
|--------|-------|
| Turn Relevancy | Is each agent turn relevant to the user's message? |
| Role Adherence | Does the agent stay in its defined role? |
| Knowledge Retention | Does the agent remember earlier turns? |
| Conversation Completeness | Does the conversation fully resolve the user's goal? |
| Goal Accuracy | Does the agent correctly infer the user's underlying goal? |
| Conversation Relevancy | Is the overall conversation on-topic? |
| Turn Faithfulness | Are per-turn claims grounded in retrieved context? |
| Turn Contextual Precision | Are the retrieved chunks ranked well per turn? |
| Turn Contextual Recall | Do chunks cover the expected per-turn answer? |
| Turn Contextual Relevancy | Are retrieved chunks relevant per turn? |
| Tool Use | Did the agent call the correct tools across the conversation? |

```bash
cd llm-eval/multi-turn-eval
python multi_turn_metrics.py
```

---

## 🗂️ Data Generation (`Data-Generation/`)

Scripts for generating evaluation data synthetically from the knowledge base:

| Script | Purpose |
|--------|---------|
| `golden_synthesis.py` | Use DeepEval's synthesizer to generate goldens from KB documents |
| `conversation_simulator.py` | Simulate full multi-turn conversations against the agent using `ConversationSimulator` with predefined personas and scenarios |

```bash
cd Data-Generation
python golden_synthesis.py
python conversation_simulator.py
```

---

## ⚙️ Configuration (`config.py`)

All model settings are centralized in the root `config.py`. **No hardcoded model names exist in any eval script.**

```python
# Agent LLM
agent_model_name = "dots-studio/dots-3-note-preview:free"

# Embedding model (Chroma)
embedding_model = "baai/bge-m3"

# Judge provider — change this one line to switch all evals
JUDGE_PROVIDER = "gemini"   # or "openrouter"

def get_judge_model():
    # Returns GeminiModel (active) or OpenRouterModel (commented out)
    ...
```

> **Why Gemini as judge?** Free-tier OpenRouter models don't support structured output, causing DAG/GEval/Safety metrics to mis-parse verdicts and produce incorrect scores. `gemini-flash-lite-latest` reliably returns structured JSON required by DeepEval's scoring engine.

---

## 🚀 Setup & Installation

### Requirements

- Python **3.12+**
- API keys for: OpenRouter, Tavily, Google AI Studio (Gemini), Confident AI

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd DeepEval-project
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

Or with `uv` (recommended, lock file included):
```bash
uv sync
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
# Agent
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key

# Judge model (DeepEval)
GOOGLE_API_KEY=your_google_ai_studio_key

# DeepEval logging (optional, for Confident AI dashboard)
CONFIDENT_AI_API_KEY=your_confident_ai_key
```

### 4. Ingest documents into the knowledge base

```bash
cd research-agent
python ingest.py
```

Place your `.txt` or `.pdf` documents in `research-agent/data/` before running.

### 5. Run the agent

```bash
cd research-agent
python agent.py
```

---

## 🔄 Running All Evaluations

```bash
# RAG quality
cd llm-eval/rag-eval && python rag-eval.py

# Agentic trace
cd llm-eval/agent-eval && python agent-eval.py

# DAG groundedness gates
cd llm-eval/DAG && python DAG.py && python conversational_DAG.py

# GEval custom criteria
cd llm-eval/GEval && python GEval.py && python conversational_GEval.py

# Safety & adversarial
cd llm-eval/safety-eval && python safety-eval.py

# MCP tool correctness
cd llm-eval/MCP-Eval && python mcp-eval.py

# Prompt A/B comparison
cd llm-eval/ARENA && python arena-GEval.py

# All 11 conversational metrics
cd llm-eval/multi-turn-eval && python multi_turn_metrics.py
```

Results are printed to the console and (if `CONFIDENT_AI_API_KEY` is set) logged to your [Confident AI dashboard](https://app.confident-ai.com).

---

## 🔗 Key Dependencies

| Package | Role |
|---------|------|
| `deepeval` | Evaluation metrics, judge models, datasets |
| `langchain` / `langchain-core` | Agent construction, tool definition |
| `langgraph` | Stateful agent runtime, checkpointer, store |
| `langchain-openrouter` | OpenRouter LLM integration |
| `langchain-chroma` | Chroma vector DB integration |
| `langchain-tavily` | Tavily web search tool |
| `langchain-mcp-adapters` | MCP → LangChain tool adapter |
| `mcp` / `fastmcp` | MCP server implementation |
| `chromadb` | Local vector database |
| `python-dotenv` | `.env` file loading |
