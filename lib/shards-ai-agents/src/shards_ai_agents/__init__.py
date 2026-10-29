import importlib
import sys
from typing import TYPE_CHECKING, Annotated, Any
import warnings

from pydantic import Field, PydanticUserError

# Pin the machine's proxy and CA for AMP requests first: importing shards_ai_agents.llm and
# shards_ai_agents.project loads the project's .env, which must not choose where the saved
# login travels. A crew run in its own process (`uv run run_crew`) never imports
# the CLI, so this import is the pin there.
import shards_ai_agents_core.plus_api  # noqa: F401

from shards_ai_agents.agent.core import Agent
from shards_ai_agents.agent.planning_config import PlanningConfig
from shards_ai_agents.context import ExecutionContext
from shards_ai_agents.crew import Crew
from shards_ai_agents.crews.crew_output import CrewOutput
from shards_ai_agents.flow.flow import Flow
from shards_ai_agents.knowledge.knowledge import Knowledge
from shards_ai_agents.llm import LLM
from shards_ai_agents.llms.base_llm import BaseLLM
from shards_ai_agents.process import Process
from shards_ai_agents.state.checkpoint_config import CheckpointConfig  # noqa: F401
from shards_ai_agents.task import Task
from shards_ai_agents.tasks.llm_guardrail import LLMGuardrail
from shards_ai_agents.tasks.task_output import TaskOutput


if TYPE_CHECKING:
    from shards_ai_agents.memory.unified_memory import Memory


def _suppress_pydantic_deprecation_warnings() -> None:
    """Suppress Pydantic deprecation warnings using targeted monkey patch."""
    original_warn = warnings.warn

    def filtered_warn(
        message: Any,
        category: type | None = None,
        stacklevel: int = 1,
        source: Any = None,
    ) -> Any:
        if (
            category
            and hasattr(category, "__module__")
            and category.__module__ == "pydantic.warnings"
        ):
            return None
        return original_warn(message, category, stacklevel + 1, source)

    warnings.warn = filtered_warn  # type: ignore[assignment]


_suppress_pydantic_deprecation_warnings()

__version__ = "1.15.33"

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "CrewBase": ("shards_ai_agents.project", "CrewBase"),
    "Memory": ("shards_ai_agents.memory.unified_memory", "Memory"),
}


def __getattr__(name: str) -> Any:
    """Lazily import heavy modules (e.g. Memory → lancedb) on first access."""
    if name in _LAZY_IMPORTS:
        module_path, attr = _LAZY_IMPORTS[name]
        mod = importlib.import_module(module_path)
        val = getattr(mod, attr)
        globals()[name] = val
        return val
    raise AttributeError(f"module 'shards_ai_agents' has no attribute {name!r}")


try:
    from shards_ai_agents.agents.agent_builder.base_agent import BaseAgent as _BaseAgent
    from shards_ai_agents.agents.agent_builder.base_agent_executor import (
        BaseAgentExecutor as _BaseAgentExecutor,
    )
    from shards_ai_agents.agents.agent_executor import AgentExecutor as _AgentExecutor
    from shards_ai_agents.agents.tools_handler import ToolsHandler as _ToolsHandler
    from shards_ai_agents.hooks.llm_hooks import (
        LLMCallHookContext as _LLMCallHookContext,
    )
    from shards_ai_agents.tools.tool_types import ToolResult as _ToolResult
    from shards_ai_agents.utilities.prompts import (
        StandardPromptResult as _StandardPromptResult,
        SystemPromptResult as _SystemPromptResult,
    )

    _base_namespace: dict[str, type] = {
        "Agent": Agent,
        "BaseAgent": _BaseAgent,
        "Crew": Crew,
        "Flow": Flow,
        "BaseLLM": BaseLLM,
        "Task": Task,
        "BaseAgentExecutor": _BaseAgentExecutor,
        "ExecutionContext": ExecutionContext,
        "StandardPromptResult": _StandardPromptResult,
        "SystemPromptResult": _SystemPromptResult,
    }

    from shards_ai_agents.tools.base_tool import BaseTool as _BaseTool
    from shards_ai_agents.tools.structured_tool import (
        CrewStructuredTool as _CrewStructuredTool,
    )

    _base_namespace["BaseTool"] = _BaseTool
    _base_namespace["CrewStructuredTool"] = _CrewStructuredTool

    try:
        from shards_ai_agents.a2a.config import (
            A2AClientConfig as _A2AClientConfig,
            A2AConfig as _A2AConfig,
            A2AServerConfig as _A2AServerConfig,
        )

        _base_namespace.update(
            {
                "A2AConfig": _A2AConfig,
                "A2AClientConfig": _A2AClientConfig,
                "A2AServerConfig": _A2AServerConfig,
            }
        )
    except ImportError:
        pass

    _full_namespace = {
        **_base_namespace,
        "ToolsHandler": _ToolsHandler,
        "StandardPromptResult": _StandardPromptResult,
        "SystemPromptResult": _SystemPromptResult,
        "LLMCallHookContext": _LLMCallHookContext,
        "ToolResult": _ToolResult,
    }

    # Dunders are left out: copying base_agent's `__name__`/`__spec__`/`__file__`
    # onto the modules below made their import errors name base_agent.
    _resolve_namespace = {
        **_full_namespace,
        **{
            name: value
            for name, value in sys.modules[_BaseAgent.__module__].__dict__.items()
            if not (name.startswith("__") and name.endswith("__"))
        },
    }

    import shards_ai_agents.state.runtime as _runtime_state_mod

    for _mod_name in (
        _BaseAgent.__module__,
        Agent.__module__,
        Crew.__module__,
        Flow.__module__,
        Task.__module__,
        _runtime_state_mod.__name__,
        _AgentExecutor.__module__,
    ):
        sys.modules[_mod_name].__dict__.update(_resolve_namespace)

    from shards_ai_agents.tasks.conditional_task import (
        ConditionalTask as _ConditionalTask,
    )

    _BaseAgentExecutor.model_rebuild(force=True, _types_namespace=_full_namespace)
    _BaseAgent.model_rebuild(force=True, _types_namespace=_full_namespace)
    Task.model_rebuild(force=True, _types_namespace=_full_namespace)
    _ConditionalTask.model_rebuild(force=True, _types_namespace=_full_namespace)
    Crew.model_rebuild(force=True, _types_namespace=_full_namespace)
    Flow.model_rebuild(force=True, _types_namespace=_full_namespace)
    _AgentExecutor.model_rebuild(force=True, _types_namespace=_full_namespace)

    from shards_ai_agents.state.runtime import RuntimeState

    Entity = Annotated[
        Flow | Crew | Agent,  # type: ignore[type-arg]
        Field(discriminator="entity_type"),
    ]

    RuntimeState.model_rebuild(
        force=True,
        _types_namespace={**_full_namespace, "Entity": Entity},
    )

    try:
        Agent.model_rebuild(force=True, _types_namespace=_full_namespace)
    except PydanticUserError:
        pass

except (ImportError, PydanticUserError):
    import logging as _logging

    _logging.getLogger(__name__).warning(
        "model_rebuild() failed; forward refs may be unresolved.",
        exc_info=True,
    )
    RuntimeState = None  # type: ignore[assignment,misc]

__all__ = [
    "LLM",
    "Agent",
    "BaseLLM",
    "Crew",
    "CrewBase",
    "CrewOutput",
    "Entity",
    "ExecutionContext",
    "Flow",
    "Knowledge",
    "LLMGuardrail",
    "Memory",
    "PlanningConfig",
    "Process",
    "RuntimeState",
    "Task",
    "TaskOutput",
    "__version__",
]
