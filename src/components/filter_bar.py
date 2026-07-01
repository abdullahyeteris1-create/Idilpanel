"""Reusable filter bar component for page-level filtering."""

from __future__ import annotations

import flet as ft

from .app_card import build_app_card


def build_filter_bar(
    filters: list[ft.Control],
    title: str = "Filtreler",
    subtitle: str = "Listeyi filtreleyin",
) -> ft.Container:
    """Build a shared filter bar with responsive filter controls."""
    return build_app_card(
        title=title,
        subtitle=subtitle,
        content=ft.ResponsiveRow(
            controls=filters,
            spacing=12,
            run_spacing=12,
        ),
    )
