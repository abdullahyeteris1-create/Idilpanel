"""Shared badge component aligned with the Idil design system."""

import flet as ft

from theme.theme import THEME_TOKENS


BADGE_VARIANTS = {
    "primary": "primary",
    "secondary": "secondary",
    "success": "success",
    "passive": "passive",
    "completed": "purple",
    "warning": "warning",
    "danger": "danger",
    "purple": "purple",
}


def _with_alpha(color: str, alpha: str = "1F") -> str:
    if len(color) == 7:
        return f"{color}{alpha}"
    return color


def build_badge(
    text: str,
    variant: str = BADGE_VARIANTS["secondary"],
    icon: str | None = None,
) -> ft.Container:
    """Create a compact semantic badge for statuses and labels."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]["small"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    tone = colors.get(variant, colors["secondary"])

    label = ft.Row(
        controls=[
            ft.Icon(icon=icon, size=16, color=tone) if icon else ft.Container(),
            ft.Text(
                value=text,
                size=typography["max_size"],
                weight=ft.FontWeight.W_400,
                color=tone,
            ),
        ],
        tight=True,
        spacing=spacing["xs"],
    )

    if not icon:
        label.controls = [label.controls[1]]

    return ft.Container(
        bgcolor=_with_alpha(tone),
        border=ft.Border(
            top=ft.BorderSide(1, tone),
            right=ft.BorderSide(1, tone),
            bottom=ft.BorderSide(1, tone),
            left=ft.BorderSide(1, tone),
        ),
        border_radius=radius["button"],
        padding=ft.Padding(
            left=spacing["sm"],
            top=spacing["xs"],
            right=spacing["sm"],
            bottom=spacing["xs"],
        ),
        content=label,
    )
