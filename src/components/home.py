
import gradio as gr
from src.components.file_list import FileList
from src.components.file_content import FileContent
from src.components.new_file import NewFile
from src.fs import FileSystem
from .schema import Component


class App(Component):
    def __init__(self):
        self.fs = FileSystem()
        self.render()

    def render(self):
        with gr.Row():
            with gr.Column(scale=1):
                self.file_list = FileList(on_click_callback=self.register_file_events)

            with gr.Column(scale=2):
                self.file_content = FileContent()
                self.new_file = NewFile(self.fs)

        # Toggle: clicking "New File" shows new_file panel, hides file_content
        self.file_list.new_button.click(
            fn=lambda: (
                gr.update(visible=False),
                gr.update(visible=True),
            ),
            outputs=[
                self.file_content.container,
                self.new_file.container,
            ],
        )

    def read_file(self, filename: str) -> str:
        content = self.fs.read(filename)
        return content

    def register_file_events(self, btn: gr.Button):
        """
        This acts as your 'ref' hook. It is called every time
        a new button is instantiated in the dynamic list.
        """
        btn.click(
            fn=self.read_file,
            inputs=[btn],  # btn acts as its own value here
            outputs=[self.file_content.content_box],
        ).then(
            fn=self.file_content.update_visibility,
            inputs=[btn],
            outputs=[
                self.file_content.run_button,
                self.file_content.stop_button,
                self.file_content.run_output,
            ],
        ).then(
            fn=lambda: (gr.update(visible=True), gr.update(visible=False)),
            outputs=[self.file_content.container, self.new_file.container],
        )
