"""App card component entrypoint."""

from __future__ import annotations

import flet as ft

from .base_components import AppCard as _AppCard


def build_app_card(
    content: ft.Control,
    title: str | None = None,
    subtitle: str | None = None,
    action: ft.Control | None = None,
) -> ft.Container:
    """Build a design-system aligned card."""
    return _AppCard(
        content=content,
        title=title,
        subtitle=subtitle,
        action=action,
    )
