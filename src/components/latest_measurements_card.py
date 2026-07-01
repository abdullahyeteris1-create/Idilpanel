"""Reusable Latest Measurements card component for dashboard and report screens."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from theme.theme import THEME_TOKENS


def _with_alpha(color: str, alpha: str = "1A") -> str:
    if len(color) == 7:
        return f"{color}{alpha}"
    return color


def _speed_trend_meta(trend: str) -> tuple[str, str]:
    colors = THEME_TOKENS["colors"]
    normalized = trend.strip().lower()

    if normalized in {"up", "artis", "yukari"}:
        return "↑", colors["success"]
    if normalized in {"down", "azalis", "asagi"}:
        return "↓", colors["danger"]
    return "→", colors["passive"]


def _understanding_color(score: int) -> str:
    colors = THEME_TOKENS["colors"]
    if 90 <= score <= 100:
        return colors["success"]
    if 75 <= score <= 89:
        return colors["primary"]
    if 60 <= score <= 74:
        return colors["warning"]
    return colors["danger"]


def _build_table_header() -> ft.Container:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    radius = THEME_TOKENS["radius"]

    return ft.Container(
        height=44,
        border_radius=radius["input"],
        bgcolor=_with_alpha(colors["background"], "FF"),
        padding=ft.Padding(12, 8, 12, 8),
        content=ft.ResponsiveRow(
            spacing=8,
            run_spacing=4,
            controls=[
                ft.Container(
                    col={"xs": 6, "sm": 3, "md": 3},
                    content=ft.Text("Tarih", size=13, weight=ft.FontWeight.W_600, color=colors["text_secondary"]),
                ),
                ft.Container(
                    col={"xs": 6, "sm": 4, "md": 4},
                    content=ft.Text("Ogrenci", size=13, weight=ft.FontWeight.W_600, color=colors["text_secondary"]),
                ),
                ft.Container(
                    col={"xs": 6, "sm": 2, "md": 2},
                    content=ft.Text("Hiz", size=13, weight=ft.FontWeight.W_600, color=colors["text_secondary"]),
                ),
                ft.Container(
                    col={"xs": 6, "sm": 3, "md": 3},
                    content=ft.Text("Anlama", size=13, weight=ft.FontWeight.W_600, color=colors["text_secondary"]),
                ),
            ],
        ),
    )


def _build_measurement_row(item: dict[str, Any]) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    radius = THEME_TOKENS["radius"]

    speed_value = str(item.get("speed", "0"))
    trend_arrow, trend_color = _speed_trend_meta(str(item.get("speed_trend", "flat")))

    understanding_score = int(item.get("understanding", 0))
    understanding_tone = _understanding_color(understanding_score)

    row = ft.Container(
        height=56,
        border_radius=radius["input"],
        padding=ft.Padding(12, 8, 12, 8),
        bgcolor=colors["surface"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        content=ft.ResponsiveRow(
            spacing=8,
            run_spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    col={"xs": 6, "sm": 3, "md": 3},
                    content=ft.Text(
                        str(item.get("date", "-")),
                        size=typography["caption"]["max_size"],
                        color=colors["text_primary"],
                        weight=ft.FontWeight.W_500,
                    ),
                ),
                ft.Container(
                    col={"xs": 6, "sm": 4, "md": 4},
                    content=ft.Text(
                        str(item.get("student", "-")),
                        size=typography["body"]["max_size"],
                        color=colors["text_primary"],
                    ),
                ),
                ft.Container(
                    col={"xs": 6, "sm": 2, "md": 2},
                    content=ft.Row(
                        spacing=4,
                        controls=[
                            ft.Text(speed_value, size=14, color=colors["text_primary"], weight=ft.FontWeight.W_600),
                            ft.Text(trend_arrow, size=14, color=trend_color, weight=ft.FontWeight.W_700),
                        ],
                    ),
                ),
                ft.Container(
                    col={"xs": 6, "sm": 3, "md": 3},
                    alignment=ft.Alignment(1, 0),
                    content=ft.Container(
                        padding=ft.Padding(8, 3, 8, 3),
                        border_radius=radius["button"],
                        bgcolor=_with_alpha(understanding_tone, "1F"),
                        border=ft.Border(
                            top=ft.BorderSide(1, understanding_tone),
                            right=ft.BorderSide(1, understanding_tone),
                            bottom=ft.BorderSide(1, understanding_tone),
                            left=ft.BorderSide(1, understanding_tone),
                        ),
                        content=ft.Text(
                            f"%{understanding_score}",
                            size=13,
                            color=understanding_tone,
                            weight=ft.FontWeight.W_600,
                        ),
                    ),
                ),
            ],
        ),
    )

    def _on_hover(e: ft.ControlEvent) -> None:
        row.bgcolor = colors["background"] if e.data == "true" else colors["surface"]
        if e.page:
            e.page.update()

    row.on_hover = _on_hover
    return row


def _build_empty_state() -> ft.Container:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    radius = THEME_TOKENS["radius"]

    return ft.Container(
        height=120,
        border_radius=radius["panel"],
        bgcolor=_with_alpha(colors["passive"], "12"),
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.STRAIGHTEN, size=28, color=colors["passive"]),
                ft.Text(
                    "Henuz olcum kaydi bulunmuyor.",
                    size=typography["body"]["max_size"],
                    color=colors["text_secondary"],
                ),
            ],
        ),
    )


def build_latest_measurements_card(
    measurements: list[dict[str, Any]] | None = None,
    on_view_all: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.Container:
    """Build reusable latest measurements card with modern table-like rows."""

    colors = THEME_TOKENS["colors"]
    shadows = THEME_TOKENS["shadows"]
    radius = THEME_TOKENS["radius"]
    spacing = THEME_TOKENS["spacing"]
    typography = THEME_TOKENS["typography"]

    items = measurements if measurements is not None else []

    body_content: ft.Control
    if items:
        body_content = ft.Column(
            spacing=8,
            controls=[_build_table_header()] + [_build_measurement_row(item) for item in items],
        )
    else:
        body_content = _build_empty_state()

    card = ft.Container(
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
                        ft.Icon(ft.Icons.STRAIGHTEN, size=22, color=colors["primary"]),
                        ft.Text(
                            "Son Olcumler",
                            size=typography["h3"]["max_size"],
                            weight=ft.FontWeight.W_600,
                            color=colors["text_primary"],
                        ),
                    ],
                ),
                ft.Text(
                    "Son yapilan olcumler",
                    size=typography["body"]["max_size"],
                    color=colors["text_secondary"],
                ),
                body_content,
                ft.Container(
                    alignment=ft.Alignment(1, 0),
                    content=ft.TextButton(
                        "Tum Olcumleri Gor",
                        icon=ft.Icons.ARROW_FORWARD,
                        on_click=on_view_all,
                        style=ft.ButtonStyle(
                            color=colors["primary"],
                            overlay_color={ft.ControlState.HOVERED: _with_alpha(colors["primary"], "1A")},
                        ),
                    ),
                ),
            ],
        ),
    )

    def _on_hover(e: ft.ControlEvent) -> None:
        card.shadow = shadows["hover"] if e.data == "true" else shadows["card"]
        if e.page:
            e.page.update()

    card.on_hover = _on_hover
    return card


def build_latest_measurements_mock_data() -> list[dict[str, Any]]:
    """Provide mock measurement rows for visual testing only."""

    return [
        {
            "date": "30.06.2026",
            "student": "Ayse Kara",
            "speed": "156",
            "speed_trend": "up",
            "understanding": 92,
        },
        {
            "date": "30.06.2026",
            "student": "Mert Demir",
            "speed": "141",
            "speed_trend": "flat",
            "understanding": 81,
        },
        {
            "date": "29.06.2026",
            "student": "Elif Yildiz",
            "speed": "128",
            "speed_trend": "down",
            "understanding": 68,
        },
        {
            "date": "29.06.2026",
            "student": "Can Arslan",
            "speed": "118",
            "speed_trend": "down",
            "understanding": 57,
        },
    ]
