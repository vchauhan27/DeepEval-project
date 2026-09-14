# MCP Server Evaluation Framework

This directory contains the evaluation suite for testing Model Context Protocol (MCP) server integrations, built using [DeepEval](https://github.com/confident-ai/deepeval). The suite evaluates whether an LLM can correctly utilize exposed MCP tools in both single-turn and multi-turn (conversational) scenarios.

## MCP Metrics

These metrics analyze the agent's ability to discover, select, and accurately pass arguments to MCP tools like `word_count` or `format_citation`.

- **MCP Use (`MCPUseMetric`)**: Measures if the agent correctly selected and executed the appropriate MCP tool for a single-turn request.
- **Multi-Turn MCP Use (`MultiTurnMCPUseMetric`)**: Evaluates the agent's tool usage over a multi-turn conversation, verifying it can chain tools or use them at the right step in a dialogue.
- **MCP Task Completion (`MCPTaskCompletionMetric`)**: Assesses whether the overall conversational task was successfully resolved using the provided MCP tools.

**Application**: Conversational test cases are provided, such as asking the agent to format a citation, followed by counting the words in a sentence. The evaluation tracks the agent's interaction with the MCP server across the conversation.

## Example Output

