"""Parent reports screen v2 built from scratch."""

from __future__ import annotations

import flet as ft

from components import PageContainer, build_app_card, build_app_header, build_app_table, build_primary_button, build_secondary_button


def build_parent_reports_page_v2() -> ft.Control:
    header = build_app_header(
        title="Veli Raporlari V2",
        subtitle="Veliye gidecek raporlar",
        actions=[build_secondary_button("Onizle"), build_primary_button("Gonder")],
    )

    preview = build_app_card(
        title="Secili Rapor Onizleme",
        content=ft.Text("Ogrenci ilerleme ozeti ve ogretmen notu bu alanda gorunur."),
    )

    history = build_app_table(
        columns=["Tarih", "Ogrenci", "Kanal", "Durum"],
        rows=[
            ["2026-06-29", "Aras", "E-posta", "Gonderildi"],
            ["2026-06-28", "Mila", "WhatsApp", "Beklemede"],
        ],
    )

    body = ft.Column(spacing=24, expand=True, controls=[header, preview, history])
    return PageContainer(content=body, max_width=1888, padding=24)
