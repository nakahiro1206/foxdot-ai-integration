from dotenv import load_dotenv
import os


class Env:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        assert self.OPENAI_API_KEY != "", (
            "OPENAI_API_KEY is not set in the environment variables"
        )
        self.data_directory = os.getenv("DATA_DIRECTORY", "./data")


env = Env()
