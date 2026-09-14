# Synthetic Data Generation

Two scripts for bootstrapping evaluation data for the research agent, based on DeepEval's [Synthesizer](https://deepeval.com/docs/golden-synthesizer) and [ConversationSimulator](https://deepeval.com/docs/conversation-simulator).

Place both files in the same directory as `agent.py`.

## Files

- `golden_synthesis.py` - generates synthetic goldens from the documents in `data/` (the same folder `ingest.py` reads). Produces:
  - single-turn goldens (`input` + `expected_output`) grounded in the knowledge base, for evaluating direct Q&A.
  - conversational goldens (`scenario` + `expected_outcome`), which define multi-turn scenarios but no actual dialogue yet.
  - Output is saved as JSON under `synthetic_data/`.

- `conversation_simulator.py` - runs full multi-turn conversations against the live agent. It defines a handful of `ConversationalGolden`s (scenario, expected outcome, persona) covering the agent's core tool paths - internal RAG lookup, web search, citation formatting, word counting, and long-term memory - then simulates a back-and-forth dialogue for each one by:
  1. Having a simulated LLM user role-play the persona and generate the next message.
  2. Passing that message to the actual `agent` from `agent.py` via a `model_callback`, keyed by a per-conversation `thread_id` so each simulated conversation gets its own checkpointer/memory session.
  3. Repeating until the expected outcome is reached or `max_user_simulations` turns pass.
  4. Printing the resulting transcripts as `ConversationalTestCase`s.

## Setup

```bash
pip install deepeval
```

DeepEval's default models (`Synthesizer`, `ConversationSimulator`'s `simulator_model`) use OpenAI's GPT models, so set:

```bash
export OPENAI_API_KEY=your_key
```

Your existing `.env` (`OPENROUTER_API_KEY`, `TAVILY_API_KEY`) is still required since `conversation_simulator.py` imports and runs the real `agent`.

If you'd rather not add an OpenAI key, pass a custom model to either tool, e.g.:

```python
synthesizer = Synthesizer(model=your_custom_deepeval_llm)
simulator = ConversationSimulator(model_callback=model_callback, simulator_model=your_custom_deepeval_llm)
```

Any model of type `DeepEvalBaseLLM` works (Anthropic, Gemini, Ollama, local models).

## Usage

Generate goldens first:

```bash
python golden_synthesis.py
```

Then run conversation simulations against the agent:

```bash
python conversation_simulator.py
```

## Suggested Order

For single-turn evaluations (like rag-eval, basic safety-eval, or ARENA), you can easily hand-write a question and answer without needing data generation.

Use golden_synthesis.py only for production when you need lots of test cases.

However, testing memory and context retention requires a multi-turn conversation history (a back-and-forth chat) to exist before the evaluation happens, which is exactly where conversation_simulator.py shines.

Here are the specific evaluations in your suite that test memory and would rely on simulated multi-turn conversations:

llm-eval/DAG/conversational_DAG.py (Memory Recall Gate)

What it tests: Checks if the agent accurately recalls a specific piece of information that the user shared earlier in the conversation (e.g., if the user said their name was Alice 4 turns ago, does the agent remember it?).
llm-eval/GEval/conversational_GEval.py (Memory Consistency)

What it tests: Uses an LLM-as-judge to verify that the agent's current response doesn't contradict facts established earlier in the conversation history.
llm-eval/multi-turn-eval/multi_turn_metrics.py (All 11 DeepEval Conversational Metrics)

What it tests: This is the big one. It runs 11 different conversational metrics on a full chat transcript, including Knowledge Retention, Conversation Completeness, Goal Accuracy (can the agent infer what the user actually wants over multiple turns), and Conversation Relevancy.
llm-eval/MCP-Eval/mcp-eval.py (Multi-Turn MCP Use)

What it tests: While this script tests single-turn tool use, it also tests if the agent knows when to invoke an MCP tool (like word_count or format_citation) across a multi-turn conversation based on ongoing context.


Example evaluation once you have test cases:

```python
from deepeval import evaluate
from deepeval.metrics import TurnRelevancyMetric

evaluate(test_cases=test_cases, metrics=[TurnRelevancyMetric()])
```

## Notes

- Review generated goldens before treating them as ground truth - synthetic data is a starting point, not a replacement for curated or production examples.
- `conversation_simulator.py` imports `agent` from `agent.py`, which means module-level setup in `agent.py` (model, vectorstore, MCP client) runs on import - make sure `chroma_db/` has already been populated via `ingest.py` and `mcp_server.py` is reachable.
- This is separate from the DeepEval **safety** evals already described in the main `README.md` (`../llm-eval/safety-eval/`) - those test adversarial/misuse behavior, while these two scripts generate the functional evaluation dataset itself.
