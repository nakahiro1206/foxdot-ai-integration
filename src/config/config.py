from pathlib import Path


class Config:
    def __init__(self):
        self.venv_python = (
            Path(__file__).resolve().parents[2] / ".venv" / "bin" / "python"
        )
        self.foxdot_instruct = (
            Path(__file__).resolve().parents[2] / "fox_dot" / "INSTRUCT.md"
        )
        self.foxdot_stub = Path(__file__).resolve().parents[2] / "fox_dot" / "stubs"


config = Config()
