"""Reusable Today's Lessons card component for dashboard and schedule screens."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from theme.theme import THEME_TOKENS

STATUS_META = {
    "bekliyor": {"label": "Bekliyor", "color_key": "warning"},
    "devam ediyor": {"label": "Devam Ediyor", "color_key": "primary"},
    "tamamlandi": {"label": "Tamamlandi", "color_key": "success"},
    "iptal": {"label": "Iptal", "color_key": "danger"},
}


def _with_alpha(color: str, alpha: str = "1A") -> str:
    if len(color) == 7:
        return f"{color}{alpha}"
    return color


def _normalize_status(status: str) -> dict[str, str]:
    normalized = status.strip().lower()
    return STATUS_META.get(normalized, {"label": status, "color_key": "passive"})


def _build_status_badge(status: str) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    radius = THEME_TOKENS["radius"]
    typography = THEME_TOKENS["typography"]

    meta = _normalize_status(status)
    tone = colors[meta["color_key"]]

    return ft.Container(
        padding=ft.Padding(10, 4, 10, 4),
        border_radius=radius["button"],
        bgcolor=_with_alpha(tone, "1F"),
        border=ft.Border(
            top=ft.BorderSide(1, tone),
            right=ft.BorderSide(1, tone),
            bottom=ft.BorderSide(1, tone),
            left=ft.BorderSide(1, tone),
        ),
        content=ft.Text(
            meta["label"],
            size=typography["caption"]["max_size"],
            weight=ft.FontWeight.W_600,
            color=tone,
        ),
    )


def _build_lesson_row(lesson: dict[str, Any]) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    radius = THEME_TOKENS["radius"]
    typography = THEME_TOKENS["typography"]

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
            run_spacing=8,
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    col={"xs": 12, "sm": 3, "md": 2},
                    content=ft.Text(
                        str(lesson.get("time", "--:--")),
                        size=typography["body"]["max_size"],
                        weight=ft.FontWeight.W_600,
                        color=colors["text_primary"],
                    ),
                ),
                ft.Container(
                    col={"xs": 12, "sm": 6, "md": 7},
                    content=ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                str(lesson.get("student", "-")),
                                size=typography["body"]["max_size"],
                                color=colors["text_primary"],
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                str(lesson.get("course", "-")),
                                size=typography["caption"]["max_size"],
                                color=colors["text_secondary"],
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    col={"xs": 12, "sm": 3, "md": 3},
                    alignment=ft.Alignment(1, 0),
                    content=_build_status_badge(str(lesson.get("status", "Bekliyor"))),
                ),
            ],
        ),
    )

    def _on_hover(e: ft.ControlEvent) -> None:
        row.bgcolor = _with_alpha(colors["primary"], "0F") if e.data == "true" else colors["surface"]
        if e.page:
            e.page.update()

    row.on_hover = _on_hover
    return row


def _build_empty_state() -> ft.Container:
    colors = THEME_TOKENS["colors"]
    radius = THEME_TOKENS["radius"]
    typography = THEME_TOKENS["typography"]

    return ft.Container(
        height=120,
        border_radius=radius["panel"],
        bgcolor=_with_alpha(colors["primary"], "0D"),
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
                ft.Icon(ft.Icons.EVENT_BUSY, size=28, color=colors["passive"]),
                ft.Text(
                    "Bugun planlanmis ders bulunmuyor.",
                    size=typography["body"]["max_size"],
                    color=colors["text_secondary"],
                ),
            ],
        ),
    )


def build_todays_lessons_card(
    lessons: list[dict[str, Any]] | None = None,
    on_view_all: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.Container:
    """Build reusable Today's Lessons card with responsive lesson rows."""

    colors = THEME_TOKENS["colors"]
    shadows = THEME_TOKENS["shadows"]
    radius = THEME_TOKENS["radius"]
    spacing = THEME_TOKENS["spacing"]
    typography = THEME_TOKENS["typography"]

    lesson_items = lessons if lessons is not None else []

    list_content: ft.Control
    if lesson_items:
        list_content = ft.Column(
            spacing=8,
            controls=[_build_lesson_row(item) for item in lesson_items],
        )
    else:
        list_content = _build_empty_state()

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
                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=22, color=colors["primary"]),
                        ft.Text(
                            "Bugunku Dersler",
                            size=typography["h3"]["max_size"],
                            weight=ft.FontWeight.W_600,
                            color=colors["text_primary"],
                        ),
                    ],
                ),
                ft.Text(
                    f"Bugunku toplam ders sayisi: {len(lesson_items)}",
                    size=typography["body"]["max_size"],
                    color=colors["text_secondary"],
                ),
                list_content,
                ft.Container(
                    alignment=ft.Alignment(1, 0),
                    content=ft.TextButton(
                        "Tumunu Gor",
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


def build_todays_lessons_mock_data() -> list[dict[str, str]]:
    """Provide mock data for visual testing only."""

    return [
        {"time": "09:00", "student": "Ayse Kara", "course": "Hizli Okuma", "status": "Bekliyor"},
        {"time": "10:30", "student": "Mert Demir", "course": "Anlama Becerisi", "status": "Devam Ediyor"},
        {"time": "13:00", "student": "Elif Yildiz", "course": "Okuma Atolyesi", "status": "Tamamlandi"},
        {"time": "15:30", "student": "Can Arslan", "course": "Dikkat Calismasi", "status": "Iptal"},
    ]
