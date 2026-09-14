# GEval Framework

This directory contains the evaluation suite for assessing the agent's output using custom LLM-as-a-judge criteria, built with [DeepEval's](https://github.com/confident-ai/deepeval) GEval metric.

## Metrics Calculated

- **Format Adherence (`GEval`)**: A custom GEval metric designed to evaluate if the agent's response follows a specific structure (e.g., answering concisely first, then providing explanations).
- **Memory Consistency (`Conversational GEval`)**: A custom conversational GEval metric used in multi-turn interactions to check if the agent's current response is consistent with facts established earlier in the conversation.

## How It Is Applied

For single-turn evaluations, we provide an `input` and capture the `actual_output`. DeepEval's GEval uses a judge LLM to score the output based on defined criteria and evaluation steps.

For multi-turn evaluations, we construct a conversation history (`messages`) and evaluate the agent's ability to maintain context across turns.

## Example Output

The metrics return a score between 0 and 1, along with a pass/fail threshold. An example successful run looks like this:

```text
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric                       ┃ Average Score   ┃ Pass Rate                        ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Format Adherence [GEval]     │ 0.60            │ 50.00% | passed=1 | failed=1     │ 2      │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric                            ┃ Average Score ┃ Pass Rate                     ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Memory Consistency                │ 1.00          │ 100.00% | passed=1 | failed=0 │ 1      │
│  [Conversational GEval]            │               │                               │        │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```
