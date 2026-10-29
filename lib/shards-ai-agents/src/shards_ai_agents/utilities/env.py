import contextvars
import os

from shards_ai_agents.events.event_bus import shards_ai_agents_event_bus
from shards_ai_agents.events.types.env_events import (
    CCEnvEvent,
    CodexEnvEvent,
    CursorEnvEvent,
    DefaultEnvEvent,
)
from shards_ai_agents.utilities.constants import CODING_AGENT_ENV_MARKERS


_env_context_emitted: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "_env_context_emitted", default=False
)

# Assistants with an event of their own. Anything else in the shared table is
# detected with the same precedence but reported as DefaultEnvEvent, so the two
# detection paths can never disagree about which assistant is present.
_AGENT_EVENTS = {
    "claude_code": CCEnvEvent,
    "codex": CodexEnvEvent,
    "cursor": CursorEnvEvent,
}


def get_env_context() -> None:
    if _env_context_emitted.get():
        return
    _env_context_emitted.set(True)

    # Walks the shared table rather than restating precedence: hard-coding the
    # order here let the two paths drift, so a marker added for telemetry was
    # invisible to this one.
    for agent_name, env_vars in CODING_AGENT_ENV_MARKERS:
        if any(os.environ.get(var) for var in env_vars):
            event = _AGENT_EVENTS.get(agent_name, DefaultEnvEvent)
            shards_ai_agents_event_bus.emit(None, event())
            return

    shards_ai_agents_event_bus.emit(None, DefaultEnvEvent())
