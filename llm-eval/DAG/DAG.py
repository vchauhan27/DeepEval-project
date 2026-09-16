import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
from agent import agent, Context  # type: ignore

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import DAGMetric
from deepeval.metrics.dag.graph import DeepAcyclicGraph
from deepeval.metrics.dag.nodes import (
    BinaryJudgementNode,
)


# ---------------------------------------------------------
# Judge model  (provider configured in config.py)
# ---------------------------------------------------------

JUDGE_MODEL = config.get_judge_model()

# ---------------------------------------------------------
# DAG metric
# ---------------------------------------------------------
# A deterministic rule tree instead of a single subjective judgement:
#   1. Does the answer reference the internal knowledge base at all?
#      - No  -> nothing to hallucinate, automatic pass (score 1).
#      - Yes -> check node 2.
#   2. Is every internal-knowledge claim actually backed by the
#      retrieved context?
#      - No  -> hard fail (score 0), regardless of anything else.
#      - Yes -> pass (score 1).

grounded_node = BinaryJudgementNode(
    criteria=(
        "Is every internal-knowledge-base claim in the actual output "
        "directly supported by the retrieval context?"
    ),
    evaluation_params=[
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.RETRIEVAL_CONTEXT,
    ],
)
grounded_node.add_verdict(False, score=0)  # hallucinated internal claim
grounded_node.add_verdict(True, score=1)

# Check retrieval_context directly (deterministic) instead of asking the judge
# to read the actual_output. This prevents false positives where the agent
# explicitly says "the internal KB had no info" — which is a KB mention in
# the output but means NO internal claims were made.
uses_internal_kb_node = BinaryJudgementNode(
    criteria=(
        "Does the retrieval context contain actual retrieved documents "
        "(i.e., it is NOT empty and does NOT consist solely of the string "
        "'No internal documents were retrieved.')?"
    ),
    evaluation_params=[SingleTurnParams.RETRIEVAL_CONTEXT],
)
uses_internal_kb_node.add_verdict(False, score=1)  # no internal retrieval → nothing to check
uses_internal_kb_node.add_verdict(True, then=grounded_node)

dag = DeepAcyclicGraph(root_nodes=[uses_internal_kb_node])

groundedness_gate_metric = DAGMetric(
    name="Internal Knowledge Groundedness Gate",
    dag=dag,
    threshold=0.5,
    model=JUDGE_MODEL,
    async_mode=False,
)


# ---------------------------------------------------------
# Run the agent and capture retrieval context, same approach as rag-eval.py
# ---------------------------------------------------------

QUESTIONS = [
    "What embedding model is used in this research agent, and how many dimensions does it produce?",
    "What are the latest developments in AI agent frameworks like LangChain?",
]


def run_agent(question: str, thread_id: str):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id="eval-user"),
    )
    messages = result["messages"]

    retrieval_context = [
        message.content
        for message in messages
        if getattr(message, "name", None) == "retrieve_documents"
    ]

    actual_output = messages[-1].content
    return actual_output, retrieval_context


test_cases = []

for i, question in enumerate(QUESTIONS):
    # Use a unique thread_id per question to prevent cross-contamination
    # from the checkpointer's conversation history.
    actual_output, retrieval_context = run_agent(question, thread_id=f"dag-eval-{i}")

    print(f"Q: {question}")
    print(f"Retrieved chunks: {len(retrieval_context)}\n")

    test_cases.append(
        LLMTestCase(
            input=question,
            actual_output=actual_output,
            retrieval_context=retrieval_context or ["No internal documents were retrieved."],
        )
    )

evaluate(
    test_cases=test_cases,
    metrics=[groundedness_gate_metric],
    async_config=AsyncConfig(
        run_async=False,
        throttle_value=1,
        max_concurrent=1,
    ),
)