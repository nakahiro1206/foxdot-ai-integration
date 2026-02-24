import streamlit as st
from langchain_core.messages import HumanMessage
from src.agent import MucisComposerService, State
from src.resources import get_resource


class NewFile:
    def __init__(self):
        self.music_composer_service = get_resource("MucisComposerService")

    def render(self):
        st.markdown("## New File")

        query = st.text_input("Describe your music idea")

        if st.button("Generate"):
            if not query.strip():
                st.warning("Please describe your music idea.")
                return

            st.markdown("### Generated Code")
            st.write_stream(self._stream_generation(query))

    async def _stream_generation(self, query: str):
        service: MucisComposerService = self.music_composer_service

        initial_state: State = {
            "messages": [HumanMessage(content=query)],
            "plan": "",
            "retry_count": 0,
        }

        async for chunk in service.astream_events(initial_state):
            yield chunk
