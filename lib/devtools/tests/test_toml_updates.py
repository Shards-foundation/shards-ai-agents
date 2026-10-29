"""Tests for TOML-based version and dependency update functions."""

from pathlib import Path
from textwrap import dedent

import pytest
from shards_ai_agents_devtools import cli as devtools_cli
from shards_ai_agents_devtools.cli import (
    _DEFAULT_WORKSPACE_PACKAGES,
    _pin_shards_ai_agents_deps,
    _repin_shards_ai_agents_install,
    _validate_deployment_repo_shards_ai_agents_pin,
    update_pyproject_dependencies,
    update_pyproject_version,
    update_template_dependencies,
)


def test_release_updates_crew_and_flow_canary_repositories(monkeypatch) -> None:
    updates = []
    monkeypatch.setattr(
        devtools_cli,
        "_update_deployment_test_repo",
        lambda repo, version, is_prerelease: updates.append(
            (repo, version, is_prerelease)
        ),
    )

    devtools_cli._update_deployment_test_repos("2.0.0a1", True)

    assert updates == [
        ("Shards-foundation/crew_deployment_test", "2.0.0a1", True),
        ("Shards-foundation/flow_deployment_test", "2.0.0a1", True),
    ]


def test_deployment_repo_validation_rejects_missing_shards_ai_agents_pin(
    tmp_path: Path,
) -> None:
    with pytest.raises(RuntimeError, match="No effective Shards-ai-agents dependency"):
        _validate_deployment_repo_shards_ai_agents_pin(
            tmp_path,
            '[project]\ndependencies = ["requests>=2"]\n',
            "2.0.0",
        )


def test_deployment_repo_validation_accepts_workflow_pin(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "test.yml").write_text(
        'run: uv pip install "shards-ai-agents[a2a]==2.0.0"\n'
    )

    _validate_deployment_repo_shards_ai_agents_pin(
        tmp_path,
        '[project]\ndependencies = ["requests>=2"]\n',
        "2.0.0",
    )


@pytest.mark.parametrize(
    "run_value",
    [
        "'uv pip install \"shards-ai-agents==2.0.0\"'",
        '"uv pip install \\"shards-ai-agents==2.0.0\\""',
    ],
)
def test_deployment_repo_validation_accepts_quoted_workflow_pin(
    tmp_path: Path,
    run_value: str,
) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "test.yml").write_text(
        f"run: {run_value}\n",
        encoding="utf-8",
    )

    _validate_deployment_repo_shards_ai_agents_pin(
        tmp_path,
        '[project]\ndependencies = ["requests>=2"]\n',
        "2.0.0",
    )


def test_deployment_repo_validation_rejects_mixed_versions(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "test.yml").write_text(
        'run: uv pip install "shards-ai-agents[a2a]==2.0.0"\n'
    )

    with pytest.raises(RuntimeError, match=r"must all pin 2\.0\.0"):
        _validate_deployment_repo_shards_ai_agents_pin(
            tmp_path,
            '[project]\ndependencies = ["shards-ai-agents==1.0.0"]\n',
            "2.0.0",
        )


def test_deployment_repo_validation_ignores_comments_and_echo(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "test.yml").write_text(
        'run: echo "shards-ai-agents==2.0.0"\n# run: pip install shards-ai-agents==2.0.0\n'
    )

    with pytest.raises(RuntimeError, match="No effective Shards-ai-agents dependency"):
        _validate_deployment_repo_shards_ai_agents_pin(
            tmp_path,
            '[project]\ndependencies = ["requests>=2"]\n',
            "2.0.0",
        )


def test_deployment_repo_validation_ignores_pyproject_comment_pin(
    tmp_path: Path,
) -> None:
    with pytest.raises(RuntimeError, match=r"must all pin 2\.0\.0"):
        _validate_deployment_repo_shards_ai_agents_pin(
            tmp_path,
            (
                "# documented pin: shards-ai-agents==2.0.0\n"
                '[project]\ndependencies = ["shards-ai-agents>=1.0"]\n'
            ),
            "2.0.0",
        )


