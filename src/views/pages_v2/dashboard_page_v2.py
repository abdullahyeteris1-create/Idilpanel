"""Dashboard screen v2 built from scratch."""

from __future__ import annotations

import flet as ft

from components import PageContainer, build_app_card, build_app_header, build_primary_button


def build_dashboard_page_v2() -> ft.Control:
    header = build_app_header(
        title="Dashboard V2",
        subtitle="Yeni nesil ozet ekrani",
        actions=[build_primary_button("Yeni Ogrenci", icon=ft.Icons.ADD)],
    )

    kpis = ft.Row(
        spacing=16,
        controls=[
            ft.Container(expand=1, content=build_app_card(title="Toplam Ogrenci", content=ft.Text("128", size=28))),
            ft.Container(expand=1, content=build_app_card(title="Aktif Program", content=ft.Text("96", size=28))),
            ft.Container(expand=1, content=build_app_card(title="Tamamlanan", content=ft.Text("24", size=28))),
        ],
    )

    body = ft.Column(
        spacing=24,
        expand=True,
        controls=[
            header,
            kpis,
            build_app_card(title="Son Aktiviteler", content=ft.Column(spacing=6, controls=[ft.Text("Bugun 4 yeni kayit"), ft.Text("2 ders tamamlandi")]))
        ],
    )
    return PageContainer(content=body, max_width=1888, padding=24)
