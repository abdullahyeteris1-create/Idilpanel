"""Shared application layout composed of sidebar, topbar, and content area."""

import flet as ft

from theme.theme import THEME_TOKENS
from views.content_area import build_content_area
from views.router import build_route_content, get_page_title
from views.sidebar import build_sidebar
from views.topbar import build_topbar


DESKTOP_BREAKPOINT = 1366
TABLET_BREAKPOINT = 768


class AppLayoutShell:
    """Reusable layout shell for all pages with route-driven content."""

    def __init__(self, page: ft.Page, on_navigate, route: str = "/dashboard") -> None:
        self.page = page
        self.on_navigate = on_navigate
        self.route = route

    def set_route(self, route: str) -> None:
        """Update active route for layout rendering."""
        self.route = route

    def build(self) -> ft.Control:
        """Create a responsive desktop-first layout structure."""
        width = self.page.width or DESKTOP_BREAKPOINT

        topbar = build_topbar(get_page_title(self.route))
        content_area = build_content_area(build_route_content(self.route))

        main_column = ft.Column(
            controls=[topbar, content_area],
            spacing=0,
            expand=True,
        )

        if width < TABLET_BREAKPOINT:
            return main_column

        compact_sidebar = width < DESKTOP_BREAKPOINT

        return ft.Row(
            spacing=0,
            expand=True,
            controls=[
                build_sidebar(
                    active_route=self.route,
                    on_navigate=self.on_navigate,
                    compact=compact_sidebar,
                ),
                ft.VerticalDivider(width=1, color=THEME_TOKENS["colors"]["border_neutral"]),
                ft.Container(padding=ft.Padding(0, 0, 0, 0), expand=True, content=main_column),
            ],
        )

    def on_resize(self, _: ft.ControlEvent) -> None:
        """Rebuild shell when viewport width changes."""
        self.page.clean()
        self.page.add(self.build())
        self.page.update()
