from pathlib import Path
from ..env import env


class FileSystem:
    def __init__(self):
        if not Path(env.data_directory).exists():
            Path(env.data_directory).mkdir(parents=True)
        self.directory = env.data_directory

    def read(self, filename: str) -> str:
        file_path = Path(self.directory) / filename
        with open(file_path, "r") as file:
            return file.read()

    def write(self, filename: str, data: str):
        file_path = Path(self.directory) / filename
        with open(file_path, "w") as file:
            file.write(data)

    def append(self, filename: str, data: str):
        file_path = Path(self.directory) / filename
        with open(file_path, "a") as file:
            file.write(data)

    def list_files(self) -> list[str]:
        return [f.name for f in Path(self.directory).iterdir() if f.is_file()]
