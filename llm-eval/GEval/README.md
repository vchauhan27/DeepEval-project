# GEval Framework

This directory contains the evaluation suite for assessing the agent's output using custom LLM-as-a-judge criteria, built with [DeepEval's](https://github.com/confident-ai/deepeval) GEval metric.

## What is GEval?

**GEval = "Use an LLM to grade another LLM's output."**

You write your grading rubric in plain English, and a judge LLM reads the output and gives it a score from 0 to 1.

### How it works (3 steps)

1. **You describe what "good" looks like** in natural language (the `evaluation_steps`).
2. **The judge LLM reads the agent's output** and works through your steps one by one (chain-of-thought).
3. **It produces a score** (0–1). DeepEval uses the judge's token log-probabilities to calculate this, making it more reliable than just asking the LLM to say a number.

### GEval vs DAG — when to use which?

| | GEval | DAG |
|---|---|---|
| **Output** | A float like `0.73` | A hard `0` or `1` |
| **How** | One LLM judge scores holistically | LLM judge answers yes/no at each node in a flowchart |
| **When it fails** | You know the score is low, but not *why* | You know **exactly which node** failed |
| **Best for** | Subjective qualities (coherence, tone, format) | Hard rules (hallucination gates, tool choice checks) |

---

## Metrics Calculated

### 1. Format Adherence (`GEval.py`)

> **Question it answers:** "Did the agent structure its answer correctly?"

Checks whether the agent's response follows the expected structure — answer first, then explanation, with internal KB sources distinguished from web sources.

**Input:** One question → one answer (`LLMTestCase`)

### 2. Coherence (`coherence_GEval.py`)

> **Question it answers:** "Does the answer make logical sense?"

Checks that the answer is logically organized, free of self-contradictions, and the reasoning actually supports the conclusion. This is distinct from Format Adherence — an answer can be perfectly formatted and still incoherent.

**Input:** One question → one answer (`LLMTestCase`)

### 3. Memory Consistency (`conversational_GEval.py`)

> **Question it answers:** "Does the agent remember what the user said earlier in the conversation?"

Tests with a 2-turn conversation where the user shares their name and research goal in turn 1, then asks a follow-up in turn 2. The judge checks if the agent used that earlier context when answering. Unlike the single-turn metrics, this one sees the **whole conversation** and grades behavior across turns.

**Input:** Multiple turns (`ConversationalTestCase`)

### Summary

| File | What it grades | Single or Multi-turn |
|---|---|---|
| `GEval.py` | Is the answer **formatted** right? | Single-turn |
| `coherence_GEval.py` | Does the answer **make sense**? | Single-turn |
| `conversational_GEval.py` | Does the agent **remember** earlier turns? | Multi-turn |

---

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