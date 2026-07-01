"""Reusable table card component based on AppTable."""

from __future__ import annotations

import flet as ft

from .app_card import build_app_card
from .app_table import build_app_table


def build_table_card(
    columns: list[str],
    rows: list[list[str | ft.Control]],
    title: str = "Tablo",
    subtitle: str = "Kayit listesi",
    footer: ft.Control | None = None,
) -> ft.Container:
    """Build a shared table card with optional footer controls."""

    controls: list[ft.Control] = [build_app_table(columns=columns, rows=rows)]
    if footer is not None:
        controls.append(footer)

    return build_app_card(
        title=title,
        subtitle=subtitle,
        content=ft.Column(controls=controls, spacing=10),
    )
