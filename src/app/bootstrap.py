import flet as ft
import traceback

from theme.theme import IdilTheme
from views.layout import AppLayoutShell
from views.router import resolve_route


def configure_app(page: ft.Page) -> None:
    """Configure base window settings and render the shared layout shell."""
    page.title = "İDİL HIZLI OKUMA"
    page.padding = 0
    page.clean()
    IdilTheme.apply_to_page(page)

    # Add error handler for page events
    def on_page_error(error: Exception) -> None:
        """Log any page-level errors."""
        tb = traceback.format_exc()
        with open('debug_page_error.log', 'a', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write(f"PAGE ERROR: {type(error).__name__}\n")
            f.write("="*70 + "\n")
            f.write(f"{error}\n")
            f.write(tb)
            f.write("\n")
        print("\n" + "="*70)
        print(f"PAGE ERROR: {type(error).__name__}")
        print("="*70)
        print(f"{error}")
        print(tb)
        print("="*70 + "\n")

    page.on_error = on_page_error

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
