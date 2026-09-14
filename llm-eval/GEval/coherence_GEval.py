
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
# Checks a subjective quality that Format Adherence does NOT cover:
# Format Adherence checks the *shape* of the answer (answer-first,
# evidence labeled, sources distinguished). Coherence checks whether
# the *argument itself* holds together -- no self-contradiction, no
# non-sequiturs, reasoning that actually supports the stated answer.
# An answer can be perfectly formatted and still incoherent.

coherence_metric = GEval(
    name="Coherence",
    evaluation_steps=[
        "Check whether the actual_output is logically organized and easy to follow "
        "from start to finish.",
        "Check for any self-contradiction within the actual_output (e.g. stating "
        "one fact early on and an incompatible fact later).",
        "Check whether the reasoning or evidence presented actually supports the "
        "conclusion/answer given, rather than being disconnected from it.",
        "Penalize outputs that read as fragmented, jump between unrelated points, "
        "or draw a conclusion that does not follow from the evidence stated.",
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
    actual_output = run_agent(question, thread_id=f"coherence-eval-{i}")

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
    metrics=[coherence_metric],
    async_config=AsyncConfig(
        run_async=False,
        throttle_value=1,
        max_concurrent=1,
    ),
)
