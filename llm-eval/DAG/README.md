# DAG Evaluation Framework

This directory contains the evaluation suite for assessing the agent's outputs using DeepAcyclicGraph (DAG) metrics from [DeepEval](https://github.com/confident-ai/deepeval). DAG metrics allow us to build deterministic rule trees instead of relying on a single subjective judgement.

## Metrics Calculated

- **Internal Knowledge Groundedness Gate (`DAGMetric`)**: A multi-step metric that checks if the agent's output relies on internal knowledge, and if so, ensures that every claim is strictly backed by the retrieved context.
- **Reasoning Validity Gate (`DAGMetric`)**: A two-step deterministic gate tailored to this agent's tool-selection + retrieval + synthesis flow:
  1. `tool_choice_node` — was an appropriate tool called for the question (not skipped when evidence was needed, not called needlessly)?
  2. `answer_follows_node` (only reached if node 1 passes) — does the final answer's conclusion actually follow from the evidence the tool returned, without unsupported leaps?

  Failing node 1 is a hard fail regardless of node 2, since a wrong tool choice makes any downstream reasoning suspect. This traces *which* reasoning step broke (tool selection vs. synthesis), which a single G-Eval float can't distinguish.
- **Memory Recall Gate (`ConversationalDAGMetric`)**: Evaluates conversational interactions using a decision tree to verify that the agent correctly recalls and uses information shared by the user in previous turns.

## How It Is Applied

For single-turn evaluations, the DAG metric traverses nodes based on the agent's `actual_output`, `retrieval_context`, and (for the Reasoning Validity Gate) `tools_called`.

- `DAG.py` runs the **Internal Knowledge Groundedness Gate**.
- `reasoning_DAG.py` runs the **Reasoning Validity Gate**, extracting `tools_called` from the agent's message trace alongside `retrieval_context`.

For multi-turn evaluations, the conversational DAG metric evaluates the agent's latest response against the entire conversation history to check for accurate recall.

- `conversational_DAG.py` runs the **Memory Recall Gate**.

## Running

```bash
python DAG.py                  # Internal Knowledge Groundedness Gate
python reasoning_DAG.py        # Reasoning Validity Gate
python conversational_DAG.py   # Memory Recall Gate
```

## Example Output