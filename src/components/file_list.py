import gradio as gr
from src.fs import FileSystemWatcher
from typing import Callable
from .schema import Component


class FileList(Component):
    def __init__(self, on_click_callback: Callable[[gr.Button], None]):
        self.file_watcher = FileSystemWatcher()
        self.files_state = gr.State(self.file_watcher.get_current_files())
        self.selected_file = gr.State("")
        self.on_click_cb = on_click_callback

        self.render()

    def render(self):
        gr.Markdown("## Files")

        self.new_button = gr.Button("New File")

        @gr.render(inputs=self.files_state)
        def render_files(files: list[str]):
            for filename in files:
                variant = "secondary"
                btn = gr.Button(filename, variant=variant)
                self.on_click_cb(btn)

        # event listener
        timer = gr.Timer(1)
        timer.tick(self.reload_files, outputs=self.files_state)

    def reload_files(self) -> list[str]:
        return self.file_watcher.get_current_files()
