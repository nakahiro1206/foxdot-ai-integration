from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from ..prompt import SYSTEM_PROMPT
from ..state import State


PLAN_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + "\n\nYou are a music composition planner. Given a user's description, "
    "decompose it into concrete musical elements. For each element, specify:\n"
    "- Role (e.g., melody, bass, drums, pad/harmony, effects)\n"
    "- Synth or play() pattern to use\n"
    "- Scale, root, tempo if relevant\n"
    "- Rhythm (dur pattern), pitch pattern, and key attributes (amp, oct, etc.)\n"
    "- How elements relate to each other (e.g., follow, shared var progression)\n"
    "- Time-varying changes (var/linvar/every transforms) for evolution\n\n"
    "Output only the structured plan as plain text. Do not write any FoxDot code yet."
)


class PlanNodeOutput(TypedDict):
    plan: str


class PlannerNode:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fn(self, state: State) -> PlanNodeOutput:
        messages = [
            {"role": "system", "content": PLAN_SYSTEM_PROMPT},
        ] + state["messages"]
        response = self.llm.invoke(messages)
        return {"plan": response.content}
