"""Students screen v2 built from scratch."""

from __future__ import annotations

import flet as ft

from components import (
    PageContainer,
    build_app_card,
    build_app_dropdown,
    build_app_header,
    build_app_input,
    build_primary_button,
    build_secondary_button,
)


def build_students_page_v2() -> ft.Control:
    header = build_app_header(
        title="Ogrenciler V2",
        subtitle="Yeni ekran, sifirdan tasarlandi",
        actions=[
            build_secondary_button("Disa Aktar", icon=ft.Icons.DOWNLOAD),
            build_primary_button("Yeni Ogrenci", icon=ft.Icons.ADD),
        ],
    )

    filters = build_app_card(
        title="Filtreler",
        subtitle="Listeyi daralt",
        content=ft.Row(
            spacing=12,
            wrap=True,
            controls=[
                build_app_input(label="", hint_text="Ara..."),
                build_app_dropdown(label="Sinif", options=["Tum Siniflar", "4-A", "5-A"], value="Tum Siniflar"),
                build_app_dropdown(label="Durum", options=["Tumu", "Aktif", "Pasif"], value="Tumu"),
                build_secondary_button("Temizle", icon=ft.Icons.CLEAR),
            ],
        ),
    )

    form = build_app_card(
        title="Ogrenci Formu",
        content=ft.Column(
            spacing=12,
            controls=[
                build_app_input(label="Ad Soyad", hint_text="Ogrenci adi"),
                build_app_input(label="Sinif", hint_text="Orn: 5-A"),
                build_app_input(label="Veli Adi", hint_text="Veli adi"),
                ft.Row(spacing=8, controls=[build_primary_button("Kaydet"), build_secondary_button("Temizle")]),
            ],
        ),
    )

    list_card = build_app_card(
        title="Ogrenci Listesi",
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Aras Alp Baglica"),
                ft.Text("Mila Vatan"),
                ft.Text("Ege Demir"),
                ft.Text("Ceren Bora"),
            ],
        ),
    )

    body = ft.Column(
        spacing=24,
        expand=True,
        controls=[
            header,
            filters,
            ft.Row(expand=True, spacing=24, controls=[ft.Container(expand=1, content=form), ft.Container(expand=2, content=list_card)]),
        ],
    )
    return PageContainer(content=body, max_width=1888, padding=24)
