"""Backwards-compatible re-export surface for the Flow framework.

The implementation now lives in three modules, split by concern:

- ``shards_ai_agents.flow.dsl`` -- authoring decorators (``@start`` / ``@listen`` /
  ``@router``, ``or_`` / ``and_``) and Python Flow class projection
- ``shards_ai_agents.flow.flow_definition`` -- the serializable Flow Definition contract
- ``shards_ai_agents.flow.runtime`` -- the Flow execution engine and state
- ``shards_ai_agents.flow.conversational_mixin`` -- conversational
  runtime extension composed onto the public ``Flow`` class

Prefer importing from those modules in new code; this module preserves the
historical ``shards_ai_agents.flow.flow`` import path.
"""

from typing import Any, TypeVar

from pydantic import BaseModel

from shards_ai_agents.flow.conversational_mixin import _ConversationalMixin
from shards_ai_agents.flow.dsl import and_, listen, or_, router, start

# Never exported here before, but the AGENTS.md scaffolded by shards_ai_agents
# 1.10.0-1.15.28 taught `from shards_ai_agents.flow.flow import persist`.
from shards_ai_agents.flow.persistence import persist
from shards_ai_agents.flow.runtime import (
    _INITIAL_STATE_CLASS_MARKER,
    Flow as RuntimeFlow,
    FlowMeta,
    FlowState,
)


T = TypeVar("T", bound=dict[str, Any] | BaseModel)


class Flow(_ConversationalMixin, RuntimeFlow[T]):
    """Public Flow class with conversational extension behavior."""


__all__ = [
    "_INITIAL_STATE_CLASS_MARKER",
    "Flow",
    "FlowMeta",
    "FlowState",
    "and_",
    "listen",
    "or_",
    "persist",
    "router",
    "start",
]
