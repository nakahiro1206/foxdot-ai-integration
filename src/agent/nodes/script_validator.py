import re
import subprocess
from src.config import config

from typing_extensions import TypedDict
from langchain_core.messages import (
    BaseMessage,
    AIMessage,
    HumanMessage,
)

from ..state import State


# ---------------------------------------------------------------------------
# Output types
# ---------------------------------------------------------------------------

class ErrorOutput(TypedDict):
    messages: list[BaseMessage]
    retry_count: int
    assembled_code: str  # write back the cleaned code so saver always gets it


class ValidationSuccessOutput(TypedDict):
    retry_count: int
    assembled_code: str  # write back the cleaned code


ScriptValidatorNodeOutput = ErrorOutput | ValidationSuccessOutput


# ---------------------------------------------------------------------------
# Runtime execution harness
# ---------------------------------------------------------------------------

# How long (seconds) to let the script run before declaring success.
# All >> assignments and FoxDot constructors are synchronous — errors surface
# before Go() is reached. os._exit() is required because FoxDot's TempoClock
# background threads prevent sys.exit() from terminating the process.
RUNTIME_TIMEOUT = 5

RUNTIME_HARNESS = """\
import os as _os
import threading as _threading
import time as _time

def Go():
    def _stopper():
        _time.sleep({timeout})
        _os._exit(0)
    t = _threading.Thread(target=_stopper, daemon=True)
    t.start()
    try:
        while True:
            _time.sleep(0.05)
    except Exception:
        pass

""".format(timeout=RUNTIME_TIMEOUT)

# stderr lines containing these strings are SC/OSC noise, not real errors
_NOISE = frozenset([
    "OSC",
    "SuperCollider",
    "Connection refused",
    "No connection",
    "sclang",
    "DeprecationWarning",
    "FutureWarning",
    "UserWarning",
    "import warnings",
    "warnings.warn",
])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(script: str) -> str:
    """Remove any markdown fences the LLM may have included."""
    if "```" in script:
        script = re.sub(r"```(?:python)?\s*", "", script).strip()
    return script


def _check_syntax(script: str) -> str | None:
    """Return an error string, or None if the script parses cleanly."""
    try:
        compile(script, "<foxdot_script>", "exec")
        return None
    except SyntaxError as e:
        return f"SyntaxError at line {e.lineno}: {e.msg}"


def _check_runtime(script: str) -> str | None:
    """
    Execute the script with a timed Go() override.

    Returns None on success (clean exit), or an error string on failure.
    The script is prepended with `from FoxDot import *` and the harness
    so that all player assignments are evaluated in a real FoxDot context.
    """
    full = "from FoxDot import *\n\n" + RUNTIME_HARNESS + script

    try:
        result = subprocess.run(
            [config.venv_python, "-c", full],
            capture_output=True,
            text=True,
            timeout=RUNTIME_TIMEOUT + 10,
        )
    except subprocess.TimeoutExpired:
        return "Runtime validation timed out."

    if result.returncode == 0:
        return None

    # Filter SC/OSC noise from stderr
    real_lines = [
        line for line in result.stderr.splitlines()
        if line.strip() and not any(noise in line for noise in _NOISE)
    ]

    if not real_lines:
        # Non-zero exit but only SC noise — treat as pass
        return None

    return "Runtime error:\n" + "\n".join(real_lines[:40])


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

class ScriptValidatorNode:

    @staticmethod
    def fn(state: State) -> ScriptValidatorNodeOutput:
        # Read from assembled_code (canonical source), fall back to last message
        script = state.get("assembled_code") or state["messages"][-1].content
        assert isinstance(script, str), "Expected script to be a string"

        # Always clean — assembler strips fences too, but this is the safety net
        script = _clean(script)

        retry_count = state.get("retry_count", 0)

        # --- Stage 1: Syntax ---
        syntax_err = _check_syntax(script)
        if syntax_err:
            return {
                "assembled_code": script,
                "messages": [
                    AIMessage(content=script),
                    HumanMessage(
                        content=(
                            f"Syntax error in the script:\n{syntax_err}\n\n"
                            "Return only the corrected FoxDot code, no markdown."
                        )
                    ),
                ],
                "retry_count": retry_count + 1,
            }

        # --- Stage 2: Runtime execution ---
        runtime_err = _check_runtime(script)
        if runtime_err:
            return {
                "assembled_code": script,
                "messages": [
                    AIMessage(content=script),
                    HumanMessage(
                        content=(
                            f"The script failed at runtime:\n{runtime_err}\n\n"
                            "Fix the error and return only the corrected FoxDot code, "
                            "no markdown."
                        )
                    ),
                ],
                "retry_count": retry_count + 1,
            }

        # All stages passed
        return {
            "assembled_code": script,
            "retry_count": retry_count,
        }
