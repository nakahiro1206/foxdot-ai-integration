import streamlit as st
from src.fs import FileSystemWatcher


class FileList:
    def __init__(self):
        if "file_watcher" not in st.session_state:
            st.session_state.file_watcher = FileSystemWatcher()

    def render(self):
        st.markdown("## Files")

        if st.button("New File", use_container_width=True):
            st.session_state.view = "new_file"
            st.session_state.selected_file = None
            st.rerun()

        files = st.session_state.file_watcher.get_current_files()
        for filename in files:
            if st.button(filename, key=f"file_{filename}", use_container_width=True):
                st.session_state.selected_file = filename
                st.session_state.view = "file_content"
                st.rerun()
