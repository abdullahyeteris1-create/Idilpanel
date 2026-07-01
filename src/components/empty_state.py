"""Reusable empty, loading and error state components."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from .app_card import build_app_card
from .secondary_button import build_secondary_button


def build_empty_state(
    title: str,
    message: str,
    primary_action: ft.Control | None = None,
    secondary_action: ft.Control | None = None,
    icon: str = ft.Icons.INBOX_OUTLINED,
) -> ft.Container:
    """Build a shared empty-state card."""

    action_controls = [control for control in [primary_action, secondary_action] if control is not None]

    body_controls: list[ft.Control] = [
        ft.Icon(icon),
        ft.Text(title),
        ft.Text(message),
    ]

    if action_controls:
        body_controls.append(
            ft.Row(
                controls=action_controls,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            )
        )

    return build_app_card(
        title="Empty State",
        subtitle="Veri goruntulenemiyor",
        content=ft.Column(
            controls=body_controls,
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


def build_loading_state(message: str = "Yukleniyor...") -> ft.Container:
    """Build a shared loading state."""
    return build_app_card(
        title="Loading",
        subtitle="Lutfen bekleyin",
        content=ft.Row(
            controls=[ft.ProgressRing(), ft.Text(message)],
            spacing=12,
        ),
    )


def build_error_state(
    message: str,
    on_retry: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.Container:
    """Build a shared error state."""
    return build_app_card(
        title="Error",
        subtitle="Bir hata olustu",
        content=ft.Column(
            controls=[
                ft.Text(message),
                build_secondary_button("Tekrar Dene", on_click=on_retry),
            ],
            spacing=8,
        ),
    )
