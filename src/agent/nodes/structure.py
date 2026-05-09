from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from ..prompt import SYSTEM_PROMPT
from ..state import State


STRUCTURE_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + """

You are the Structure Agent. Given the musical concept, produce a section map for the composition.

Output a plain-text list. Each section on its own block with these fields:

Section: <name, e.g. Intro, Build, Drop, Breakdown, Outro>
Bars: <number of bars this section lasts, multiples of 4>
Energy: <low | medium | high>
Techniques: <comma-separated FoxDot mechanisms that govern this section's evolution>
  Valid techniques include: var chord change, linvar filter sweep, expvar filter sweep,
  sinvar amplitude, Pvar pattern switch, every() rotate/shuffle/reverse/stutter,
  temporal recursion, per-player bpm shift, PBern gating, delay swing,
  accompany voice-leading, Group amplify sidechain

Example output:

Section: Intro
Bars: 8
Energy: low
Techniques: linvar filter sweep, every() rotate, sinvar amplitude

Section: Build
Bars: 16
Energy: medium
Techniques: var chord change, expvar filter sweep, PBern gating, every() shuffle

Section: Drop
Bars: 16
Energy: high
Techniques: Pvar pattern switch, every() stutter, Group amplify sidechain, accompany voice-leading

Section: Outro
Bars: 8
Energy: low
Techniques: linvar filter sweep, every() reverse, temporal recursion fade

Also assign the four player group names that all layer agents must use:
Drums players: d1, d2, d3
Harmony players: p1, p2, p3
Bass players: b1
Texture players: s1, s2

Do not write FoxDot code. Output only the section list and player assignments.
"""
)


class StructureNodeOutput(TypedDict):
    structure: str


class StructureNode:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fn(self, state: State) -> StructureNodeOutput:
        prompt = state.get("enhanced_prompt") or state["messages"][0].content
        messages = [
            {"role": "system", "content": STRUCTURE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Creative brief:\n"
                    + prompt
                    + "\n\nConcept:\n"
                    + state.get("concept", "")
                ),
            },
        ]
        response = self.llm.invoke(messages)
        return {"structure": response.content}
