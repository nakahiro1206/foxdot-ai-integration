import gradio as gr
from src.components.file_list import FileList
from src.components.file_content import FileContent
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

    def read_file(self, filename: str) -> tuple[str, str]:
        content = self.fs.read(filename)
        return filename, content

    def register_file_events(self, btn: gr.Button, selected: gr.Textbox):
        """
        This acts as your 'ref' hook. It is called every time
        a new button is instantiated in the dynamic list.
        """
        btn.click(
            fn=self.read_file,
            inputs=[btn],  # btn acts as its own value here
            outputs=[selected, self.file_content.content_box],
        ).then(
            fn=FileContent.update_visibility,
            inputs=[selected],
            outputs=[
                self.file_content.run_button,
                self.file_content.stop_button,
                self.file_content.run_output,
            ],
        )
