"""Reusable Upcoming Lessons card component for dashboard and weekly schedule usage."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from theme.theme import THEME_TOKENS


def _with_alpha(color: str, alpha: str = "1A") -> str:
    if len(color) == 7:
        return f"{color}{alpha}"
    return color


def _remaining_tone(remaining: str) -> tuple[str, str]:
    colors = THEME_TOKENS["colors"]
    normalized = remaining.strip().lower()

    if normalized == "yarin":
        return colors["passive"], "Yarin"

    if "dk" in normalized:
        amount_str = "".join(ch for ch in normalized if ch.isdigit())
        if amount_str:
            minutes = int(amount_str)
            if minutes <= 15:
                return colors["warning"], remaining
            return colors["secondary"], remaining

    if "saat" in normalized:
        return colors["secondary"], remaining

    return colors["passive"], remaining


def _build_remaining_badge(remaining: str) -> ft.Container:
    radius = THEME_TOKENS["radius"]
    typography = THEME_TOKENS["typography"]

    tone, text = _remaining_tone(remaining)

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
            text,
            size=typography["caption"]["max_size"],
            weight=ft.FontWeight.W_600,
            color=tone,
        ),
    )


def _build_upcoming_row(lesson: dict[str, Any]) -> ft.Container:
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
                    content=_build_remaining_badge(str(lesson.get("remaining", "-"))),
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
        bgcolor=_with_alpha(colors["secondary"], "0D"),
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
                ft.Icon(ft.Icons.SCHEDULE, size=28, color=colors["passive"]),
                ft.Text(
                    "Planlanmis yaklasan ders bulunmuyor.",
                    size=typography["body"]["max_size"],
                    color=colors["text_secondary"],
                ),
            ],
        ),
    )


def build_upcoming_lessons_card(
    lessons: list[dict[str, Any]] | None = None,
    on_view_schedule: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.Container:
    """Build reusable Upcoming Lessons card with responsive lesson rows."""

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
            controls=[_build_upcoming_row(item) for item in lesson_items],
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
                        ft.Icon(ft.Icons.ACCESS_TIME, size=22, color=colors["primary"]),
                        ft.Text(
                            "Yaklasan Dersler",
                            size=typography["h3"]["max_size"],
                            weight=ft.FontWeight.W_600,
                            color=colors["text_primary"],
                        ),
                    ],
                ),
                ft.Text(
                    "Bugun baslayacak siradaki dersler",
                    size=typography["body"]["max_size"],
                    color=colors["text_secondary"],
                ),
                list_content,
                ft.Container(
                    alignment=ft.Alignment(1, 0),
                    content=ft.TextButton(
                        "Tum Programi Gor",
                        icon=ft.Icons.ARROW_FORWARD,
                        on_click=on_view_schedule,
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


def build_upcoming_lessons_mock_data() -> list[dict[str, str]]:
    """Provide mock upcoming lesson data for visual testing only."""

    return [
        {"time": "11:00", "student": "Deniz Kaya", "course": "Okuma Stratejisi", "remaining": "5 dk"},
        {"time": "12:30", "student": "Ece Aksoy", "course": "Anlama Pratigi", "remaining": "15 dk"},
        {"time": "14:00", "student": "Ali Can", "course": "Hizli Okuma", "remaining": "30 dk"},
        {"time": "16:00", "student": "Zeynep Aras", "course": "Odak Calismasi", "remaining": "1 Saat"},
        {"time": "Yarin", "student": "Mina Yalcin", "course": "Kelime Gelisimi", "remaining": "Yarin"},
    ]
