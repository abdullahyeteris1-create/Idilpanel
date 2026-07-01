"""App header component entrypoint."""

from __future__ import annotations

import flet as ft

from .layout_components import AppHeader as _AppHeader


def build_app_header(
    title: str,
    subtitle: str | None = None,
    leading: ft.Control | None = None,
    actions: list[ft.Control] | None = None,
) -> ft.Container:
    """Build a design-system aligned page header."""
    return _AppHeader(
        title=title,
        subtitle=subtitle,
        leading=leading,
        actions=actions,
    )
