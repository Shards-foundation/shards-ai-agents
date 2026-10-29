"""Deprecated compatibility alias for :mod:`shards_ai_agents.flow.conversational_mixin`."""

import sys

from shards_ai_agents.flow import conversational_mixin as _real


sys.modules[__name__] = _real
