from src.components.home import App
import gradio as gr

if __name__ == "__main__":
    with gr.Blocks() as demo:
        App()
    demo.launch()
