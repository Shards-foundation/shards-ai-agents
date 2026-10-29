"""Deprecated: use ``shards_ai_agents_core.printer`` instead."""

from __future__ import annotations

import warnings

from shards_ai_agents_core.printer import (
    PRINTER as PRINTER,
    ColoredText as ColoredText,
    Printer as Printer,
    PrinterColor as PrinterColor,
)


__all__ = ["PRINTER", "ColoredText", "Printer", "PrinterColor"]


warnings.warn(
    "shards_ai_agents.utilities.printer is deprecated; import from shards_ai_agents_core.printer.",
    DeprecationWarning,
    stacklevel=2,
)
