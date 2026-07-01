"""Settings screen v2 built from scratch."""

from __future__ import annotations

import flet as ft

from components import PageContainer, build_app_card, build_app_header, build_app_input, build_primary_button, build_secondary_button


def build_settings_page_v2() -> ft.Control:
    header = build_app_header(
        title="Ayarlar V2",
        subtitle="Yeni ayar deneyimi",
        actions=[build_secondary_button("Vazgec"), build_primary_button("Kaydet")],
    )

    profile = build_app_card(
        title="Profil",
        content=ft.Column(
            spacing=10,
            controls=[
                build_app_input("Ad Soyad", hint_text="Kullanici adi"),
                build_app_input("E-posta", hint_text="ornek@mail.com"),
            ],
        ),
    )

    preferences = build_app_card(
        title="Tercihler",
        content=ft.Column(spacing=8, controls=[ft.Checkbox(label="Bildirimleri ac"), ft.Checkbox(label="Haftalik ozet gonder")]),
    )

    body = ft.Column(spacing=24, expand=True, controls=[header, profile, preferences])
    return PageContainer(content=body, max_width=1888, padding=24)
