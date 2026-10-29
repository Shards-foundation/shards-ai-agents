import os


def get_platform_integration_token() -> str:
    """Get the Platform integration token from the environment."""
    token = os.getenv(
        "SHARDS_AI_AGENTS_ENTERPRISE_ACTION_AUTH_TOKEN",
        os.getenv("SHARDS_AI_AGENTS_PLATFORM_INTEGRATION_TOKEN", ""),
    )
    if not token:
        raise ValueError(
            "No Enterprise Action Auth Token found, please set the "
            "SHARDS_AI_AGENTS_ENTERPRISE_ACTION_AUTH_TOKEN environment variable"
        )
    return token  # TODO: Use context manager to get token
