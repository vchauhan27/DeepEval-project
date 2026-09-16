import os
import sys
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
import config

from pathlib import Path
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_core.messages import ToolMessage

from deepeval.test_case import LLMTestCase, ConversationalTestCase, Turn
from deepeval.test_case.mcp import MCPServer, MCPToolCall
from deepeval.metrics import MCPUseMetric, MultiTurnMCPUseMetric, MCPTaskCompletionMetric
from deepeval import evaluate

from agent import agent, Context  # type: ignore

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
MCP_SERVER_PATH = BASE_DIR.parent.parent / "research-agent" / "mcp_server.py"


# ---------------------------------------------------------
# 1. Judge model  (provider configured in config.py)
# ---------------------------------------------------------

judge_model = config.get_judge_model()


# ---------------------------------------------------------
# 2. Fetch the MCP server's available primitives
# ---------------------------------------------------------

async def get_mcp_server_definition() -> MCPServer:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(MCP_SERVER_PATH)],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tool_list = await session.list_tools()
            return MCPServer(
                server_name="research-agent-utils",
                transport="stdio",
                available_tools=tool_list.tools,
            )


# ---------------------------------------------------------
# 3. Run the agent and pull out MCP tool calls per turn
# ---------------------------------------------------------

MCP_TOOL_NAMES = {"word_count", "format_citation"}


def extract_mcp_tool_calls(messages) -> list[MCPToolCall]:
    tool_calls_by_id = {}
    for m in messages:
        if getattr(m, "tool_calls", None):
            for tc in m.tool_calls:
                tool_calls_by_id[tc["id"]] = {"name": tc["name"], "args": tc["args"]}

    calls = []
    for m in messages:
        if isinstance(m, ToolMessage) and m.tool_call_id in tool_calls_by_id:
            call = tool_calls_by_id[m.tool_call_id]
            if call["name"] in MCP_TOOL_NAMES:
                calls.append(MCPToolCall(name=call["name"], args=call["args"], result=m.content))
    return calls


async def run_turn(agent, Context, question: str, thread_id: str, user_id: str = "mcp-eval-user"):
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id=user_id),
    )
    messages = result["messages"]
    answer = messages[-1].content
    mcp_calls = extract_mcp_tool_calls(messages)
    return answer, mcp_calls


# ---------------------------------------------------------
# 4. Single-turn MCP-Use
# ---------------------------------------------------------

async def eval_single_turn(mcp_server: MCPServer):

    question = (
        "How many words are in this paragraph: 'Retrieval augmented generation "
        "combines a language model with an external knowledge base so answers "
        "can be grounded in real documents instead of memorized text.' "
        "Also give me an APA citation for a 2023 article titled "
        "'Grounding LLMs with RAG' by Smith, J. on TechJournal."
    )
    answer, mcp_calls = await run_turn(agent, Context, question, thread_id="mcp-eval-single")

    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        mcp_servers=[mcp_server],
        mcp_tools_called=mcp_calls,
    )

    evaluate([test_case], [MCPUseMetric(model=judge_model)])


# ---------------------------------------------------------
# 5. Multi-turn MCP-Use + MCP Task Completion
# ---------------------------------------------------------

async def eval_multi_turn(mcp_server: MCPServer):

    thread_id = "mcp-eval-multi"
    turns = []

    conversation = [
        "Give me an MLA citation for a 2021 book titled 'Deep Learning Basics' "
        "by Doe, Jane, published by O'Reilly.",
        "Now count the words in this sentence: 'Short and to the point.'",
        "Thanks, that's all I needed.",
    ]

    for question in conversation:
        answer, mcp_calls = await run_turn(agent, Context, question, thread_id=thread_id)
        turns.append(Turn(role="user", content=question))
        turns.append(Turn(role="assistant", content=answer, mcp_tools_called=mcp_calls))

    convo_test_case = ConversationalTestCase(turns=turns, mcp_servers=[mcp_server])

    evaluate(
        [convo_test_case],
        [
            MultiTurnMCPUseMetric(model=judge_model),
            MCPTaskCompletionMetric(model=judge_model),
        ],
    )


async def main():
    mcp_server = await get_mcp_server_definition()

    print("Running single-turn MCP-Use eval...")
    await eval_single_turn(mcp_server)

    print("\nRunning multi-turn MCP-Use + MCP Task Completion eval...")
    await eval_multi_turn(mcp_server)


if __name__ == "__main__":
    asyncio.run(main())