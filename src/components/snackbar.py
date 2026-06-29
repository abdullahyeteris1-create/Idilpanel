"""Shared snackbar component aligned with the Idil design system."""

import flet as ft

from theme.theme import THEME_TOKENS


SNACKBAR_VARIANTS = {
    "success": "success",
    "warning": "warning",
    "danger": "danger",
    "primary": "primary",
    "secondary": "secondary",
}


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def build_snackbar(
    message: str,
    variant: str = SNACKBAR_VARIANTS["primary"],
    action_label: str | None = None,
    on_action=None,
    show_close_icon: bool = True,
) -> ft.SnackBar:
    """Create a semantic snackbar for feedback states."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]["body"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    tone = colors.get(variant, colors["primary"])

    return ft.SnackBar(
        content=ft.Text(
            value=message,
            size=typography["max_size"],
            weight=_font_weight(typography["weight"]),
            color=colors["surface"],
        ),
        bgcolor=tone,
        action=action_label,
        on_action=on_action,
        show_close_icon=show_close_icon,
        close_icon_color=colors["surface"],
        behavior=ft.SnackBarBehavior.FLOATING,
        margin=spacing["md"],
        padding=ft.Padding(
            left=spacing["md"],
            top=spacing["sm"],
            right=spacing["md"],
            bottom=spacing["sm"],
        ),
        shape=ft.RoundedRectangleBorder(radius=radius["panel"]),
    )
