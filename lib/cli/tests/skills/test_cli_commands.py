"""Tests for the top-level `shards-agents skill` command group.

The Skills Repository graduated from the gated `shards_ai_agents experimental skill`
group: the commands must be reachable at `shards-agents skill ...` without
SHARDS_AI_AGENTS_EXPERIMENTAL set.
"""

from unittest import mock

from click.testing import CliRunner
from shards_ai_agents_cli.cli import shards_ai_agents
import pytest


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def no_experimental_env(monkeypatch):
    monkeypatch.delenv("SHARDS_AI_AGENTS_EXPERIMENTAL", raising=False)


class TestSkillGroupIsTopLevel:
    def test_skill_group_registered_at_top_level(self, runner, no_experimental_env):
        result = runner.invoke(shards_ai_agents, ["skill", "--help"])
        assert result.exit_code == 0, result.output
        for subcommand in ("create", "install", "publish", "list", "search"):
            assert subcommand in result.output

    def test_skill_group_not_gated_by_experimental_env(
        self, runner, no_experimental_env
    ):
        with mock.patch("shards_ai_agents_cli.skills.main.SkillCommand") as mock_cmd:
            result = runner.invoke(shards_ai_agents, ["skill", "create", "my-skill"])
        assert result.exit_code == 0, result.output
        mock_cmd.return_value.create.assert_called_once_with(
            "my-skill", in_project=True
        )

    def test_skill_create_no_project_flag(self, runner, no_experimental_env):
        with mock.patch("shards_ai_agents_cli.skills.main.SkillCommand") as mock_cmd:
            result = runner.invoke(shards_ai_agents, ["skill", "create", "my-skill", "--no-project"])
        assert result.exit_code == 0, result.output
        mock_cmd.return_value.create.assert_called_once_with(
            "my-skill", in_project=False
        )


class TestSkillPublishIsOrgScopedOnly:
    def test_publish_rejects_public_flag(self, runner, no_experimental_env):
        result = runner.invoke(shards_ai_agents, ["skill", "publish", "--public"])
        assert result.exit_code != 0
        assert "No such option" in result.output

    def test_publish_passes_org_and_force_only(self, runner, no_experimental_env):
        with mock.patch("shards_ai_agents_cli.skills.main.SkillCommand") as mock_cmd:
            result = runner.invoke(
                shards_ai_agents, ["skill", "publish", "--org", "acme", "--force"]
            )
        assert result.exit_code == 0, result.output
        mock_cmd.return_value.publish.assert_called_once_with(org="acme", force=True)


class TestSkillSearchCommand:
    @pytest.mark.parametrize(
        ("args", "query"), [(["support triage"], "support triage"), ([], None)]
    )
    def test_search_passes_the_optional_query(
        self, runner, no_experimental_env, args, query
    ):
        with mock.patch("shards_ai_agents_cli.skills.main.SkillCommand") as mock_cmd:
            result = runner.invoke(shards_ai_agents, ["skill", "search", *args])
        assert result.exit_code == 0, result.output
        mock_cmd.return_value.search.assert_called_once_with(query)

    def test_list_still_shows_installed_skills_only(self, runner, no_experimental_env):
        with mock.patch("shards_ai_agents_cli.skills.main.SkillCommand") as mock_cmd:
            result = runner.invoke(shards_ai_agents, ["skill", "list"])
        assert result.exit_code == 0, result.output
        mock_cmd.return_value.list_cached.assert_called_once_with()
        mock_cmd.return_value.search.assert_not_called()
