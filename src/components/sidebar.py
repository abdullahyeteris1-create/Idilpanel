"""Reusable sidebar component aligned with the design system."""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from theme.theme import THEME_TOKENS


SidebarItem = tuple[str, str, str]


DEFAULT_SIDEBAR_ITEMS: list[SidebarItem] = [
    ("/dashboard", ft.Icons.DASHBOARD, "Dashboard"),
    ("/students", ft.Icons.PERSON, "Ogrenciler"),
    ("/weekly-program", ft.Icons.CALENDAR_MONTH, "Haftalik Program"),
    ("/lesson-records", ft.Icons.MENU_BOOK, "Ders Kayitlari"),
    ("/measurements", ft.Icons.STRAIGHTEN, "Olcumler"),
    ("/progress-reports", ft.Icons.ANALYTICS, "Gelisim Raporlari"),
    ("/parent-reports", ft.Icons.DESCRIPTION, "Veli Raporlari"),
    ("/settings", ft.Icons.SETTINGS, "Ayarlar"),
]


def _active_text_color(is_active: bool, colors: dict[str, str]) -> str:
    return colors["primary"] if is_active else f"{colors['surface']}D9"


def _item_background(is_active: bool, colors: dict[str, str]) -> str | None:
    return colors["surface"] if is_active else None


def _build_menu_item(
    item: SidebarItem,
    active_route: str,
    on_navigate: Callable[[str], None],
) -> ft.Container:
    route, icon_data, label = item
    colors = THEME_TOKENS["colors"]
    hover_color = colors.get("primary_hover", colors["primary"])
    spacing = THEME_TOKENS["spacing"]
    is_active = route == active_route

    content_row = ft.Row(
        spacing=spacing["12"],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Icon(icon_data, size=24, color=_active_text_color(is_active, colors)),
            ft.Text(
                label,
                size=16,
                weight=ft.FontWeight.W_600,
                color=_active_text_color(is_active, colors),
            ),
        ],
    )

    item_container = ft.Container(
        height=48,
        border_radius=10,
        bgcolor=_item_background(is_active, colors),
        padding=ft.Padding(spacing["12"], 0, spacing["12"], 0),
        alignment=ft.Alignment(-1, 0),
        content=content_row,
        on_click=lambda _: on_navigate(route),
    )

    def _on_hover(e: ft.ControlEvent) -> None:
        if is_active:
            return

        item_container.bgcolor = hover_color if e.data == "true" else None
        if e.page:
            e.page.update()

    item_container.on_hover = _on_hover
    return item_container


def build_sidebar_component(
    active_route: str,
    on_navigate: Callable[[str], None],
    user_name: str = "Abdullah Yeter",
    user_role: str = "Yonetici",
    items: list[SidebarItem] | None = None,
) -> ft.Container:
    """Build a reusable sidebar component.

    The active route is determined by the given route value.
    Only one menu item can be active at a time.
    """

    colors = THEME_TOKENS["colors"]
    spacing = THEME_TOKENS["spacing"]

    sidebar_items = items if items is not None else DEFAULT_SIDEBAR_ITEMS

    menu_controls = [_build_menu_item(item, active_route, on_navigate) for item in sidebar_items]

    logo_block = ft.Column(
        spacing=4,
        controls=[
            ft.Row(
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.MENU_BOOK, color=colors["surface"], size=24),
                    ft.Text("IDIL HIZLI OKUMA", size=18, weight=ft.FontWeight.W_700, color=colors["surface"]),
                ],
            ),
            ft.Text("Yonetim Sistemi", size=13, color=f"{colors['surface']}D9"),
            ft.Text("v1.0.0", size=12, color=f"{colors['surface']}B3"),
        ],
    )

    footer_block = ft.Column(
        spacing=8,
        controls=[
            ft.Divider(height=1, color=f"{colors['surface']}4D"),
            ft.Row(
                spacing=10,
                controls=[
                    ft.Container(
                        width=36,
                        height=36,
                        border_radius=18,
                        bgcolor=f"{colors['surface']}26",
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color=colors["surface"], size=20),
                    ),
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(user_name, size=14, color=colors["surface"], weight=ft.FontWeight.W_600),
                            ft.Text(user_role, size=12, color=f"{colors['surface']}D9"),
                        ],
                    ),
                ],
            ),
            ft.Container(
                height=40,
                border_radius=10,
                padding=ft.Padding(spacing["12"], 0, spacing["12"], 0),
                alignment=ft.Alignment(-1, 0),
                content=ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(ft.Icons.LOGOUT, size=20, color=colors["surface"]),
                        ft.Text("Cikis Yap", size=14, color=colors["surface"], weight=ft.FontWeight.W_600),
                    ],
                ),
            ),
        ],
    )

    return ft.Container(
        width=260,
        bgcolor=colors["primary"],
        padding=spacing["24"],
        content=ft.Column(
            expand=True,
            spacing=24,
            controls=[
                logo_block,
                ft.Column(expand=True, spacing=8, controls=menu_controls),
                footer_block,
            ],
        ),
    )
