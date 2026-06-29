"""Progress reports page migrated to shared design system components."""

from __future__ import annotations

import flet as ft

from components import AppCard, AppDropdown, AppInput, ContentCard, PageContainer, PrimaryButton, SecondaryButton, ThreeColumnLayout, TwoColumnLayout
from theme.theme import THEME_TOKENS


def _status_chip(status: str) -> ft.Control:
    if status == "Hazir":
        bg, fg = "#DCFCE7", "#166534"
    elif status == "Taslak":
        bg, fg = "#FEF3C7", "#92400E"
    else:
        bg, fg = "#DBEAFE", "#1E3A8A"

    return ft.Container(
        padding=ft.Padding(10, 4, 10, 4),
        border_radius=999,
        bgcolor=bg,
        content=ft.Text(status, size=12, color=fg, weight=ft.FontWeight.W_600),
    )


def _metric_card(title: str, value: str, subtitle: str) -> ft.Control:
    colors = THEME_TOKENS["colors"]
    return AppCard(
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, size=13, color=colors["text_secondary"]),
                ft.Text(value, size=28, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
                ft.Text(subtitle, size=12, color=colors["text_secondary"]),
            ],
        )
    )


def build_progress_reports_page() -> ft.Control:
    """Build progress reports page with design-system-aligned UI."""
    colors = THEME_TOKENS["colors"]

    search_field = AppInput(label="", hint_text="Rapor ara...")
    search_field.prefix_icon = ft.Icons.SEARCH
    search_field.width = 280

    period_dropdown = AppDropdown(
        label="Donem",
        options=["Bu Hafta", "Bu Ay", "Son 3 Ay"],
        value="Bu Ay",
    )
    period_dropdown.width = 180

    class_dropdown = AppDropdown(
        label="Sinif",
        options=["Tum Siniflar", "4-A", "4-B", "5-A", "5-B"],
        value="Tum Siniflar",
    )
    class_dropdown.width = 180

    header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    ft.Text("Gelisim Raporlari", size=24, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
                    ft.Text("Ogrenci ilerleme raporlarini yonetin", size=15, color=colors["text_secondary"]),
                ],
            ),
            ft.Row(
                spacing=8,
                controls=[
                    SecondaryButton("PDF Onizleme", icon=ft.Icons.PICTURE_AS_PDF),
                    PrimaryButton("Yeni Rapor", icon=ft.Icons.ADD),
                ],
            ),
        ],
    )

    filters = ContentCard(
        title="Filtreler",
        subtitle="Rapor listesini daraltin",
        content=ft.Row(
            spacing=12,
            wrap=True,
            controls=[
                search_field,
                period_dropdown,
                class_dropdown,
                SecondaryButton("Temizle", icon=ft.Icons.CLEAR),
            ],
        ),
    )

    metrics = ThreeColumnLayout(
        first=_metric_card("Toplam Rapor", "42", "Bu ay olusturulan"),
        second=_metric_card("Hazir", "27", "Paylasima hazir"),
        third=_metric_card("Taslak", "15", "Duzenlenmeyi bekleyen"),
        spacing=24,
    )

    report_rows_data = [
        ("Aras Alp Baglica", "5-A • Haftalik Rapor", "2026-06-29", "Hazir"),
        ("Mila Vatan", "5-A • Aylik Rapor", "2026-06-27", "Taslak"),
        ("Ege Demir", "4-A • Haftalik Rapor", "2026-06-25", "Gonderildi"),
        ("Ceren Bora", "4-A • Aylik Rapor", "2026-06-21", "Hazir"),
    ]

    report_rows: list[ft.Control] = []
    for student_name, meta, report_date, status in report_rows_data:
        initials = "".join(part[0] for part in student_name.split()[:2]).upper()
        report_rows.append(
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
                                        ft.Text(student_name, size=15, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                                        ft.Text(f"{meta} • {report_date}", size=12, color=colors["text_secondary"]),
                                    ],
                                ),
                            ],
                        ),
                        ft.Row(
                            spacing=8,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                _status_chip(status),
                                SecondaryButton("", icon=ft.Icons.MORE_HORIZ),
                            ],
                        ),
                    ],
                )
            )
        )

    reports_panel = ContentCard(
        title="Rapor Listesi",
        subtitle="Olusturulan tum raporlar",
        content=ft.Column(
            spacing=12,
            controls=report_rows,
        ),
    )

    summary_panel = ContentCard(
        title="Rapor Ozeti",
        subtitle="Hizli istatistikler",
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Ortalama Anlama"), ft.Text("%81", weight=ft.FontWeight.W_700)]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Ortalama WPM"), ft.Text("132", weight=ft.FontWeight.W_700)]),
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Veliye Gonderilen"), ft.Text("18", weight=ft.FontWeight.W_700)]),
                ft.Divider(height=1, color=colors["border"]),
                PrimaryButton("PDF Cikti Al", icon=ft.Icons.DOWNLOAD),
            ],
        ),
    )

    body = ft.Column(
        spacing=24,
        expand=True,
        controls=[
            header,
            filters,
            metrics,
            TwoColumnLayout(left=reports_panel, right=summary_panel, left_flex=2, right_flex=1, spacing=24),
        ],
    )

    return PageContainer(content=body, max_width=1888, padding=24)
