"""Tests for the ``shards-agents run`` command and its subprocess plumbing."""

import os
from pathlib import Path
import subprocess
import sys
from types import ModuleType
from types import SimpleNamespace
from unittest import mock

from click.testing import CliRunner
import pytest

import shards_ai_agents_cli
from shards_ai_agents_cli.cli import run
from shards_ai_agents_cli.run_crew import (
    _SHARDS_AI_AGENTS_CLI_RUNNER_PACKAGE_DIR_ENV,
    _SHARDS_AI_AGENTS_JSON_CREW_DEFINITION_ENV,
    _JSON_CREW_RUNNER_CODE,
    _execute_uv_script,
    _load_json_crew_for_tui,
    _missing_input_names,
    _resolve_crew_inputs,
)


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@mock.patch("shards_ai_agents_cli.run_crew.run_crew")
def test_run_passes_filename_to_run_crew(run_crew_mock: mock.Mock, runner: CliRunner) -> None:
    result = runner.invoke(run, ["-f", "my_custom_trained.pkl"])

    run_crew_mock.assert_called_once_with(
        trained_agents_file="my_custom_trained.pkl",
        definition=None,
        inputs=None,
    )
    assert result.exit_code == 0


@mock.patch("shards_ai_agents_cli.run_crew.run_crew")
def test_run_without_filename_passes_none(run_crew_mock: mock.Mock, runner: CliRunner) -> None:
    result = runner.invoke(run)

    run_crew_mock.assert_called_once_with(
        trained_agents_file=None,
        definition=None,
        inputs=None,
    )
    assert result.exit_code == 0


@mock.patch("shards_ai_agents_cli.run_crew.subprocess.run")
@mock.patch(
    "shards_ai_agents_cli.run_crew.build_env_with_all_tool_credentials",
    return_value={"EXISTING": "value"},
)
def test_execute_command_sets_env_var_when_filename_provided(
    _build_env: mock.Mock, subprocess_run: mock.Mock
) -> None:
    _execute_uv_script(
        "run_crew",
        entity_type="crew",
        trained_agents_file="my_custom_trained.pkl",
    )

    _, kwargs = subprocess_run.call_args
    assert kwargs["env"]["SHARDS_AI_AGENTS_TRAINED_AGENTS_FILE"] == "my_custom_trained.pkl"
    assert kwargs["env"]["EXISTING"] == "value"


@mock.patch("shards_ai_agents_cli.run_crew.subprocess.run")
@mock.patch(
    "shards_ai_agents_cli.run_crew.build_env_with_all_tool_credentials",
    return_value={"EXISTING": "value"},
)
def test_execute_command_omits_env_var_when_filename_absent(
    _build_env: mock.Mock, subprocess_run: mock.Mock
) -> None:
    _execute_uv_script("run_crew", entity_type="crew")

    _, kwargs = subprocess_run.call_args
    assert "SHARDS_AI_AGENTS_TRAINED_AGENTS_FILE" not in kwargs["env"]


def test_missing_input_names_scans_agent_and_task_placeholders() -> None:
    crew = SimpleNamespace(
        agents=[
            SimpleNamespace(
                role="Researcher for {topic}",
                goal="Write for {audience}",
                backstory="Ignore escaped {{not_an_input}}",
            )
        ],
        tasks=[
            SimpleNamespace(
                description="Research {topic}",
                expected_output="A post for {channel}",
                output_file="{slug}.md",
            )
        ],
    )

    assert _missing_input_names(crew, {"topic": "AI"}) == [
        "audience",
        "channel",
        "slug",
    ]


def test_resolve_crew_inputs_merges_runtime_values(monkeypatch) -> None:
    crew = SimpleNamespace(
        agents=[SimpleNamespace(role="Researcher", goal="Cover {topic}", backstory="")],
        tasks=[
            SimpleNamespace(
                description="Write for {audience}",
                expected_output="Post",
                output_file=None,
            )
        ],
    )
    values = {"audience": "developers"}

    def prompt(label: str, **_kwargs: object) -> str:
        if "audience" in str(label):
            return values["audience"]
        raise AssertionError(f"Unexpected prompt: {label}")

    # Prompting now lives in the shared shards_ai_agents_cli.input_prompt helper.
    monkeypatch.setattr("shards_ai_agents_cli.input_prompt.click.prompt", prompt)

    assert _resolve_crew_inputs(crew, {"topic": "AI"}, None, interactive=True) == {
        "topic": "AI",
        "audience": "developers",
    }


