# ruff: noqa: E501
# pylint: disable=logging-fstring-interpolation
import logging
import os

from collections.abc import AsyncIterable
from typing import Any, Literal

import httpx

from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.runnables.config import RunnableConfig
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel


logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str


# The structured output is persisted in LangGraph checkpoints. Explicitly allow
# this local Pydantic model so restoring a checkpoint remains forward-compatible.
memory = MemorySaver(
    serde=JsonPlusSerializer(
        allowed_msgpack_modules=[('ticket_agent', 'ResponseFormat')]
    )
)


class TicketAgent:
    """Ticket Agent for querying 12306 train tickets."""

    SYSTEM_INSTRUCTION = (
        "You are a specialized assistant for querying 12306 train tickets. "
        "Use the provided tools to query train availability for the requested "
        "date and route. Rely exclusively on tool output and never invent "
        "trains, prices, or availability. Format the final answer in Markdown "
        "with train number, departure/arrival station and time, seat class, "
        "remaining tickets, and price. Only query and report tickets; do not "
        "book, pay for, or place any order."
    )

    RESPONSE_FORMAT_INSTRUCTION: str = (
        'Select status as "completed" if the request is fully addressed and no further input is needed. '
        'Select status as "input_required" if you need more information from the user or are asking a clarifying question. '
        'Select status as "error" if an error occurred or the request cannot be fulfilled.'
    )

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

    def __init__(self, mcp_tools: list[Any]):
        """Initializes the ticket agent with preloaded MCP tools."""
        logger.info('Initializing TicketAgent with preloaded MCP tools...')
        try:
            model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
            self.model = ChatDeepSeek(model=model)
            logger.info('ChatDeepSeek model initialized successfully.')
        except Exception as e:
            logger.error(
                f'Failed to initialize ChatDeepSeek model: {e}',
                exc_info=True,
            )
            raise

        self.mcp_tools = mcp_tools
        if not self.mcp_tools:
            raise ValueError('No MCP tools provided to TicketAgent')

    def _create_agent(self):
        return create_react_agent(
            self.model,
            tools=self.mcp_tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=(
                self.RESPONSE_FORMAT_INSTRUCTION,
                ResponseFormat,
            ),
        )

    def _get_agent_response_from_state(
        self, config: RunnableConfig, agent_runnable
    ) -> dict[str, Any]:
        """Retrieves the structured response from the LangGraph state."""
        try:
            current_state_snapshot = agent_runnable.get_state(config)
            state_values = getattr(current_state_snapshot, 'values', None)
        except Exception as e:
            logger.error(
                f'Error getting state from agent_runnable: {e}', exc_info=True
            )
            return {
                'is_task_complete': True,
                'require_user_input': False,
                'content': 'Error: Could not retrieve agent state.',
            }

        if not state_values:
            return {
                'is_task_complete': True,
                'require_user_input': False,
                'content': 'Error: Agent state is unavailable.',
            }

        structured_response = (
            state_values.get('structured_response')
            if isinstance(state_values, dict)
            else getattr(state_values, 'structured_response', None)
        )

        if structured_response and isinstance(
            structured_response, ResponseFormat
        ):
            if structured_response.status == 'completed':
                return {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': structured_response.message,
                }
            return {
                'is_task_complete': False,
                'require_user_input': structured_response.status
                == 'input_required',
                'content': structured_response.message,
            }

        final_messages = (
            state_values.get('messages', [])
            if isinstance(state_values, dict)
            else getattr(state_values, 'messages', [])
        )

        if final_messages and isinstance(final_messages[-1], AIMessage):
            ai_content = final_messages[-1].content
            if isinstance(ai_content, str) and ai_content:
                return {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': ai_content,
                }
            if isinstance(ai_content, list):
                text_parts = [
                    part['text']
                    for part in ai_content
                    if isinstance(part, dict) and part.get('type') == 'text'
                ]
                if text_parts:
                    return {
                        'is_task_complete': True,
                        'require_user_input': False,
                        'content': '\n'.join(text_parts),
                    }

        return {
            'is_task_complete': False,
            'require_user_input': True,
            'content': (
                'We are unable to process your request at the moment due to '
                'an unexpected response format. Please try again.'
            ),
        }

    async def stream(self, query: str, session_id: str) -> AsyncIterable[Any]:
        """Streams progress and the final response for a ticket query."""
        agent_runnable = self._create_agent()
        config: RunnableConfig = {'configurable': {'thread_id': session_id}}
        langgraph_input = {'messages': [('user', query)]}

        try:
            async for chunk in agent_runnable.astream_events(
                langgraph_input, config, version='v1'
            ):
                event_name = chunk.get('event')
                data = chunk.get('data', {})
                content_to_yield = None

                if event_name == 'on_tool_start':
                    tool_name = data.get('name', 'a tool')
                    content_to_yield = f'Using tool: {tool_name}...'
                elif event_name == 'on_chat_model_stream':
                    message_chunk = data.get('chunk')
                    if (
                        isinstance(message_chunk, AIMessageChunk)
                        and message_chunk.content
                    ):
                        content_to_yield = message_chunk.content

                if content_to_yield:
                    yield {
                        'is_task_complete': False,
                        'require_user_input': False,
                        'content': content_to_yield,
                    }

            final_response = self._get_agent_response_from_state(
                config, agent_runnable
            )
            yield final_response

        except httpx.HTTPStatusError as http_err:
            logger.error(
                f'HTTPStatusError in TicketAgent.stream: {http_err.response.status_code}',
                exc_info=True,
            )
            yield {
                'is_task_complete': True,
                'require_user_input': False,
                'content': (
                    f'An error occurred with an external service for ticket '
                    f'query: {http_err.response.status_code}'
                ),
            }
        except Exception as e:
            logger.error(
                f'Error during TicketAgent.stream: {e}', exc_info=True
            )
            yield {
                'is_task_complete': True,
                'require_user_input': False,
                'content': (
                    'An error occurred during streaming: '
                    f'{getattr(e, "message", str(e))}'
                ),
            }
