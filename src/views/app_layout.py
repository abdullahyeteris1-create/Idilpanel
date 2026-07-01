"""Shared AppLayout foundation for all application screens.

This module provides a reusable layout structure with:
- Fixed Sidebar (no scroll)
- Fixed Topbar (no scroll)
- Fixed viewport content region (no page-level scroll)

All screens (Dashboard, Students, Weekly Program, Lessons, Measurements, Reports, Settings)
use this layout for consistency and responsive behavior.
"""

from __future__ import annotations

import flet as ft

from theme.theme import THEME_TOKENS
from views.sidebar import build_sidebar
from views.topbar import build_topbar


DESKTOP_BREAKPOINT = 1366
TABLET_BREAKPOINT = 768


class AppLayout:
    """Reusable layout container for all application screens.
    
    Provides a three-part layout:
    - Sidebar (fixed, left)
    - Topbar (fixed, top)
    - Content Area (fixed viewport, inner modules manage their own scroll)
    
    The layout is responsive and adapts to different screen sizes.
    """

    def __init__(
        self,
        content: ft.Control,
        page_width: float = DESKTOP_BREAKPOINT,
        page_title: str = "Dashboard",
        active_route: str = "/dashboard",
        on_navigate=None,
    ) -> None:
        """Initialize AppLayout.

        Args:
            content: The scrollable content to display
            page_width: Current page width for responsive sizing
            page_title: Page title for topbar
            active_route: Current active route for sidebar highlighting
            on_navigate: Callback function for navigation
        """
        self.content = content
        self.page_width = page_width or DESKTOP_BREAKPOINT
        self.page_title = page_title
        self.active_route = active_route
        self.on_navigate = on_navigate or (lambda x: None)

    def build(self) -> ft.Control:
        """Build the layout structure.

        Returns:
            A responsive layout with fixed sidebar/topbar and fixed viewport content.

        Layout structure:
        ┌────────────────────────────────────┐
        │ Sidebar (Fixed) | Topbar (Fixed)   │
        │ (no scroll)     ├──────────────────┤
        │                 │ Content Area     │
        │                 │ (fixed viewport) │
        └────────────────────────────────────┘
        """
        colors = THEME_TOKENS["colors"]

        def _log_control_state(
            name: str,
            control: ft.Control,
            event: ft.ControlEvent | None = None,
        ) -> None:
            event_width = getattr(event, "width", None)
            event_height = getattr(event, "height", None)
            width = event_width if event_width is not None else getattr(control, "width", None)
            height = event_height if event_height is not None else getattr(control, "height", None)
            expand = getattr(control, "expand", None)
            scroll = getattr(control, "scroll", None)
            print(
                "[LAYOUT-DEBUG][AppLayout] "
                f"{name}: width={width}, height={height}, expand={expand}, scroll={scroll}"
            )

        def _size_logger(name: str, control: ft.Control):
            def _handler(e: ft.ControlEvent) -> None:
                _log_control_state(name, control, e)

            return _handler

        # Build topbar with page title
        topbar = build_topbar(self.page_title)

        # Build fixed viewport content area.
        # Module internals are responsible for scoped scrolling.
        content_area = ft.Container(
            expand=True,
            content=self.content,
        )
        content_area.on_size_change = _size_logger("content_area", content_area)
        _log_control_state("content_area.initial", content_area)

        # Main column: topbar (fixed) + content area (fixed viewport)
        main_column = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                topbar,  # Fixed at top
                content_area,
            ],
        )

        # Mobile layout (< TABLET_BREAKPOINT)
        if self.page_width < TABLET_BREAKPOINT:
            return ft.Container(
                expand=True,
                bgcolor=colors["background"],
                content=main_column,
            )

        # Desktop/Tablet layout
        # Sidebar (fixed) + Main Column (with topbar + scrollable content)
        compact_sidebar = self.page_width < DESKTOP_BREAKPOINT

        return ft.Row(
            spacing=0,
            expand=True,
            controls=[
                # Sidebar (fixed, no scroll)
                build_sidebar(
                    active_route=self.active_route,
                    on_navigate=self.on_navigate,
                    compact=compact_sidebar,
                ),
                # Vertical divider
                ft.VerticalDivider(
                    width=1,
                    color=THEME_TOKENS["colors"]["border_neutral"],
                ),
                # Main content container
                ft.Container(
                    expand=True,
                    bgcolor=colors["background"],
                    content=main_column,
                ),
            ],
        )


def build_app_layout(
    content: ft.Control,
    page_width: float = DESKTOP_BREAKPOINT,
    page_title: str = "Dashboard",
    active_route: str = "/dashboard",
    on_navigate=None,
) -> ft.Control:
    """Convenience function to build AppLayout.

    Args:
        content: The content to display in scrollable area
        page_width: Current page width for responsive sizing
        page_title: Page title for topbar
        active_route: Current active route for sidebar highlighting
        on_navigate: Navigation callback

    Returns:
        A fully constructed AppLayout control
    """
    layout = AppLayout(
        content=content,
        page_width=page_width,
        page_title=page_title,
        active_route=active_route,
        on_navigate=on_navigate,
    )
    return layout.build()
