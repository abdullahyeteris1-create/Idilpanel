"""Shared placeholder builder for empty page skeletons."""

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


def build_page_placeholder(title: str) -> ft.Control:
    """Build a consistent placeholder used by all empty page skeletons."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]

    return build_card(
        title=title,
        subtitle="Bu sayfa geliştirme aşamasındadır.",
        content=ft.Container(
            padding=spacing["xs"],
            content=ft.Text(
                value="Bu sayfa geliştirme aşamasındadır.",
                size=typography["body"]["max_size"],
                weight=_font_weight(typography["body"]["weight"]),
                color=colors["text_secondary"],
            ),
        ),
    )
