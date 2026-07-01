"""Shared content area shell aligned with the design system."""

import flet as ft

from components.card import build_card
from theme.theme import THEME_TOKENS


def build_content_area(content: ft.Control | None = None) -> ft.Container:
    """Build a dynamic content region for page-level modules."""
    colors = THEME_TOKENS["colors"]
    spacing = THEME_TOKENS["spacing"]

    placeholder = build_card(
        title="Content Area",
        subtitle="Dynamic module content will be injected here.",
        content=ft.Text(value="Layout shell is ready."),
    )

    return ft.Container(
        expand=True,
        bgcolor=colors["background"],
        padding=ft.Padding(
            left=spacing["lg"],
            top=spacing["lg"],
            right=spacing["lg"],
            bottom=spacing["lg"],
        ),
        content=ft.Container(
            expand=True,
            content=content or placeholder,
        ),
    )
