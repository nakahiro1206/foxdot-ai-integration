from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from ..prompt import SYSTEM_PROMPT
from ..state import State


CONCEPT_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + """

You are the Concept Agent. Given a user's music description, produce a concise musical identity document.

Output plain text with these exact headings:

BPM: <number>
Scale: <scale name, e.g. minor, major, dorian, minorPentatonic>
Root: <note name, e.g. C, D#, F>
Mood: <1-2 word description>
Genre: <1-2 word description>
Energy arc: <describe how energy evolves: e.g. "builds from sparse intro to dense drop then fades">
Section count: <number of distinct sections, 3-6>
Key techniques: <comma-separated list of FoxDot features suited to this piece, e.g. linvar filter sweeps, PEuclid drums, temporal recursion, Pvar pattern switching, accompany voice-leading>

Be specific and decisive. Do not hedge. Do not write FoxDot code.
"""
)


class ConceptNodeOutput(TypedDict):
    concept: str


class ConceptNode:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fn(self, state: State) -> ConceptNodeOutput:
        # Prefer the expanded prompt if the enhancer has already run
        prompt = state.get("enhanced_prompt") or state["messages"][0].content
        messages = [
            {"role": "system", "content": CONCEPT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        response = self.llm.invoke(messages)
        return {"concept": response.content}
