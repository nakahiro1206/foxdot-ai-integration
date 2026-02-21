import subprocess
from pathlib import Path
from typing import Any, Iterator

from .schema import Component
import gradio as gr

VENV_PYTHON = str(Path(__file__).resolve().parents[2] / ".venv" / "bin" / "python")

UpdateEvent = dict[str, Any]


class FileContent(Component):
    def __init__(self):
        # process manager
        self.process: subprocess.Popen | None = None
        self.render()

    def render(self):
        gr.Markdown("## Content")
        self.content_box = gr.Code(
            label="Select a file to view its content.", interactive=False
        )

        with gr.Row():
            self.run_button = gr.Button("▶ Run", visible=False)
            self.stop_button = gr.Button("⏹ Stop", visible=False, variant="stop")

        self.run_output = gr.Code(label="Output", interactive=False, visible=False)

        # run script
        self.run_button.click(
            fn=self.run_script,
            inputs=[self.content_box],
            outputs=[self.run_output, self.run_button, self.stop_button],
        )

        # stop script
        self.stop_button.click(
            fn=self.stop_script,
            inputs=[],
            outputs=[self.run_output, self.run_button, self.stop_button],
        )

    def run_script(
        self, content: str
    ) -> Iterator[tuple[str, UpdateEvent, UpdateEvent]]:
        self.kill_process()
        try:
            self.process = subprocess.Popen(
                [VENV_PYTHON, "-c", content],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except Exception as e:
            yield f"Error: {e}", gr.update(interactive=True), gr.update(visible=False)
            return

        # show running state
        yield "Running...", gr.update(interactive=False), gr.update(visible=True)

        # wait for process to finish (or be killed by stop_script)
        proc = self.process
        stdout, stderr = proc.communicate()
        self.process = None

        if proc.returncode < 0:
            # killed by signal (stop button)
            return

        output = stdout
        if stderr:
            output += "\n[stderr]\n" + stderr
        yield (
            output or "(no output)",
            gr.update(interactive=True),
            gr.update(visible=False),
        )

    def stop_script(self) -> tuple[str, UpdateEvent, UpdateEvent]:
        if self.process is None:
            return (
                "(no process running)",
                gr.update(interactive=True),
                gr.update(visible=False),
            )

        self.kill_process()
        return "Stopped.", gr.update(interactive=True), gr.update(visible=False)

    def kill_process(self) -> None:
        if self.process is not None:
            try:
                self.process.kill()
                self.process.wait(timeout=5)
            except Exception:
                pass
            self.process = None

    @staticmethod
    def update_visibility(
        filename: str,
    ) -> tuple[UpdateEvent, UpdateEvent, UpdateEvent]:
        is_py = filename.endswith(".py")
        return (
            gr.update(visible=is_py),
            gr.update(visible=False),
            gr.update(visible=is_py, value=""),
        )
