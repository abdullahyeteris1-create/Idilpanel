"""App input component entrypoint."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .base_components import AppInput as _AppInput


def build_app_input(
    label: str,
    hint_text: str = "",
    value: str = "",
    required: bool = False,
    error_text: str | None = None,
    disabled: bool = False,
    on_change: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.TextField:
    """Build a design-system aligned text input."""
    return _AppInput(
        label=label,
        hint_text=hint_text,
        value=value,
        required=required,
        error_text=error_text,
        disabled=disabled,
        on_change=on_change,
    )
