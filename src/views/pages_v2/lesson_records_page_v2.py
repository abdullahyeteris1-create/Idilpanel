"""Lesson records screen v2 built from scratch."""

from __future__ import annotations

import flet as ft

from components import (
    PageContainer,
    build_app_card,
    build_app_datepicker,
    build_app_dropdown,
    build_app_header,
    build_app_input,
    build_primary_button,
    build_secondary_button,
)


def build_lesson_records_page_v2() -> ft.Control:
    header = build_app_header(title="Ders Kayitlari V2", subtitle="Yeni CRUD yerlesimi")

    form = build_app_card(
        title="Ders Formu",
        content=ft.Column(
            spacing=12,
            controls=[
                build_app_dropdown("Ogrenci", options=["Aras", "Mila", "Ege"]),
                build_app_dropdown("Kurs", options=["Kur 1", "Kur 2"]),
                build_app_datepicker("Tarih"),
                build_app_input("Metin", hint_text="Ders metni"),
                ft.Row(spacing=8, controls=[build_primary_button("Kaydet"), build_secondary_button("Sil")]),
            ],
        ),
    )

    list_card = build_app_card(title="Kayitlar", content=ft.Column(spacing=6, controls=[ft.Text("Kur 1 - Ders 3"), ft.Text("Kur 2 - Ders 1")]))

    body = ft.Column(
        spacing=24,
        expand=True,
        controls=[header, ft.Row(expand=True, spacing=24, controls=[ft.Container(expand=1, content=form), ft.Container(expand=2, content=list_card)])],
    )
    return PageContainer(content=body, max_width=1888, padding=24)
