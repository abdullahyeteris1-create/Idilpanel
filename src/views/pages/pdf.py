"""PDF page skeleton."""

import flet as ft

from views.pages.placeholder import build_page_placeholder


def build_pdf_page() -> ft.Control:
    """Build PDF page placeholder content."""
    return build_page_placeholder("PDF")
