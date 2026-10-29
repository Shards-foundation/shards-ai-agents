"""Re-export of ``shards_ai_agents_core.token_manager.TokenManager``.

Kept as a stable import path for the CLI; new code should import from
``shards_ai_agents_core.token_manager`` directly.
"""

from __future__ import annotations

from shards_ai_agents_core.token_manager import TokenManager as TokenManager


__all__ = ["TokenManager"]
