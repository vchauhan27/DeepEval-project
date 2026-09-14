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
from deepeval.metrics import GEval


# ---------------------------------------------------------
# Judge model  (provider configured in config.py)
# ---------------------------------------------------------

JUDGE_MODEL = config.get_judge_model()

# ---------------------------------------------------------
# G-Eval metric
# ---------------------------------------------------------
# Checks a subjective quality that no other metric covers: does the
# answer actually follow the format rules laid out in the system prompt
# (answer first, then reasoning, then distinguish internal vs web
# sources)?

format_adherence_metric = GEval(
    name="Format Adherence",
    evaluation_steps=[
        "Check whether the answer is given first, before any explanation.",
        "Check whether reasoning or evidence is explained after the answer.",
        "Check whether internal knowledge base info is clearly distinguished "
        "from web search info, when both are used in the answer.",
        "Penalize heavily if the answer does not follow this structure.",
    ],
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
    ],
    threshold=0.7,
    model=JUDGE_MODEL,
    async_mode=False,
)


# ---------------------------------------------------------
# Test cases
# ---------------------------------------------------------

QUESTIONS = [
    "What embedding model is used in this research agent, and how many dimensions does it produce?",
    "Compare the internal research-agent architecture with the latest LangChain architecture.",
]


def run_agent(question: str, thread_id: str) -> str:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id="eval-user"),
    )
    return result["messages"][-1].content


test_cases = []

for i, question in enumerate(QUESTIONS):
    # Use a unique thread_id per question to prevent cross-contamination
    # from the checkpointer's conversation history.
    actual_output = run_agent(question, thread_id=f"geval-eval-{i}")

    print(f"Q: {question}")
    print(f"A: {actual_output[:200]}...\n")

    test_cases.append(
        LLMTestCase(
            input=question,
            actual_output=actual_output,
        )
    )

evaluate(
    test_cases=test_cases,
    metrics=[format_adherence_metric],
    async_config=AsyncConfig(
        run_async=False,
        throttle_value=1,
        max_concurrent=1,
    ),
)