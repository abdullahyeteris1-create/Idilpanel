"""App date picker component entrypoint."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .base_components import AppDatePicker as _AppDatePicker


def build_app_datepicker(
    label: str,
    hint_text: str = "YYYY-MM-DD",
    value: str = "",
    required: bool = False,
    on_date_change: Callable[[str], None] | None = None,
) -> ft.Control:
    """Build a design-system aligned date picker."""
    return _AppDatePicker(
        label=label,
        hint_text=hint_text,
        value=value,
        required=required,
        on_date_change=on_date_change,
    )
