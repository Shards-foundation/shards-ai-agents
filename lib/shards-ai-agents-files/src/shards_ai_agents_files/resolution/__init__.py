"""File resolution logic."""

from shards_ai_agents_files.resolution.resolver import FileResolver
from shards_ai_agents_files.resolution.utils import (
    is_file_source,
    normalize_input_files,
    wrap_file_source,
)


__all__ = [
    "FileResolver",
    "is_file_source",
    "normalize_input_files",
    "wrap_file_source",
]
