# MCP Server Evaluation Framework

This directory contains the evaluation suite for testing Model Context Protocol (MCP) server integrations, built using [DeepEval](https://github.com/confident-ai/deepeval). The suite evaluates whether an LLM can correctly utilize exposed MCP tools in both single-turn and multi-turn (conversational) scenarios.

## MCP Metrics

These metrics analyze the agent's ability to discover, select, and accurately pass arguments to MCP tools like `word_count` or `format_citation`.

- **MCP Use (`MCPUseMetric`)**: Measures if the agent correctly selected and executed the appropriate MCP tool for a single-turn request.
- **Multi-Turn MCP Use (`MultiTurnMCPUseMetric`)**: Evaluates the agent's tool usage over a multi-turn conversation, verifying it can chain tools or use them at the right step in a dialogue.
- **MCP Task Completion (`MCPTaskCompletionMetric`)**: Assesses whether the overall conversational task was successfully resolved using the provided MCP tools.

**Application**: Conversational test cases are provided, such as asking the agent to format a citation, followed by counting the words in a sentence. The evaluation tracks the agent's interaction with the MCP server across the conversation.

## Example Output

The evaluation logs the conversational turns and checks if the correct MCP tools were invoked at the right time. The judge evaluates the correctness of the tool calls and the final resolution, generating an aggregate metrics table:

```text
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                           │
│                                                                                             │
│  Metric                   ┃ Average Score     ┃ Pass Rate                         ┃ Total   │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━ │
│  Multi-Turn MCP Use       │ 0.00              │ 0.00% | passed=0 | failed=1       │ 1       │
│  MCP Task Completion      │ 0.00              │ 0.00% | passed=0 | failed=1       │ 1       │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

**Note on MCP Task Completion**: In the example above, the metrics scored **0.00** (and thus failed). The judge LLM provided a reason for this failure: the application failed to achieve any successful outcomes, implying the agent might have hallucinated the word count and citation instead of actually invoking the MCP server's tools. DeepEval exposes these details to debug tool-calling pipelines.
