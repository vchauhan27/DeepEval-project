import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
from agent import agent, Context  # type: ignore

from deepteam import red_team
from deepteam.vulnerabilities import Robustness
from deepteam.attacks.single_turn import PromptInjection, ContextPoisoning

CALL_COUNT = 0


async def model_callback(input: str) -> str:
    global CALL_COUNT
    CALL_COUNT += 1
    thread_id = f"fault-injection-{CALL_COUNT}"
    result = agent.invoke(
        {"messages": [{"role": "user", "content": input}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id="eval-user"),
    )
    return result["messages"][-1].content


risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=[Robustness()],
    attacks=[PromptInjection(weight=3), ContextPoisoning(weight=2)],
)

print(risk_assessment)
