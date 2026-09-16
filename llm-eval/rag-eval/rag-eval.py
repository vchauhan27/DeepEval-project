import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
import config

from agent import agent  # type: ignore

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)


# ---------------------------------------------------------
# Judge model  (provider configured in config.py)
# ---------------------------------------------------------

os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "120")

JUDGE_MODEL = config.get_judge_model()

# ---------------------------------------------------------
# Test cases
# ---------------------------------------------------------

TEST_CASES = [
    {
        "input": "What embedding model is used in this research agent, and how many dimensions does it produce?",
        "expected_output": (
            "The agent uses the BGE-M3 embedding model from BAAI, accessed "
            "through OpenRouter with the identifier baai/bge-m3. It produces "
            "1024-dimensional dense embeddings, which are stored in the Chroma "
            "vector database."
        ),
    }
]


# ---------------------------------------------------------
# Run the agent and capture the retrieval context
# ---------------------------------------------------------

def run_rag(question: str):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": str(uuid.uuid4())}},
    )
    messages = result["messages"]

    retrieval_context = [
        message.content
        for message in messages
        if getattr(message, "name", None) == "retrieve_documents"
    ]

    return messages[-1].content, retrieval_context


# ---------------------------------------------------------
# Metrics — all share the same config, so build them in a loop
# ---------------------------------------------------------

metrics = [
    AnswerRelevancyMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
    FaithfulnessMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
    ContextualRelevancyMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
    ContextualPrecisionMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
    ContextualRecallMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
]

test_cases = []

for item in TEST_CASES:
    actual_output, retrieval_context = run_rag(item["input"])

    print(f"Q: {item['input']}")
    print(f"Retrieved chunks: {len(retrieval_context)}\n")

    if not retrieval_context:
        print("  Skipping RAG-context metrics (no internal retrieval occurred).\n")
        continue

    test_cases.append(
        LLMTestCase(
            input=item["input"],
            actual_output=actual_output,
            expected_output=item["expected_output"],
            retrieval_context=retrieval_context,
        )
    )

if test_cases:
    evaluate(
        test_cases=test_cases,
        metrics=metrics,
        async_config=AsyncConfig(
            run_async=False,
            throttle_value=1,
            max_concurrent=1,
        ),
    )
else:
    print("No test cases had internal retrieval context to evaluate against.")