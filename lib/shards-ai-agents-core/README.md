# shards-ai-agents-core

Shared utilities used by both `shards_ai_agents` and `shards-ai-agents-cli`: version lookup, storage
paths, user-data helpers, telemetry, and the printer.

This package is a leaf — it has no dependency on the `shards_ai_agents` framework — and is
pulled in transitively by `shards_ai_agents` and `shards-ai-agents-cli`. End users do not normally
install it directly.
