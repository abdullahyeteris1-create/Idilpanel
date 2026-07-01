"""Secondary button component entrypoint."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .base_components import SecondaryButton as _SecondaryButton


def build_secondary_button(
    label: str,
    on_click: Callable[[ft.ControlEvent], None] | None = None,
    icon: str | None = None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.ElevatedButton:
    """Build a design-system aligned secondary button."""
    return _SecondaryButton(
        label=label,
        on_click=on_click,
        icon=icon,
        disabled=disabled,
        expand=expand,
    )