def test_deployment_repo_validation_accepts_spaced_extras_and_marker(
    tmp_path: Path,
) -> None:
    _validate_deployment_repo_shards_ai_agents_pin(
        tmp_path,
        (
            "[project]\ndependencies = [\n"
            "  \"shards-ai-agents[tools, embeddings]==2.0.0; python_version >= '3.10'\",\n"
            "]\n"
        ),
        "2.0.0",
    )


def test_deployment_repo_validation_reads_multiline_workflow_install(
    tmp_path: Path,
) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "test.yml").write_text(
        "steps:\n"
        "  - name: Install\n"
        "    run: |\n"
        "      uv pip install \\\n"
        "        \"shards-ai-agents[tools, embeddings]==2.0.0; python_version >= '3.10'\"\n"
    )

    _validate_deployment_repo_shards_ai_agents_pin(
        tmp_path,
        '[project]\ndependencies = ["requests>=2"]\n',
        "2.0.0",
    )


def test_deployment_repo_validation_reads_install_after_comment(
    tmp_path: Path,
) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "test.yml").write_text(
        "steps:\n"
        "  - name: Install\n"
        "    run: |\n"
        "      # Install the canary dependency\n"
        '      uv pip install "shards-ai-agents==2.0.0"\n',
        encoding="utf-8",
    )

    _validate_deployment_repo_shards_ai_agents_pin(
        tmp_path,
        '[project]\ndependencies = ["requests>=2"]\n',
        "2.0.0",
    )


def test_deployment_repo_validation_reads_folded_workflow_install(
    tmp_path: Path,
) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "test.yml").write_text(
        "steps:\n"
        "  - name: Install\n"
        "    run: >\n"
        "      uv pip install\n"
        '      "shards-ai-agents==2.0.0"\n',
        encoding="utf-8",
    )

    _validate_deployment_repo_shards_ai_agents_pin(
        tmp_path,
        '[project]\ndependencies = ["requests>=2"]\n',
        "2.0.0",
    )


def test_deployment_repo_validation_skips_non_file_workflow_entries(
    tmp_path: Path,
) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ignored.yml").mkdir()
    (workflows / "test.yaml").write_text(
        '# UTF-8 workflow: déploiement\nrun: uv pip install "shards-ai-agents==2.0.0"\n',
        encoding="utf-8",
    )

    _validate_deployment_repo_shards_ai_agents_pin(
        tmp_path,
        '[project]\ndependencies = ["requests>=2"]\n',
        "2.0.0",
    )


