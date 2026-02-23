import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from src.config import config

from typing_extensions import TypedDict
from langchain_core.messages import (
    BaseMessage,
    AIMessage,
    HumanMessage,
)

from ..state import State


class SyntaxErrorOutput(TypedDict):
    messages: list[BaseMessage]
    retry_count: int


class UndefinedNamesOutput(TypedDict):
    messages: list[BaseMessage]
    retry_count: int


class ValidationSuccessOutput(TypedDict):
    retry_count: int


ScriptValidatorNodeOutput = (
    SyntaxErrorOutput | UndefinedNamesOutput | ValidationSuccessOutput
)


class ScriptValidatorNode:
    @staticmethod
    def run_pyright(script: str) -> list[str]:
        """Run pyright on a FoxDot script and return undefined-variable errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)

            # Pyright config pointing to static FoxDot stubs
            (tmp / "pyrightconfig.json").write_text(
                json.dumps(
                    {
                        "stubPath": str(config.foxdot_stub),
                        "reportMissingModuleSource": False,
                        "reportUnusedExpression": False,
                    }
                )
            )

            # Script file (prepend the FoxDot import)
            script_path = tmp / "script.py"
            script_path.write_text(f"from FoxDot import *\n{script}")

            result = subprocess.run(
                [sys.executable, "-m", "pyright", "--outputjson", str(script_path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tmpdir,
            )

            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError:
                return []

            errors: list[str] = []
            for diag in data.get("generalDiagnostics", []):
                if diag.get("rule") == "reportUndefinedVariable":
                    line = diag["range"]["start"]["line"]  # 0-indexed; line 0 = import
                    msg = diag.get("message", "")
                    errors.append(f"Line {line}: {msg}")
            return errors

    @staticmethod
    def fn(state: State) -> ScriptValidatorNodeOutput:
        script = state["messages"][-1].content
        assert isinstance(script, str), (
            "Expected the last message content to be a string containing the FoxDot script"
        )
        # Clean markdown if the LLM ignored instructions
        if script.startswith("```"):
            script = re.sub(r"```python|```", "", script).strip()

        try:
            compile(script, "<foxdot_script>", "exec")
        except SyntaxError as e:
            error_msg = f"Syntax error at line {e.lineno}: {e.msg}"
            retry_count = state.get("retry_count", 0) + 1
            return {
                "messages": [
                    AIMessage(content=script),
                    HumanMessage(
                        content=f"The generated script has a syntax error:\n{error_msg}\nPlease fix it and return only the corrected FoxDot code."
                    ),
                ],
                "retry_count": retry_count,
            }

        pyright_errors = ScriptValidatorNode.run_pyright(script)
        if pyright_errors:
            error_msg = "Pyright found undefined names:\n" + "\n".join(pyright_errors)
            retry_count = state.get("retry_count", 0) + 1
            return {
                "messages": [
                    AIMessage(content=script),
                    HumanMessage(
                        content=f"The generated script has undefined names:\n{error_msg}\n"
                        "Use only valid FoxDot synths and built-in objects. "
                        "Please fix it and return only the corrected FoxDot code."
                    ),
                ],
                "retry_count": retry_count,
            }
        return {"retry_count": state.get("retry_count", 0)}
