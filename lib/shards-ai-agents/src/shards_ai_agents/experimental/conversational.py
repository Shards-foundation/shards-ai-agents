"""Deprecated compatibility alias for :mod:`shards_ai_agents.flow.conversational`."""

import sys

from shards_ai_agents.flow import conversational as _real


sys.modules[__name__] = _real
