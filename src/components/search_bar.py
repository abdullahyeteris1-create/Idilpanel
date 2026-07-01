"""Reusable search bar card component."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .app_card import build_app_card
from .search_box import build_search_box


def build_search_bar(
    hint_text: str,
    on_change: Callable[[ft.ControlEvent], None] | None = None,
    on_submit: Callable[[ft.ControlEvent], None] | None = None,
    title: str = "Arama",
    subtitle: str = "Liste icinde ara",
) -> ft.Container:
    """Build a shared search section backed by SearchBox component."""

    return build_app_card(
        title=title,
        subtitle=subtitle,
        content=build_search_box(
            hint_text=hint_text,
            on_change=on_change,
            on_submit=on_submit,
        ),
    )
