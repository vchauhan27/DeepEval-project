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
# A deterministic two-step reasoning gate, tailored to what THIS agent
# actually does (tool-selection + retrieval + synthesis), not a generic
# "root cause dependency graph" -- that pattern fits a diagnostics agent,
# not a research agent.
#
#   1. Did the agent pick an appropriate tool for the question
#      (retrieve_documents / search_web not skipped when needed, not
#      called when unnecessary)?
#      - No  -> hard fail (score 0). A wrong tool choice makes any
#               downstream reasoning suspect regardless of fluency.
#      - Yes -> check node 2.
#   2. Does the final answer's conclusion actually follow from what
#      that tool returned, without unsupported leaps?
#      - No  -> hard fail (score 0).
#      - Yes -> pass (score 1).
#
# This traces WHICH reasoning step broke, unlike a single G-Eval float --
# useful for telling "bad tool choice" apart from "right tool, bad
# synthesis of the result."

answer_follows_node = BinaryJudgementNode(
    criteria=(
        "Does the actual_output's conclusion logically follow from the "
        "evidence in the retrieval context, without unsupported leaps "
        "or claims the retrieved evidence does not back up?"
    ),
    evaluation_params=[
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.RETRIEVAL_CONTEXT,
    ],
)
answer_follows_node.add_verdict(False, score=0)  # conclusion doesn't follow from evidence
answer_follows_node.add_verdict(True, score=1)

tool_choice_node = BinaryJudgementNode(
    criteria=(
        "Given the input question, was the set of tools called an "
        "appropriate choice -- i.e. retrieval/web-search was not skipped "
        "when the question required evidence, and was not called "
        "needlessly when the question didn't require it?"
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.TOOLS_CALLED,
    ],
)
tool_choice_node.add_verdict(False, score=0)  # wrong tool choice, downstream reasoning is moot
tool_choice_node.add_verdict(True, then=answer_follows_node)

dag = DeepAcyclicGraph(root_nodes=[tool_choice_node])

reasoning_validity_gate_metric = DAGMetric(
    name="Reasoning Validity Gate",
    dag=dag,
    threshold=0.5,
    model=JUDGE_MODEL,
    async_mode=False,
)


# ---------------------------------------------------------
# Run the agent and capture retrieval context + tools called
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

    # Every message carrying a tool "name" attribute represents a tool call
    # made along the way, e.g. retrieve_documents / search_web / word_count.
    tools_called = [
        message.name
        for message in messages
        if getattr(message, "name", None)
    ]

    actual_output = messages[-1].content
    return actual_output, retrieval_context, tools_called


test_cases = []

for i, question in enumerate(QUESTIONS):
    # Use a unique thread_id per question to prevent cross-contamination
    # from the checkpointer's conversation history.
    actual_output, retrieval_context, tools_called = run_agent(
        question, thread_id=f"reasoning-dag-eval-{i}"
    )

    print(f"Q: {question}")
    print(f"Tools called: {tools_called}")
    print(f"Retrieved chunks: {len(retrieval_context)}\n")

    test_cases.append(
        LLMTestCase(
            input=question,
            actual_output=actual_output,
            retrieval_context=retrieval_context or ["No internal documents were retrieved."],
            tools_called=tools_called,
        )
    )

evaluate(
    test_cases=test_cases,
    metrics=[reasoning_validity_gate_metric],
    async_config=AsyncConfig(
        run_async=False,
        throttle_value=1,
        max_concurrent=1,
    ),
)
