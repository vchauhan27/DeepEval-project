import asyncio
from deepeval.dataset import ConversationalGolden
from deepeval.simulator import ConversationSimulator

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'research-agent')))
from agent import agent, Context  # type: ignore

conversational_goldens = [
    ConversationalGolden(
        scenario="A graduate student wants to understand retrieval augmented generation using the agent's internal knowledge base, then asks for an APA citation for a source they mention.",
        expected_outcome="The agent answers using internal documents and returns a correctly formatted APA citation via the format_citation tool.",
        user_description="A graduate student new to LLM research who asks follow-up questions when confused.",
        multimodal=False,
    ),
    ConversationalGolden(
        scenario="A software engineer asks about the latest release of a specific open-source library, then asks how many words are in the agent's summary.",
        expected_outcome="The agent uses web search for current release information and calls word_count to report the summary length.",
        user_description="A software engineer who wants concise, current answers and checks tool usage.",
        multimodal=False,
    ),
    ConversationalGolden(
        scenario="A returning user states a preference for concise answers, then later asks a new research question expecting the agent to remember that preference.",
        expected_outcome="The agent saves the stated preference with remember_fact and applies it when answering the later question.",
        user_description="A repeat user who expects the agent to remember earlier context.",
        multimodal=False,
    ),
]


# ConversationSimulator.model_callback must be sync (str) -> str.
# We run the async agent in a new event loop per call, and carry a
# thread_id in a closure so each simulated conversation is isolated.

def make_model_callback(thread_id: str):
    """Return a sync callback scoped to a specific thread_id."""
    def callback(input: str) -> str:
        async def _run():
            result = await asyncio.to_thread(
                lambda: agent.invoke(
                    {"messages": [{"role": "user", "content": input}]},
                    config={"configurable": {"thread_id": thread_id}},
                    context=Context(user_id=thread_id),
                )
            )
            last = result["messages"][-1].content
            # content can be list[...] in multi-part responses
            if isinstance(last, list):
                last = " ".join(
                    p.get("text", "") if isinstance(p, dict) else str(p)
                    for p in last
                )
            return last

        return asyncio.run(_run())

    return callback


simulator = ConversationSimulator(
    model_callback=make_model_callback("sim-thread-default"),
)

test_cases = simulator.simulate(
    conversational_goldens=conversational_goldens,
    max_user_simulations=6,
)

for i, test_case in enumerate(test_cases, start=1):
    print(f"\n--- Conversation {i} ---")
    for turn in test_case.turns:
        print(f"{turn.role}: {turn.content}")
