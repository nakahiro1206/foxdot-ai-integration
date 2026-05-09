from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from ..prompt import SYSTEM_PROMPT
from ..state import State


CRITIC_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + """

You are the Critic Agent. Evaluate the assembled FoxDot script for musical quality.

Score each criterion as PASS or FAIL with a one-line reason:

1. TEMPORAL EVOLUTION: Does the script have meaningful change over time?
   PASS if: at least 2 of {every(), var with >1 value, linvar/sinvar/expvar, Pvar, temporal recursion Clock.future}
   FAIL if: all players are static with no evolution.

2. HARMONIC COHERENCE: Do players share a common harmonic foundation?
   PASS if: var.chords is defined and used by at least 2 players (harmony + bass minimum).
   FAIL if: each player uses unrelated, independent pitch sequences.

3. RHYTHMIC INTEREST: Is there rhythmic variation beyond a single repeating loop?
   PASS if: at least one of {PEuclid/PDur, PBern gating, delay swing, every() stutter/rotate, angle-bracket layering}.
   FAIL if: all players use simple fixed dur=1 with no rhythmic variation.

4. MIX BALANCE: Are amplitude levels reasonable across all layers?
   PASS if: no single player dominates (no amp > 0.9 unless intentional), and texture players have amp < 0.4.
   FAIL if: all players at amp=1 or amp values are clearly unbalanced.

5. INTER-LAYER BINDING: Do layers reference each other?
   PASS if: at least one use of .accompany(), .follow(), or p1.pitch / b1.pitch reference.
   FAIL if: all layers are completely independent with no cross-referencing.

6. STRUCTURAL ARC: Does energy visibly change across the piece?
   PASS if: amplitude, filter, or pattern changes correspond to different sections (different var durations or Clock.future transitions).
   FAIL if: the piece sounds identical from start to finish.

After scoring, output:

OVERALL: PASS  (if 5 or 6 criteria pass)
OVERALL: FAIL  (if 4 or fewer criteria pass)

FEEDBACK:
<If FAIL: list specific, actionable FoxDot fixes. Be concrete — name the player, the attribute, and the fix.>
<If PASS: write "No changes needed.">

Do not rewrite the code. Only evaluate and give feedback.
"""
)


class CriticNodeOutput(TypedDict):
    critic_feedback: str
    critic_pass: bool


class CriticNode:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fn(self, state: State) -> CriticNodeOutput:
        code = state.get("assembled_code", "")
        messages = [
            {"role": "system", "content": CRITIC_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Concept:\n"
                    + state.get("concept", "")
                    + "\n\nStructure:\n"
                    + state.get("structure", "")
                    + "\n\nAssembled script:\n"
                    + code
                ),
            },
        ]
        response = self.llm.invoke(messages)
        text: str = response.content

        passed = "OVERALL: PASS" in text
        return {
            "critic_feedback": text,
            "critic_pass": passed,
        }
