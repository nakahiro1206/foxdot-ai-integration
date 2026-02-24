"""
users can re-create the existing file content by sending a query
"""

import streamlit as st
from langchain_core.messages import HumanMessage
from src.agent import MusicComposerService, State
from src.resources import get_resource


class EditRequest:
    def __init__(self):
        self.music_composer_service = get_resource("MusicComposerService")
        self.fs = get_resource("FileSystem")

    def render(self):
        filename = st.session_state.get("selected_file")
        if not filename:
            return

        st.markdown("## Edit Request")

        query = st.text_input("Describe how to modify this music")

        if st.button("Regenerate"):
            if not query.strip():
                st.warning("Please describe how you want to edit the music.")
                return

            content = self.fs.read(filename)
            prompt = (
                f"The current file '{filename}' has the following content:\n"
                f"```\n{content}\n```\n\n"
                f"Edit request: {query}"
            )

            st.markdown("### Regenerated Code")
            st.write_stream(self._stream_generation(prompt))

    async def _stream_generation(self, query: str):
        service: MusicComposerService = self.music_composer_service

        initial_state: State = {
            "messages": [HumanMessage(content=query)],
            "plan": "",
            "retry_count": 0,
        }

        async for chunk in service.astream_events(initial_state):
            yield chunk
