"""Reusable dashboard chart card components with placeholder chart areas."""

from __future__ import annotations

import flet as ft

from theme.theme import THEME_TOKENS


def _build_chart_placeholder(variant: str = "line") -> ft.Container:
    colors = THEME_TOKENS["colors"]

    icon_name = ft.Icons.SHOW_CHART if variant == "line" else ft.Icons.BAR_CHART

    return ft.Container(
        expand=True,
        height=150,
        border_radius=12,
        bgcolor=colors["background"],
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
                ft.Icon(icon_name, size=40, color=colors["primary"]),
                ft.Text("Chart Placeholder", size=14, color=colors["text_secondary"]),
            ],
        ),
    )


def build_chart_card(
    title: str,
    subtitle: str,
    updated_at: str,
    trend_text: str,
    description: str,
    variant: str = "line",
) -> ft.Container:
    """Build a reusable chart card with DS-compliant spacing and card styling."""

    colors = THEME_TOKENS["colors"]
    shadows = THEME_TOKENS["shadows"]

    card = ft.Container(
        height=320,
        border_radius=16,
        padding=24,
        bgcolor=colors["surface"],
        shadow=shadows["card"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        content=ft.Column(
            expand=True,
            spacing=14,
            controls=[
                ft.Text(title, size=22, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                ft.Text(subtitle, size=16, color=colors["text_secondary"]),
                _build_chart_placeholder(variant),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(f"Son guncelleme: {updated_at}", size=13, color=colors["text_secondary"]),
                        ft.Text(f"Trend: {trend_text}", size=13, color=colors["text_primary"], weight=ft.FontWeight.W_500),
                        ft.Text(description, size=13, color=colors["text_secondary"]),
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


def build_dashboard_chart_card_placeholders() -> list[ft.Container]:
    """Return the two dashboard chart cards for placeholder usage."""

    return [
        build_chart_card(
            title="Okuma Hizi Gelisimi",
            subtitle="Son 30 gun performans gorunumu",
            updated_at="Bugun 09:45",
            trend_text="Yukari yonlu",
            description="Duzene devam edilirse aylik hedefe ulasilabilir.",
            variant="line",
        ),
        build_chart_card(
            title="Anlama Orani",
            subtitle="Haftalik degerlendirme dagilimi",
            updated_at="Bugun 09:45",
            trend_text="Sabit",
            description="Son olcumde denge korunuyor.",
            variant="bar",
        ),
    ]
