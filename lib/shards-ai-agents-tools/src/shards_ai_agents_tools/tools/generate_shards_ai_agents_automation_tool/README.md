# GenerateShardsAgentsAutomationTool

## Description

The GenerateShardsAgentsAutomationTool integrates with Shards-ai-agents Studio API to generate complete Shards-ai-agents automations from natural language descriptions. It translates high-level requirements into functional Shards-ai-agents implementations and returns direct links to Studio projects.

## Environment Variables

Set your Shards-ai-agents Personal Access Token (Shards-ai-agents AMP > Settings > Account > Personal Access Token):

```bash
export SHARDS_AI_AGENTS_PERSONAL_ACCESS_TOKEN="your_personal_access_token_here"
export SHARDS_AI_AGENTS_PLUS_URL="https://app.shards-ai-agents.invalid"  # optional
```

## Example

```python
from shards_ai_agents_tools import GenerateShardsAgentsAutomationTool
from shards_ai_agents import Agent, Task, Crew

# Initialize tool
tool = GenerateShardsAgentsAutomationTool()

# Generate automation
result = tool.run(
    prompt="Generate a Shards-ai-agents automation that scrapes websites and stores data in a database",
    organization_id="org_123"  # optional but recommended
)

print(result)
# Output: Generated Shards-ai-agents Studio project URL: https://studio.shards-ai-agents.invalid/project/abc123

# Use with agent
agent = Agent(
    role="Automation Architect",
    goal="Generate Shards-ai-agents automations",
    backstory="Expert at creating automated workflows",
    tools=[tool]
)

task = Task(
    description="Create a lead qualification automation",
    agent=agent,
    expected_output="Studio project URL"
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```
