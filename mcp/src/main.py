from src.components.home import App
import gradio as gr
import signal
import sys
from src.resources import resources


if __name__ == "__main__":
    with gr.Blocks() as demo:
        app = App()

    def handle_sigint(sig, frame):
        print("\nCtrl+C pressed. Shutting down...")
        resources.cleanup()
        demo.close()
        sys.exit(0)

    # Gracefully handle Ctrl+C to ensure cleanup
    signal.signal(signal.SIGINT, handle_sigint)
    demo.launch()
