"""Progress reports screen v2 built from scratch."""

from __future__ import annotations

import flet as ft

from components import PageContainer, build_app_card, build_app_dropdown, build_app_header, build_app_input, build_primary_button, build_secondary_button


def build_progress_reports_page_v2() -> ft.Control:
    header = build_app_header(
        title="Gelisim Raporlari V2",
        subtitle="Rapor merkezi",
        actions=[build_secondary_button("PDF Onizleme"), build_primary_button("Yeni Rapor")],
    )

    filters = build_app_card(
        title="Filtreler",
        content=ft.Row(
            spacing=12,
            wrap=True,
            controls=[
                build_app_input(label="", hint_text="Rapor ara..."),
                build_app_dropdown(label="Donem", options=["Bu Hafta", "Bu Ay"], value="Bu Ay"),
                build_app_dropdown(label="Sinif", options=["Tum Siniflar", "4-A", "5-A"], value="Tum Siniflar"),
            ],
        ),
    )

    reports = build_app_card(
        title="Rapor Listesi",
        content=ft.Column(spacing=8, controls=[ft.Text("Aras - Haftalik"), ft.Text("Mila - Aylik"), ft.Text("Ege - Haftalik")]),
    )

    body = ft.Column(spacing=24, expand=True, controls=[header, filters, reports])
    return PageContainer(content=body, max_width=1888, padding=24)
