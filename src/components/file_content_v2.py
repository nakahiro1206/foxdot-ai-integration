import streamlit as st
from src.process import ProcessManager
from src.resources import get_resource


class FileContent:
    def __init__(self):
        self.process_manager = get_resource("ProcessManager")
        self.fs = get_resource("FileSystem")

    def render(self):
        filename = st.session_state.get("selected_file")
        if not filename:
            return

        st.markdown("## Content")

        is_py = filename.endswith(".py")

        if is_py:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("▶ Run"):
                    self._run_script(st.session_state.file_content_text)
            with col2:
                if st.button("⏹ Stop"):
                    self._stop_script()

        content = self.fs.read(filename)
        st.session_state.file_content_text = content

        st.code(content, language="python" if is_py else None)

        if is_py and "run_output" in st.session_state:
            st.markdown("### Output")
            st.code(st.session_state.run_output)

    def _run_script(self, content: str):
        pm: ProcessManager = self.process_manager
        pm.stop_script()
        output = ""
        for status in pm.run_python_script(content):
            if status.code == "complete":
                output = status.message
            elif status.code == "error":
                output = status.message
            elif status.code == "stopped":
                output = status.message
        st.session_state.run_output = output

    def _stop_script(self):
        pm: ProcessManager = self.process_manager
        status = pm.stop_script()
        st.session_state.run_output = status.message
