import subprocess
from typing import Iterator
from src.config import config
from src.resources import Resource
from typing import Literal


class Status:
    code: Literal["running", "stopped", "error", "complete"]
    message: str

    def __init__(
        self, code: Literal["running", "stopped", "error", "complete"], message: str
    ):
        self.code = code
        self.message = message


class ProcessManager(Resource):
    def __init__(self) -> None:
        super().register()
        self.process: subprocess.Popen | None = None
        self.venv_python = config.venv_python

    def cleanup(self) -> None:
        self.kill_process()

    def is_process_alive(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def is_process_stopped(self) -> bool:
        return self.process is not None and self.process.poll() is not None

    def run_python_script(self, content: str) -> Iterator[Status]:
        self.kill_process()
        try:
            self.process = subprocess.Popen(
                [self.venv_python, "-c", content],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except Exception as e:
            yield Status(code="error", message=f"Error: {e}")
            return

        # yield status
        yield Status(code="running", message="Running...")

        # wait for process to finish
        proc = self.process
        stdout, stderr = proc.communicate()
        self.process = None

        if proc.returncode < 0:
            # killed by signal (stop button)
            yield Status(code="stopped", message="Process was stopped.")
            return

        output = stdout
        if stderr:
            output += "\n[stderr]\n" + stderr
        yield Status(code="complete", message=output or "(no output)")

    def stop_script(self) -> Status:
        if self.is_process_stopped():
            return Status(code="stopped", message="(no process running)")

        self.kill_process()
        return Status(code="stopped", message="Stopped.")

    def kill_process(self) -> None:
        if self.process is not None:
            try:
                self.process.kill()
                self.process.wait(timeout=5)
            except Exception:
                pass
            self.process = None
