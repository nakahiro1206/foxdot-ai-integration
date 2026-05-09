import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from typing_extensions import TypedDict

from ..prompt import SYSTEM_PROMPT
from ..state import State


ASSEMBLER_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + """

You are the Assembler Agent. You receive four independent FoxDot code fragments
(drums, harmony, bass, texture) plus the concept and structure documents.
Your job: merge them into one complete, coherent FoxDot script.

Assembly rules:

1. GLOBAL SETUP (always first):
   - Clock.clear()
   - Clock.bpm = <from concept>
   - Scale.default = "<from concept>"
   - Root.default = "<from concept>"
   - Any shared var definitions (var.chords, var.bassline) must appear BEFORE all players.

2. LAYER ORDER: harmony vars → harmony players → bass → drums → texture.
   This order ensures var.chords is defined before bass and texture reference it.

3. INTER-LAYER BINDING — inject where missing:
   - If texture players do not reference p1.pitch, add:
       s1 >> <synth>(p1.pitch.accompany([0,3,5]), ...)
     or keep as-is if s1 uses loop()/play().
   - If bass does not use .follow() or var.chords, add var.chords reference.

4. TEMPORAL STRUCTURE — inject Clock.future() transitions matching the structure:
   - For each section boundary, calculate cumulative bar offset in beats (bars * 4).
   - Use temporal recursion to switch patterns at the right beat:
       def section_drop(n=0):
           p1 >> pads(...)   # drop pattern
           d1 >> play(...)   # drop drums
           Clock.future(<bars*4>, section_outro, args=(0,))
       Clock.future(<intro_bars*4 + build_bars*4>, section_drop, args=(0,))

5. EVERY() CALLS — ensure each melodic player has at least one every() call.
   If a layer is missing them, add sensible defaults (rotate every 8, shuffle every 16).

6. GROUP AMPLIFY for sidechain feel where structure specifies it:
   g_melody = Group(p1, p2, p3)
   g_melody.amplify = var([1, 0.4], [<drop_bars*4>, <rest>])

7. OUTPUT: Only valid FoxDot Python. No markdown. No imports (saver adds them).
   No Go() (saver adds it). Comments are welcome to label sections.

Think step by step. Resolve any conflicts (duplicate var names, overlapping player names).
The output must be the complete merged script body.
"""
)


class AssemblerNodeOutput(TypedDict):
    assembled_code: str
    messages: list[AIMessage]
    revision_count: int


class AssemblerNode:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def fn(self, state: State) -> AssemblerNodeOutput:
        user_content = (
            "Concept:\n"
            + state.get("concept", "")
            + "\n\nStructure:\n"
            + state.get("structure", "")
            + "\n\n--- DRUMS LAYER ---\n"
            + state.get("layer_drums", "# (empty)")
            + "\n\n--- HARMONY LAYER ---\n"
            + state.get("layer_harmony", "# (empty)")
            + "\n\n--- BASS LAYER ---\n"
            + state.get("layer_bass", "# (empty)")
            + "\n\n--- TEXTURE LAYER ---\n"
            + state.get("layer_texture", "# (empty)")
        )

        # If critic provided feedback, include it
        feedback = state.get("critic_feedback", "")
        if feedback:
            user_content += "\n\n--- CRITIC FEEDBACK (fix these) ---\n" + feedback

        messages = [
            {"role": "system", "content": ASSEMBLER_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]
        response = self.llm.invoke(messages)
        code = response.content

        # Strip markdown fences here — once — so all downstream nodes see clean code.
        code = re.sub(r"```(?:python)?\s*", "", code).strip()

        # --- Explainability header ---
        # Prepend a comment block that documents what the piece is and why.
        # This makes every saved file self-explanatory when opened later.
        original_request = state["messages"][0].content
        enhanced = state.get("enhanced_prompt", "")
        concept  = state.get("concept", "")
        header_lines = ["# " + "-" * 72]
        header_lines.append(f"# Request:  {original_request.strip()}")
        if enhanced:
            # Wrap enhanced prompt at ~70 chars per comment line
            words, line = enhanced.split(), ""
            header_lines.append("# Brief:")
            for word in words:
                if len(line) + len(word) + 1 > 70:
                    header_lines.append(f"#   {line.strip()}")
                    line = word + " "
                else:
                    line += word + " "
            if line.strip():
                header_lines.append(f"#   {line.strip()}")
        if concept:
            header_lines.append("# Concept:")
            for cline in concept.strip().splitlines():
                header_lines.append(f"#   {cline}")
        header_lines.append("# " + "-" * 72)
        header = "\n".join(header_lines)

        code = header + "\n\n" + code

        return {
            "assembled_code": code,
            # Put in messages so the validator can read state["messages"][-1].content
            "messages": [AIMessage(content=code)],
            "revision_count": state.get("revision_count", 0) + 1,
        }
