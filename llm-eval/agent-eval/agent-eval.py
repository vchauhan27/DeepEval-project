import sys
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
from agent import agent, invoke_with_tracing, Context  # type: ignore

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import (
    TaskCompletionMetric,
    StepEfficiencyMetric,
    PlanAdherenceMetric,
    PlanQualityMetric,
    ToolCorrectnessMetric,
    ArgumentCorrectnessMetric,
)


# ===========================================================
# PART 1 -- Trace-based metrics
# ===========================================================

# ---------------------------------------------------------
# Judge model  (provider configured in config.py)
# ---------------------------------------------------------

JUDGE_MODEL_NAME = config.JUDGE_PROVIDER
JUDGE_MODEL = config.get_judge_model()

print(f"Using judge model: {JUDGE_MODEL_NAME} (via config.py)\n")


# ===========================================================
# PART 1 -- Trace-based metrics
# (Task Completion, Step Efficiency, Plan Adherence, Plan Quality)
# ===========================================================
# These score the agent's full execution trace, not a single
# input/output pair, so they run through evals_iterator +
# invoke_with_tracing() instead of a manually-built LLMTestCase.

trace_metrics = [
    TaskCompletionMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False),
    StepEfficiencyMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False),
    PlanAdherenceMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False),
    PlanQualityMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False),
]

trace_dataset = EvaluationDataset(
    goldens=[
        Golden(input="Compare the internal research-agent architecture with the latest LangChain architecture.", multimodal=False),
    ]
)

print("=" * 70)
print("PART 1: Trace-based agentic metrics")
print("=" * 70)

for golden in trace_dataset.evals_iterator(metrics=trace_metrics):
    invoke_with_tracing(golden.input)


# ===========================================================
# PART 2 -- Tool-call-based metrics
# (Tool Correctness, Argument Correctness)
# ===========================================================
# These only need tools_called (and expected_tools) on a plain
# LLMTestCase -- no tracing required.

TOOL_TEST_CASES = [
    {
        "input": "Compare the internal research-agent architecture with the latest LangChain architecture.",
        "expected_tools": [
            ToolCall(name="retrieve_documents",  input_parameters={}),
            ToolCall(name="search_web",  input_parameters={}),
        ],
    },
]


def run_agent(question: str):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": "agent-eval-tool"}},
        context=Context(user_id="eval-user"),  # required for memory tools
    )
    messages = result["messages"]

    tools_called = []
    for message in messages:
        for call in getattr(message, "tool_calls", None) or []:
            tools_called.append(
                ToolCall(
                    name=call["name"],
                    input_parameters=call.get("args", {}),
                )
            )

    actual_output = messages[-1].content
    return actual_output, tools_called


tool_test_cases = []

for item in TOOL_TEST_CASES:
    actual_output, tools_called = run_agent(item["input"])

    print(f"\nQ: {item['input']}")
    print(f"Tools called: {[t.name for t in tools_called] or 'none'}")
    print(f"Expected tools: {[t.name for t in item['expected_tools']]}")

    tool_test_cases.append(
        LLMTestCase(
            input=item["input"],
            actual_output=actual_output,
            tools_called=tools_called,
            expected_tools=item["expected_tools"],
        )
    )

tool_metrics = [
    ToolCorrectnessMetric(threshold=0.7, include_reason=True),
    ArgumentCorrectnessMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False, include_reason=True),
]

print("\n" + "=" * 70)
print("PART 2: Tool-call-based agentic metrics")
print("=" * 70)

evaluate(
    test_cases=tool_test_cases,
    metrics=tool_metrics,
    async_config=AsyncConfig(
        run_async=False,
        throttle_value=1,
        max_concurrent=1,
    ),
)