Q: What embedding model is used in this research agent, and how many dimensions does it produce?
Retrieved chunks: 1

Q: What are the latest developments in AI agent frameworks like LangChain?
Retrieved chunks: 1

✨ You're running DeepEval's latest Internal Knowledge Groundedness Gate [DAG] Metric! 
(using dots-studio/dots-3-note-preview:free (OpenRouter), strict=False, 
async_mode=False)...

╭───────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                       │
│  ❌ test_case_0                                                                       │
│  ├──   Input:            What embedding model is used in this research agent, and     │
│  │                       how many dimensions does it produce?                         │
│  │     Actual Output:                                                                 │
│  │                                                                                    │
│  │                       Based on the internal documentation, the research agent      │
│  │                       uses the **BGE-M3** embedding model (developed by BAAI),     │
│  │                       accessed through OpenRouter under the model identifier       │
│  │                       `baai/bge-m3`.                                               │
│  │                                                                                    │
│  │                       This model produces **1024-dimensional** dense               │
│  │                       embeddings, which are stored in the Chroma vector            │
│  │                       database.                                                    │
│  │                                                                                    │
│  │                       **Reasoning and evidence:**                                  │
│  │                       - The internal knowledge base explicitly states: "The        │
│  │                       research agent uses the BGE-M3 model through OpenRouter.     │
│  │                       The model identifier is baai/bge-m3."                        │
│  │                       - It further specifies: "BGE-M3 produces 1024-dimensional    │
│  │                       dense embeddings. These vectors are stored in the Chroma     │
│  │                       vector database."                                            │
│  │                                                                                    │
│  │                       This information is internal to the project documentation    │
│  │                       and does not require external web research.                  │
│  └── Metrics                                                                          │
│       Status ┃ Metric                 ┃ Score ┃ Threshold ┃ Reason                    │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ Internal Knowledge     │ 0.10  │ 0.50      │ The score is 0.1          │
│              │ Groundedness Gate      │       │           │ because the DAG           │
│              │ [DAG]                  │       │           │ traversal path through    │
│              │                        │       │           │ the BinaryJudgementNode   │
│              │                        │       │           │ at level 0 (verdict       │
│              │                        │       │           │ True, confirming          │
│              │                        │       │           │ non-empty retrieval       │
│              │                        │       │           │ context) and the          │
│              │                        │       │           │ BinaryJudgementNode at    │
│              │                        │       │           │ level 1 (verdict True,    │
│              │                        │       │           │ confirming all claims     │
│              │                        │       │           │ are supported) leads to   │
│              │                        │       │           │ a VerdictNode at level    │
│              │                        │       │           │ 2 with verdict True,      │
│              │                        │       │           │ indicating high           │
│              │                        │       │           │ internal knowledge        │
│              │                        │       │           │ groundedness, which       │
│              │                        │       │           │ corresponds to a low      │
│              │                        │       │           │ score on this metric.     │
│                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                       │
│  ❌ test_case_1                                                                       │
│  ├──   Input:            What are the latest developments in AI agent frameworks      │
│  │                       like LangChain?                                              │
│  │     Actual Output:                                                                 │
│  │                                                                                    │
│  │                       Based on current information from 2025, here are the         │
│  │                       latest developments in AI agent frameworks like              │
│  │                       LangChain:                                                   │
│  │                                                                                    │
│  │                       ## Key Developments in AI Agent Frameworks                   │
│  │                                                                                    │
│  │                       ### 1. **LangChain's Strategic Shift to LangGraph**          │
│  │                       The LangChain team now explicitly recommends **using         │
│  │                       LangGraph for agents, not LangChain**. LangGraph reached     │
│  │                       General Availability in May 2025 and has become the          │
│  │                       default runtime for LangChain agents. It provides:           │
│  │                       - Graph-based control over dynamic, stateful workflows       │
│  │                       - Precise state management across complex workflows          │
│  │                       - Native human-in-the-loop support                           │
│  │                       - Production-ready fault tolerance                           │
│  │                       - Integration with the broader LangChain ecosystem           │
│  │                                                                                    │
│  │                       ### 2. **Microsoft's Unified Agent Framework**               │
│  │                       Microsoft merged AutoGen and Semantic Kernel into a          │
│  │                       single **Microsoft Agent Framework**, announced in           │
│  │                       October 2025. This unified SDK combines:                     │
│  │                       - AutoGen's conversational multi-agent abstractions          │
│  │                       - Semantic Kernel's enterprise features (session-based       │
│  │                       state management, middleware, telemetry, type safety)        │
│  │                       - Graph-based workflows for explicit control over            │
│  │                       multi-agent execution paths                                  │
│  │                                                                                    │
│  │                       ### 3. **CrewAI's Rapid Growth**                             │
│  │                       CrewAI raised $18M and now powers agents for **60% of        │
│  │                       Fortune 500 companies**. It's particularly strong for:       │
│  │                       - Rapid role-based development                               │
│  │                       - Marketing teams and research departments                   │
│  │                       - Mid-sized businesses seeking low-barrier entry into        │
│  │                       agent automation                                             │
│  │                                                                                    │
│  │                       ### 4. **Production Validation and Enterprise Adoption**     │
│  │                       - **LangGraph** is running in production at LinkedIn (AI     │
│  │                       recruiter, SQL Bot), Uber (large-scale code migrations),     │
│  │                       Replit (AI copilot), and 400+ other companies                │
│  │                       - Independent benchmarks show LangGraph runs ~2.2x faster    │
│  │                       than CrewAI on identical tasks                               │
│  │                                                                                    │
│  │                       ### 5. **Emerging Frameworks**                               │
│  │                       Several new frameworks have entered the landscape:           │
│  │                       - **Google ADK** (Agent Development Kit)                     │
│  │                       - **OpenAI Agents SDK**                                      │
│  │                       - **Mastra** (for TypeScript teams)                          │
│  │                                                                                    │
│  │                       ### 6. **Key Trends**                                        │
│  │                       - **Multi-agent collaboration** and autonomous               │
│  │                       capabilities                                                 │
│  │                       - **Advanced reasoning** and context management              │
│  │                       - **Task routing** and coordination between agents           │
│  │                       - **Automation of repetitive administrative tasks**          │
│  │                       - **Human-in-the-loop** integration for critical             │
│  │                       workflows                                                    │
│  │                                                                                    │
│  │                       The landscape has transformed from "chaos to clarity"        │
│  │                       with three frameworks dominating: LangGraph for              │
│  │                       production-grade complexity, CrewAI for rapid role-based     │
│  │                       development, and Microsoft Agent Framework for enterprise    │
│  │                       .NET/Azure environments.                                     │
│  │                                                                                    │
│  │                       Would you like me to dive deeper into any specific           │
│  │                       framework or trend?                                          │
│  └── Metrics                                                                          │
│       Status ┃ Metric                 ┃ Score ┃ Threshold ┃ Reason                    │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ Internal Knowledge     │ 0.00  │ 0.50      │ The score is 0.0          │
│              │ Groundedness Gate      │       │           │ because the DAG           │
│              │ [DAG]                  │       │           │ traversal results in a    │
│              │                        │       │           │ VerdictNode with          │
│              │                        │       │           │ Verdict: False, as the    │
│              │                        │       │           │ BinaryJudgementNode at    │
│              │                        │       │           │ Level 1 determined that   │
│              │                        │       │           │ the internal knowledge    │
│              │                        │       │           │ claims are not            │
│              │                        │       │           │ supported by the          │
│              │                        │       │           │ retrieval context.        │
│                                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                     │
│                                                                                       │
│  Metric                        ┃ Average Score ┃ Pass Rate                   ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Internal Knowledge            │ 0.05          │ 0.00% | passed=0 | failed=2 │ 2      │
│  Groundedness Gate [DAG]       │               │                             │        │
╰───────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================
✓ Done 🎉! View results on 
https://app.confident-ai.com/project/cmtyaseol003amy0tvr2de0bp/test-runs/cmu2isoik0000nr0
th9x80awa
[PostHog] analytics lane flush ran out of budget (1.0s granted) with 1 items pending.





