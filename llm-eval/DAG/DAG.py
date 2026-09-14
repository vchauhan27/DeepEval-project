import sys
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
from agent import agent, Context  # type: ignore

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.models import OpenRouterModel
from deepeval.metrics import DAGMetric
from deepeval.metrics.dag.graph import DeepAcyclicGraph
from deepeval.metrics.dag.nodes import (
    BinaryJudgementNode,
)


# ---------------------------------------------------------
# Judge model
# ---------------------------------------------------------

JUDGE_MODEL = OpenRouterModel(
    model=config.eval_model_name,
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

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

uses_internal_kb_node = BinaryJudgementNode(
    criteria="Does the actual output reference information from the internal knowledge base?",
    evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
)
uses_internal_kb_node.add_verdict(False, score=1)  # no internal claims, nothing to check
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


def run_agent(question: str):
    result = agent.invoke(
    {"messages": [{"role": "user", "content": question}]},
    config={"configurable": {"thread_id": "eval-thread"}},
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

for question in QUESTIONS:
    actual_output, retrieval_context = run_agent(question)

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