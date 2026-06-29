"""Shared card component aligned with the Idil design system."""

import flet as ft

from theme.theme import THEME_TOKENS


def build_card(
    content: ft.Control,
    title: str | None = None,
    subtitle: str | None = None,
    action: ft.Control | None = None,
    padding_size: str = "md",
) -> ft.Container:
    """Create a card with 12 px radius and soft shadow."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]
    shadows = THEME_TOKENS["shadows"]

    header_controls: list[ft.Control] = []

    if title:
        header_controls.append(
            ft.Text(
                value=title,
                size=typography["card_title"]["max_size"],
                weight=ft.FontWeight.W_600,
                color=colors["text_primary"],
            )
        )

    if subtitle:
        header_controls.append(
            ft.Text(
                value=subtitle,
                size=typography["small"]["max_size"],
                weight=ft.FontWeight.W_400,
                color=colors["text_secondary"],
            )
        )

    if action:
        header_controls.append(action)

    column_children: list[ft.Control] = []
    if header_controls:
        column_children.append(ft.Column(controls=header_controls, spacing=spacing["xs"]))

    column_children.append(content)

    return ft.Container(
        bgcolor=colors["surface"],
        border_radius=radius["card"],
        shadow=shadows["card"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border_neutral"]),
            right=ft.BorderSide(1, colors["border_neutral"]),
            bottom=ft.BorderSide(1, colors["border_neutral"]),
            left=ft.BorderSide(1, colors["border_neutral"]),
        ),
        padding=spacing.get(padding_size, spacing["md"]),
        content=ft.Column(
            controls=column_children,
            spacing=spacing["md"],
        ),
    )
