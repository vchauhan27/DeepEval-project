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
from deepeval.test_case import Turn, MultiTurnParams, ConversationalTestCase
from deepeval.models import OpenRouterModel
from deepeval.metrics import ConversationalGEval


# ---------------------------------------------------------
# Judge model
# ---------------------------------------------------------

JUDGE_MODEL = OpenRouterModel(
    model=config.eval_model_name,
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

# ---------------------------------------------------------
# Run a multi-turn conversation on one thread_id
# ---------------------------------------------------------
# Each call only sends the new user message -- the checkpointer attached
# in agent.py merges it with prior turns automatically via thread_id.

CONVERSATION = [
    "My name is Alex and I'm researching agentic RAG systems.",
    "Given what I just told you, what part of this knowledge base should I focus on first?",
]


def run_conversation(questions, thread_id="geval-conversation-1"):  # or dag-conversation-1
    config = {"configurable": {"thread_id": thread_id}}
    result = None
    for question in questions:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config=config,
            context=Context(user_id="eval-user"),
        )
    if result is None:
        return []
    return result["messages"]


def to_turns(messages):
    turns = []
    for message in messages:
        kind = type(message).__name__
        if kind == "HumanMessage":
            turns.append(Turn(role="user", content=message.content))
        elif kind == "AIMessage" and message.content:
            turns.append(Turn(role="assistant", content=message.content))
    return turns


messages = run_conversation(CONVERSATION)
turns = to_turns(messages)

print("Conversation:")
for turn in turns:
    print(f"  [{turn.role}] {turn.content[:150]}")
print()

convo_test_case = ConversationalTestCase(turns=turns)


# ---------------------------------------------------------
# Conversational G-Eval metric
# ---------------------------------------------------------
# Subjective, whole-conversation criterion: does the assistant actually
# use what the user said earlier (name, stated goal) in later replies?

memory_consistency_metric = ConversationalGEval(
    name="Memory Consistency",
    criteria=(
        "Determine whether the assistant remembers information the user "
        "shared earlier in the conversation (such as their name or stated "
        "research goal) and uses it appropriately in later replies, rather "
        "than ignoring it or asking for it again."
    ),
    evaluation_params=[MultiTurnParams.ROLE, MultiTurnParams.CONTENT],
    threshold=0.7,
    model=JUDGE_MODEL,
    async_mode=False,
)

evaluate(
    test_cases=[convo_test_case],
    metrics=[memory_consistency_metric],
    async_config=AsyncConfig(
        run_async=False,
        throttle_value=1,
        max_concurrent=1,
    ),
)