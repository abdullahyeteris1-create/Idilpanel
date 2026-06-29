"""Shared dialog component aligned with the Idil design system."""

from collections.abc import Callable

import flet as ft

from theme.theme import THEME_TOKENS


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def _build_action_button(
    text: str,
    variant: str,
    handler: Callable[[ft.ControlEvent], None] | None,
) -> ft.TextButton:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]["button"]

    return ft.TextButton(
        content=ft.Text(value=text),
        on_click=handler,
        style=ft.ButtonStyle(
            color=colors.get(variant, colors["primary"]),
            text_style=ft.TextStyle(
                size=typography["max_size"],
                weight=_font_weight(typography["weight"]),
            ),
        ),
    )


def build_dialog(
    title: str,
    content: str,
    confirm_text: str = "Onayla",
    cancel_text: str = "Vazgec",
    on_confirm: Callable[[ft.ControlEvent], None] | None = None,
    on_cancel: Callable[[ft.ControlEvent], None] | None = None,
    modal: bool = True,
) -> ft.AlertDialog:
    """Create a semantic dialog for confirmations and important notices."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    title_type = typography["subtitle"]
    body_type = typography["body"]

    return ft.AlertDialog(
        modal=modal,
        bgcolor=colors["surface"],
        shape=ft.RoundedRectangleBorder(radius=radius["panel"]),
        title_padding=ft.Padding(
            left=spacing["md"],
            top=spacing["md"],
            right=spacing["md"],
            bottom=spacing["sm"],
        ),
        content_padding=ft.Padding(
            left=spacing["md"],
            top=spacing["xs"],
            right=spacing["md"],
            bottom=spacing["md"],
        ),
        actions_padding=ft.Padding(
            left=spacing["sm"],
            top=spacing["xs"],
            right=spacing["sm"],
            bottom=spacing["sm"],
        ),
        title=ft.Text(
            value=title,
            size=title_type["max_size"],
            weight=_font_weight(title_type["weight"]),
            color=colors["text_primary"],
        ),
        content=ft.Text(
            value=content,
            size=body_type["max_size"],
            weight=_font_weight(body_type["weight"]),
            color=colors["text_secondary"],
        ),
        actions=[
            _build_action_button(cancel_text, "secondary", on_cancel),
            _build_action_button(confirm_text, "danger", on_confirm),
        ],
    )
