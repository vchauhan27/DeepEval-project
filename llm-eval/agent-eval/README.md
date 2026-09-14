# Agent Evaluation Framework

This directory contains the evaluation suite for the AI Agent workflow, built using [DeepEval](https://github.com/confident-ai/deepeval). The suite goes beyond final answers and looks at the agent's step-by-step reasoning, tool usage, and overall trajectory using a capable judge LLM (e.g., `nvidia/nemotron-3-super-120b-a12b:free`).

## Part 1: Trace-Based Metrics

These metrics analyze the entire execution trace (trajectory) of the agent, including its internal thought process and sequence of actions.

- **Task Completion (`TaskCompletionMetric`)**: Measures whether the agent ultimately completed the requested task successfully.
- **Step Efficiency (`StepEfficiencyMetric`)**: Evaluates whether the agent reached the goal using an optimal sequence of steps, penalizing unnecessary or redundant actions.
- **Plan Adherence (`PlanAdherenceMetric`)**: Measures how well the agent adhered to a logical plan or instructions during its execution loop.
- **Plan Quality (`PlanQualityMetric`)**: Assesses the quality, safety, and robustness of the agent's internal planning.

**Application**: A golden query is provided, such as *"Compare the internal research-agent architecture with the latest LangChain architecture."* The agent is invoked with tracing enabled (`invoke_with_tracing`), capturing every intermediate step, thought, and tool call for the judge model to analyze.

## Part 2: Tool-Call-Based Metrics

These metrics focus specifically on the agent's ability to select and use its available tools correctly.

- **Tool Correctness (`ToolCorrectnessMetric`)**: Measures if the agent selected the correct tool(s) for the job.
- **Argument Correctness (`ArgumentCorrectnessMetric`)**: Measures if the parameters and arguments passed to the chosen tools were accurate and well-formed.

**Application**: We define test cases that specify the `expected_tools` (e.g., `retrieve_documents` followed by `search_web`). The script captures the tools the agent *actually* called and their arguments, comparing them to the expectations.

## Example Output

