import sys
import os
import statistics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
from agent import agent, Context  # type: ignore

from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

JUDGE_MODEL = config.get_judge_model()

QUESTIONS = [
    "What embedding model is used in this research agent, and how many dimensions does it produce?",
    "What are the latest developments in AI agent frameworks like LangChain?",
]

NUM_PARAPHRASES = 3


def generate_paraphrases(question, n):
    prompt = (
        f"Generate {n} paraphrases of the following question. "
        "Keep the exact same meaning and intent, only change the wording. "
        "Return them as a numbered list, nothing else.\n\n"
        f"Question: {question}"
    )
    output = JUDGE_MODEL.generate(prompt)
    if isinstance(output, tuple):
        output = output[0]
    output_str = str(output)
    lines = [line.strip() for line in output_str.split("\n") if line.strip()]
    paraphrases = []
    for line in lines:
        cleaned = line.lstrip("0123456789.-) ").strip()
        if cleaned:
            paraphrases.append(cleaned)
    return paraphrases[:n]


def run_agent(question, thread_id):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id="eval-user"),
    )
    return result["messages"][-1].content


metric = AnswerRelevancyMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False)

for q_index, question in enumerate(QUESTIONS):
    paraphrases = [question] + generate_paraphrases(question, NUM_PARAPHRASES)

    print(f"Original: {question}")
    scores = []

    for p_index, paraphrase in enumerate(paraphrases):
        actual_output = run_agent(paraphrase, thread_id=f"paraphrase-{q_index}-{p_index}")
        test_case = LLMTestCase(input=paraphrase, actual_output=actual_output)
        metric.measure(test_case)
        scores.append(metric.score)
        print(f"  [{p_index}] {paraphrase}")
        print(f"      score = {metric.score:.3f}")

    mean = statistics.mean(scores)
    stdev = statistics.stdev(scores) if len(scores) > 1 else 0.0
    print(f"  mean = {mean:.3f}  stdev = {stdev:.3f}\n")
