import streamlit as st
from src.components.file_list_v2 import FileList
from src.components.file_content_v2 import FileContent
from src.components.new_file_v2 import NewFile


def app():
    st.set_page_config(page_title="MCP Music Composition", layout="wide")

    # Initialize session state
    if "view" not in st.session_state:
        st.session_state.view = None
    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None

    file_list = FileList()
    file_content = FileContent()
    new_file = NewFile()

    col_left, col_right = st.columns([1, 2])

    with col_left:
        file_list.render()

    with col_right:
        if st.session_state.view == "new_file":
            new_file.render()
        elif st.session_state.view == "file_content":
            file_content.render()


if __name__ == "__main__":
    app()