def test_load_json_crew_for_tui_prepares_metadata_before_prompt(monkeypatch) -> None:
    class FakeApp:
        pass

    fake_tui_module = ModuleType("shards_ai_agents_cli.crew_run_tui")
    fake_tui_module.CrewRunApp = FakeApp
    monkeypatch.setitem(sys.modules, "shards_ai_agents_cli.crew_run_tui", fake_tui_module)

    crew = SimpleNamespace(
        name="Demo Crew",
        tasks=[
            SimpleNamespace(name="research_task", description="Research"),
            SimpleNamespace(name="", description="Write summary for developers"),
        ],
        agents=[
            SimpleNamespace(role="Researcher", name="researcher"),
            SimpleNamespace(role="", name="writer"),
        ],
    )
    prepared: list[object] = []

    monkeypatch.setattr(
        "shards_ai_agents_cli.run_crew._json_loading_status",
        lambda _message: mock.MagicMock(),
    )
    monkeypatch.setattr(
        "shards_ai_agents_cli.run_crew._load_json_crew",
        lambda _path: (crew, {"topic": "AI"}),
    )
    monkeypatch.setattr(
        "shards_ai_agents_cli.run_crew._prepare_json_crew_for_tui",
        lambda loaded_crew: prepared.append(loaded_crew),
    )

    app_cls, loaded_crew, default_inputs, task_names, agent_names = (
        _load_json_crew_for_tui(Path("crew.jsonc"))
    )

    assert app_cls is FakeApp
    assert loaded_crew is crew
    assert default_inputs == {"topic": "AI"}
    assert task_names == ["research_task", "Write summary for developers"]
    assert agent_names == ["Researcher", "writer"]
    assert prepared == [crew]


# Mirrors lib/cli/tests/test_run_crew.py, which CI does not run: the runner execs this
# CLI against the project's own (possibly older) shards-ai-agents-core, so a module-level
# import of a newer core symbol on the runner path must fail here.
def test_json_runner_imports_with_older_project_env_shards_ai_agents_core(tmp_path: Path) -> None:
    old_parent = tmp_path / "old_env"
    old_shards_ai_agents_core = old_parent / "shards_ai_agents_core"
    old_shards_ai_agents_core.mkdir(parents=True)
    (old_shards_ai_agents_core / "__init__.py").write_text("")
    (old_shards_ai_agents_core / "constants.py").write_text(
        "SHARDS_AI_AGENTS_TRAINED_AGENTS_FILE_ENV = 'SHARDS_AI_AGENTS_TRAINED_AGENTS_FILE'\n"
    )
    (old_shards_ai_agents_core / "project.py").write_text(
        "def read_toml(*args, **kwargs):\n"
        "    return {}\n"
        "def parse_toml(*args, **kwargs):\n"
        "    return {}\n"
        "def get_project_description(*args, **kwargs):\n"
        "    return None\n"
        "def get_project_name(*args, **kwargs):\n"
        "    return None\n"
        "def get_project_version(*args, **kwargs):\n"
        "    return None\n"
    )
    (old_shards_ai_agents_core / "tool_credentials.py").write_text(
        "def build_env_with_all_tool_credentials(*args, **kwargs):\n"
        "    return {}\n"
        "def build_env_with_tool_repository_credentials(*args, **kwargs):\n"
        "    return {}\n"
    )
    (old_shards_ai_agents_core / "version.py").write_text(
        "def check_version(*args, **kwargs):\n"
        "    return None\n"
        "def get_shards_ai_agents_version(*args, **kwargs):\n"
        "    return '1.0.0'\n"
        "def get_latest_version_from_pypi(*args, **kwargs):\n"
        "    return None\n"
        "def is_current_version_yanked(*args, **kwargs):\n"
        "    return False\n"
        "def is_newer_version_available(*args, **kwargs):\n"
        "    return False\n"
    )

    marker = tmp_path / "marker.txt"
    old_shards_ai_agents_project = old_parent / "shards_ai_agents" / "project"
    old_shards_ai_agents_project.mkdir(parents=True)
    (old_parent / "shards_ai_agents" / "__init__.py").write_text("")
    (old_shards_ai_agents_project / "__init__.py").write_text("")
    (old_shards_ai_agents_project / "crew_loader.py").write_text(
        "from pathlib import Path\n"
        "class Crew:\n"
        "    agents = []\n"
        "    tasks = []\n"
        "    def kickoff(self, inputs):\n"
        f"        Path({str(marker)!r}).write_text('ran')\n"
        "        return 'done'\n"
        "def load_crew(path):\n"
        "    return Crew(), {}\n"
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(old_parent)
    env["SHARDS_AI_AGENTS_DMN"] = "true"
    env[_SHARDS_AI_AGENTS_CLI_RUNNER_PACKAGE_DIR_ENV] = str(
        Path(shards_ai_agents_cli.__file__).resolve().parent
    )
    env[_SHARDS_AI_AGENTS_JSON_CREW_DEFINITION_ENV] = "crew.jsonc"

    subprocess.run(
        [sys.executable, "-c", _JSON_CREW_RUNNER_CODE],
        check=True,
        env=env,
        cwd=tmp_path,
    )

    assert marker.read_text() == "ran"
