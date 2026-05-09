from langchain_openai import ChatOpenAI
from typing import Literal
from typing_extensions import TypedDict

from ..prompt import SYSTEM_PROMPT
from ..state import State


LayerRole = Literal["drums", "harmony", "bass", "texture"]


LAYER_ROLE_PROMPTS: dict[LayerRole, str] = {
    "drums": """
You are the Drums Layer Agent. Write only the drum and percussion players (d1, d2, d3).

Rules:
- Use play() with string patterns for all drum voices.
- d1 = kick, d2 = snare/hi-hat, d3 = percussion/cymbals/effects.
- Use PEuclid, PDur, PBern, angle-bracket layering <...>, square-bracket rolls [--].
- Apply every() with rotate, shuffle, stutter for rhythmic evolution across sections.
- Use var([amp1,amp2], bars) to modulate amplitude across sections matching the structure.
- Add delay=[...] for swing where the energy is medium or high.
- Do NOT define Clock.bpm, Scale, Root — the assembler handles global setup.
- Output only raw FoxDot player lines and their every() calls. No imports, no Go().
""",

    "harmony": """
You are the Harmony Layer Agent. Write only the harmonic/melodic players (p1, p2, p3).

Rules:
- p1 = main pad or chord player using var.chords + PGroup offsets.
- p2 = melodic pluck or lead using PWalk, PChain, or arp() for interest.
- p3 = high bell or accent layer (optional; use amp=0 if not needed).
- Always define: var.chords = var([...], bars) matching the structure's bar lengths.
- Use .accompany() on p1.pitch for p2 or p3 where suitable.
- Use Pvar for whole-pattern switching between sections.
- Use linvar/sinvar on lpf, amp, room for evolution within sections.
- Use P*(x,y,z) or P^(x,y,z,step) for arpeggiated chords where energy is high.
- Apply every() rotate, shuffle, mirror on melodic players.
- Do NOT define Clock.bpm — the assembler handles global setup.
- Output only raw FoxDot player lines. No imports, no Go().
""",

    "bass": """
You are the Bass Layer Agent. Write only the bass player (b1).

Rules:
- b1 = bass synth tracking var.chords with rhythmic displacement.
- Use PDur(n, k) for Euclidean rhythm on bass.
- Use var.chords + var.bassline where bassline = var([offsets], bars).
- Apply lpf + lpr for warmth; room should be low (0.1-0.2).
- Use glide=[...] on selected steps for portamento feel.
- Use oct=var([3,4], bars) to shift register across sections.
- The harmony layer will define var.chords — reference it directly (do not redefine it).
- Do NOT define Clock.bpm or var.chords — reference what harmony defines.
- Output only raw FoxDot player lines. No imports, no Go().
""",

    "texture": """
You are the Texture Layer Agent. Write only the texture/atmosphere players (s1, s2).

Rules:
- s1 = atmospheric swell, pad wash, or loop layer. Use swell, pads, or loop().
- s2 = FX accent: use echo, spin, formant, tremolo, pshift creatively.
- s2 may use play() for rhythmic texture samples.
- Use linvar/expvar/sinvar heavily on hpf, lpf, amp, room, pan for movement.
- Use every() reverse, shuffle on s1 for slow evolution.
- Use PwhiteI or PSine for panning and modulation.
- Keep amps low (0.1-0.3) — texture layers fill space, not foreground.
- s2 may reference p1.pitch.accompany() for tonal alignment with harmony.
- Do NOT define Clock.bpm — the assembler handles global setup.
- Output only raw FoxDot player lines. No imports, no Go().
""",
}


LAYER_OUTPUT_KEYS: dict[LayerRole, str] = {
    "drums": "layer_drums",
    "harmony": "layer_harmony",
    "bass": "layer_bass",
    "texture": "layer_texture",
}


class LayerNodeOutput(TypedDict, total=False):
    layer_drums: str
    layer_harmony: str
    layer_bass: str
    layer_texture: str


class LayerNode:
    def __init__(self, llm: ChatOpenAI, role: LayerRole):
        self.llm = llm
        self.role = role
        self.output_key = LAYER_OUTPUT_KEYS[role]
        self.role_prompt = LAYER_ROLE_PROMPTS[role]

    def fn(self, state: State) -> LayerNodeOutput:
        system = SYSTEM_PROMPT + "\n\n" + self.role_prompt
        prompt = state.get("enhanced_prompt") or state["messages"][0].content
        user_content = (
            "Creative brief:\n"
            + prompt
            + "\n\nConcept:\n"
            + state.get("concept", "")
            + "\n\nStructure:\n"
            + state.get("structure", "")
        )
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]
        response = self.llm.invoke(messages)
        return {self.output_key: response.content}  # type: ignore[return-value]
