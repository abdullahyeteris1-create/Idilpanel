"""App dropdown component entrypoint."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .base_components import AppDropdown as _AppDropdown


def build_app_dropdown(
    label: str,
    options: list[str] | list[tuple[str, str]],
    value: str | None = None,
    required: bool = False,
    disabled: bool = False,
    hint_text: str = "",
    error_text: str | None = None,
    on_change: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.Dropdown:
    """Build a design-system aligned dropdown input."""
    return _AppDropdown(
        label=label,
        options=options,
        value=value,
        required=required,
        disabled=disabled,
        hint_text=hint_text,
        error_text=error_text,
        on_change=on_change,
    )
