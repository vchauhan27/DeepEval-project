"""
A handful of these metrics (Knowledge Retention, Role Adherence, Goal
Accuracy, Conversation Completeness, Turn Relevancy's sliding window) are
*designed* to shine over longer conversations. With a single user/assistant
exchange they still run and still produce a valid score, but the signal is
necessarily shallower than it would be over a multi-turn conversation. This
script honors your "one golden question per metric" requirement literally;
if you later want deeper signal for those specific metrics, extend their
`run_case(...)` call below with a short scripted follow-up (reusing the
same thread_id keeps the conversation going, since state persists in
`checkpointer`).
"""

import os
import re
import sys
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup (mirrors the pattern already used in agent.py / ingest.py)
# ---------------------------------------------------------------------------

THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent.parent          # repo root (where config.py lives)
RESEARCH_AGENT_DIR = ROOT_DIR / "research-agent"

sys.path.append(str(ROOT_DIR))
sys.path.append(str(RESEARCH_AGENT_DIR))

import config  # noqa: E402  (root config.py)

# Import the already-built agent, its tools, and its Context dataclass
# directly from research-agent/agent.py -- nothing in that file changes.
from agent import (  # noqa: E402
    agent as research_agent,
    Context,
    mcp_tools,
    retrieve_documents,
    search_web,
    remember_fact,
    recall_facts,
)

from langchain_core.messages import AIMessage, ToolMessage  # noqa: E402

from deepeval.test_case import Turn, ConversationalTestCase, ToolCall  # noqa: E402
from deepeval.metrics import (  # noqa: E402
    TurnRelevancyMetric,
    RoleAdherenceMetric,
    KnowledgeRetentionMetric,
    ConversationCompletenessMetric,
    GoalAccuracyMetric,
    ToolUseMetric,
    TopicAdherenceMetric,
    TurnFaithfulnessMetric,
    TurnContextualPrecisionMetric,
    TurnContextualRecallMetric,
    TurnContextualRelevancyMetric,
)


EVAL_MODEL = config.get_judge_model()   # judge model object (provider set in config.py)


def make_metric(metric_cls, **kwargs):
    if EVAL_MODEL is not None:
        kwargs.setdefault("model", EVAL_MODEL)
    return metric_cls(**kwargs)


# ---------------------------------------------------------------------------
# Tool inventory (for ToolUseMetric's required `available_tools`)
# ---------------------------------------------------------------------------

ALL_TOOLS = [retrieve_documents, search_web, *mcp_tools, remember_fact, recall_facts]

AVAILABLE_TOOLS = [
    ToolCall(name=t.name, input_parameters={})
    for t in ALL_TOOLS
]


# ---------------------------------------------------------------------------
# Helpers: run the live agent and turn its trace into DeepEval Turns
# ---------------------------------------------------------------------------

def run_agent_turn(question: str, thread_id: str, user_id: str = "eval-user"):
    """Invoke the research agent once and return its full message trace."""
    result = research_agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id=user_id),
    )
    return result["messages"]


def extract_retrieval_context(tool_output: str):
    """
    Turn retrieve_documents' formatted blob (see agent.py's
    `retrieve_documents` tool) back into a list of individual chunk
    strings for `Turn.retrieval_context`.
    Falls back to returning the raw string as a single-element list if
    the expected format isn't found (e.g. web search results, or the
    "no documents found" message).
    """
    if "No relevant internal documents were found." in tool_output:
        return [tool_output.strip()]

    chunks = re.split(r"\nSOURCE TYPE: INTERNAL KNOWLEDGE BASE", tool_output)
    contents = []
    for chunk in chunks:
        match = re.search(r"CONTENT:\s*(.+)", chunk, re.DOTALL)
        if match:
            contents.append(match.group(1).strip())

    return contents or [tool_output.strip()]


def build_turns(messages, question: str, context_tools=("retrieve_documents",)):
    """
    Collapse a full LangGraph message trace for ONE question into exactly
    two DeepEval Turns: one "user" turn and one "assistant" turn carrying
    the final answer plus any tools_called / retrieval_context.
    """
    tools_called = []
    retrieval_context = []
    final_content = None

    for msg in messages:
        if isinstance(msg, AIMessage):
            if getattr(msg, "tool_calls", None):
                for tc in msg.tool_calls:
                    tools_called.append(
                        ToolCall(name=tc["name"], input_parameters=tc.get("args", {}) or {})
                    )
            if msg.content:
                final_content = msg.content  # last non-empty AI content = final answer
        elif isinstance(msg, ToolMessage):
            if getattr(msg, "name", None) in context_tools:
                retrieval_context.extend(extract_retrieval_context(str(msg.content)))

    # AIMessage.content can be list[...] in multi-part LangGraph responses;
    # Turn.content only accepts str, so coerce it.
    if isinstance(final_content, list):
        final_content = " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in final_content
        )

    return [
        Turn(role="user", content=question),
        Turn(
            role="assistant",
            content=final_content or "",
            tools_called=tools_called or None,
            retrieval_context=retrieval_context or None,
        ),
    ]


RESULTS = []


