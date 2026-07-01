"""Weekly program screen v2 built from scratch."""

from __future__ import annotations

import flet as ft

from components import PageContainer, build_app_card, build_app_header, build_primary_button


def build_weekly_program_page_v2() -> ft.Control:
    header = build_app_header(
        title="Haftalik Program V2",
        subtitle="Slot bazli yeni gorunum",
        actions=[build_primary_button("Dersi Ac", icon=ft.Icons.OPEN_IN_NEW)],
    )

    days = ["Pzt", "Sali", "Cars", "Pers", "Cuma", "Ctesi", "Pazar"]
    day_cards = [
        ft.Container(
            width=220,
            content=build_app_card(
                title=day,
                content=ft.Column(spacing=8, controls=[ft.Text("09:00 - Bos"), ft.Text("10:00 - Dolu"), ft.Text("11:00 - Bos")]),
            ),
        )
        for day in days
    ]

    body = ft.Column(spacing=24, expand=True, controls=[header, ft.Row(scroll=ft.ScrollMode.AUTO, spacing=12, controls=day_cards)])
    return PageContainer(content=body, max_width=1888, padding=24)
