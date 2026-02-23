from typing import Any
from uuid import UUID

from langchain_core.agents import AgentFinish
from langchain_core.outputs import LLMResult
from langchain_core.messages import (
    BaseMessage,
)
from langchain_core.callbacks import AsyncCallbackHandler


from logging import getLogger

logger = getLogger(__name__)


class Handler(AsyncCallbackHandler):
    async def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        logger.info(f"Chat model started with messages: {messages}")

    async def on_llm_new_token(
        self,
        token: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        print(token, end="", flush=True)

    async def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        print()  # newline after streamed tokens
        for generation in response.generations:
            for g in generation:
                logger.info(f"LLM response: {g.text}")

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        logger.info(f"Agent finished with output: {finish.return_values}")
