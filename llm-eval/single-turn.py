#A single-turn test case is a blueprint provided by deepeval to unit test LLM outputs, and represents a single, atomic unit of interaction with your LLM app

from deepeval.test_case import LLMTestCase, ToolCall

test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    expected_output="You're eligible for a 30 day refund at no extra cost.",
    actual_output="We offer a 30-day full refund at no extra cost.",
    context=["All customers are eligible for a 30 day full refund at no extra cost."],
    retrieval_context=["Only shoes can be refunded."],
    tools_called=[ToolCall(name="WebSearch", input_parameters={"query": "shoes refund policy"})]
)