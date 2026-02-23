from typing import Any, Iterator

from .schema import Component
import gradio as gr
from src.process import ProcessManager

UpdateEvent = dict[str, Any]


class FileContent(Component):
    def __init__(self):
        # process manager
        self.process_manager = ProcessManager()
        self.render()

    def render(self):
        with gr.Column(visible=False) as self.container:
            gr.Markdown("## Content")

            with gr.Row():
                self.run_button = gr.Button("▶ Run", visible=False)
                self.stop_button = gr.Button("⏹ Stop", visible=False, variant="stop")

            self.run_output = gr.Code(label="Output", interactive=False, visible=False)

            self.content_box = gr.Code(
                label="Select a file to view its content.", interactive=False
            )

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
        for status in self.process_manager.run_python_script(content):
            if status.code == "running":
                yield (
                    status.message,
                    gr.update(interactive=False),
                    gr.update(visible=True),
                )
            elif status.code == "stopped":
                yield (
                    status.message,
                    gr.update(interactive=True),
                    gr.update(visible=False),
                )
            elif status.code == "error":
                yield (
                    status.message,
                    gr.update(interactive=True),
                    gr.update(visible=False),
                )
            elif status.code == "complete":
                yield (
                    status.message,
                    gr.update(interactive=True),
                    gr.update(visible=False),
                )
            else:
                raise ValueError("never reaches here")

    def stop_script(self) -> tuple[str, UpdateEvent, UpdateEvent]:
        status = self.process_manager.stop_script()
        return (status.message, gr.update(interactive=True), gr.update(visible=False))

    def update_visibility(
        self,
        filename: str,
    ) -> tuple[UpdateEvent, UpdateEvent, UpdateEvent]:
        # on updating the view, we should stop script process to avoid zombie processes
        # TODO: to improve UX, I should decouple the run/stop button from script view panel.
        self.process_manager.stop_script()
        is_py = filename.endswith(".py")
        return (
            gr.update(visible=is_py),
            gr.update(visible=False),
            gr.update(visible=is_py, value=""),
        )
