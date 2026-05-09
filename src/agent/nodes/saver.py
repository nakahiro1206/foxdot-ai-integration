from datetime import datetime

from ..state import State
from src.fs import FileSystem
from typing_extensions import TypedDict


class SaverNodeOutput(TypedDict):
    pass


class SaverNode:
    def __init__(self, fs: FileSystem):
        self.fs = fs

    def fn(self, state: State) -> SaverNodeOutput:
        script = state.get("assembled_code", "")
        if not script:
            return {}
        
        script = "from FoxDot import *\n\n" + script + "\n\nGo()"
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{date_str}.py"
        self.fs.write(filename, script)
        print(f"Saved generated script to {filename}")
        return {}
