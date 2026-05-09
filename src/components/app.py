import streamlit as st
from src.components.file_list_v2 import FileList
from src.components.file_content_v2 import FileContent
from src.components.new_file_v2 import NewFile
from src.components.regenerate import EditRequest
from .schema import Component


class App(Component):
    def __init__(self):
        st.set_page_config(page_title="MCP Music Composition", layout="wide")

        # Initialize session state
        if "view" not in st.session_state:
            st.session_state.view = None
        if "selected_file" not in st.session_state:
            st.session_state.selected_file = None

        self.file_list = FileList()
        self.file_content = FileContent()
        self.new_file = NewFile()
        self.edit_request = EditRequest()

    def render(self):
        col_left, col_right = st.columns([1, 2])

        with col_left:
            self.file_list.render()

        with col_right:
            if st.session_state.view == "new_file":
                self.new_file.render()
            elif st.session_state.view == "file_content":
                self.file_content.render()
                self.edit_request.render()
