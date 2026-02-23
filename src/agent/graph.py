from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from src.fs import FileSystem
from langchain_core.messages import (
    BaseMessageChunk,
    ToolMessage,
    AIMessage,
    HumanMessage,
)
from .nodes import (
    CoderNode,
    ErrorNode,
    ScriptValidatorNode,
    PlannerNode,
    SaverNode,
)
from .handler import Handler

from src.env import env
from .state import State
from typing_extensions import AsyncIterator

MAX_RETRIES = 3


def should_retry(state: State) -> str:
    last = state["messages"][-1]
    if isinstance(last, AIMessage):
        return "save"
    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "error"
    return "code"


class MucisComposerService:
    def __init__(self, fs: FileSystem):
        self.fs = fs
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=env.OPENAI_API_KEY,
            streaming=True,
        )
        self.coder_node = CoderNode(self.llm)
        self.script_validator_node = ScriptValidatorNode()
        self.planner_node = PlannerNode(self.llm)
        self.save_node = SaverNode(self.fs)
        self.error_node = ErrorNode()
        self.callback_handler = Handler()

        self.graph = self.compile_graph()

    def compile_graph(self):
        graph_builder = StateGraph(State)
        graph_builder.add_node("plan", self.planner_node.fn)
        graph_builder.add_node("code", self.coder_node.fn)
        graph_builder.add_node("validate", self.script_validator_node.fn)
        graph_builder.add_node("save", self.save_node.fn)
        graph_builder.add_node("error", self.error_node.fn)
        graph_builder.add_edge(START, "plan")
        graph_builder.add_edge("plan", "code")
        graph_builder.add_edge("code", "validate")
        graph_builder.add_conditional_edges("validate", should_retry)
        graph_builder.add_edge("save", END)
        graph_builder.add_edge("error", END)

        graph = graph_builder.compile()
        return graph

    async def astream_events(self, state: State) -> AsyncIterator[str]:
        async for event in self.graph.astream_events(state, version="v2"):
            kind = event["event"]
            data = event["data"]
            name = event["name"]

            if kind == "on_chat_model_stream":
                chunk = data.get("chunk", None)
                assert isinstance(chunk, BaseMessageChunk)
                yield chunk.content
            elif kind == "on_tool_end":
                output = data.get("output", {})
                assert isinstance(output, ToolMessage)
                yield output.content
            elif kind == "on_chain_end":
                output = data.get("output", {})
                if name == "error":
                    yield output.get("messages", [AIMessage(content="")])[-1].content


if __name__ == "__main__":
    service = MucisComposerService(FileSystem())
    initial_state: State = {
        "messages": [
            HumanMessage(
                content="Compose a futuristic music piece with metallic kinky sounds."
            )
        ],
        "plan": "",
        "retry_count": 0,
    }

    async def test():
        await service.graph.ainvoke(
            initial_state, {"callbacks": [service.callback_handler]}
        )

    import asyncio

    asyncio.run(test())
