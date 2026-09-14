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

1. `golden_synthesis.py` → single-turn goldens for evaluating direct RAG/web-search answers with metrics like `AnswerRelevancyMetric` or `FaithfulnessMetric`.
2. `conversation_simulator.py` → multi-turn `ConversationalTestCase`s for evaluating tool selection, memory, and conversational coherence with multi-turn metrics like `TurnRelevancyMetric`.

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