class TestUpdatePyprojectVersion:
    def test_updates_version(self, tmp_path: Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            dedent("""\
            [project]
            name = "my-pkg"
            version = "1.0.0"
        """)
        )

        assert update_pyproject_version(pyproject, "2.0.0") is True
        assert 'version = "2.0.0"' in pyproject.read_text()

    def test_returns_false_when_already_current(self, tmp_path: Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            dedent("""\
            [project]
            name = "my-pkg"
            version = "1.0.0"
        """)
        )

        assert update_pyproject_version(pyproject, "1.0.0") is False

    def test_returns_false_when_no_project_section(self, tmp_path: Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[tool.ruff]\nline-length = 88\n")

        assert update_pyproject_version(pyproject, "1.0.0") is False

    def test_returns_false_when_version_is_dynamic(self, tmp_path: Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            dedent("""\
            [project]
            name = "my-pkg"
            dynamic = ["version"]
        """)
        )

        assert update_pyproject_version(pyproject, "1.0.0") is False
        assert 'version = "1.0.0"' not in pyproject.read_text()

    def test_returns_false_for_missing_file(self, tmp_path: Path) -> None:
        assert update_pyproject_version(tmp_path / "nope.toml", "1.0.0") is False

    def test_preserves_comments_and_formatting(self, tmp_path: Path) -> None:
        content = dedent("""\
            # This is important
            [project]
            name = "my-pkg"
            version = "1.0.0"  # current version
            description = "A package"
        """)
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(content)

        update_pyproject_version(pyproject, "2.0.0")
        result = pyproject.read_text()

        assert "# This is important" in result
        assert 'description = "A package"' in result


class TestPinShardsAgentsDeps:
    def test_pins_exact_version(self) -> None:
        content = dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents==1.0.0",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert '"shards-ai-agents==2.0.0"' in result

    def test_pins_minimum_version(self) -> None:
        content = dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents>=1.0.0",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert '"shards-ai-agents==2.0.0"' in result
        assert ">=" not in result

    def test_pins_with_tools_extra(self) -> None:
        content = dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents[tools]==1.0.0",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert '"shards-ai-agents[tools]==2.0.0"' in result

    def test_leaves_unrelated_deps_alone(self) -> None:
        content = dedent("""\
            [project]
            dependencies = [
                "requests>=2.0",
                "shards-ai-agents==1.0.0",
                "click~=8.1",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert '"requests>=2.0"' in result
        assert '"click~=8.1"' in result

    def test_handles_optional_dependencies(self) -> None:
        content = dedent("""\
            [project]
            dependencies = []

            [project.optional-dependencies]
            tools = [
                "shards-ai-agents[tools]>=1.0.0",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "3.0.0")
        assert '"shards-ai-agents[tools]==3.0.0"' in result

    def test_handles_multiple_shards_ai_agents_entries(self) -> None:
        content = dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents==1.0.0",
                "shards-ai-agents[tools]==1.0.0",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert '"shards-ai-agents==2.0.0"' in result
        assert '"shards-ai-agents[tools]==2.0.0"' in result

    def test_preserves_arbitrary_extras(self) -> None:
        content = dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents[a2a]==1.0.0",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert '"shards-ai-agents[a2a]==2.0.0"' in result

    def test_no_deps_returns_unchanged(self) -> None:
        content = dedent("""\
            [project]
            name = "empty"
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert "empty" in result

    def test_skips_shards_ai_agents_without_version_specifier(self) -> None:
        content = dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents-tools~=1.0",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert '"shards-ai-agents-tools~=1.0"' in result

    def test_skips_shards_ai_agents_extras_without_pin(self) -> None:
        content = dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents[tools]",
            ]
        """)
        result = _pin_shards_ai_agents_deps(content, "2.0.0")
        assert '"shards-ai-agents[tools]"' in result
        assert "==" not in result


class TestRepinShardsAgentsInstall:
    def test_repins_a2a_extra(self) -> None:
        result = _repin_shards_ai_agents_install(
            'uv pip install "shards-ai-agents[a2a]==1.14.0"', "2.0.0"
        )
        assert result == 'uv pip install "shards-ai-agents[a2a]==2.0.0"'

    def test_repins_tools_extra(self) -> None:
        result = _repin_shards_ai_agents_install(
            'uv pip install "shards-ai-agents[tools]==1.0.0"', "3.0.0"
        )
        assert result == 'uv pip install "shards-ai-agents[tools]==3.0.0"'

    def test_leaves_unrelated_commands_alone(self) -> None:
        cmd = "uv pip install requests"
        assert _repin_shards_ai_agents_install(cmd, "2.0.0") == cmd

    def test_handles_multiple_pins(self) -> None:
        cmd = 'pip install "shards-ai-agents[a2a]==1.0.0" "shards-ai-agents[tools]==1.0.0"'
        result = _repin_shards_ai_agents_install(cmd, "2.0.0")
        assert (
            result
            == 'pip install "shards-ai-agents[a2a]==2.0.0" "shards-ai-agents[tools]==2.0.0"'
        )

    def test_preserves_surrounding_text(self) -> None:
        cmd = (
            'echo hello && uv pip install "shards-ai-agents[a2a]==1.14.0" && echo done'
        )
        result = _repin_shards_ai_agents_install(cmd, "2.0.0")
        assert (
            result
            == 'echo hello && uv pip install "shards-ai-agents[a2a]==2.0.0" && echo done'
        )

    def test_no_version_specifier_unchanged(self) -> None:
        cmd = 'pip install "shards-ai-agents[tools]>=1.0"'
        assert _repin_shards_ai_agents_install(cmd, "2.0.0") == cmd


class TestUpdatePyprojectDependencies:
    def test_default_packages_cover_all_workspace_members(self) -> None:
        """Every workspace member must be in the default rewrite list.

        Without this, a version bump silently leaves stale pins behind for any
        workspace package missing from the list (see incident with 1.14.5a5).
        """
        import tomlkit

        workspace_root = Path(__file__).resolve().parents[3]
        root_pyproject = (workspace_root / "pyproject.toml").read_text()

        members = tomlkit.parse(root_pyproject)["tool"]["uv"]["workspace"]["members"]
        expected = {
            tomlkit.parse((workspace_root / m / "pyproject.toml").read_text())[
                "project"
            ]["name"]
            for m in members
        }

        assert expected.issubset(set(_DEFAULT_WORKSPACE_PACKAGES))

    def test_rewrites_all_workspace_pins(self, tmp_path: Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents-core==1.0.0",
                "shards-ai-agents-cli==1.0.0",
                "requests>=2.0",
            ]

            [project.optional-dependencies]
            tools = [
                "shards-ai-agents-tools==1.0.0",
            ]
            files = [
                "shards-ai-agents-files==1.0.0",
            ]
        """)
        )

        assert update_pyproject_dependencies(pyproject, "2.0.0") is True
        result = pyproject.read_text()
        assert '"shards-ai-agents-core==2.0.0"' in result
        assert '"shards-ai-agents-cli==2.0.0"' in result
        assert '"shards-ai-agents-tools==2.0.0"' in result
        assert '"shards-ai-agents-files==2.0.0"' in result
        assert '"requests>=2.0"' in result

    def test_skips_shards_ai_agents_files_in_file_processing_extra(
        self, tmp_path: Path
    ) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            dedent("""\
            [project.optional-dependencies]
            file-processing = [
                "shards-ai-agents-files==1.0.0",
            ]
            other = [
                "shards-ai-agents-files==1.0.0",
            ]
        """)
        )

        update_pyproject_dependencies(pyproject, "2.0.0")
        result = pyproject.read_text()
        assert '"shards-ai-agents-files==1.0.0"' in result
        assert '"shards-ai-agents-files==2.0.0"' in result

    def test_leaves_bare_shards_ai_agents_pin_alone(self, tmp_path: Path) -> None:
        """`shards_ai_agents==` must not collide with `shards-ai-agents-core==` etc."""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            dedent("""\
            [project]
            dependencies = [
                "shards-ai-agents==1.0.0",
                "shards-ai-agents-core==1.0.0",
            ]
        """)
        )

        update_pyproject_dependencies(pyproject, "2.0.0")
        result = pyproject.read_text()
        assert '"shards-ai-agents==2.0.0"' in result
        assert '"shards-ai-agents-core==2.0.0"' in result


class TestUpdateTemplateDependencies:
    def test_updates_jinja_template(self, tmp_path: Path) -> None:
        """Template pyproject.toml files with Jinja placeholders should not break."""
        tpl = tmp_path / "crew" / "pyproject.toml"
        tpl.parent.mkdir()
        tpl.write_text(
            dedent("""\
            [project]
            name = "{{folder_name}}"
            version = "0.1.0"
            dependencies = [
                "shards-ai-agents[tools]==1.14.0"
            ]

            [project.scripts]
            {{folder_name}} = "{{folder_name}}.main:run"
        """)
        )

        updated = update_template_dependencies(tmp_path, "2.0.0")

        assert len(updated) == 1
        content = tpl.read_text()
        assert '"shards-ai-agents[tools]==2.0.0"' in content
        assert "{{folder_name}}" in content

    def test_updates_bare_shards_ai_agents(self, tmp_path: Path) -> None:
        tpl = tmp_path / "pyproject.toml"
        tpl.write_text('dependencies = [\n    "shards-ai-agents==1.0.0"\n]\n')

        updated = update_template_dependencies(tmp_path, "3.0.0")

        assert len(updated) == 1
        assert '"shards-ai-agents==3.0.0"' in tpl.read_text()

    def test_skips_unrelated_deps(self, tmp_path: Path) -> None:
        tpl = tmp_path / "pyproject.toml"
        tpl.write_text('dependencies = [\n    "requests>=2.0"\n]\n')

        updated = update_template_dependencies(tmp_path, "2.0.0")

        assert len(updated) == 0
        assert '"requests>=2.0"' in tpl.read_text()
