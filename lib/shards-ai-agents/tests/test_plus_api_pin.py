"""`import shards_ai_agents` pins AMP's proxy and CA before it loads a project's .env.

A classic crew runs in its own process (`uv run run_crew`), which never imports the
CLI. There, `import shards_ai_agents` is the first thing to read the project's `.env`, so the
machine's transport settings have to be captured before that happens. That holds
only if the process starts without the `.env` already in its environment, which
`shards-agents eval` has to see to when it loads the `.env` and then runs the crew.
"""

import json
import os
from pathlib import Path
import subprocess
import sys

from shards_ai_agents_core import plus_api
import pytest


def test_import_shards_ai_agents_pins_the_machines_proxy_before_the_project_env_loads(
    tmp_path: Path,
) -> None:
    (tmp_path / ".env").write_text(
        "HTTPS_PROXY=http://project-proxy.test:8080\nSSL_CERT_FILE=/project/ca.pem\n"
    )
    env = {key: value for key, value in os.environ.items() if not plus_api._sets_transport(key)}
    probe = (
        "import json, os\n"
        "import shards_ai_agents\n"
        "from shards_ai_agents_core import plus_api\n"
        "print(json.dumps({'loaded': os.environ.get('HTTPS_PROXY'),"
        " 'pinned': plus_api._MACHINE_TRANSPORT_ENV}))\n"
    )

    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    seen = json.loads(result.stdout.strip().splitlines()[-1])
    # shards_ai_agents loaded the project's .env (so the test means something) ...
    assert seen["loaded"] == "http://project-proxy.test:8080"
    # ... after the pin, which holds only what the machine set: nothing.
    assert seen["pinned"] == {}


@pytest.mark.parametrize(
    "machine",
    [{}, {"HTTPS_PROXY": "http://machine-proxy.test:3128"}],
    ids=["machine-sets-none", "machine-sets-its-own"],
)
def test_the_crew_shards_ai_agents_eval_runs_pins_the_machines_proxy_not_the_project_envs(
    tmp_path: Path, machine: dict[str, str]
) -> None:
    """`shards-agents eval` loads the project's .env, then starts the crew with `uv run`
    in a child process that inherits its environment and pins from it. The .env
    also names itself as uv's env file, which uv would load before Python starts."""
    (tmp_path / ".env").write_text(
        "HTTPS_PROXY=http://project-proxy.test:8080\n"
        "SSL_CERT_FILE=/project/ca.pem\n"
        "SHARDS_AI_AGENTS_PLUS_URL=https://amp.project.test\n"
        "UV_ENV_FILE=.env\n"
    )
    env = {key: value for key, value in os.environ.items() if not plus_api._sets_transport(key)}
    env.pop("SHARDS_AI_AGENTS_PLUS_URL", None)
    env.update(machine)
    probe = (
        "import json, os, subprocess, sys\n"
        "import shards_ai_agents_cli.cli\n"
        "from shards_ai_agents_cli.experimental.eval_crew import _load_project_env\n"
        "from shards_ai_agents_core.tool_credentials import build_env_with_all_tool_credentials\n"
        "_load_project_env()\n"
        "run = subprocess.run(['uv', 'run', '--no-project', '--python', sys.executable,"
        " 'python', '-c', 'import json, shards_ai_agents;"
        " from shards_ai_agents_core import plus_api; print(json.dumps(plus_api._MACHINE_TRANSPORT_ENV))'],"
        " env=build_env_with_all_tool_credentials(), capture_output=True, text=True, check=True)\n"
        "print(json.dumps({'amp': os.environ.get('SHARDS_AI_AGENTS_PLUS_URL'),"
        " 'run_pinned': json.loads(run.stdout.strip().splitlines()[-1])}))\n"
    )

    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    seen = json.loads(result.stdout.strip().splitlines()[-1])
    # The command loaded the project's .env (so the test means something) ...
    assert seen["amp"] == "https://amp.project.test"
    # ... and the run it started pinned only what the machine set.
    assert seen["run_pinned"] == machine
