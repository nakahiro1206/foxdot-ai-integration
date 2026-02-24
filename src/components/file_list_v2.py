import streamlit as st
from src.resources import get_resource


class FileList:
    def __init__(self):
        self.file_watcher = get_resource("FileSystemWatcher")

    def render(self):
        st.markdown("## Files")

        if st.button("New File", use_container_width=True):
            st.session_state.view = "new_file"
            st.session_state.selected_file = None
            st.rerun()

        self._poll_files()

    @st.fragment(run_every=1)
    def _poll_files(self):
        files = self.file_watcher.get_current_files()
        for filename in files:
            if st.button(filename, key=f"file_{filename}", use_container_width=True):
                st.session_state.selected_file = filename
                st.session_state.view = "file_content"
                st.rerun()
