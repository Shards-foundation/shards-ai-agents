"""Persistent per-user data + tracing-consent helpers.

This is the single source of truth for the ``.shards_ai_agents_user.json`` file used by
both shards_ai_agents (to record trace consent) and shards-ai-agents-cli (to read/write it via
``shards-agents traces enable/disable/status``).
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, cast

from shards_ai_agents_core.lock_store import lock as store_lock
from shards_ai_agents_core.paths import db_storage_path


logger = logging.getLogger(__name__)


def _user_data_file() -> Path:
    base = Path(db_storage_path())
    base.mkdir(parents=True, exist_ok=True)
    return base / ".shards_ai_agents_user.json"


def _user_data_lock_name() -> str:
    """Return a stable lock name for the user data file."""
    return f"file:{os.path.realpath(_user_data_file())}"


def _load_user_data() -> dict[str, Any]:
    """Read the user-data JSON file, returning ``{}`` on missing/corrupt."""
    p = _user_data_file()
    if p.exists():
        try:
            return cast(dict[str, Any], json.loads(p.read_text()))
        except (json.JSONDecodeError, OSError, PermissionError) as e:
            logger.warning("Failed to load user data: %s", e)
    return {}


def _save_user_data(data: dict[str, Any]) -> None:
    """Write the full user-data dict, ignoring write errors with a warning."""
    try:
        p = _user_data_file()
        p.write_text(json.dumps(data, indent=2))
    except (OSError, PermissionError) as e:
        logger.warning("Failed to save user data: %s", e)


def update_user_data(updates: dict[str, Any]) -> None:
    """Atomically read-modify-write the user data file under a file lock.

    Args:
        updates: Key-value pairs to merge into the existing user data.
    """
    try:
        with store_lock(_user_data_lock_name()):
            data = _load_user_data()
            data.update(updates)
            _save_user_data(data)
    except (OSError, PermissionError) as e:
        logger.warning("Failed to update user data: %s", e)


def has_user_declined_tracing() -> bool:
    """Return True if the user has explicitly declined trace collection."""
    data = _load_user_data()
    if data.get("first_execution_done", False):
        return data.get("trace_consent", False) is False
    return False


def is_tracing_enabled() -> bool:
    """Return True if tracing should currently be active.

    Mirrors the runtime gate (``shards_ai_agents.events.listeners.tracing.utils.
    should_enable_tracing``): ``SHARDS_AI_AGENTS_TRACING_ENABLED=false`` (or ``0``)
    always deactivates and ``true`` (or ``1``) always activates; otherwise
    recorded consent activates; otherwise off. Used by ``shards-agents traces status``
    so the displayed state matches what crews and flows actually do.
    """
    env_value = os.getenv("SHARDS_AI_AGENTS_TRACING_ENABLED", "").lower()
    if env_value in ("false", "0"):
        return False
    if env_value in ("true", "1"):
        return True
    if has_user_declined_tracing():
        return False
    data = _load_user_data()
    return data.get("trace_consent", False) is not False
