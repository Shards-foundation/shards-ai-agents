# shards-ai-agents-cli

CLI for Shards-ai-agents — scaffold, run, deploy and manage AI agent crews without
installing the full framework.

## Installation

```bash
pip install shards-ai-agents-cli
```

This pulls in `shards-ai-agents-core` (shared utilities) but not the `shards_ai_agents` framework
itself, so commands that don't need a crew loaded — `shards-agents version`,
`shards-agents login`, `shards-agents org list`, `shards-agents config *`, `shards-agents traces *`,
`shards-agents create`, `shards-agents template *` — work standalone.

Commands that load a user's crew or flow (`shards-agents run`, `shards-agents train`,
`shards-agents test`, `shards-agents chat`, `shards-agents replay`, `shards-agents reset-memories`,
`shards-agents deploy push`, `shards-agents tool publish`) require `shards_ai_agents` to be installed
in the project's environment. They print a clear error if it is missing.

To install both at once:

```bash
pip install shards-ai-agents[cli]
```
