# DAG Evaluation Framework

This directory contains the evaluation suite for assessing the agent's outputs using DeepAcyclicGraph (DAG) metrics from [DeepEval](https://github.com/confident-ai/deepeval). DAG metrics allow us to build deterministic rule trees instead of relying on a single subjective judgement.

## What is DAG?

**DAG = "A decision tree of yes/no questions, evaluated in order."**

Instead of one LLM judge giving a single score (like GEval does), you build a **flowchart**. Each node asks a yes/no question. Based on the answer, it either gives a final score or moves to the next node.

### How it works (3 steps)

1. **You define nodes**, each with a yes/no question (e.g., "Is every claim backed by the retrieved context?").
2. **You wire nodes together** into a flowchart — each verdict either gives a final score or points to the next node.
3. **The judge LLM walks through the tree**, answering each node's question until it hits a final score.

### DAG vs GEval — when to use which?

| | DAG | GEval |
|---|---|---|
| **Output** | A hard `0` or `1` | A float like `0.73` |
| **How** | LLM judge answers yes/no at each node in a flowchart | One LLM judge scores holistically |
| **When it fails** | You know **exactly which node** failed | You know the score is low, but not *why* |
| **Best for** | Hard rules (hallucination gates, tool choice checks) | Subjective qualities (coherence, tone, format) |

---

## Metrics Calculated

### 1. Groundedness Gate (`DAG.py`)

> **Question it answers:** "Is the agent making stuff up from the knowledge base?"

The flowchart:
```
Did the agent actually retrieve any documents?
  │
  ├─ No  → score 1 (nothing retrieved = nothing to hallucinate, auto-pass)
  │
  └─ Yes → Is every KB claim backed by what was retrieved?
              │
              ├─ No  → score 0 (hallucinated, hard fail)
              └─ Yes → score 1 (pass)
```

**Input:** One question → one answer + retrieval context (`LLMTestCase`)

### 2. Reasoning Validity Gate (`reasoning_DAG.py`)

> **Question it answers:** "Did the agent pick the right tool AND reason correctly from it?"

The flowchart:
```
Did the agent pick the right tool for this question?
  │
  ├─ No  → score 0 (wrong tool = everything downstream is suspect)
  │
  └─ Yes → Does the conclusion follow from the retrieved evidence?
              │
              ├─ No  → score 0 (right tool, bad reasoning)
              └─ Yes → score 1 (pass)
```

**Input:** One question → one answer + retrieval context + tools called (`LLMTestCase`)

### 3. Memory Recall Gate (`conversational_DAG.py`)

> **Question it answers:** "Did the agent remember what the user said earlier?"

The flowchart (single node):
```
Did the assistant use the user's name/goal from turn 1 when answering turn 2?
  │
  ├─ No  → score 0 (forgot, hard fail)
  └─ Yes → score 10 (pass)
```

**Input:** A multi-turn conversation (`ConversationalTestCase`)

### Summary

| File | What it checks | Single or Multi-turn |
|---|---|---|
| `DAG.py` | Is the agent **hallucinating** KB claims? | Single-turn |
| `reasoning_DAG.py` | Did the agent pick the right **tool** and **reason** correctly? | Single-turn |
| `conversational_DAG.py` | Does the agent **remember** earlier turns? | Multi-turn |

---

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