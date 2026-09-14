# GEval Framework

This directory contains the evaluation suite for assessing the agent's output using custom LLM-as-a-judge criteria, built with [DeepEval's](https://github.com/confident-ai/deepeval) GEval metric.

## Metrics Calculated

- **Format Adherence (`GEval`)**: A custom GEval metric designed to evaluate if the agent's response follows a specific structure (e.g., answering concisely first, then providing explanations).
- **Coherence (`GEval`)**: A custom GEval metric that checks whether the answer *itself* holds together as an argument — logically organized, free of self-contradiction, and with reasoning that actually supports the stated conclusion. This is distinct from Format Adherence: an answer can follow the correct structure (answer-first, evidence labeled) and still be incoherent internally.
- **Memory Consistency (`Conversational GEval`)**: A custom conversational GEval metric used in multi-turn interactions to check if the agent's current response is consistent with facts established earlier in the conversation.

## How It Is Applied

For single-turn evaluations, we provide an `input` and capture the `actual_output`. DeepEval's GEval uses a judge LLM to score the output based on defined criteria and evaluation steps.

- `GEval.py` runs **Format Adherence**.
- `coherence_GEval.py` runs **Coherence**, using the same `run_agent()` pattern against a fresh `thread_id` per question.

For multi-turn evaluations, we construct a conversation history (`messages`) and evaluate the agent's ability to maintain context across turns.

- `conversational_GEval.py` runs **Memory Consistency**.

## Running

```bash
python GEval.py               # Format Adherence
python coherence_GEval.py     # Coherence
python conversational_GEval.py  # Memory Consistency
```

## Example Output