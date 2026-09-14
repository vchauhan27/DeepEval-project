# DAG Evaluation Framework

This directory contains the evaluation suite for assessing the agent's outputs using DeepAcyclicGraph (DAG) metrics from [DeepEval](https://github.com/confident-ai/deepeval). DAG metrics allow us to build deterministic rule trees instead of relying on a single subjective judgement.

## Metrics Calculated

- **Internal Knowledge Groundedness Gate (`DAGMetric`)**: A multi-step metric that checks if the agent's output relies on internal knowledge, and if so, ensures that every claim is strictly backed by the retrieved context.
- **Memory Recall Gate (`ConversationalDAGMetric`)**: Evaluates conversational interactions using a decision tree to verify that the agent correctly recalls and uses information shared by the user in previous turns.

## How It Is Applied

For single-turn evaluations, the DAG metric traverses nodes (like `uses_internal_kb_node` and `grounded_node`) based on the agent's `actual_output` and `retrieval_context`.

For multi-turn evaluations, the conversational DAG metric evaluates the agent's latest response against the entire conversation history to check for accurate recall.

## Example Output

The DAG metrics traverse the decision tree to calculate a score and return a reason for the outcome. An example output looks like this:

```text
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric                              ┃ Average Score ┃ Pass Rate                   ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Internal Knowledge Groundedness     │ 0.10          │ 0.00% | passed=0 | failed=2 │ 2      │
│  Gate [DAG]                          │               │                             │        │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric                            ┃ Average Score ┃ Pass Rate                     ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Memory Recall Gate                │ 1.00          │ 100.00% | passed=1 | failed=0 │ 1      │
│  [ConversationalDAG]               │               │                               │        │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```
