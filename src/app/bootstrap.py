import flet as ft

from theme.theme import IdilTheme
from views.layout import AppLayoutShell
from views.router import resolve_route


def configure_app(page: ft.Page) -> None:
    """Configure base window settings and render the shared layout shell."""
    page.title = "İDİL HIZLI OKUMA"
    page.padding = 0
    page.clean()
    IdilTheme.apply_to_page(page)

    def navigate(route: str) -> None:
        if page.route != route:
            page.go(route)

    shell = AppLayoutShell(page=page, on_navigate=navigate)

    def render_current_route() -> None:
        active_route = resolve_route(page.route)
        shell.set_route(active_route)
        page.clean()
        page.add(shell.build())
        page.update()

    def on_route_change(_: ft.RouteChangeEvent) -> None:
        normalized_route = resolve_route(page.route)
        if normalized_route != page.route:
            page.go(normalized_route)
            return
        render_current_route()

    page.on_route_change = on_route_change
    page.on_resized = shell.on_resize
    page.go(resolve_route(page.route))
