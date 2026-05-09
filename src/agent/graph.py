from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessageChunk, AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import AsyncIterator

from src.fs import FileSystem
from src.env import env
from .state import State
from .nodes import (
    EnhancerNode,
    ConceptNode,
    StructureNode,
    LayerNode,
    AssemblerNode,
    CriticNode,
    ScriptValidatorNode,
    SaverNode,
    ErrorNode,
)

MAX_RETRIES = 3  # validator retries (syntax/pyright)
MAX_REVISIONS = 1  # critic→assembler revision passes


# ---------------------------------------------------------------------------
# Edge conditions
# ---------------------------------------------------------------------------


def should_revise(state: State) -> str:
    """After critic: revise once if failed, else validate."""
    if (
        not state.get("critic_pass", False)
        and state.get("revision_count", 0) < MAX_REVISIONS
    ):
        return "revise"
    return "validate"


def should_retry(state: State) -> str:
    """After validator: save on success, retry or error on failure."""
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and not isinstance(last, HumanMessage):
        # Validator returned success (no HumanMessage error appended)
        # Check: last message should be the assembled code AIMessage with no follow-up error
        msgs = state["messages"]
        if len(msgs) >= 1 and isinstance(msgs[-1], AIMessage):
            # If the validator found no errors it returns only retry_count update,
            # leaving the last message as the AIMessage code — go to save.
            return "save"
    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "error"
    return "assemble"  # retry: send back to assembler with error in messages


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class MusicComposerService:
    def __init__(self, fs: FileSystem):
        self.fs = fs
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=env.OPENAI_API_KEY,
            streaming=True,
        )

        # Instantiate all nodes
        self.enhancer_node = EnhancerNode(self.llm)
        self.concept_node = ConceptNode(self.llm)
        self.structure_node = StructureNode(self.llm)
        self.drums_node = LayerNode(self.llm, "drums")
        self.harmony_node = LayerNode(self.llm, "harmony")
        self.bass_node = LayerNode(self.llm, "bass")
        self.texture_node = LayerNode(self.llm, "texture")
        self.assembler_node = AssemblerNode(self.llm)
        self.critic_node = CriticNode(self.llm)
        self.validator_node = ScriptValidatorNode()
        self.saver_node = SaverNode(fs)
        self.error_node = ErrorNode()

        self.graph = self._compile_graph()

    def _compile_graph(self):
        g = StateGraph(State)

        # --- Stage 0: Enhancer ---
        g.add_node("enhance", self.enhancer_node.fn)

        # --- Stage 1: Concept ---
        g.add_node("concept", self.concept_node.fn)

        # --- Stage 2: Structure ---
        g.add_node("structure", self.structure_node.fn)

        # --- Stage 3: Parallel layer agents ---
        g.add_node("drums", self.drums_node.fn)
        g.add_node("harmony", self.harmony_node.fn)
        g.add_node("bass", self.bass_node.fn)
        g.add_node("texture", self.texture_node.fn)

        # --- Stage 4: Assembler (fan-in + revision target) ---
        g.add_node("assemble", self.assembler_node.fn)

        # --- Stage 5: Critic ---
        g.add_node("critic", self.critic_node.fn)

        # --- Stage 6: Validator ---
        g.add_node("validate", self.validator_node.fn)

        # --- Terminal nodes ---
        g.add_node("save", self.saver_node.fn)
        g.add_node("error", self.error_node.fn)

        # --- Edges ---
        # Linear: start → enhance → concept → structure
        g.add_edge(START, "enhance")
        g.add_edge("enhance", "concept")
        g.add_edge("concept", "structure")

        # Fan-out: structure → all four layers in parallel
        g.add_edge("structure", "drums")
        g.add_edge("structure", "harmony")
        g.add_edge("structure", "bass")
        g.add_edge("structure", "texture")

        # Fan-in: all layers → assembler
        g.add_edge("drums", "assemble")
        g.add_edge("harmony", "assemble")
        g.add_edge("bass", "assemble")
        g.add_edge("texture", "assemble")

        # Assembler → critic
        g.add_edge("assemble", "critic")

        # Critic → conditional: revise (back to assembler) or validate
        g.add_conditional_edges(
            "critic",
            should_revise,
            {
                "revise": "assemble",
                "validate": "validate",
            },
        )

        # Validator → conditional: save, retry (assembler), or error
        g.add_conditional_edges(
            "validate",
            should_retry,
            {
                "save": "save",
                "assemble": "assemble",
                "error": "error",
            },
        )

        g.add_edge("save", END)
        g.add_edge("error", END)

        return g.compile()

    async def astream_events(self, state: State) -> AsyncIterator[str]:
        async for event in self.graph.astream_events(state, version="v2"):
            kind = event["event"]
            data = event["data"]
            name = event["name"]

            if kind == "on_chat_model_stream":
                chunk = data.get("chunk", None)
                if isinstance(chunk, BaseMessageChunk) and chunk.content:
                    yield chunk.content
            elif kind == "on_chain_end":
                if name == "error":
                    output = data.get("output", {})
                    msgs = output.get("messages", [])
                    if msgs:
                        yield msgs[-1].content
                if name == "validate":
                    output = data.get("output", {})
                    msgs = output.get("messages", [])
                    if msgs:
                        last_msg = msgs[-1]
                        if isinstance(last_msg, AIMessage):
                            yield "Validation successful. Code is ready to save."
                        else:
                            yield "Validation failed. Returning to assembler for revision."
