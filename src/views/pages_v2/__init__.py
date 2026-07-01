"""V2 page package exports."""

from .dashboard_page_v2 import build_dashboard_page_v2
from .students_page_v2 import build_students_page_v2
from .weekly_program_page_v2 import build_weekly_program_page_v2
from .lesson_records_page_v2 import build_lesson_records_page_v2
from .measurements_page_v2 import build_measurements_page_v2
from .progress_reports_page_v2 import build_progress_reports_page_v2
from .parent_reports_page_v2 import build_parent_reports_page_v2
from .settings_page_v2 import build_settings_page_v2

__all__ = [
    "build_dashboard_page_v2",
    "build_students_page_v2",
    "build_weekly_program_page_v2",
    "build_lesson_records_page_v2",
    "build_measurements_page_v2",
    "build_progress_reports_page_v2",
    "build_parent_reports_page_v2",
    "build_settings_page_v2",
]
