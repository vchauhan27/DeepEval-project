# RAG Evaluation Framework

This directory contains the evaluation suite for the Retrieval-Augmented Generation (RAG) pipeline, built using [DeepEval](https://github.com/confident-ai/deepeval). It uses a judge LLM (e.g., Gemini Flash) to grade the information retrieval process and the generation of the final answer.

## Metrics Calculated

- **Answer Relevancy (`AnswerRelevancyMetric`)**: Evaluates whether the agent's final generated answer is directly relevant to the user's question, avoiding tangential or unhelpful information.
- **Faithfulness (`FaithfulnessMetric`)**: Measures whether the final answer is faithful to the retrieved context. It penalizes hallucinations or claims that are not supported by the retrieved documents.
- **Contextual Relevancy (`ContextualRelevancyMetric`)**: Assesses if the retrieved documents themselves are actually relevant to the question asked.
- **Contextual Precision (`ContextualPrecisionMetric`)**: Measures the ranking quality of the retrieved contexts—specifically, whether the most highly relevant chunks are ranked at the top.
- **Contextual Recall (`ContextualRecallMetric`)**: Evaluates if the retriever successfully found all the necessary information required to answer the question.

## How It Is Applied

We provide a set of test cases with an `input` (the question) and an `expected_output`. For example: 
*"What embedding model is used in this research agent, and how many dimensions does it produce?"* 

The script runs the agent to capture the `actual_output` and the `retrieval_context` (the exact document chunks the agent fetched). DeepEval then compares the actual output and context against the expected output to calculate the metrics.

## Example Output

