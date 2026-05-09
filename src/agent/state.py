from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage


class State(TypedDict):
    # Conversation history (carries user request + validation error messages)
    messages: Annotated[list[BaseMessage], add_messages]
    retry_count: int

    # Stage 0 – EnhancerNode: expanded user prompt
    enhanced_prompt: str  # rich musical description expanded from the raw user input

    # Stage 1 – ConceptNode: global musical identity
    concept: str          # BPM, scale, root, mood, genre, energy arc in plain text

    # Stage 2 – StructureNode: section map
    structure: str        # plain text: [{name, bars, energy, techniques[]}]

    # Stage 3 – parallel LayerNodes (each knows the others' player names)
    layer_drums: str      # raw FoxDot code fragment, no imports
    layer_harmony: str
    layer_bass: str
    layer_texture: str

    # Stage 4 – AssemblerNode: merged, transition-injected script
    assembled_code: str

    # Stage 5 – CriticNode: quality gate
    critic_feedback: str
    critic_pass: bool
    revision_count: int
