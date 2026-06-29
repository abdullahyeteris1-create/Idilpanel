"""Shared layout components aligned with the Idil design system."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from theme.theme import THEME_TOKENS


def _font_weight(token_weight: int) -> ft.FontWeight:
    weight_map = {
        400: ft.FontWeight.W_400,
        600: ft.FontWeight.W_600,
        700: ft.FontWeight.W_700,
    }
    return weight_map.get(token_weight, ft.FontWeight.W_400)


def AppHeader(
    title: str,
    subtitle: str | None = None,
    leading: ft.Control | None = None,
    actions: list[ft.Control] | None = None,
) -> ft.Container:
    """Top-level page header with optional subtitle and action area."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]

    header_left_controls: list[ft.Control] = []
    if leading is not None:
        header_left_controls.append(leading)

    text_controls: list[ft.Control] = [
        ft.Text(
            value=title,
            size=typography["h1"]["max_size"],
            weight=_font_weight(typography["h1"]["weight"]),
            color=colors["text_primary"],
        )
    ]
    if subtitle:
        text_controls.append(
            ft.Text(
                value=subtitle,
                size=typography["body"]["max_size"],
                weight=_font_weight(typography["body"]["weight"]),
                color=colors["text_secondary"],
            )
        )

    header_left_controls.append(ft.Column(controls=text_controls, spacing=spacing["4"]))

    right_controls = actions or []

    return ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(spacing=spacing["12"], controls=header_left_controls),
                ft.Row(spacing=spacing["8"], controls=right_controls),
            ],
        )
    )


def AppSidebar(
    brand_title: str = "Idil Panel",
    brand_subtitle: str = "Yonetim",
    items: list[tuple[str, str, Callable[[ft.ControlEvent], None] | None]] | None = None,
    footer: ft.Control | None = None,
    width: int = 280,
) -> ft.Container:
    """Vertical application sidebar with brand area and menu items."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]
    shadows = THEME_TOKENS["shadows"]

    menu_items = items or []
    menu_controls: list[ft.Control] = []
    for label, icon, on_click in menu_items:
        menu_controls.append(
            ft.TextButton(
                on_click=on_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=radius["10"]),
                    overlay_color=f"{colors['primary']}14",
                    padding=ft.Padding(spacing["12"], spacing["8"], spacing["12"], spacing["8"]),
                ),
                content=ft.Row(
                    spacing=spacing["12"],
                    controls=[
                        ft.Icon(icon, size=20, color=colors["text_secondary"]),
                        ft.Text(
                            value=label,
                            size=typography["body"]["max_size"],
                            weight=_font_weight(typography["body"]["weight"]),
                            color=colors["text_primary"],
                        ),
                    ],
                ),
            )
        )

    sidebar_body_controls: list[ft.Control] = [
        ft.Container(
            content=ft.Column(
                spacing=spacing["4"],
                controls=[
                    ft.Text(
                        value=brand_title,
                        size=typography["h2"]["max_size"],
                        weight=_font_weight(typography["h2"]["weight"]),
                        color=colors["text_primary"],
                    ),
                    ft.Text(
                        value=brand_subtitle,
                        size=typography["caption"]["max_size"],
                        weight=_font_weight(typography["caption"]["weight"]),
                        color=colors["text_secondary"],
                    ),
                ],
            )
        ),
        ft.Divider(height=1, color=colors["border"]),
        ft.Column(spacing=spacing["8"], controls=menu_controls, expand=True),
    ]

    if footer is not None:
        sidebar_body_controls.append(ft.Divider(height=1, color=colors["border"]))
        sidebar_body_controls.append(footer)

    return ft.Container(
        width=width,
        bgcolor=colors["surface"],
        border_radius=radius["16"],
        shadow=shadows["card"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        padding=spacing["24"],
        content=ft.Column(
            spacing=spacing["16"],
            controls=sidebar_body_controls,
            expand=True,
        ),
    )


def PageContainer(
    content: ft.Control,
    max_width: int = 1440,
    padding: int | None = None,
) -> ft.Container:
    """Centered page wrapper with consistent paddings."""
    spacing = THEME_TOKENS["spacing"]
    page_padding = spacing["24"] if padding is None else padding

    return ft.Container(
        expand=True,
        padding=page_padding,
        content=ft.Container(
            expand=True,
            alignment=ft.Alignment(0, -1),
            content=ft.Container(
                width=max_width,
                expand=True,
                content=content,
            ),
        ),
    )


def ContentCard(
    content: ft.Control,
    title: str | None = None,
    subtitle: str | None = None,
    action: ft.Control | None = None,
) -> ft.Container:
    """Reusable content card for sections and blocks."""
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
                size=typography["h3"]["max_size"],
                weight=_font_weight(typography["h3"]["weight"]),
                color=colors["text_primary"],
            )
        )
    if subtitle:
        header_controls.append(
            ft.Text(
                value=subtitle,
                size=typography["caption"]["max_size"],
                weight=_font_weight(typography["caption"]["weight"]),
                color=colors["text_secondary"],
            )
        )
    if action:
        header_controls.append(action)

    controls: list[ft.Control] = []
    if header_controls:
        controls.append(ft.Column(controls=header_controls, spacing=spacing["4"]))
    controls.append(content)

    return ft.Container(
        bgcolor=colors["surface"],
        border_radius=radius["16"],
        shadow=shadows["card"],
        padding=spacing["24"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        content=ft.Column(controls=controls, spacing=spacing["16"]),
    )


def TwoColumnLayout(
    left: ft.Control,
    right: ft.Control,
    left_flex: int = 1,
    right_flex: int = 1,
    spacing: int | None = None,
) -> ft.Row:
    """Two-column layout with configurable flex values."""
    tokens = THEME_TOKENS["spacing"]
    gap = tokens["24"] if spacing is None else spacing

    return ft.Row(
        spacing=gap,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(content=left, expand=left_flex),
            ft.Container(content=right, expand=right_flex),
        ],
    )


def ThreeColumnLayout(
    first: ft.Control,
    second: ft.Control,
    third: ft.Control,
    first_flex: int = 1,
    second_flex: int = 1,
    third_flex: int = 1,
    spacing: int | None = None,
) -> ft.Row:
    """Three-column layout with configurable flex values."""
    tokens = THEME_TOKENS["spacing"]
    gap = tokens["24"] if spacing is None else spacing

    return ft.Row(
        spacing=gap,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(content=first, expand=first_flex),
            ft.Container(content=second, expand=second_flex),
            ft.Container(content=third, expand=third_flex),
        ],
    )


def ResponsiveContainer(
    content: ft.Control,
    xs: int = 12,
    sm: int = 12,
    md: int = 10,
    lg: int = 10,
    xl: int = 10,
    spacing: int | None = None,
    run_spacing: int | None = None,
) -> ft.ResponsiveRow:
    """Responsive wrapper to keep content centered across breakpoints."""
    tokens = THEME_TOKENS["spacing"]
    gap = tokens["16"] if spacing is None else spacing
    run_gap = tokens["16"] if run_spacing is None else run_spacing

    return ft.ResponsiveRow(
        columns=12,
        spacing=gap,
        run_spacing=run_gap,
        controls=[
            ft.Container(
                col={"xs": xs, "sm": sm, "md": md, "lg": lg, "xl": xl},
                content=content,
            )
        ],
    )
