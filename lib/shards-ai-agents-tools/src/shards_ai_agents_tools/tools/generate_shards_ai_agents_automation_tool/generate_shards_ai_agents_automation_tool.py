import os
from typing import Any

from pydantic import BaseModel, Field
import requests
from shards_ai_agents.tools import BaseTool, EnvVar


class GenerateShardsAgentsAutomationToolSchema(BaseModel):
    prompt: str = Field(
        description="The prompt to generate the Shards-ai-agents automation, e.g. 'Generate a Shards-ai-agents automation that will scrape the website and store the data in a database.'"
    )
    organization_id: str | None = Field(
        default=None,
        description="The identifier for the Shards-ai-agents AMP organization. If not specified, a default organization will be used.",
    )


class GenerateShardsAgentsAutomationTool(BaseTool):
    name: str = "Generate Shards-ai-agents Automation"
    description: str = (
        "A tool that leverages Shards-ai-agents Studio's capabilities to automatically generate complete Shards-ai-agents "
        "automations based on natural language descriptions. It translates high-level requirements into "
        "functional Shards-ai-agents implementations."
    )
    args_schema: type[BaseModel] = GenerateShardsAgentsAutomationToolSchema
    shards_ai_agents_enterprise_url: str = Field(
        default_factory=lambda: os.getenv(
            "SHARDS_AI_AGENTS_PLUS_URL", "https://app.shards-ai-agents.invalid"
        ),
        description="The base URL of Shards-ai-agents AMP. If not provided, it will be loaded from the environment variable SHARDS_AI_AGENTS_PLUS_URL with default https://app.shards-ai-agents.invalid.",
    )
    personal_access_token: str | None = Field(
        default_factory=lambda: os.getenv("SHARDS_AI_AGENTS_PERSONAL_ACCESS_TOKEN"),
        description="The user's Personal Access Token to access Shards-ai-agents AMP API. If not provided, it will be loaded from the environment variable SHARDS_AI_AGENTS_PERSONAL_ACCESS_TOKEN.",
    )
    env_vars: list[EnvVar] = Field(
        default_factory=lambda: [
            EnvVar(
                name="SHARDS_AI_AGENTS_PERSONAL_ACCESS_TOKEN",
                description="Personal Access Token for Shards-ai-agents Enterprise API",
                required=True,
            ),
            EnvVar(
                name="SHARDS_AI_AGENTS_PLUS_URL",
                description="Base URL for Shards-ai-agents Enterprise API",
                required=False,
            ),
        ]
    )

    def _run(self, **kwargs: Any) -> str:
        input_data = GenerateShardsAgentsAutomationToolSchema(**kwargs)
        response = requests.post(  # noqa: S113
            f"{self.shards_ai_agents_enterprise_url}/shards_ai_agents_plus/api/v1/studio",
            headers=self._get_headers(input_data.organization_id),
            json={"prompt": input_data.prompt},
        )

        response.raise_for_status()
        studio_project_url = response.json().get("url")
        return f"Generated Shards-ai-agents Studio project URL: {studio_project_url}"

    def _get_headers(self, organization_id: str | None = None) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.personal_access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if organization_id:
            headers["X-Shards-Agents-Organization-Id"] = organization_id

        return headers