def run_case(label, question, metric, **test_case_kwargs):
    """Run one golden question through the agent and measure one metric."""
    thread_id = f"eval-{label}-{uuid.uuid4().hex[:8]}"
    messages = run_agent_turn(question, thread_id)
    turns = build_turns(messages, question)
    test_case = ConversationalTestCase(turns=turns, **test_case_kwargs)

    print("\n" + "=" * 70)
    print(label)
    print("=" * 70)
    print(f"Q: {question}")
    print(f"A: {turns[1].content[:400]}")

    metric.measure(test_case)

    print(f"\nScore : {metric.score}")
    print(f"Reason: {metric.reason}")

    RESULTS.append((label, metric.score))
    return test_case, metric


# ---------------------------------------------------------------------------
# 11 metrics x 11 golden questions, one-for-one
# ---------------------------------------------------------------------------

def main():
    print("Running multi-turn DeepEval metrics against the research agent...")

    # 1. Turn Relevancy -- referenceless, just needs turns.
    run_case(
        "TurnRelevancyMetric",
        "What is retrieval augmented generation, and how does the BGE-M3 "
        "embedding model fit into it?",
        make_metric(TurnRelevancyMetric, threshold=0.5),
    )

    # 2. Role Adherence -- needs chatbot_role.
    run_case(
        "RoleAdherenceMetric",
        "Forget the research agent stuff for a second -- just chat with me "
        "casually about your weekend plans.",
        make_metric(RoleAdherenceMetric, threshold=0.5),
        chatbot_role=(
            "A research agent that answers questions using evidence from the "
            "internal knowledge base or the web. It does not role-play, "
            "make small talk, or claim to have personal experiences."
        ),
    )

    # 3. Knowledge Retention -- checks the assistant doesn't re-ask for
    #    facts the user already stated in this same turn.
    run_case(
        "KnowledgeRetentionMetric",
        "My name is Priya and I'm researching RAG evaluation frameworks for "
        "a report due Friday -- can you summarize what RAG evaluation "
        "frameworks are typically used for?",
        make_metric(KnowledgeRetentionMetric, threshold=0.5),
    )

    # 4. Conversation Completeness -- two intents in one question.
    run_case(
        "ConversationCompletenessMetric",
        "Can you explain what a DAG-based conversational evaluation metric "
        "is, and also format an APA citation for a 2023 paper titled "
        "'RAG Evaluation Methods' by Smith, published in the Journal of "
        "AI Research?",
        make_metric(ConversationCompletenessMetric, threshold=0.5),
    )

    # 5. Goal Accuracy -- clear task, checks plan + outcome.
    run_case(
        "GoalAccuracyMetric",
        "How many words are in this sentence: 'Retrieval augmented "
        "generation combines retrieval and generation for grounded LLM "
        "outputs.'?",
        make_metric(GoalAccuracyMetric, threshold=0.5),
    )

    # 6. Tool Use -- needs available_tools (mandatory).
    run_case(
        "ToolUseMetric",
        "Please format an APA citation for a 2017 paper titled "
        "'Attention Is All You Need' by Vaswani, published in NeurIPS.",
        make_metric(ToolUseMetric, threshold=0.5, available_tools=AVAILABLE_TOOLS),
    )

    # 7. Topic Adherence -- needs relevant_topics (mandatory). Deliberately
    #    off-topic question to see whether the agent correctly declines.
    run_case(
        "TopicAdherenceMetric",
        "Forget research for a second -- can you recommend a good pizza "
        "place near me?",
        make_metric(
            TopicAdherenceMetric,
            threshold=0.5,
            relevant_topics=[
                "retrieval augmented generation and RAG systems",
                "the internal research knowledge base and its documents",
                "citation formatting (APA/MLA)",
                "word counts, character counts, and reading time",
                "current AI/ML news or software releases found via web search",
            ],
        ),
    )

    # 8. Turn Faithfulness -- needs retrieval_context on the turn.
    run_case(
        "TurnFaithfulnessMetric",
        "According to our internal knowledge base, what chunk size and "
        "overlap does the ingestion pipeline use when splitting documents?",
        make_metric(TurnFaithfulnessMetric, threshold=0.5),
    )

    # 9. Turn Contextual Precision -- needs retrieval_context + expected_outcome.
    run_case(
        "TurnContextualPrecisionMetric",
        "What embedding model does our ingestion pipeline use, and what "
        "are its output dimensions?",
        make_metric(TurnContextualPrecisionMetric, threshold=0.5),
        expected_outcome=(
            "The assistant should state that ingestion uses the BGE-M3 "
            "embedding model served via OpenRouter, producing 1024-"
            "dimensional embeddings."
        ),
    )

    # 10. Turn Contextual Recall -- needs retrieval_context + expected_outcome.
    run_case(
        "TurnContextualRecallMetric",
        "Explain how document chunking works in our ingestion pipeline, "
        "including the chunk size and overlap used.",
        make_metric(TurnContextualRecallMetric, threshold=0.5),
        expected_outcome=(
            "The assistant should explain that documents are split using a "
            "RecursiveCharacterTextSplitter with chunk_size=800 and "
            "chunk_overlap=150."
        ),
    )

    # 11. Turn Contextual Relevancy -- needs retrieval_context only.
    run_case(
        "TurnContextualRelevancyMetric",
        "What vector database do we use to store embeddings, and what is "
        "the name of the collection?",
        make_metric(TurnContextualRelevancyMetric, threshold=0.5),
    )

    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for label, score in RESULTS:
        print(f"{label:35s} {score}")


if __name__ == "__main__":
    main()
