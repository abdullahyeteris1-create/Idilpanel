"""Reusable form card wrapper for page forms."""

from __future__ import annotations

import flet as ft

from .app_card import build_app_card


def build_form_card(
    fields: list[ft.Control],
    actions: list[ft.Control] | None = None,
    title: str = "Form",
    subtitle: str = "Alanlari doldurun",
    max_height: int = 500,
) -> ft.Container:
    """Build a shared form card with scrollable fields and fixed footer actions.
    
    Layout structure:
    - Title/Subtitle (header, not scrolled)
    - Scrollable fields area (expands to available space or max_height)
    - Fixed action buttons (always visible, never scrolled)
    """

    # Scrollable fields container - responsive height
    # Use scroll=AUTO to enable scrolling when content exceeds available space
    fields_container = ft.Column(
        controls=[
            ft.ResponsiveRow(
                controls=fields,
                spacing=12,
                run_spacing=12,
            )
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,  # Expand to fill available space
    )

    # Action buttons row (fixed, always visible)
    actions_row = ft.Row(
        controls=actions or [],
        alignment=ft.MainAxisAlignment.END,
        spacing=8,
    ) if actions else ft.Column()

    # Create a column with scrollable fields and fixed buttons
    content_column = ft.Column(
        controls=[
            # Scrollable fields section - responsive height
            # Uses expand=True to fill available space, allowing footer to stay fixed below
            ft.Container(
                content=fields_container,
                height=max_height,  # Fallback height for layout calculation
                expand=True,  # Expand to fill available space in parent
            ),
            # Fixed buttons section (always visible, never scrolls)
            ft.Container(
                content=actions_row,
                padding=12,
                expand=False,  # Don't expand, fixed size
            ),
        ],
        spacing=0,
        expand=True,  # Expand to fill parent container
    )

    return build_app_card(
        title=title,
        subtitle=subtitle,
        content=content_column,
    )
