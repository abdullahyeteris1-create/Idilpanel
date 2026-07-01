"""Shared card component aligned with the Idil design system."""

import flet as ft

from components.badge import build_badge
from theme.theme import THEME_TOKENS


def build_card(
    content: ft.Control,
    title: str | None = None,
    subtitle: str | None = None,
    action: ft.Control | None = None,
    padding_size: str = "card",
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
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS,
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


def build_lesson_card(
    student_name: str,
    class_name: str,
    level_no: str,
    progress_text: str,
    status_text: str,
    status_variant: str = "secondary",
) -> ft.Container:
    """Create a compact lesson card for static weekly schedule slots."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    return ft.Container(
        bgcolor=colors["surface"],
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        height=spacing["xxxl"] * 2,
        border=ft.Border(
            top=ft.BorderSide(1, colors["border_neutral"]),
            right=ft.BorderSide(1, colors["border_neutral"]),
            bottom=ft.BorderSide(1, colors["border_neutral"]),
            left=ft.BorderSide(1, colors["border_neutral"]),
        ),
        border_radius=radius["input"],
        padding=ft.Padding(
            left=spacing["md"],
            top=spacing["sm"],
            right=spacing["md"],
            bottom=spacing["sm"],
        ),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Text(
                                value=student_name,
                                size=typography["body"]["max_size"],
                                weight=ft.FontWeight.W_600,
                                color=colors["text_primary"],
                                no_wrap=True,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ),
                        ft.Container(
                            alignment=ft.Alignment(1, 0),
                            content=build_badge(text=status_text, variant=status_variant),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=spacing["sm"],
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            value="Sinif",
                            size=typography["small"]["max_size"],
                            weight=ft.FontWeight.W_400,
                            color=colors["text_secondary"],
                        ),
                        ft.Text(
                            value=class_name,
                            size=typography["small"]["max_size"],
                            weight=ft.FontWeight.W_600,
                            color=colors["text_primary"],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            value="Kur No",
                            size=typography["small"]["max_size"],
                            weight=ft.FontWeight.W_400,
                            color=colors["text_secondary"],
                        ),
                        ft.Text(
                            value=level_no,
                            size=typography["small"]["max_size"],
                            weight=ft.FontWeight.W_600,
                            color=colors["text_primary"],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            value="Ilerleme",
                            size=typography["small"]["max_size"],
                            weight=ft.FontWeight.W_400,
                            color=colors["text_secondary"],
                        ),
                        ft.Text(
                            value=progress_text,
                            size=typography["small"]["max_size"],
                            weight=ft.FontWeight.W_600,
                            color=colors["text_primary"],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=spacing["sm"],
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )
