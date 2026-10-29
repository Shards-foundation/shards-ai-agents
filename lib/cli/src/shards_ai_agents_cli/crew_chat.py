"""Wrapper for the crew chat command.

Delegates to ``shards_ai_agents.utilities.crew_chat.run_chat`` when the full shards_ai_agents
package is installed, otherwise prints a helpful error message.
"""

from __future__ import annotations

from pathlib import Path

from shards_ai_agents_cli.run_crew import (
    _full_shards_ai_agents_install_error,
    _is_missing_shards_ai_agents_package,
    configured_project_json_crew,
    load_project_env,
)


def run_chat() -> None:
    try:
        from shards_ai_agents.utilities.crew_chat import run_chat as _run_chat
    except ModuleNotFoundError as exc:
        if _is_missing_shards_ai_agents_package(exc):
            raise _full_shards_ai_agents_install_error() from None
        raise

    # Chat runs in the CLI's interpreter, where shards_ai_agents's import-time
    # load_dotenv() never finds the project's .env; load it like `shards-agents run`
    # does for JSON crews so MODEL and the provider key apply.
    env_file = Path.cwd() / ".env"
    if configured_project_json_crew() is not None and env_file.exists():
        load_project_env(env_file)

    _run_chat()
