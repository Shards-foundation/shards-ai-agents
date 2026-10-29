"""Project package for Shards-ai-agents."""

from shards_ai_agents.project.annotations import (
    after_kickoff,
    agent,
    before_kickoff,
    cache_handler,
    callback,
    crew,
    llm,
    output_json,
    output_pydantic,
    task,
    tool,
)
from shards_ai_agents.project.crew_base import CrewBase
from shards_ai_agents.project.crew_definition import (
    AgentDefinition,
    CrewAgentDefinition,
    CrewDefinition,
    CrewTaskDefinition,
    PythonReferenceDefinition,
)
from shards_ai_agents.project.crew_loader import load_crew, load_crew_and_kickoff
from shards_ai_agents.project.json_loader import (
    load_agent,
    load_agent_from_definition,
    strip_jsonc_comments,
)


__all__ = [
    "AgentDefinition",
    "CrewAgentDefinition",
    "CrewBase",
    "CrewDefinition",
    "CrewTaskDefinition",
    "PythonReferenceDefinition",
    "after_kickoff",
    "agent",
    "before_kickoff",
    "cache_handler",
    "callback",
    "crew",
    "llm",
    "load_agent",
    "load_agent_from_definition",
    "load_crew",
    "load_crew_and_kickoff",
    "output_json",
    "output_pydantic",
    "strip_jsonc_comments",
    "task",
    "tool",
]
