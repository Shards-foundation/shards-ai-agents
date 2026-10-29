"""The former experimental conversational imports remain compatible."""

from importlib import import_module
from pydoc import locate

from shards_ai_agents.flow import (
    AgentMessage,
    ConversationConfig,
    ConversationEvent,
    ConversationMessage,
    ConversationState,
    RouterConfig,
)
from shards_ai_agents.utilities.declarative_refs import resolve_ref


def test_experimental_conversational_module_aliases_stable_module() -> None:
    experimental = import_module("shards_ai_agents.experimental.conversational")
    stable = import_module("shards_ai_agents.flow.conversational")

    assert experimental is stable


def test_experimental_namespace_reexports_stable_types() -> None:
    from shards_ai_agents.experimental import (
        AgentMessage as ExperimentalAgentMessage,
        ConversationConfig as ExperimentalConversationConfig,
        ConversationEvent as ExperimentalConversationEvent,
        ConversationMessage as ExperimentalConversationMessage,
        ConversationState as ExperimentalConversationState,
        RouterConfig as ExperimentalRouterConfig,
    )

    assert ExperimentalAgentMessage is AgentMessage
    assert ExperimentalConversationConfig is ConversationConfig
    assert ExperimentalConversationEvent is ConversationEvent
    assert ExperimentalConversationMessage is ConversationMessage
    assert ExperimentalConversationState is ConversationState
    assert ExperimentalRouterConfig is RouterConfig


def test_experimental_conversational_mixin_aliases_stable_module() -> None:
    experimental = import_module("shards_ai_agents.experimental.conversational_mixin")
    stable = import_module("shards_ai_agents.flow.conversational_mixin")

    assert experimental is stable
    assert experimental._ConversationalMixin is stable._ConversationalMixin


def test_legacy_declarative_references_still_resolve() -> None:
    assert (
        resolve_ref(
            "shards_ai_agents.experimental.conversational:ConversationState",
            field="state",
        )
        is ConversationState
    )
    assert (
        locate("shards_ai_agents.experimental.conversational.ConversationState")
        is ConversationState
    )
