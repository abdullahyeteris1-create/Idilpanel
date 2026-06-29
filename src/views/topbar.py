"""Shared topbar shell aligned with the design system."""

import flet as ft

from components.badge import build_badge
from components.button import build_button
from components.search_box import build_search_box
from theme.theme import THEME_TOKENS


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def build_topbar(title: str) -> ft.Container:
    """Build the shared topbar used by all pages."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]

    return ft.Container(
        bgcolor=colors["surface"],
        border=ft.Border(bottom=ft.BorderSide(1, colors["border_neutral"])),
        padding=ft.Padding(
            left=spacing["lg"],
            top=spacing["sm"],
            right=spacing["lg"],
            bottom=spacing["sm"],
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value=title,
                    size=typography["subtitle"]["max_size"],
                    weight=_font_weight(typography["subtitle"]["weight"]),
                    color=colors["text_primary"],
                ),
                ft.Row(
                    spacing=spacing["md"],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(width=spacing["xxxl"] * 4, content=build_search_box()),
                        build_badge(text="Online", variant="success"),
                        build_button(label="New", variant="primary"),
                    ],
                ),
            ],
        ),
    )
