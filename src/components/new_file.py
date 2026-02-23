import gradio as gr
from src.fs import FileSystem
from src.agent import State, MucisComposerService
from langchain_core.messages import HumanMessage
from .schema import Component


class NewFile(Component):
    def __init__(self, fs: FileSystem):
        self.fs = fs
        self.music_composer_service = MucisComposerService(self.fs)
        self.render()

    def render(self):
        with gr.Column(visible=False) as self.container:
            gr.Markdown("## New File")

            self.user_query = gr.Textbox(
                label="Describe your music idea", interactive=True
            )
            self.generation_button = gr.Button("Generate")
            self.output_box = gr.Code(label="Generated Music Script", interactive=False)
            self.status_text = gr.Markdown("")

            self.generation_button.click(
                fn=self.generate,
                inputs=[self.user_query],
                outputs=[self.output_box, self.status_text],
            )

    async def generate(self, query: str):
        if not query.strip():
            yield "", "⚠️ Please describe your music idea."
            return

        initial_state: State = {
            "messages": [HumanMessage(content=query)],
            "plan": "",
            "retry_count": 0,
        }

        accumulated = ""
        yield accumulated, "⏳ Generating..."

        async for chunk_json in self.music_composer_service.astream_events(
            initial_state
        ):
            accumulated += chunk_json
            yield accumulated, "⏳ Generating..."

        yield accumulated, "✅ Generation complete."
