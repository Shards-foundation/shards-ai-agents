from shards_ai_agents.tools import BaseTool

from shards_ai_agents_tools.tools.shards_ai_agents_platform_tools.integrations_client import (
    ApplicationSelector,
    client_for_selector,
)
from shards_ai_agents_tools.tools.shards_ai_agents_platform_tools.shards_ai_agents_platform_action_tool import (
    ShardsAgentsPlatformActionTool,
)


def ShardsAgentsPlatformTools(  # noqa: N802
    apps: list[str],
) -> list[BaseTool]:
    """Factory function that returns shards_ai_agents platform tools.

    Args:
        apps: List of platform apps to get tools that are available on the platform.

    Returns:
        A list of BaseTool instances for platform actions
    """
    selectors = [ApplicationSelector.from_string(app) for app in apps]
    tools: list[BaseTool] = []

    for selector in selectors:
        client = client_for_selector(selector)
        tools.extend(
            ShardsAgentsPlatformActionTool(tool_info, client=client)
            for tool_info in client.get_actions([selector])
        )

    return tools
