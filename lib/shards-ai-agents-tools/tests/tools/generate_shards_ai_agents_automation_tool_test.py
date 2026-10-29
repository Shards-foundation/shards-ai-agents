import os
from unittest.mock import MagicMock, patch

from shards_ai_agents_tools.tools.generate_shards_ai_agents_automation_tool.generate_shards_ai_agents_automation_tool import (
    GenerateShardsAgentsAutomationTool,
    GenerateShardsAgentsAutomationToolSchema,
)
import pytest
import requests


@pytest.fixture(autouse=True)
def mock_env():
    with patch.dict(os.environ, {"SHARDS_AI_AGENTS_PERSONAL_ACCESS_TOKEN": "test_token"}):
        os.environ.pop("SHARDS_AI_AGENTS_PLUS_URL", None)
        yield


@pytest.fixture
def tool():
    return GenerateShardsAgentsAutomationTool()


@pytest.fixture
def custom_url_tool():
    with patch.dict(os.environ, {"SHARDS_AI_AGENTS_PLUS_URL": "https://custom.shards-ai-agents.invalid"}):
        return GenerateShardsAgentsAutomationTool()


def test_default_initialization(tool):
    assert tool.shards_ai_agents_enterprise_url == "https://app.shards-ai-agents.invalid"
    assert tool.personal_access_token == "test_token"
    assert tool.name == "Generate Shards-ai-agents Automation"


def test_custom_base_url_from_environment(custom_url_tool):
    assert custom_url_tool.shards_ai_agents_enterprise_url == "https://custom.shards-ai-agents.invalid"


def test_personal_access_token_from_environment(tool):
    assert tool.personal_access_token == "test_token"


def test_valid_prompt_only():
    schema = GenerateShardsAgentsAutomationToolSchema(
        prompt="Create a web scraping automation"
    )
    assert schema.prompt == "Create a web scraping automation"
    assert schema.organization_id is None


def test_valid_prompt_with_organization_id():
    schema = GenerateShardsAgentsAutomationToolSchema(
        prompt="Create automation", organization_id="org-123"
    )
    assert schema.prompt == "Create automation"
    assert schema.organization_id == "org-123"


def test_empty_prompt_validation():
    schema = GenerateShardsAgentsAutomationToolSchema(prompt="")
    assert schema.prompt == ""
    assert schema.organization_id is None


@patch("requests.post")
def test_successful_generation_without_org_id(mock_post, tool):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "url": "https://app.shards-ai-agents.invalid/studio/project-123"
    }
    mock_post.return_value = mock_response

    result = tool.run(prompt="Create automation")

    assert (
        result
        == "Generated Shards-ai-agents Studio project URL: https://app.shards-ai-agents.invalid/studio/project-123"
    )
    mock_post.assert_called_once_with(
        "https://app.shards-ai-agents.invalid/shards_ai_agents_plus/api/v1/studio",
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={"prompt": "Create automation"},
    )


@patch("requests.post")
def test_successful_generation_with_org_id(mock_post, tool):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "url": "https://app.shards-ai-agents.invalid/studio/project-456"
    }
    mock_post.return_value = mock_response

    result = tool.run(prompt="Create automation", organization_id="org-456")

    assert (
        result
        == "Generated Shards-ai-agents Studio project URL: https://app.shards-ai-agents.invalid/studio/project-456"
    )
    mock_post.assert_called_once_with(
        "https://app.shards-ai-agents.invalid/shards_ai_agents_plus/api/v1/studio",
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Shards-Agents-Organization-Id": "org-456",
        },
        json={"prompt": "Create automation"},
    )


@patch("requests.post")
def test_custom_base_url_usage(mock_post, custom_url_tool):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "url": "https://custom.shards-ai-agents.invalid/studio/project-789"
    }
    mock_post.return_value = mock_response

    custom_url_tool.run(prompt="Create automation")

    mock_post.assert_called_once_with(
        "https://custom.shards-ai-agents.invalid/shards_ai_agents_plus/api/v1/studio",
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={"prompt": "Create automation"},
    )


@patch("requests.post")
def test_api_error_response_handling(mock_post, tool):
    mock_post.return_value.raise_for_status.side_effect = requests.HTTPError(
        "400 Bad Request"
    )

    with pytest.raises(requests.HTTPError):
        tool.run(prompt="Create automation")


@patch("requests.post")
def test_network_error_handling(mock_post, tool):
    mock_post.side_effect = requests.ConnectionError("Network unreachable")

    with pytest.raises(requests.ConnectionError):
        tool.run(prompt="Create automation")


@patch("requests.post")
def test_api_response_missing_url(mock_post, tool):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}
    mock_post.return_value = mock_response

    result = tool.run(prompt="Create automation")

    assert result == "Generated Shards-ai-agents Studio project URL: None"


def test_authorization_header_construction(tool):
    headers = tool._get_headers()

    assert headers["Authorization"] == "Bearer test_token"
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "application/json"
    assert "X-Shards-Agents-Organization-Id" not in headers


def test_authorization_header_with_org_id(tool):
    headers = tool._get_headers(organization_id="org-123")

    assert headers["Authorization"] == "Bearer test_token"
    assert headers["X-Shards-Agents-Organization-Id"] == "org-123"


def test_missing_personal_access_token():
    with patch.dict(os.environ, {}, clear=True):
        tool = GenerateShardsAgentsAutomationTool()
        assert tool.personal_access_token is None
