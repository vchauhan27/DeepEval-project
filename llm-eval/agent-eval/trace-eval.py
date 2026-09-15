import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
from agent import agent, invoke_with_tracing, Context  # type: ignore

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import (
    TaskCompletionMetric,
    StepEfficiencyMetric,
    PlanAdherenceMetric,
    PlanQualityMetric,
)

# ---------------------------------------------------------
# Judge model  (provider configured in config.py)
# ---------------------------------------------------------
JUDGE_MODEL = config.get_judge_model()

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
