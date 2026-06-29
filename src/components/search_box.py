"""Shared search box component aligned with the Idil design system."""

import flet as ft

from theme.theme import THEME_TOKENS


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def build_search_box(
    hint_text: str = "Ara...",
    value: str = "",
    on_change=None,
    on_submit=None,
    disabled: bool = False,
) -> ft.TextField:
    """Create a search box variant based on the shared text-field rules."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    body_type = typography["body"]
    small_type = typography["small"]

    return ft.TextField(
        value=value,
        hint_text=hint_text,
        disabled=disabled,
        on_change=on_change,
        on_submit=on_submit,
        bgcolor=colors["surface"],
        color=colors["text_primary"],
        text_size=body_type["max_size"],
        border=ft.InputBorder.OUTLINE,
        border_color=colors["border_neutral"],
        focused_border_color=colors["primary"],
        border_radius=radius["input"],
        prefix_icon=ft.Icons.SEARCH,
        content_padding=ft.Padding(
            left=spacing["md"],
            top=spacing["sm"],
            right=spacing["md"],
            bottom=spacing["sm"],
        ),
        hint_style=ft.TextStyle(
            size=small_type["max_size"],
            weight=_font_weight(small_type["weight"]),
            color=colors["text_secondary"],
        ),
        text_style=ft.TextStyle(
            size=body_type["max_size"],
            weight=_font_weight(body_type["weight"]),
            color=colors["text_primary"],
        ),
    )
