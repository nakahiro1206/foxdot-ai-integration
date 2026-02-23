from datetime import datetime

from langchain_core.messages import AIMessage

from src.fs import FileSystem
from ..state import State
from typing_extensions import TypedDict


class SaverNodeOutput(TypedDict):
    pass


class SaverNode:
    def __init__(self, fs: FileSystem):
        self.fs = fs

    def fn(self, state: State) -> SaverNodeOutput:
        script: str | None = None
        for msg in reversed(state["messages"]):
            if isinstance(msg, AIMessage) and msg.content:
                script = msg.content
                break
        else:
            return {}

        if not script:
            return {}

        script = "from FoxDot import *\n\n" + script + "\n\nGo()"
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{date_str}.py"
        self.fs.write(filename, script)
        print(f"Saved generated script to {filename}")
        return {}
