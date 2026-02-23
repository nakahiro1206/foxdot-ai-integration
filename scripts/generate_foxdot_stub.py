"""Generate a pyright stub file from the installed FoxDot package.

Usage:
    uv run python scripts/generate_foxdot_stub.py

This introspects `from FoxDot import *` at runtime and writes a .pyi stub
so that pyright can validate generated FoxDot scripts for undefined names.
Re-run this script whenever you upgrade the FoxDot package.
"""

import importlib
import keyword
from pathlib import Path

OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "fox_dot"
    / "stubs"
    / "FoxDot"
    / "__init__.pyi"
)


def main() -> None:
    mod = importlib.import_module("FoxDot")
    all_names = getattr(mod, "__all__", None) or dir(mod)

    names = [
        n
        for n in all_names
        if not n.startswith("_") and n.isidentifier() and not keyword.iskeyword(n)
    ]

    lines = ["from typing import Any", ""]
    for name in sorted(names):
        lines.append(f"{name}: Any")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines) + "\n")
    print(f"Wrote {len(names)} names to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
