"""Shared sidebar shell aligned with the design system."""

import flet as ft

from components.badge import build_badge
from theme.theme import THEME_TOKENS


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def build_sidebar(
    active_route: str,
    on_navigate,
    compact: bool = False,
) -> ft.Container:
    """Build the shared left navigation area for all pages."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    sidebar_width = spacing["xxxl"] if compact else spacing["xxxl"] * 4

    nav_items = [
        ("/dashboard", ft.Icons.DASHBOARD, "Dashboard"),
        ("/weekly-program", ft.Icons.CALENDAR_MONTH, "Haftalik Program"),
        ("/students", ft.Icons.GROUP, "Ogrenciler"),
        ("/courses", ft.Icons.MENU_BOOK, "Kurslar"),
        ("/lesson-records", ft.Icons.SCHOOL, "Ders Kayitlari"),
        ("/progress-reports", ft.Icons.INSERT_CHART, "Gelisim Raporlari"),
        ("/pdf", ft.Icons.PICTURE_AS_PDF, "PDF"),
        ("/settings", ft.Icons.SETTINGS, "Ayarlar"),
    ]

    item_controls: list[ft.Control] = []
    for route, icon, label in nav_items:
        is_active = route == active_route
        tone = colors["primary"] if is_active else colors["text_secondary"]
        item_bg = f"{colors['primary']}1A" if is_active else colors["surface"]

        row_controls = [
            ft.Icon(icon=icon, color=tone, size=spacing["lg"]),
        ]
        if not compact:
            row_controls.append(
                ft.Text(
                    value=label,
                    size=typography["body"]["max_size"],
                    weight=_font_weight(typography["body"]["weight"]),
                    color=tone,
                )
            )

        item_controls.append(
            ft.Container(
                bgcolor=item_bg,
                border_radius=radius["button"],
                padding=spacing["sm"],
                on_click=lambda _, next_route=route: on_navigate(next_route),
                content=ft.Row(controls=row_controls, spacing=spacing["sm"]),
            )
        )

    header_controls: list[ft.Control] = [
        ft.Text(
            value="IDIL",
            size=typography["card_title"]["max_size"],
            weight=_font_weight(typography["card_title"]["weight"]),
            color=colors["primary"],
        )
    ]
    if not compact:
        header_controls.append(build_badge(text="Admin", variant="secondary"))

    return ft.Container(
        width=sidebar_width,
        bgcolor=colors["surface"],
        border=ft.Border(right=ft.BorderSide(1, colors["border_neutral"])),
        padding=ft.Padding(
            left=spacing["md"],
            top=spacing["lg"],
            right=spacing["md"],
            bottom=spacing["lg"],
        ),
        content=ft.Column(
            controls=[
                ft.Column(controls=header_controls, spacing=spacing["sm"]),
                ft.Divider(height=spacing["md"], color=colors["border_neutral"]),
                ft.Column(controls=item_controls, spacing=spacing["sm"], expand=True),
            ],
            spacing=spacing["md"],
            expand=True,
        ),
    )
