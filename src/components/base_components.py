"""Base UI components built on top of the central design system tokens."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

import flet as ft

from theme.theme import THEME_TOKENS


def _font_weight(token_weight: int) -> ft.FontWeight:
    weight_map = {
        400: ft.FontWeight.W_400,
        600: ft.FontWeight.W_600,
        700: ft.FontWeight.W_700,
    }
    return weight_map.get(token_weight, ft.FontWeight.W_400)


def _base_button(
    label: str,
    variant: str,
    on_click: Callable[[ft.ControlEvent], None] | None = None,
    icon: str | None = None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.ElevatedButton:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]["button"]
    radius = THEME_TOKENS["radius"]
    spacing = THEME_TOKENS["spacing"]

    if variant == "secondary":
        bgcolor = colors["surface"]
        text_color = colors["text_secondary"]
    else:
        bgcolor = colors.get(variant, colors["primary"])
        text_color = colors["surface"]

    return ft.ElevatedButton(
        content=ft.Text(value=label),
        icon=icon,
        on_click=on_click,
        disabled=disabled,
        expand=expand,
        height=48,
        style=ft.ButtonStyle(
            bgcolor=bgcolor,
            color=text_color,
            shape=ft.RoundedRectangleBorder(radius=radius["button"]),
            side=ft.BorderSide(1, colors["border"]),
            elevation={
                ft.ControlState.DEFAULT: 0,
                ft.ControlState.HOVERED: 2,
                ft.ControlState.PRESSED: 1,
            },
            padding=ft.Padding(spacing["16"], spacing["8"], spacing["16"], spacing["8"]),
            text_style=ft.TextStyle(
                size=typography["max_size"],
                weight=_font_weight(typography["weight"]),
            ),
        ),
    )


def PrimaryButton(
    label: str,
    on_click: Callable[[ft.ControlEvent], None] | None = None,
    icon: str | None = None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.ElevatedButton:
    """Primary action button."""
    return _base_button(label=label, variant="primary", on_click=on_click, icon=icon, disabled=disabled, expand=expand)


def SecondaryButton(
    label: str,
    on_click: Callable[[ft.ControlEvent], None] | None = None,
    icon: str | None = None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.ElevatedButton:
    """Secondary action button."""
    return _base_button(label=label, variant="secondary", on_click=on_click, icon=icon, disabled=disabled, expand=expand)


def AppInput(
    label: str,
    hint_text: str = "",
    value: str = "",
    required: bool = False,
    error_text: str | None = None,
    disabled: bool = False,
    on_change: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.TextField:
    """Single-line text input aligned with theme tokens."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    radius = THEME_TOKENS["radius"]
    spacing = THEME_TOKENS["spacing"]

    body_type = typography["body"]
    caption_type = typography["caption"]
    resolved_label = f"{label} *" if required else label

    return ft.TextField(
        label=resolved_label,
        hint_text=hint_text,
        value=value,
        error=error_text,
        disabled=disabled,
        on_change=on_change,
        height=48,
        filled=True,
        bgcolor=colors["surface"],
        border=ft.InputBorder.OUTLINE,
        border_color=colors["border"],
        focused_border_color=colors["primary"],
        border_radius=radius["input"],
        content_padding=ft.Padding(spacing["12"], spacing["8"], spacing["12"], spacing["8"]),
        label_style=ft.TextStyle(
            size=caption_type["max_size"],
            weight=_font_weight(caption_type["weight"]),
            color=colors["text_secondary"],
        ),
        hint_style=ft.TextStyle(
            size=caption_type["max_size"],
            weight=_font_weight(caption_type["weight"]),
            color=colors["text_secondary"],
        ),
        text_style=ft.TextStyle(
            size=body_type["max_size"],
            weight=_font_weight(body_type["weight"]),
            color=colors["text_primary"],
        ),
    )


