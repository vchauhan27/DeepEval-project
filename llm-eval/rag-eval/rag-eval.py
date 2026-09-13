from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import LLMTestCase
from deepeval.models import GeminiModel
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'research-agent')))
from agent import agent  # type: ignore


# ---------------------------------------------------------
# Judge model
# ---------------------------------------------------------

os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "120")

JUDGE_MODEL_NAME = os.environ.get("JUDGE_MODEL_NAME", "gemini-flash-lite-latest")

JUDGE_MODEL = GeminiModel(
    model=JUDGE_MODEL_NAME,
    api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=0,
)

print(f"Using judge model: {JUDGE_MODEL_NAME} (Google AI Studio)\n")


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
# Run the agent and capture the retrieval context it actually used
# ---------------------------------------------------------

def run_rag(question: str):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    messages = result["messages"]

    retrieval_context = [
        message.content
        for message in messages
        if getattr(message, "name", None) == "retrieve_documents"
    ]

    tools_called = sorted(
        {
            call["name"]
            for message in messages
            if hasattr(message, "tool_calls")
            for call in (message.tool_calls or [])
        }
    )

    actual_output = messages[-1].content

    return actual_output, retrieval_context, tools_called


# async_mode=False forces each metric's internal LLM calls to run
# sequentially instead of concurrently -- critical when the judge is a
# free, rate-limited model. This will be noticeably slower wall-clock,
# but far less likely to time out or get throttled.
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
    actual_output, retrieval_context, tools_called = run_rag(item["input"])

    print(f"Q: {item['input']}")
    print(f"Tools called: {tools_called or 'none'}")
    print(f"Retrieved chunks: {len(retrieval_context)}\n")

    if not retrieval_context:
        print(
            "  Skipping RAG-context metrics for this question "
            "(no internal retrieval occurred).\n"
        )
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
    # Gemini's free tier still has per-minute rate limits (e.g. Flash
    # models are typically capped around 15 requests/minute), so keep
    # concurrency low rather than letting all 5 metrics fire at once.
    # If you're on a paid Gemini tier, you can safely raise max_concurrent
    # and set async_mode=True on the metrics above for faster runs.
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