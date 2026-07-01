"""Reusable topbar component aligned with the design system."""

from __future__ import annotations

import flet as ft

from theme.theme import THEME_TOKENS


PAGE_TITLES: dict[str, str] = {
    "/dashboard": "Dashboard",
    "/students": "Ogrenciler",
    "/weekly-program": "Haftalik Program",
    "/lesson-records": "Ders Kayitlari",
    "/measurements": "Olcumler",
    "/courses": "Kurslar",
    "/progress-reports": "Gelisim Raporlari",
    "/parent-reports": "Veli Raporlari",
    "/settings": "Ayarlar",
}


def _resolve_title(route: str) -> str:
    return PAGE_TITLES.get(route, "Dashboard")


def _build_breadcrumb(route: str) -> str:
    page = _resolve_title(route)
    return f"Ana Sayfa > {page}"


def _build_global_search() -> ft.Control:
    colors = THEME_TOKENS["colors"]

    return ft.Container(
        width=320,
        height=48,
        border_radius=999,
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        padding=ft.Padding(12, 0, 12, 0),
        alignment=ft.Alignment(-1, 0),
        content=ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.SEARCH, size=20, color=colors["text_secondary"]),
                ft.Text("Ogrenci, kurs veya ders ara...", size=14, color=colors["text_secondary"]),
            ],
        ),
    )


def _build_notification_button(notification_count: int = 0) -> ft.Control:
    colors = THEME_TOKENS["colors"]

    badge = ft.Container(
        width=16,
        height=16,
        border_radius=8,
        bgcolor=colors["danger"],
        alignment=ft.Alignment(0, 0),
        content=ft.Text(str(notification_count), size=10, color=colors["surface"]),
        right=2,
        top=2,
        visible=notification_count > 0,
    )

    return ft.Container(
        width=48,
        height=48,
        border_radius=999,
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        alignment=ft.Alignment(0, 0),
        content=ft.Stack(
            controls=[
                ft.Icon(ft.Icons.NOTIFICATIONS, size=20, color=colors["text_secondary"]),
                badge,
            ]
        ),
    )


def _build_quick_action_menu() -> ft.Control:
    colors = THEME_TOKENS["colors"]

    return ft.PopupMenuButton(
        content=ft.Container(
            height=48,
            border_radius=10,
            bgcolor=colors["primary"],
            padding=ft.Padding(16, 0, 16, 0),
            alignment=ft.Alignment(0, 0),
            content=ft.Text("+ Yeni", size=16, color=colors["surface"], weight=ft.FontWeight.W_600),
        ),
        items=[
            ft.PopupMenuItem(content=ft.Text("Yeni Ogrenci")),
            ft.PopupMenuItem(content=ft.Text("Yeni Ders")),
            ft.PopupMenuItem(content=ft.Text("Yeni Olcum")),
            ft.PopupMenuItem(content=ft.Text("Yeni Kurs")),
            ft.PopupMenuItem(content=ft.Text("Yeni Rapor")),
        ],
    )


def _build_profile_menu(user_name: str, user_role: str) -> ft.Control:
    colors = THEME_TOKENS["colors"]

    profile_content = ft.Container(
        height=48,
        padding=ft.Padding(8, 0, 8, 0),
        content=ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=40,
                    height=40,
                    border_radius=20,
                    bgcolor=f"{colors['primary']}1A",
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=22, color=colors["primary"]),
                ),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text(user_name, size=13, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                        ft.Text(user_role, size=12, color=colors["text_secondary"]),
                    ],
                ),
                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, size=18, color=colors["text_secondary"]),
            ],
        ),
    )

    return ft.PopupMenuButton(
        content=profile_content,
        items=[
            ft.PopupMenuItem(content=ft.Text("Profil")),
            ft.PopupMenuItem(content=ft.Text("Sifre Degistir")),
            ft.PopupMenuItem(content=ft.Text("Yedek Al")),
            ft.PopupMenuItem(content=ft.Text("Cikis Yap")),
        ],
    )


def build_topbar_component(
    route: str,
    notification_count: int = 0,
    user_name: str = "Abdullah Yeter",
    user_role: str = "Yonetici",
) -> ft.Container:
    """Build a reusable topbar component.

    - Title is derived from route.
    - Breadcrumb is derived from route.
    - Search, notifications, quick actions and profile are modular parts.
    """

    colors = THEME_TOKENS["colors"]
    title = _resolve_title(route)
    breadcrumb = _build_breadcrumb(route)

    left_side = ft.Column(
        spacing=2,
        controls=[
            ft.Text(title, size=28, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
            ft.Text(breadcrumb, size=14, color=colors["text_secondary"]),
        ],
    )

    right_side = ft.Row(
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            _build_global_search(),
            _build_notification_button(notification_count=notification_count),
            _build_quick_action_menu(),
            _build_profile_menu(user_name=user_name, user_role=user_role),
        ],
    )

    return ft.Container(
        height=72,
        bgcolor=colors["surface"],
        border=ft.Border(bottom=ft.BorderSide(1, colors["border"])),
        padding=ft.Padding(24, 12, 24, 12),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[left_side, right_side],
        ),
    )
