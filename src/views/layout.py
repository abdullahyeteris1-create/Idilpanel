"""Shared application layout composed of sidebar, topbar, and content area."""

import flet as ft

from theme.theme import THEME_TOKENS
from views.app_layout import build_app_layout
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
        """Create a responsive desktop-first layout structure using AppLayout."""
        width = self.page.width or DESKTOP_BREAKPOINT

        # Build route content (what to display)
        route_content = build_route_content(self.route)
        
        # Get page title for topbar
        page_title = get_page_title(self.route)
        
        # Wrap content in content area (adds padding and background)
        content_area = build_content_area(route_content)

        # Use unified AppLayout for all screens
        return build_app_layout(
            content=content_area,
            page_width=width,
            page_title=page_title,
            active_route=self.route,
            on_navigate=self.on_navigate,
        )

    def on_resize(self, _: ft.ControlEvent) -> None:
        """Rebuild shell when viewport width changes."""
        self.page.clean()
        self.page.add(self.build())
        self.page.update()
