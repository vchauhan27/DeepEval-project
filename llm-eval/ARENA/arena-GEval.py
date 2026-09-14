import sys
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))

from langchain.agents import create_agent
from agent import model, retrieve_documents, search_web, remember_fact, recall_facts, checkpointer, store, Context, BASE_DIR #type:ignore

from deepeval import compare
from deepeval.test_case import ArenaTestCase, LLMTestCase, SingleTurnParams, Contestant
from deepeval.models import OpenRouterModel
from deepeval.metrics import ArenaGEval


# ---------------------------------------------------------
# Judge model
# ---------------------------------------------------------

JUDGE_MODEL = OpenRouterModel(
    model=config.eval_model_name,
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)



# ---------------------------------------------------------
# Build one agent per prompt file and get its answer
# ---------------------------------------------------------
# agent.py no longer switches prompts via env var, so we build two
# independent agent instances directly here, reusing the same model and
# tools already set up in agent.py.

def get_answer(prompt_filename: str, question: str, thread_id: str) -> str:
    prompt_text = (BASE_DIR / prompt_filename).read_text(encoding="utf-8")

    variant_agent = create_agent(
        model=model,
        tools=[retrieve_documents, search_web, remember_fact, recall_facts],
        system_prompt=prompt_text,
        checkpointer=checkpointer,
        store=store,
        context_schema=Context,
    )

    result = variant_agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id="eval-user"),
    )
    return result["messages"][-1].content


QUESTION = "Compare the internal research-agent architecture with the latest LangChain architecture."

print(f"Q: {QUESTION}\n")

answer_prompt1 = get_answer("prompt1.txt", QUESTION, thread_id="arena-prompt1")
print("--- prompt1.txt answer ---")
print(answer_prompt1[:300], "...\n")

answer_prompt2 = get_answer("prompt2.txt", QUESTION, thread_id="arena-prompt2")
print("--- prompt2.txt answer ---")
print(answer_prompt2[:300], "...\n")


# ---------------------------------------------------------
# Arena G-Eval
# ---------------------------------------------------------

arena_test_case = ArenaTestCase(
    contestants=[
        Contestant(
            name="prompt1 (original)",
            hyperparameters={"prompt_file": "prompt1.txt"},
            test_case=LLMTestCase(
                input=QUESTION,
                actual_output=answer_prompt1,
            ),
        ),
        Contestant(
            name="prompt2 (with planning step)",
            hyperparameters={"prompt_file": "prompt2.txt"},
            test_case=LLMTestCase(
                input=QUESTION,
                actual_output=answer_prompt2,
            ),
        ),
    ]
)

quality_metric = ArenaGEval(
    name="Answer Quality",
    criteria=(
        "Choose the contestant whose answer better follows the agent's "
        "expected answer format: giving the answer first, then explaining "
        "the reasoning/evidence, and clearly distinguishing internal "
        "knowledge base information from web search information."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
    ],
    model=JUDGE_MODEL,
    async_mode=False,
)

compare(test_cases=[arena_test_case], metric=quality_metric)