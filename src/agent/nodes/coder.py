from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langchain_core.messages import (
    BaseMessage,
)


from ..state import State
from ..prompt import SYSTEM_PROMPT


class CoderNodeOutput(TypedDict):
    messages: list[BaseMessage]


class CoderNode:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fn(self, state: State) -> CoderNodeOutput:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
                + "\n\nOutput only FoxDot code. Do not include any explanations or markdown code tags.",
            },
            {
                "role": "user",
                "content": (
                    "Here is the composition plan to follow:\n\n"
                    + state.get("plan", "")
                    + "\n\nNow generate the FoxDot code based on this plan."
                    + "\nRemember to add explanatory comments in the code to describe what each part corresponds to in the plan."
                ),
            },
        ] + state["messages"]
        response = self.llm.invoke(messages)
        return {"messages": [response]}
