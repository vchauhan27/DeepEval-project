Q: What embedding model is used in this research agent, and how many dimensions does it produce?
A: 

The research agent uses the **BGE-M3** embedding model (via OpenRouter, model identifier `baai/bge-m3`). It produces **1024-dimensional** dense embeddings, which are stored in the Chroma vector data...

Q: Compare the internal research-agent architecture with the latest LangChain architecture.
A: 

Based on the internal documentation and current web information, here's a comparison:

## Internal Research-Agent Architecture

**Core Components:**
- **Language Model**: Uses an LLM via OpenRouter ...

✨ You're running DeepEval's latest Format Adherence [GEval] Metric! (using 
nvidia/nemotron-3-super-120b-a12b:fre (OpenRouter), strict=False, async_mode=False)...

╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_0 (Passed 1 metrics)                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                             │
│  ❌ test_case_1                                                                             │
│  ├──   Input:            Compare the internal research-agent architecture with the          │
│  │                       latest LangChain architecture.                                     │
│  │     Actual Output:                                                                       │
│  │                                                                                          │
│  │                       Based on the internal documentation and current web                │
│  │                       information, here's a comparison:                                  │
│  │                                                                                          │
│  │                       ## Internal Research-Agent Architecture                            │
│  │                                                                                          │
│  │                       **Core Components:**                                               │
│  │                       - **Language Model**: Uses an LLM via OpenRouter as the            │
│  │                       decision-maker                                                     │
│  │                       - **Tools**: Internal retrieval (Chroma vector database with       │
│  │                       BGE-M3 embeddings, 1024 dimensions) and web search                 │
│  │                       - **Execution Loop**: The LLM decides when to call tools,          │
│  │                       inspects results, and determines if more information is needed     │
│  │                                                                                          │
│  │                       **Key Characteristics:**                                           │
│  │                       - **Agentic RAG**: Unlike conventional RAG (where retrieval        │
│  │                       happens automatically before generation), this system lets the     │
│  │                       LLM decide *whether* and *when* to retrieve, and *which*           │
│  │                       retrieval tool to use                                              │
│  │                       - **Dual Information Sources**: Internal knowledge base            │
│  │                       (Chroma) and public web search                                     │
│  │                       - **Evaluation Focus**: Tool selection, retrieval quality,         │
│  │                       evidence usage, groundedness, and trajectory quality               │
│  │                                                                                          │
│  │                       ## Latest LangChain Architecture (2024-2025)                       │
│  │                                                                                          │
│  │                       **Major Shift:** LangChain has publicly pivoted, recommending      │
│  │                       **LangGraph** for agent orchestration rather than LangChain's      │
│  │                       traditional chain-based design.                                    │
│  │                                                                                          │
│  │                       **LangGraph Architecture:**                                        │
│  │                       - **Graph-Based**: Uses directed graphs instead of linear          │
│  │                       chains (step 1 → step 2 → step 3)                                  │
│  │                       - **Stateful**: Agents maintain context and state throughout       │
│  │                       interactions                                                       │
│  │                       - **Advanced Flow Control**: Supports cycles (revisiting           │
│  │                       steps), conditionals (routing based on state), and parallel        │
│  │                       execution (multiple agents running concurrently)                   │
│  │                       - **Integration**: Works with LangChain components and             │
│  │                       integrates with LangSmith for monitoring                           │
│  │                                                                                          │
│  │                       **Current Trends:**                                                │
│  │                       - **MCP Protocol**: Model Context Protocol (introduced by          │
│  │                       Anthropic) standardizes how AI models interact with tools and      │
│  │                       data sources                                                       │
│  │                       - **Lightweight SDKs**: Newer frameworks (OpenAI Agents SDK,       │
│  │                       Google ADK) favor minimal abstraction over heavy frameworks        │
│  │                       - **Coding Agents**: Tools like Claude Code and Cursor             │
│  │                       represent a shift toward code-first agent approaches               │
│  │                                                                                          │
│  │                       ## Key Differences                                                 │
│  │                                                                                          │
│  │                       | Aspect | Internal Research Agent | Latest LangChain/LangGraph    │
│  │                       |                                                                  │
│  │                       |--------|------------------------|---------------------------…    │
│  │                       | **Architecture** | Agentic RAG with tool-use loop |              │
│  │                       Graph-based stateful workflows |                                   │
│  │                       | **Retrieval** | LLM-decided (internal + web) | Typically         │
│  │                       integrated via chains or custom graphs |                           │
│  │                       | **State Management** | Simple execution loop | Explicit state    │
│  │                       persistence and multi-actor support |                              │
│  │                       | **Complexity** | Focused on research Q&A with dual sources |     │
│  │                       Designed for complex production multi-agent systems |              │
│  │                       | **Philosophy** | Minimal agentic retrieval with evaluation       │
│  │                       focus | Comprehensive orchestration with monitoring |              │
│  │                                                                                          │
│  │                       The internal research agent represents a more targeted, agentic    │
│  │                       RAG approach focused on research question-answering, while the     │
│  │                       latest LangChain ecosystem (particularly LangGraph) provides a     │
│  │                       more general-purpose, production-grade framework for building      │
│  │                       complex stateful agents with cycles, parallelism, and              │
│  │                       multi-agent collaboration.                                         │
│  └── Metrics                                                                                │
│       Status ┃ Metric                   ┃ Score ┃ Threshold ┃ Reason                        │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ Format Adherence [GEval] │ 0.20  │ 0.70      │ The response does not begin   │
│              │                          │       │           │ with a concise answer;        │
│              │                          │       │           │ instead it starts with a      │
│              │                          │       │           │ preamble and dives into       │
│              │                          │       │           │ details, violating the        │
│              │                          │       │           │ required structure of         │
│              │                          │       │           │ answer-first then             │
│              │                          │       │           │ explanation. While it does    │
│              │                          │       │           │ distinguish internal          │
│              │                          │       │           │ knowledge from web search     │
│              │                          │       │           │ for the research agent, the   │
│              │                          │       │           │ lack of an upfront answer     │
│              │                          │       │           │ warrants a heavy penalty.     │
│                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric                       ┃ Average Score   ┃ Pass Rate                        ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Format Adherence [GEval]     │ 0.60            │ 50.00% | passed=1 | failed=1     │ 2      │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================
✓ Done 🎉! View results on 
https://app.confident-ai.com/project/cmtyaseol003amy0tvr2de0bp/test-runs/cmu0x2wgz001zms0tk68vs
a9v

Conversation:
  [user] My name is Alex and I'm researching agentic RAG systems.
  [assistant]

Hello Alex! It's nice to meet you. I've noted that you're researching agentic RAG systems - that's a fascinating and rapidly evolving area of AI.

H
  [user] Given what I just told you, what part of this knowledge base should I focus on first? 
  [assistant]



  [assistant]

Based on the knowledge base content, I'd recommend starting with **Document 1**, which directly addresses the core distinction between conventional

✨ You're running DeepEval's latest Memory Consistency [Conversational GEval] Metric! (using   
dots-studio/dots-3-note-preview:free (OpenRouter), strict=False, async_mode=False)...

╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ conversational_test_case_0 (Passed 1 metrics)                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric                            ┃ Average Score ┃ Pass Rate                     ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Memory Consistency                │ 1.00          │ 100.00% | passed=1 | failed=0 │ 1      │
│  [Conversational GEval]            │               │                               │        │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================
✓ Done 🎉! View results on 
https://app.confident-ai.com/project/cmtyaseol003amy0tvr2de0bp/test-runs/cmu0y0xa8004alc0t4fxwb
5aq
[PostHog] analytics lane flush ran out of budget (1.0s granted) with 1 items pending.