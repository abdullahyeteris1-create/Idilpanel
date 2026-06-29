"""Routing registry for shared application pages."""

from collections.abc import Callable

import flet as ft

from views.pages.courses import build_courses_page
from views.pages.dashboard import build_dashboard_page
from views.pages.lesson_records import build_lesson_records_page
from views.pages.pdf import build_pdf_page
from views.pages.progress_reports import build_progress_reports_page
from views.pages.settings import build_settings_page
from views.pages.students import build_students_page
from views.pages.weekly_program import build_weekly_program_page


RouteBuilder = Callable[[], ft.Control]


ROUTE_REGISTRY: dict[str, dict[str, str | RouteBuilder]] = {
    "/dashboard": {"title": "Dashboard", "builder": build_dashboard_page},
    "/weekly-program": {"title": "Haftalik Program", "builder": build_weekly_program_page},
    "/students": {"title": "Ogrenciler", "builder": build_students_page},
    "/courses": {"title": "Kurslar", "builder": build_courses_page},
    "/lesson-records": {"title": "Ders Kayitlari", "builder": build_lesson_records_page},
    "/progress-reports": {"title": "Gelisim Raporlari", "builder": build_progress_reports_page},
    "/pdf": {"title": "PDF", "builder": build_pdf_page},
    "/settings": {"title": "Ayarlar", "builder": build_settings_page},
}


def resolve_route(route: str | None) -> str:
    """Resolve unknown paths to the dashboard route."""
    if not route or route == "/":
        return "/dashboard"
    return route if route in ROUTE_REGISTRY else "/dashboard"


def get_page_title(route: str) -> str:
    """Get topbar title for the active route."""
    resolved = resolve_route(route)
    return str(ROUTE_REGISTRY[resolved]["title"])


def build_route_content(route: str) -> ft.Control:
    """Build content control for the active route."""
    resolved = resolve_route(route)
    builder = ROUTE_REGISTRY[resolved]["builder"]
    return builder()
