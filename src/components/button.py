"""Shared button component aligned with the Idil design system."""

from typing import Callable

import flet as ft

from theme.theme import THEME_TOKENS


BUTTON_VARIANTS = {
    "primary": "primary",
    "secondary": "secondary",
    "success": "success",
    "warning": "warning",
    "danger": "danger",
}


def _button_colors(variant: str) -> tuple[str, str]:
    colors = THEME_TOKENS["colors"]
    background = colors.get(variant, colors["primary"])
    return background, colors["surface"]


def build_button(
    label: str,
    on_click: Callable[[ft.ControlEvent], None] | None = None,
    variant: str = BUTTON_VARIANTS["primary"],
    icon: str | None = None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.ElevatedButton:
    """Create a design-system-compliant semantic button."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]["button"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    bgcolor, text_color = _button_colors(variant)

    return ft.ElevatedButton(
        content=ft.Text(value=label),
        icon=icon,
        on_click=on_click,
        disabled=disabled,
        expand=expand,
        style=ft.ButtonStyle(
            bgcolor=bgcolor,
            color=text_color,
            shape=ft.RoundedRectangleBorder(radius=radius["button"]),
            text_style=ft.TextStyle(
                size=typography["max_size"],
                weight=ft.FontWeight.W_600,
                color=text_color,
            ),
            padding=ft.Padding(
                left=spacing["md"],
                top=spacing["sm"],
                right=spacing["md"],
                bottom=spacing["sm"],
            ),
            side=ft.BorderSide(1, colors["border_neutral"]),
        ),
    )
