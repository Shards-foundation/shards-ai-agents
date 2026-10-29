"""Provider detection utilities."""

from __future__ import annotations

from shards_ai_agents.state.provider.core import BaseProvider


_SQLITE_MAGIC = b"SQLite format 3\x00"


def detect_provider(path: str) -> BaseProvider:
    """Detect the storage provider from a checkpoint path.

    Reads the file's magic bytes to determine if it's a SQLite database.
    For paths containing ``#``, checks the portion before the ``#``.
    Falls back to JsonProvider.

    Args:
        path: A checkpoint file path, directory, or ``db_path#checkpoint_id``.

    Returns:
        The appropriate provider instance.
    """
    from shards_ai_agents.state.provider.json_provider import JsonProvider
    from shards_ai_agents.state.provider.sqlite_provider import SqliteProvider

    file_path = path.split("#")[0] if "#" in path else path
    try:
        with open(file_path, "rb") as f:
            if f.read(16) == _SQLITE_MAGIC:
                return SqliteProvider()
    except OSError:
        pass
    return JsonProvider()
