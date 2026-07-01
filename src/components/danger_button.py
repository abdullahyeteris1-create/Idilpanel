"""Danger button component entrypoint."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .button import BUTTON_VARIANTS, build_button


def build_danger_button(
    label: str,
    on_click: Callable[[ft.ControlEvent], None] | None = None,
    icon: str | None = None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.ElevatedButton:
    """Build a semantic danger action button."""
    return build_button(
        label=label,
        on_click=on_click,
        variant=BUTTON_VARIANTS["danger"],
        icon=icon,
        disabled=disabled,
        expand=expand,
    )
