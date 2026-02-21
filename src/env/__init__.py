from dotenv import load_dotenv
import os
from pathlib import Path


class _Env:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        assert self.OPENAI_API_KEY, (
            "OPENAI_API_KEY is not set in the environment variables"
        )
        self.data_directory = os.getenv("DATA_DIRECTORY", "./data")
        self.venv_python = (
            Path(__file__).resolve().parents[2] / ".venv" / "bin" / "python"
        )


env = _Env()
