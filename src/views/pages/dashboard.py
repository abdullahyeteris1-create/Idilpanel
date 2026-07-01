"""Dashboard page built with shared design system components."""

from __future__ import annotations

import flet as ft

from components import AppCard, ContentCard, PageContainer, PrimaryButton, SecondaryButton, ThreeColumnLayout
from theme.theme import THEME_TOKENS


def _kpi_card(title: str, value: str, tone: str, subtitle: str) -> ft.Control:
    colors = THEME_TOKENS["colors"]

    return AppCard(
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, size=13, color=colors["text_secondary"]),
                ft.Text(value, size=28, weight=ft.FontWeight.W_700, color=tone),
                ft.Text(subtitle, size=12, color=colors["text_secondary"]),
            ],
        )
    )


def _status_chip(text: str, bg: str, fg: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding(10, 4, 10, 4),
        border_radius=999,
        bgcolor=bg,
        content=ft.Text(text, size=12, color=fg, weight=ft.FontWeight.W_600),
    )


def build_dashboard_page() -> ft.Control:
    """Build dashboard page using the shared design system language."""
    colors = THEME_TOKENS["colors"]

    actions = ft.Row(
        spacing=8,
        controls=[
            SecondaryButton("Haftalik Program", icon=ft.Icons.CALENDAR_MONTH),
            PrimaryButton("Yeni Ogrenci", icon=ft.Icons.ADD),
        ],
    )

    header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    ft.Text("Dashboard", size=24, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
                    ft.Text("Genel durum ve ozet metrikler", size=15, color=colors["text_secondary"]),
                ],
            ),
            actions,
        ],
    )

    kpi_row = ThreeColumnLayout(
        first=_kpi_card("Toplam Ogrenci", "128", colors["primary"], "Bu ay +12 ogrenci"),
        second=_kpi_card("Aktif Ogrenci", "96", colors["success"], "Derse devam eden"),
        third=_kpi_card("Tamamlanan", "24", colors["secondary"], "Programi bitiren"),
        spacing=24,
    )

    activity_items = [
        ("Aras Alp Baglica", "5-A • 2. Kur", "Aktif"),
        ("Mila Vatan", "5-A • 2. Kur", "Aktif"),
        ("Ege Demir", "4-A • 1. Kur", "Tamamlandi"),
        ("Ceren Bora", "4-A • 1. Kur", "Pasif"),
    ]

    activity_rows: list[ft.Control] = []
    for name, sub, status in activity_items:
        if status == "Aktif":
            chip = _status_chip("Aktif", "#DCFCE7", "#166534")
        elif status == "Pasif":
            chip = _status_chip("Pasif", "#FEF3C7", "#92400E")
        else:
            chip = _status_chip("Tamamlandi", "#DBEAFE", "#1E3A8A")

        initials = "".join(part[0] for part in name.split()[:2]).upper()
        activity_rows.append(
            AppCard(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=36,
                                    height=36,
                                    border_radius=18,
                                    bgcolor=f"{colors['primary']}1F",
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.Text(initials, size=12, weight=ft.FontWeight.W_700, color=colors["primary"]),
                                ),
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(name, size=15, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                                        ft.Text(sub, size=12, color=colors["text_secondary"]),
                                    ],
                                ),
                            ],
                        ),
                        chip,
                    ],
                )
            )
        )

    right_summary = ContentCard(
        title="Haftalik Ozet",
        subtitle="Genel ilerleme durumu",
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Planlanan Ders"), ft.Text("42", weight=ft.FontWeight.W_700)]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Tamamlanan Ders"), ft.Text("31", weight=ft.FontWeight.W_700)]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Bekleyen Ders"), ft.Text("11", weight=ft.FontWeight.W_700)]),
                ft.Divider(height=1, color=colors["border"]),
                ft.Text("Hedef Tamamlama", size=13, color=colors["text_secondary"]),
                ft.ProgressBar(value=0.74, color=colors["primary"], bgcolor="#E5E7EB", height=10, border_radius=6),
                ft.Text("%74", size=16, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
            ],
        ),
    )

    # Scrollable content area (only content scrolls, not header)
    scrollable_content = ft.Column(
        spacing=24,
        controls=[
            kpi_row,
            ft.Row(
                spacing=24,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        expand=2,
                        content=ContentCard(
                            title="Son Ogrenci Hareketleri",
                            subtitle="Guncel liste ozet gorunumu",
                            content=ft.Column(spacing=12, controls=activity_rows),
                        ),
                    ),
                    ft.Container(expand=1, content=right_summary),
                ],
            ),
        ],
    )

    # Main layout: header (fixed) + scrollable content area
    body = ft.Column(
        spacing=24,
        expand=True,
        controls=[
            # Header section (does not scroll)
            header,
            # Content section (scrollable)
            ft.Container(
                expand=True,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    controls=[scrollable_content],
                ),
            ),
        ],
    )

    return PageContainer(content=body, max_width=1888, padding=24)
