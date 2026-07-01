"""Reusable action panel component for cross-screen quick operations."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypedDict

import flet as ft

from theme.theme import THEME_TOKENS


class ActionItem(TypedDict, total=False):
    """Action configuration item for the reusable panel."""

    key: str
    title: str
    subtitle: str
    icon: str
    on_click: Callable[[ft.ControlEvent], None] | None


def _with_alpha(color: str, alpha: str = "1A") -> str:
    if len(color) == 7:
        return f"{color}{alpha}"
    return color


def _build_action_button(action: ActionItem) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    radius = THEME_TOKENS["radius"]
    shadows = THEME_TOKENS["shadows"]

    button = ft.Container(
        height=72,
        col={"xs": 12, "sm": 6, "md": 6},
        border_radius=radius["card"],
        padding=ft.Padding(12, 8, 12, 8),
        bgcolor=colors["surface"],
        shadow=shadows["card"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        on_click=action.get("on_click"),
        content=ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=32,
                    height=32,
                    border_radius=16,
                    bgcolor=_with_alpha(colors["primary"], "1F"),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(action.get("icon", ft.Icons.BOLT), size=18, color=colors["primary"]),
                ),
                ft.Column(
                    expand=True,
                    spacing=2,
                    controls=[
                        ft.Text(
                            action.get("title", "Action"),
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=colors["text_primary"],
                        ),
                        ft.Text(
                            action.get("subtitle", ""),
                            size=14,
                            color=colors["text_secondary"],
                            overflow=ft.TextOverflow.ELLIPSIS,
                            max_lines=1,
                        ),
                    ],
                ),
            ],
        ),
    )

    def _on_hover(e: ft.ControlEvent) -> None:
        button.shadow = shadows["hover"] if e.data == "true" else shadows["card"]
        if e.page:
            e.page.update()

    button.on_hover = _on_hover
    return button


def build_action_panel(
    title: str,
    subtitle: str,
    actions: list[ActionItem],
) -> ft.Container:
    """Build a reusable action panel with responsive action grid.

    Desktop/Tablet: 2-column grid.
    Mobile: 1-column stack.
    """

    colors = THEME_TOKENS["colors"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]
    shadows = THEME_TOKENS["shadows"]

    panel = ft.Container(
        border_radius=radius["panel"],
        padding=spacing["lg"],
        bgcolor=colors["surface"],
        shadow=shadows["card"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        content=ft.Column(
            spacing=spacing["md"],
            controls=[
                ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.FLASH_ON, size=22, color=colors["primary"]),
                        ft.Text(title, size=22, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                    ],
                ),
                ft.Text(subtitle, size=16, color=colors["text_secondary"]),
                ft.ResponsiveRow(
                    spacing=12,
                    run_spacing=12,
                    controls=[_build_action_button(action) for action in actions],
                ),
            ],
        ),
    )

    def _on_hover(e: ft.ControlEvent) -> None:
        panel.shadow = shadows["hover"] if e.data == "true" else shadows["card"]
        if e.page:
            e.page.update()

    panel.on_hover = _on_hover
    return panel


def build_dashboard_action_panel_placeholders() -> list[ActionItem]:
    """Provide default dashboard actions as placeholder-only config."""

    return [
        {
            "key": "new-student",
            "title": "Yeni Ogrenci",
            "subtitle": "Kayit olustur",
            "icon": ft.Icons.PERSON_ADD,
            "on_click": None,
        },
        {
            "key": "new-lesson",
            "title": "Yeni Ders",
            "subtitle": "Programa ekle",
            "icon": ft.Icons.MENU_BOOK,
            "on_click": None,
        },
        {
            "key": "new-measurement",
            "title": "Yeni Olcum",
            "subtitle": "Deger girisi yap",
            "icon": ft.Icons.STRAIGHTEN,
            "on_click": None,
        },
        {
            "key": "new-report",
            "title": "Yeni Rapor",
            "subtitle": "Rapor olustur",
            "icon": ft.Icons.DESCRIPTION,
            "on_click": None,
        },
    ]
