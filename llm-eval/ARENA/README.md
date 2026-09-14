# LLM Arena Evaluation Framework

This directory contains the evaluation suite for running A/B comparisons (Arena) between different prompts, models, or architectures using [DeepEval's](https://github.com/confident-ai/deepeval) Arena framework.

## How It Is Applied

The Arena test compares the outputs of two different variations (e.g., comparing responses generated from `prompt1.txt` vs `prompt2.txt`). 
It takes an `input` question and evaluates the corresponding outputs side-by-side. A judge LLM determines which response is better based on quality, detail, and relevance.

## Example Output

The output determines a "winner" for each test case or declares a tie. An example run looks like this:

```text
 Arena completed! (time taken: 62.0s | token cost: 0.0 USD)                                  
 Results (1 total test cases):
    » prompt1 (original): 1 wins

 Done ! View results on 
https://app.confident-ai.com/project/...
```
