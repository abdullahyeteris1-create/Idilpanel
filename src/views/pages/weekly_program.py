"""Weekly program page skeleton."""

import flet as ft

from components.card import build_card
from theme.theme import THEME_TOKENS


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def _build_slot() -> ft.Container:
    colors = THEME_TOKENS["colors"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]
    typography = THEME_TOKENS["typography"]

    return ft.Container(
        bgcolor=colors["background"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border_neutral"]),
            right=ft.BorderSide(1, colors["border_neutral"]),
            bottom=ft.BorderSide(1, colors["border_neutral"]),
            left=ft.BorderSide(1, colors["border_neutral"]),
        ),
        border_radius=radius["input"],
        padding=spacing["sm"],
        content=ft.Row(
            controls=[
                ft.Text(
                    value="+",
                    size=typography["subtitle"]["min_size"],
                    weight=_font_weight(typography["subtitle"]["weight"]),
                    color=colors["text_secondary"],
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


def _build_day_column(day_name: str) -> ft.Container:
    spacing = THEME_TOKENS["spacing"]

    return ft.Container(
        expand=True,
        content=build_card(
            title=day_name,
            content=ft.Column(
                controls=[_build_slot() for _ in range(9)],
                spacing=spacing["xs"],
            ),
            padding_size="sm",
        ),
    )


def _build_schedule_grid() -> ft.Control:
    spacing = THEME_TOKENS["spacing"]

    day_names = [
        "Pazartesi",
        "Sali",
        "Carsamba",
        "Persembe",
        "Cuma",
        "Cumartesi",
        "Pazar",
    ]

    return build_card(
        title="Haftalik Program",
        subtitle="7 gun ve her gun icin 9 statik ders slotu",
        content=ft.Row(
            controls=[_build_day_column(day_name) for day_name in day_names],
            spacing=spacing["sm"],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )


def _build_detail_panel() -> ft.Control:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]

    return build_card(
        title="Detay Paneli",
        subtitle="Secilen slot detaylari bu alanda gosterilecektir.",
        content=ft.Text(
            value="Bu sayfa gelistirme asamasindadir.",
            size=typography["body"]["max_size"],
            weight=_font_weight(typography["body"]["weight"]),
            color=colors["text_secondary"],
        ),
    )


def _build_summary_card(title: str, value: str) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]

    return ft.Container(
        expand=True,
        content=build_card(
            title=title,
            content=ft.Text(
                value=value,
                size=typography["card_title"]["max_size"],
                weight=_font_weight(typography["card_title"]["weight"]),
                color=colors["text_primary"],
            ),
        ),
    )


def build_weekly_program_page() -> ft.Control:
    """Build static weekly-program skeleton content without business logic."""
    spacing = THEME_TOKENS["spacing"]

    top_section = ft.Row(
        controls=[
            ft.Container(expand=4, content=_build_schedule_grid()),
            ft.Container(expand=2, content=_build_detail_panel()),
        ],
        spacing=spacing["md"],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    summary_section = ft.Row(
        controls=[
            _build_summary_card("Toplam Ders", "0"),
            _build_summary_card("Bos Saat", "0"),
            _build_summary_card("Haftalik Sure", "0 dk"),
        ],
        spacing=spacing["md"],
    )

    return ft.Column(
        controls=[top_section, summary_section],
        spacing=spacing["md"],
        expand=True,
    )
