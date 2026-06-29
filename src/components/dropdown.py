"""Shared dropdown component aligned with the Idil design system."""

import flet as ft

from theme.theme import THEME_TOKENS


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def build_dropdown(
    label: str,
    options: list[str],
    value: str | None = None,
    required: bool = False,
    disabled: bool = False,
    error_text: str | None = None,
    hint_text: str = "",
    on_change=None,
) -> ft.Dropdown:
    """Create a design-system-compliant dropdown field."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    body_type = typography["body"]
    small_type = typography["small"]
    resolved_label = f"{label} *" if required else label

    return ft.Dropdown(
        value=value,
        label=resolved_label,
        hint_text=hint_text,
        options=[ft.dropdown.Option(option) for option in options],
        disabled=disabled,
        on_select=on_change,
        bgcolor=colors["surface"],
        color=colors["text_primary"],
        text_size=body_type["max_size"],
        border_color=colors["border_neutral"],
        focused_border_color=colors["primary"],
        border_radius=radius["input"],
        content_padding=ft.Padding(
            left=spacing["md"],
            top=spacing["sm"],
            right=spacing["md"],
            bottom=spacing["sm"],
        ),
        label_style=ft.TextStyle(
            size=small_type["max_size"],
            weight=_font_weight(small_type["weight"]),
            color=colors["text_secondary"],
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
        error_text=error_text,
    )
