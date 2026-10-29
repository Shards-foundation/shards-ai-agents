"""Deprecated: use ``shards_ai_agents_cli`` instead.

The CLI was extracted into the standalone ``shards-ai-agents-cli`` package. Legacy
``from shards_ai_agents.cli.X import Y`` imports are intercepted here and resolved to
the corresponding ``shards_ai_agents_cli.X`` module so downstream code keeps working.
"""

from __future__ import annotations

from collections.abc import Sequence
import importlib
import importlib.abc
import importlib.machinery
import sys
from types import ModuleType
import warnings


_PREFIX = "shards_ai_agents.cli"
_TARGET = "shards_ai_agents_cli"


warnings.warn(
    "shards_ai_agents.cli is deprecated; import from shards_ai_agents_cli instead.",
    DeprecationWarning,
    stacklevel=2,
)


class _ShimLoader(importlib.abc.Loader):
    """Returns an already-imported ``shards_ai_agents_cli`` submodule without re-executing it."""

    def __init__(self, target_name: str) -> None:
        self._target_name = target_name

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> ModuleType:
        return importlib.import_module(self._target_name)

    def exec_module(self, module: ModuleType) -> None:
        return None


class _ShimFinder(importlib.abc.MetaPathFinder):
    """Maps ``shards_ai_agents.cli[.X]`` imports onto ``shards_ai_agents_cli[.X]``."""

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: ModuleType | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        if fullname != _PREFIX and not fullname.startswith(_PREFIX + "."):
            return None

        mapped = _TARGET + fullname[len(_PREFIX) :]
        try:
            module = importlib.import_module(mapped)
        except ImportError:
            return None

        spec = importlib.machinery.ModuleSpec(
            name=fullname,
            loader=_ShimLoader(mapped),
            origin=getattr(module, "__file__", None),
            is_package=hasattr(module, "__path__"),
        )
        if hasattr(module, "__path__"):
            spec.submodule_search_locations = []
        return spec


_finder = _ShimFinder()
if _finder not in sys.meta_path:
    sys.meta_path.insert(0, _finder)
