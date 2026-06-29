import flet as ft

from app.bootstrap import configure_app


def main(page: ft.Page) -> None:
    """Initialize the app shell for Sprint 01 Epic 1."""
    configure_app(page)


if __name__ == "__main__":
    ft.run(main)
