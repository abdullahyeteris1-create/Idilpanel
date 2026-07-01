"""Measurements screen v2 built from scratch."""

from __future__ import annotations

import flet as ft

from components import PageContainer, build_app_card, build_app_header, build_app_input, build_app_table, build_primary_button


def build_measurements_page_v2() -> ft.Control:
    header = build_app_header(
        title="Olcumler V2",
        subtitle="WPM ve anlama takibi",
        actions=[build_primary_button("Olcum Kaydet", icon=ft.Icons.SAVE)],
    )

    form = build_app_card(
        title="Yeni Olcum",
        content=ft.Column(
            spacing=10,
            controls=[
                build_app_input("Kelime Sayisi", hint_text="Orn: 180"),
                build_app_input("Sure", hint_text="Dakika"),
                build_app_input("Anlama", hint_text="0-100"),
            ],
        ),
    )

    table = build_app_table(
        columns=["Tarih", "WPM", "Anlama", "Durum"],
        rows=[
            ["2026-06-28", "132", "%81", "Iyi"],
            ["2026-06-21", "126", "%77", "Iyi"],
        ],
    )

    body = ft.Column(spacing=24, expand=True, controls=[header, form, table])
    return PageContainer(content=body, max_width=1888, padding=24)
