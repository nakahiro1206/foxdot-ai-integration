import gradio as gr
from src.fs import FileSystemWatcher
from typing import Callable
from .schema import Component


class FileList(Component):
    def __init__(self, on_click_callback: Callable[[gr.Button, gr.Textbox], None]):
        self.file_watcher = FileSystemWatcher()
        self.files_state = gr.State(self.file_watcher.get_current_files())
        self.on_click_cb = on_click_callback

        self.render()

    def render(self):
        gr.Markdown("## Files")
        selected = gr.Textbox(label="Selected File", interactive=False)

        @gr.render(inputs=self.files_state)
        def render_files(files: list[str]):
            for filename in files:
                btn = gr.Button(filename)
                self.on_click_cb(btn, selected)

        # event listener
        timer = gr.Timer(1)
        timer.tick(self.reload_files, outputs=self.files_state)

    def reload_files(self) -> list[str]:
        return self.file_watcher.get_current_files()

    def update_files(self, files: list[str]):
        self.files_state.value = files

    @staticmethod
    def on_click(filename: str) -> str:
        return filename
