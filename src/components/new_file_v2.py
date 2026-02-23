import asyncio

import streamlit as st
from langchain_core.messages import HumanMessage

from src.agent import MucisComposerService, State
from src.fs import FileSystem


class NewFile:
    def __init__(self):
        if "music_composer_service" not in st.session_state:
            fs = FileSystem()
            st.session_state.music_composer_service = MucisComposerService(fs)

    def render(self):
        st.markdown("## New File")

        query = st.text_input("Describe your music idea")
        generate = st.button("Generate")

        if "generated_code" in st.session_state:
            st.code(st.session_state.generated_code, language="python")

        if "generation_status" in st.session_state:
            st.markdown(st.session_state.generation_status)

        if generate:
            if not query.strip():
                st.session_state.generation_status = "⚠️ Please describe your music idea."
                st.rerun()
                return

            self._generate(query)
            st.rerun()

    def _generate(self, query: str):
        service: MucisComposerService = st.session_state.music_composer_service

        initial_state: State = {
            "messages": [HumanMessage(content=query)],
            "plan": "",
            "retry_count": 0,
        }

        async def _run():
            accumulated = ""
            async for chunk in service.astream_events(initial_state):
                accumulated += chunk
            return accumulated

        st.session_state.generation_status = "⏳ Generating..."
        result = asyncio.run(_run())
        st.session_state.generated_code = result
        st.session_state.generation_status = "✅ Generation complete."
