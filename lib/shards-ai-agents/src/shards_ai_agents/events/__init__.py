"""Shards-ai-agents events system for monitoring and extending agent behavior.

This module provides the event infrastructure that allows users to:
- Monitor agent, task, and crew execution
- Track memory operations and performance
- Build custom logging and analytics
- Extend Shards-ai-agents with custom event handlers
- Declare handler dependencies for ordered execution

Event type classes are lazy-loaded on first access to avoid importing
~12 Pydantic model modules (and their transitive deps) at package init time.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

from shards_ai_agents.events.base_event_listener import BaseEventListener
from shards_ai_agents.events.depends import Depends
from shards_ai_agents.events.event_bus import shards_ai_agents_event_bus
from shards_ai_agents.events.handler_graph import CircularDependencyError


if TYPE_CHECKING:
    from shards_ai_agents.events.types.agent_events import (
        AgentEvaluationCompletedEvent,
        AgentEvaluationFailedEvent,
        AgentEvaluationStartedEvent,
        AgentExecutionCompletedEvent,
        AgentExecutionErrorEvent,
        AgentExecutionStartedEvent,
        LiteAgentExecutionCompletedEvent,
        LiteAgentExecutionErrorEvent,
        LiteAgentExecutionStartedEvent,
    )
    from shards_ai_agents.events.types.checkpoint_events import (
        CheckpointBaseEvent,
        CheckpointCompletedEvent,
        CheckpointFailedEvent,
        CheckpointForkBaseEvent,
        CheckpointForkCompletedEvent,
        CheckpointForkStartedEvent,
        CheckpointPrunedEvent,
        CheckpointRestoreBaseEvent,
        CheckpointRestoreCompletedEvent,
        CheckpointRestoreFailedEvent,
        CheckpointRestoreStartedEvent,
        CheckpointStartedEvent,
    )
    from shards_ai_agents.events.types.crew_events import (
        CrewKickoffCompletedEvent,
        CrewKickoffFailedEvent,
        CrewKickoffStartedEvent,
        CrewTestCompletedEvent,
        CrewTestFailedEvent,
        CrewTestResultEvent,
        CrewTestStartedEvent,
        CrewTrainCompletedEvent,
        CrewTrainFailedEvent,
        CrewTrainStartedEvent,
    )
    from shards_ai_agents.events.types.flow_events import (
        ConversationMessageAddedEvent,
        ConversationRouteSelectedEvent,
        ConversationTurnCompletedEvent,
        ConversationTurnFailedEvent,
        ConversationTurnStartedEvent,
        FlowCreatedEvent,
        FlowEvent,
        FlowFailedEvent,
        FlowFinishedEvent,
        FlowPlotEvent,
        FlowStartedEvent,
        HumanFeedbackReceivedEvent,
        HumanFeedbackRequestedEvent,
        MethodExecutionFailedEvent,
        MethodExecutionFinishedEvent,
        MethodExecutionStartedEvent,
    )
    from shards_ai_agents.events.types.knowledge_events import (
        KnowledgeQueryCompletedEvent,
        KnowledgeQueryFailedEvent,
        KnowledgeQueryStartedEvent,
        KnowledgeRetrievalCompletedEvent,
        KnowledgeRetrievalStartedEvent,
        KnowledgeSearchQueryFailedEvent,
    )
    from shards_ai_agents.events.types.llm_events import (
        ContextWindowSummarizationCompletedEvent,
        ContextWindowSummarizationFailedEvent,
        ContextWindowSummarizationStartedEvent,
        LLMCallCompletedEvent,
        LLMCallFailedEvent,
        LLMCallStartedEvent,
        LLMStreamChunkEvent,
    )
    from shards_ai_agents.events.types.llm_guardrail_events import (
        LLMGuardrailCompletedEvent,
        LLMGuardrailStartedEvent,
    )
    from shards_ai_agents.events.types.logging_events import (
        AgentLogsExecutionEvent,
        AgentLogsStartedEvent,
    )
    from shards_ai_agents.events.types.mcp_events import (
        MCPConfigFetchFailedEvent,
        MCPConnectionCompletedEvent,
        MCPConnectionFailedEvent,
        MCPConnectionStartedEvent,
        MCPToolExecutionCompletedEvent,
        MCPToolExecutionFailedEvent,
        MCPToolExecutionStartedEvent,
    )
    from shards_ai_agents.events.types.memory_events import (
        MemoryQueryCompletedEvent,
        MemoryQueryFailedEvent,
        MemoryQueryStartedEvent,
        MemoryRetrievalCompletedEvent,
        MemoryRetrievalFailedEvent,
        MemoryRetrievalStartedEvent,
        MemorySaveCompletedEvent,
        MemorySaveFailedEvent,
        MemorySaveStartedEvent,
    )
    from shards_ai_agents.events.types.observation_events import (
        PlanStepCompletedEvent,
        PlanStepEvent,
        PlanStepStartedEvent,
    )
    from shards_ai_agents.events.types.reasoning_events import (
        AgentReasoningCompletedEvent,
        AgentReasoningFailedEvent,
        AgentReasoningStartedEvent,
        ReasoningEvent,
    )
    from shards_ai_agents.events.types.skill_events import (
        SkillActivatedEvent,
        SkillDiscoveryCompletedEvent,
        SkillDiscoveryStartedEvent,
        SkillEvent,
        SkillLoadFailedEvent,
        SkillLoadedEvent,
        SkillUsedEvent,
    )
    from shards_ai_agents.events.types.task_events import (
        TaskCompletedEvent,
        TaskEvaluationEvent,
        TaskFailedEvent,
        TaskStartedEvent,
    )
    from shards_ai_agents.events.types.tool_usage_events import (
        ToolExecutionErrorEvent,
        ToolFailureDetectedEvent,
        ToolSelectionErrorEvent,
        ToolUsageErrorEvent,
        ToolUsageEvent,
        ToolUsageFinishedEvent,
        ToolUsageStartedEvent,
        ToolValidateInputErrorEvent,
    )

_LAZY_EVENT_MAPPING: dict[str, str] = {
    "AgentEvaluationCompletedEvent": "shards_ai_agents.events.types.agent_events",
    "AgentEvaluationFailedEvent": "shards_ai_agents.events.types.agent_events",
    "AgentEvaluationStartedEvent": "shards_ai_agents.events.types.agent_events",
    "AgentExecutionCompletedEvent": "shards_ai_agents.events.types.agent_events",
    "AgentExecutionErrorEvent": "shards_ai_agents.events.types.agent_events",
    "AgentExecutionStartedEvent": "shards_ai_agents.events.types.agent_events",
    "LiteAgentExecutionCompletedEvent": "shards_ai_agents.events.types.agent_events",
    "LiteAgentExecutionErrorEvent": "shards_ai_agents.events.types.agent_events",
    "LiteAgentExecutionStartedEvent": "shards_ai_agents.events.types.agent_events",
    "CheckpointBaseEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointCompletedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointFailedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointForkBaseEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointForkCompletedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointForkStartedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointPrunedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointRestoreBaseEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointRestoreCompletedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointRestoreFailedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointRestoreStartedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CheckpointStartedEvent": "shards_ai_agents.events.types.checkpoint_events",
    "CrewKickoffCompletedEvent": "shards_ai_agents.events.types.crew_events",
    "CrewKickoffFailedEvent": "shards_ai_agents.events.types.crew_events",
    "CrewKickoffStartedEvent": "shards_ai_agents.events.types.crew_events",
    "CrewTestCompletedEvent": "shards_ai_agents.events.types.crew_events",
    "CrewTestFailedEvent": "shards_ai_agents.events.types.crew_events",
    "CrewTestResultEvent": "shards_ai_agents.events.types.crew_events",
    "CrewTestStartedEvent": "shards_ai_agents.events.types.crew_events",
    "CrewTrainCompletedEvent": "shards_ai_agents.events.types.crew_events",
    "CrewTrainFailedEvent": "shards_ai_agents.events.types.crew_events",
    "CrewTrainStartedEvent": "shards_ai_agents.events.types.crew_events",
    "ConversationMessageAddedEvent": "shards_ai_agents.events.types.flow_events",
    "ConversationRouteSelectedEvent": "shards_ai_agents.events.types.flow_events",
    "ConversationTurnCompletedEvent": "shards_ai_agents.events.types.flow_events",
    "ConversationTurnFailedEvent": "shards_ai_agents.events.types.flow_events",
    "ConversationTurnStartedEvent": "shards_ai_agents.events.types.flow_events",
    "FlowCreatedEvent": "shards_ai_agents.events.types.flow_events",
    "FlowEvent": "shards_ai_agents.events.types.flow_events",
    "FlowFailedEvent": "shards_ai_agents.events.types.flow_events",
    "FlowFinishedEvent": "shards_ai_agents.events.types.flow_events",
    "FlowPlotEvent": "shards_ai_agents.events.types.flow_events",
    "FlowStartedEvent": "shards_ai_agents.events.types.flow_events",
    "HumanFeedbackReceivedEvent": "shards_ai_agents.events.types.flow_events",
    "HumanFeedbackRequestedEvent": "shards_ai_agents.events.types.flow_events",
    "MethodExecutionFailedEvent": "shards_ai_agents.events.types.flow_events",
    "MethodExecutionFinishedEvent": "shards_ai_agents.events.types.flow_events",
    "MethodExecutionStartedEvent": "shards_ai_agents.events.types.flow_events",
    "KnowledgeQueryCompletedEvent": "shards_ai_agents.events.types.knowledge_events",
    "KnowledgeQueryFailedEvent": "shards_ai_agents.events.types.knowledge_events",
    "KnowledgeQueryStartedEvent": "shards_ai_agents.events.types.knowledge_events",
    "KnowledgeRetrievalCompletedEvent": "shards_ai_agents.events.types.knowledge_events",
    "KnowledgeRetrievalStartedEvent": "shards_ai_agents.events.types.knowledge_events",
    "KnowledgeSearchQueryFailedEvent": "shards_ai_agents.events.types.knowledge_events",
    "ContextWindowSummarizationCompletedEvent": "shards_ai_agents.events.types.llm_events",
    "ContextWindowSummarizationFailedEvent": "shards_ai_agents.events.types.llm_events",
    "ContextWindowSummarizationStartedEvent": "shards_ai_agents.events.types.llm_events",
    "LLMCallCompletedEvent": "shards_ai_agents.events.types.llm_events",
    "LLMCallFailedEvent": "shards_ai_agents.events.types.llm_events",
    "LLMCallStartedEvent": "shards_ai_agents.events.types.llm_events",
    "LLMStreamChunkEvent": "shards_ai_agents.events.types.llm_events",
    "LLMGuardrailCompletedEvent": "shards_ai_agents.events.types.llm_guardrail_events",
    "LLMGuardrailStartedEvent": "shards_ai_agents.events.types.llm_guardrail_events",
    "AgentLogsExecutionEvent": "shards_ai_agents.events.types.logging_events",
    "AgentLogsStartedEvent": "shards_ai_agents.events.types.logging_events",
    "MCPConfigFetchFailedEvent": "shards_ai_agents.events.types.mcp_events",
    "MCPConnectionCompletedEvent": "shards_ai_agents.events.types.mcp_events",
    "MCPConnectionFailedEvent": "shards_ai_agents.events.types.mcp_events",
    "MCPConnectionStartedEvent": "shards_ai_agents.events.types.mcp_events",
    "MCPToolExecutionCompletedEvent": "shards_ai_agents.events.types.mcp_events",
    "MCPToolExecutionFailedEvent": "shards_ai_agents.events.types.mcp_events",
    "MCPToolExecutionStartedEvent": "shards_ai_agents.events.types.mcp_events",
    "MemoryQueryCompletedEvent": "shards_ai_agents.events.types.memory_events",
    "MemoryQueryFailedEvent": "shards_ai_agents.events.types.memory_events",
    "MemoryQueryStartedEvent": "shards_ai_agents.events.types.memory_events",
    "MemoryRetrievalCompletedEvent": "shards_ai_agents.events.types.memory_events",
    "MemoryRetrievalFailedEvent": "shards_ai_agents.events.types.memory_events",
    "MemoryRetrievalStartedEvent": "shards_ai_agents.events.types.memory_events",
    "MemorySaveCompletedEvent": "shards_ai_agents.events.types.memory_events",
    "MemorySaveFailedEvent": "shards_ai_agents.events.types.memory_events",
    "MemorySaveStartedEvent": "shards_ai_agents.events.types.memory_events",
    "PlanStepCompletedEvent": "shards_ai_agents.events.types.observation_events",
    "PlanStepEvent": "shards_ai_agents.events.types.observation_events",
    "PlanStepStartedEvent": "shards_ai_agents.events.types.observation_events",
    "AgentReasoningCompletedEvent": "shards_ai_agents.events.types.reasoning_events",
    "AgentReasoningFailedEvent": "shards_ai_agents.events.types.reasoning_events",
    "AgentReasoningStartedEvent": "shards_ai_agents.events.types.reasoning_events",
    "ReasoningEvent": "shards_ai_agents.events.types.reasoning_events",
    "SkillActivatedEvent": "shards_ai_agents.events.types.skill_events",
    "SkillDiscoveryCompletedEvent": "shards_ai_agents.events.types.skill_events",
    "SkillDiscoveryStartedEvent": "shards_ai_agents.events.types.skill_events",
    "SkillEvent": "shards_ai_agents.events.types.skill_events",
    "SkillLoadFailedEvent": "shards_ai_agents.events.types.skill_events",
    "SkillLoadedEvent": "shards_ai_agents.events.types.skill_events",
    "SkillUsedEvent": "shards_ai_agents.events.types.skill_events",
    "TaskCompletedEvent": "shards_ai_agents.events.types.task_events",
    "TaskEvaluationEvent": "shards_ai_agents.events.types.task_events",
    "TaskFailedEvent": "shards_ai_agents.events.types.task_events",
    "TaskStartedEvent": "shards_ai_agents.events.types.task_events",
    "ToolExecutionErrorEvent": "shards_ai_agents.events.types.tool_usage_events",
    "ToolFailureDetectedEvent": "shards_ai_agents.events.types.tool_usage_events",
    "ToolSelectionErrorEvent": "shards_ai_agents.events.types.tool_usage_events",
    "ToolUsageErrorEvent": "shards_ai_agents.events.types.tool_usage_events",
    "ToolUsageEvent": "shards_ai_agents.events.types.tool_usage_events",
    "ToolUsageFinishedEvent": "shards_ai_agents.events.types.tool_usage_events",
    "ToolUsageStartedEvent": "shards_ai_agents.events.types.tool_usage_events",
    "ToolValidateInputErrorEvent": "shards_ai_agents.events.types.tool_usage_events",
}

_extension_exports: dict[str, Any] = {}


def __getattr__(name: str) -> Any:
    """Lazy import for event types and registered extensions."""
    if name in _LAZY_EVENT_MAPPING:
        module_path = _LAZY_EVENT_MAPPING[name]
        module = importlib.import_module(module_path)
        val = getattr(module, name)
        globals()[name] = val  # cache for subsequent access
        return val

    if name in _extension_exports:
        value = _extension_exports[name]
        if isinstance(value, str):
            module_path, _, attr_name = value.rpartition(".")
            if module_path:
                module = importlib.import_module(module_path)
                return getattr(module, attr_name)
            return importlib.import_module(value)
        return value

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


__all__ = [
    "AgentEvaluationCompletedEvent",
    "AgentEvaluationFailedEvent",
    "AgentEvaluationStartedEvent",
    "AgentExecutionCompletedEvent",
    "AgentExecutionErrorEvent",
    "AgentExecutionStartedEvent",
    "AgentLogsExecutionEvent",
    "AgentLogsStartedEvent",
    "AgentReasoningCompletedEvent",
    "AgentReasoningFailedEvent",
    "AgentReasoningStartedEvent",
    "BaseEventListener",
    "CheckpointBaseEvent",
    "CheckpointCompletedEvent",
    "CheckpointFailedEvent",
    "CheckpointForkBaseEvent",
    "CheckpointForkCompletedEvent",
    "CheckpointForkStartedEvent",
    "CheckpointPrunedEvent",
    "CheckpointRestoreBaseEvent",
    "CheckpointRestoreCompletedEvent",
    "CheckpointRestoreFailedEvent",
    "CheckpointRestoreStartedEvent",
    "CheckpointStartedEvent",
    "CircularDependencyError",
    "ContextWindowSummarizationCompletedEvent",
    "ContextWindowSummarizationFailedEvent",
    "ContextWindowSummarizationStartedEvent",
    "ConversationMessageAddedEvent",
    "ConversationRouteSelectedEvent",
    "ConversationTurnCompletedEvent",
    "ConversationTurnFailedEvent",
    "ConversationTurnStartedEvent",
    "CrewKickoffCompletedEvent",
    "CrewKickoffFailedEvent",
    "CrewKickoffStartedEvent",
    "CrewTestCompletedEvent",
    "CrewTestFailedEvent",
    "CrewTestResultEvent",
    "CrewTestStartedEvent",
    "CrewTrainCompletedEvent",
    "CrewTrainFailedEvent",
    "CrewTrainStartedEvent",
    "Depends",
    "FlowCreatedEvent",
    "FlowEvent",
    "FlowFailedEvent",
    "FlowFinishedEvent",
    "FlowPlotEvent",
    "FlowStartedEvent",
    "HumanFeedbackReceivedEvent",
    "HumanFeedbackRequestedEvent",
    "KnowledgeQueryCompletedEvent",
    "KnowledgeQueryFailedEvent",
    "KnowledgeQueryStartedEvent",
    "KnowledgeRetrievalCompletedEvent",
    "KnowledgeRetrievalStartedEvent",
    "KnowledgeSearchQueryFailedEvent",
    "LLMCallCompletedEvent",
    "LLMCallFailedEvent",
    "LLMCallStartedEvent",
    "LLMGuardrailCompletedEvent",
    "LLMGuardrailStartedEvent",
    "LLMStreamChunkEvent",
    "LiteAgentExecutionCompletedEvent",
    "LiteAgentExecutionErrorEvent",
    "LiteAgentExecutionStartedEvent",
    "MCPConfigFetchFailedEvent",
    "MCPConnectionCompletedEvent",
    "MCPConnectionFailedEvent",
    "MCPConnectionStartedEvent",
    "MCPToolExecutionCompletedEvent",
    "MCPToolExecutionFailedEvent",
    "MCPToolExecutionStartedEvent",
    "MemoryQueryCompletedEvent",
    "MemoryQueryFailedEvent",
    "MemoryQueryStartedEvent",
    "MemoryRetrievalCompletedEvent",
    "MemoryRetrievalFailedEvent",
    "MemoryRetrievalStartedEvent",
    "MemorySaveCompletedEvent",
    "MemorySaveFailedEvent",
    "MemorySaveStartedEvent",
    "MethodExecutionFailedEvent",
    "MethodExecutionFinishedEvent",
    "MethodExecutionStartedEvent",
    "PlanStepCompletedEvent",
    "PlanStepEvent",
    "PlanStepStartedEvent",
    "ReasoningEvent",
    "SkillActivatedEvent",
    "SkillDiscoveryCompletedEvent",
    "SkillDiscoveryStartedEvent",
    "SkillEvent",
    "SkillLoadFailedEvent",
    "SkillLoadedEvent",
    "SkillUsedEvent",
    "TaskCompletedEvent",
    "TaskEvaluationEvent",
    "TaskFailedEvent",
    "TaskStartedEvent",
    "ToolExecutionErrorEvent",
    "ToolFailureDetectedEvent",
    "ToolSelectionErrorEvent",
    "ToolUsageErrorEvent",
    "ToolUsageEvent",
    "ToolUsageFinishedEvent",
    "ToolUsageStartedEvent",
    "ToolValidateInputErrorEvent",
    "_extension_exports",
    "shards_ai_agents_event_bus",
]
