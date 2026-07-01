"""Primary button component entrypoint."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .base_components import PrimaryButton as _PrimaryButton


def build_primary_button(
    label: str,
    on_click: Callable[[ft.ControlEvent], None] | None = None,
    icon: str | None = None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.ElevatedButton:
    """Build a design-system aligned primary button."""
    return _PrimaryButton(
        label=label,
        on_click=on_click,
        icon=icon,
        disabled=disabled,
        expand=expand,
    )
