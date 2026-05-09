from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from ..state import State


ENHANCER_SYSTEM_PROMPT = """\
You are a music prompt engineer specialising in electronic and experimental music.

Given a short user description of a desired piece of music, expand it into a rich,
detailed creative brief that downstream composition agents can use to make informed,
specific decisions.

Your output must cover all of these dimensions — be concrete, not vague:

- Emotional tone: what feeling should the listener experience, and how does it shift?
- Rhythmic character: straight or swing? dense or sparse? mechanical or organic?
- Harmonic language: consonant/dissonant? which scale family? chord density?
- Textural layers: what roles should each layer play (foreground, mid, background)?
- Dynamic arc: how does energy build and release across the piece?
- Sonic references: name 2-3 specific artists, tracks, or production styles as anchors.
- Distinctive details: at least one unusual or unexpected element that makes this piece
  memorable (e.g. "a vocal chop that stutters on every 5th beat", "a bitcrushed hi-hat
  that only appears in the drop", "a bass that slides a major 7th on the last beat of
  each bar").

Write in plain prose, 150-250 words. Do not write FoxDot code. Do not use bullet points
or headers — flowing paragraphs only.
"""


class EnhancerNodeOutput(TypedDict):
    enhanced_prompt: str


class EnhancerNode:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fn(self, state: State) -> EnhancerNodeOutput:
        user_input = state["messages"][0].content
        messages = [
            {"role": "system", "content": ENHANCER_SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]
        response = self.llm.invoke(messages)
        return {"enhanced_prompt": response.content}
