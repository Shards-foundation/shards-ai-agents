"""Telemetry configuration constants.

This module defines constants used for Shards-ai-agents telemetry configuration.
"""

import os
from typing import Final


# Shards-ai-agents does not phone home. The upstream telemetry endpoint was removed in
# this fork; telemetry stays inert unless you point it at your own OTLP/HTTP collector
# by setting SHARDS_AI_AGENTS_TELEMETRY_BASE_URL (e.g. https://otel.example.com:4318).
SHARDS_AI_AGENTS_TELEMETRY_BASE_URL: Final[str] = os.environ.get(
    "SHARDS_AI_AGENTS_TELEMETRY_BASE_URL", ""
).rstrip("/")
SHARDS_AI_AGENTS_TELEMETRY_SERVICE_NAME: Final[str] = "shards-ai-agents-telemetry"

TRACER_NAME: Final[str] = "shards_ai_agents.telemetry"
