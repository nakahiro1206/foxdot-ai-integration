from langchain_core.messages import AIMessage
from typing_extensions import TypedDict

from ..state import State


class ErrorNodeOutput(TypedDict):
    messages: list[AIMessage]


class ErrorNode:
    def fn(self, state: State) -> ErrorNodeOutput:
        retry_count = state.get("retry_count", 0)
        return {
            "messages": [
                AIMessage(
                    content=f"Failed to generate a valid script after {retry_count} retries."
                )
            ]
        }
