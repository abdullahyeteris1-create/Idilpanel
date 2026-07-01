"""App sidebar component entrypoint."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .layout_components import AppSidebar as _AppSidebar


def build_app_sidebar(
    brand_title: str = "Idil Panel",
    brand_subtitle: str = "Yonetim",
    items: list[tuple[str, str, Callable[[ft.ControlEvent], None] | None]] | None = None,
    footer: ft.Control | None = None,
    width: int = 280,
) -> ft.Container:
    """Build a design-system aligned sidebar."""
    return _AppSidebar(
        brand_title=brand_title,
        brand_subtitle=brand_subtitle,
        items=items,
        footer=footer,
        width=width,
    )
