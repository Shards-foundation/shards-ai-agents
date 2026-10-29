from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict, PrivateAttr

from shards_ai_agents.agents.agent_builder.base_agent import BaseAgent


if TYPE_CHECKING:
    from shards_ai_agents.tools.base_tool import BaseTool


class BaseAgentAdapter(BaseAgent, ABC):
    """Base class for all agent adapters in Shards-ai-agents.

    This abstract class defines the common interface and functionality that all
    agent adapters must implement. It extends BaseAgent to maintain compatibility
    with the Shards-ai-agents framework while adding adapter-specific requirements.
    """

    adapted_structured_output: bool = False
    _agent_config: dict[str, Any] | None = PrivateAttr(default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, agent_config: dict[str, Any] | None = None, **kwargs: Any):
        super().__init__(adapted_agent=True, **kwargs)
        self._agent_config = agent_config

    @abstractmethod
    def configure_tools(self, tools: list[BaseTool] | None = None) -> None:
        """Configure and adapt tools for the specific agent implementation.

        Args:
            tools: Optional list of BaseTool instances to be configured
        """

    @abstractmethod
    def configure_structured_output(self, task: Any) -> None:
        """Configure the structured output for the specific agent implementation.

        Args:
            task: The task object containing output format specifications.
        """