def PasswordInput(
    label: str,
    hint_text: str = "",
    value: str = "",
    required: bool = False,
    error_text: str | None = None,
    disabled: bool = False,
    on_change: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.TextField:
    """Password input with reveal support."""
    field = AppInput(
        label=label,
        hint_text=hint_text,
        value=value,
        required=required,
        error_text=error_text,
        disabled=disabled,
        on_change=on_change,
    )
    field.password = True
    field.can_reveal_password = True
    return field


def AppDropdown(
    label: str,
    options: list[str] | list[tuple[str, str]],
    value: str | None = None,
    required: bool = False,
    disabled: bool = False,
    hint_text: str = "",
    error_text: str | None = None,
    on_change: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.Dropdown:
    """Dropdown input aligned with theme tokens."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    radius = THEME_TOKENS["radius"]
    spacing = THEME_TOKENS["spacing"]

    body_type = typography["body"]
    caption_type = typography["caption"]
    resolved_label = f"{label} *" if required else label

    normalized_options: list[ft.dropdown.Option] = []
    for option in options:
        if isinstance(option, tuple):
            key, text = option
            normalized_options.append(ft.dropdown.Option(key=key, text=text))
        else:
            normalized_options.append(ft.dropdown.Option(option))

    return ft.Dropdown(
        value=value,
        label=resolved_label,
        hint_text=hint_text,
        options=normalized_options,
        disabled=disabled,
        on_select=on_change,
        error_text=error_text,
        height=48,
        filled=True,
        bgcolor=colors["surface"],
        border_color=colors["border"],
        focused_border_color=colors["primary"],
        border_radius=radius["input"],
        content_padding=ft.Padding(spacing["12"], spacing["8"], spacing["12"], spacing["8"]),
        label_style=ft.TextStyle(
            size=caption_type["max_size"],
            weight=_font_weight(caption_type["weight"]),
            color=colors["text_secondary"],
        ),
        text_style=ft.TextStyle(
            size=body_type["max_size"],
            weight=_font_weight(body_type["weight"]),
            color=colors["text_primary"],
        ),
    )


def AppDatePicker(
    label: str,
    hint_text: str = "YYYY-MM-DD",
    value: str = "",
    required: bool = False,
    on_date_change: Callable[[str], None] | None = None,
) -> ft.Control:
    """Date picker composed of input + calendar button + Flet DatePicker dialog."""

    date_field = AppInput(
        label=label,
        hint_text=hint_text,
        value=value,
        required=required,
    )
    date_field.read_only = True

    def _handle_picker_change(e: ft.ControlEvent) -> None:
        picked = e.control.value
        if isinstance(picked, date):
            value_text = picked.isoformat()
            date_field.value = value_text
            if on_date_change is not None:
                on_date_change(value_text)
            e.page.update()

    date_picker = ft.DatePicker(on_change=_handle_picker_change)

    def _open_picker(e: ft.ControlEvent) -> None:
        e.page.show_dialog(date_picker)

    open_button = SecondaryButton(label="", icon=ft.Icons.CALENDAR_MONTH, on_click=_open_picker)
    open_button.width = 48

    row = ft.Row(
        spacing=8,
        controls=[
            ft.Container(expand=True, content=date_field),
            open_button,
        ],
    )
    row.data = {"field": date_field, "picker": date_picker}
    return row


def AppTextArea(
    label: str,
    hint_text: str = "",
    value: str = "",
    required: bool = False,
    error_text: str | None = None,
    disabled: bool = False,
    min_height: int = 140,
    min_lines: int = 6,
    max_lines: int = 10,
    on_change: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.TextField:
    """Multiline textarea aligned with theme tokens."""
    field = AppInput(
        label=label,
        hint_text=hint_text,
        value=value,
        required=required,
        error_text=error_text,
        disabled=disabled,
        on_change=on_change,
    )
    field.height = min_height
    field.multiline = True
    field.min_lines = min_lines
    field.max_lines = max_lines
    return field


def AppSearchBox(
    hint_text: str = "Ara...",
    value: str = "",
    disabled: bool = False,
    on_change: Callable[[ft.ControlEvent], None] | None = None,
    on_submit: Callable[[ft.ControlEvent], None] | None = None,
) -> ft.TextField:
    """Search input variant with leading search icon."""
    field = AppInput(
        label="",
        hint_text=hint_text,
        value=value,
        disabled=disabled,
        on_change=on_change,
    )
    field.on_submit = on_submit
    field.prefix_icon = ft.Icons.SEARCH
    return field


def AppCard(
    content: ft.Control,
    title: str | None = None,
    subtitle: str | None = None,
    action: ft.Control | None = None,
) -> ft.Container:
    """Base white surface card aligned with tokenized radius, spacing and shadows."""
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
        border_radius=radius["card"],
        padding=spacing["24"],
        shadow=shadows["card"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        content=ft.Column(controls=controls, spacing=spacing["16"]),
    )
