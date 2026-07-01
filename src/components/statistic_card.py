"""Reusable statistic card component for dashboard KPI blocks."""

from __future__ import annotations

import flet as ft

from theme.theme import THEME_TOKENS


def _trend_style(trend: str) -> tuple[str, str]:
    colors = THEME_TOKENS["colors"]
    normalized = trend.strip().lower()

    if normalized in {"up", "yukari"}:
        return "↑", colors["success"]
    if normalized in {"down", "asagi"}:
        return "↓", colors["danger"]
    return "→", colors.get("passive", colors["text_secondary"])


def build_statistic_card(
    icon: str,
    title: str,
    value: str,
    subtitle: str = "",
    trend: str = "flat",
) -> ft.Container:
    """Build a reusable statistic card aligned with design-system rules.

    Structure:
    icon -> title -> value -> subtitle -> trend
    """

    colors = THEME_TOKENS["colors"]
    shadows = THEME_TOKENS["shadows"]

    trend_arrow, trend_color = _trend_style(trend)

    card = ft.Container(
        height=120,
        border_radius=16,
        padding=ft.Padding(24, 16, 24, 16),
        bgcolor=colors["surface"],
        shadow=shadows["card"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        content=ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=48,
                    height=48,
                    border_radius=24,
                    bgcolor=f"{colors['primary']}1A",
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(icon, size=24, color=colors["primary"]),
                ),
                ft.Column(
                    expand=True,
                    spacing=2,
                    controls=[
                        ft.Text(title, size=18, weight=ft.FontWeight.W_500, color=colors["text_primary"]),
                        ft.Text(value, size=32, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
                        ft.Text(subtitle, size=14, color=colors["text_secondary"]),
                        ft.Row(
                            spacing=6,
                            controls=[
                                ft.Text(trend_arrow, size=14, color=trend_color, weight=ft.FontWeight.W_700),
                                ft.Text(trend.capitalize(), size=13, color=trend_color, weight=ft.FontWeight.W_600),
                            ],
                        ),
                    ],
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


def build_dashboard_statistic_card_placeholders() -> list[ft.Container]:
    """Provide the four dashboard placeholder statistic cards for layout usage."""

    return [
        build_statistic_card(ft.Icons.PERSON, "Toplam Ogrenci", "128", "+12 bu ay", "up"),
        build_statistic_card(ft.Icons.SCHOOL, "Aktif Kurs", "34", "+3 bugune gore", "up"),
        build_statistic_card(ft.Icons.CALENDAR_MONTH, "Bugunku Ders", "12", "Degisim yok", "flat"),
        build_statistic_card(ft.Icons.CHECK_CIRCLE, "Tamamlanan Ders", "46", "-2 gecen haftaya gore", "down"),
    ]
