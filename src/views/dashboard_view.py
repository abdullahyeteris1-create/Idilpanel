"""Dashboard integration view composed from reusable UI components."""

from __future__ import annotations

from datetime import date, datetime

import flet as ft

from components.action_panel import build_action_panel, build_dashboard_action_panel_placeholders
from components.chart_card import build_dashboard_chart_card_placeholders
from components.latest_measurements_card import build_latest_measurements_card
from components.sidebar import build_sidebar_component
from components.statistic_card import build_statistic_card
from components.todays_lessons_card import build_todays_lessons_card
from components.topbar import build_topbar_component
from components.upcoming_lessons_card import build_upcoming_lessons_card
from controllers import (
    build_course_controller,
    build_lesson_controller,
    build_measurement_controller,
    build_schedule_controller,
    build_student_controller,
)
from theme.theme import THEME_TOKENS


DESKTOP_BREAKPOINT = 1366
TABLET_BREAKPOINT = 768
DATA_LIMIT = 1000


class DashboardView:
    """Build dashboard by integrating existing reusable components only."""

    def __init__(self, on_navigate) -> None:
        self._on_navigate = on_navigate
        self._student_controller = build_student_controller()
        self._course_controller = build_course_controller()
        self._schedule_controller = build_schedule_controller()
        self._lesson_controller = build_lesson_controller()
        self._measurement_controller = build_measurement_controller()

    @staticmethod
    def _safe_int(value: object, default: int = 0) -> int:
        try:
            return int(str(value).strip())
        except (TypeError, ValueError, AttributeError):
            return default

    @staticmethod
    def _safe_float(value: object, default: float = 0.0) -> float:
        try:
            return float(str(value).strip())
        except (TypeError, ValueError, AttributeError):
            return default

    @staticmethod
    def _parse_date(value: object) -> date | None:
        text = str(value or "").strip()
        if not text:
            return None

        for parser in (date.fromisoformat, DashboardView._parse_datetime_to_date):
            try:
                return parser(text)
            except ValueError:
                continue
        return None

    @staticmethod
    def _parse_datetime_to_date(value: str) -> date:
        return datetime.fromisoformat(value).date()

    @staticmethod
    def _parse_time(value: object) -> datetime | None:
        text = str(value or "").strip()
        if not text:
            return None
        for time_format in ("%H:%M", "%H:%M:%S"):
            try:
                parsed = datetime.strptime(text, time_format)
                return parsed
            except ValueError:
                continue
        return None

    @staticmethod
    def _normalized_status(raw_status: object) -> str:
        text = str(raw_status or "").strip().casefold()
        if text == "tamamlandi":
            return "Tamamlandi"
        if text in {"iptal", "gelmedi"}:
            return "Iptal"
        if text in {"yarim kaldi", "yarimkaldi", "devam ediyor", "devam_ediyor"}:
            return "Devam Ediyor"
        return "Bekliyor"

    def _load_students(self) -> list[dict]:
        try:
            return list(self._student_controller.list_students(limit=DATA_LIMIT, offset=0))
        except Exception:
            return []

    def _load_courses(self) -> list[dict]:
        try:
            return list(self._course_controller.list_courses(limit=DATA_LIMIT, offset=0))
        except Exception:
            return []

    def _load_schedules(self) -> list[dict]:
        try:
            return list(self._schedule_controller.list_schedules(limit=DATA_LIMIT, offset=0))
        except Exception:
            return []

    def _load_measurements(self) -> list[dict]:
        try:
            return list(self._measurement_controller.list_measurements(limit=DATA_LIMIT, offset=0))
        except Exception:
            return []

    @staticmethod
    def _is_active_record(record: dict) -> bool:
        return int(record.get("is_active", 1) or 1) == 1

    def _load_dashboard_data(self) -> dict[str, list[dict]]:
        students = self._load_students()
        courses = self._load_courses()
        schedules = self._load_schedules()
        measurements = self._load_measurements()

        lessons: list[dict]
        try:
            lessons = list(self._lesson_controller.list_lessons(limit=DATA_LIMIT, offset=0))
        except Exception:
            lessons = []

        return {
            "students": students,
            "courses": courses,
            "schedules": schedules,
            "measurements": measurements,
            "lessons": lessons,
        }

    def _build_dashboard_statistics(self, students: list[dict], courses: list[dict], schedules: list[dict]) -> list[ft.Container]:
        today = date.today()

        active_courses = [record for record in courses if str(record.get("durum") or "Aktif").strip() == "Aktif"]
        todays_schedules = [
            record for record in schedules if self._parse_date(record.get("plan_tarihi")) == today and self._is_active_record(record)
        ]
        completed_lessons = [record for record in schedules if str(record.get("durum") or "").strip() == "Tamamlandi"]

        return [
            build_statistic_card(
                ft.Icons.PERSON,
                "Toplam Ogrenci",
                str(len(students)),
                "Kayitli aktif ogrenciler",
                "flat",
            ),
            build_statistic_card(
                ft.Icons.SCHOOL,
                "Aktif Kurs",
                str(len(active_courses)),
                "Aktif kur sayisi",
                "flat",
            ),
            build_statistic_card(
                ft.Icons.CALENDAR_MONTH,
                "Bugunku Ders",
                str(len(todays_schedules)),
                "Bugune planlanan dersler",
                "flat",
            ),
            build_statistic_card(
                ft.Icons.CHECK_CIRCLE,
                "Tamamlanan Ders",
                str(len(completed_lessons)),
                "Tum zamanlar toplam",
                "flat",
            ),
        ]

    def _build_todays_lessons(self, schedules: list[dict], student_map: dict[int, str], course_map: dict[int, str]) -> list[dict[str, str]]:
        today = date.today()
        now = datetime.now()
        rows: list[dict[str, str]] = []

        for record in schedules:
            if not self._is_active_record(record):
                continue
            if self._parse_date(record.get("plan_tarihi")) != today:
                continue

            start_time = str(record.get("baslangic_saati") or "--:--").strip() or "--:--"
            end_dt = self._parse_time(record.get("bitis_saati"))

            status = self._normalized_status(record.get("durum"))
            if status == "Bekliyor":
                start_dt = self._parse_time(record.get("baslangic_saati"))
                if start_dt and end_dt:
                    start_time_today = now.replace(
                        hour=start_dt.hour,
                        minute=start_dt.minute,
                        second=0,
                        microsecond=0,
                    )
                    end_time_today = now.replace(
                        hour=end_dt.hour,
                        minute=end_dt.minute,
                        second=0,
                        microsecond=0,
                    )
                    if start_time_today <= now <= end_time_today:
                        status = "Devam Ediyor"

            student_id = self._safe_int(record.get("student_id"))
            course_id = self._safe_int(record.get("course_id"))

            rows.append(
                {
                    "time": start_time,
                    "student": student_map.get(student_id, f"Ogrenci {student_id}"),
                    "course": course_map.get(course_id, "Kurs"),
                    "status": status,
                }
            )

        rows.sort(key=lambda item: item.get("time", "99:99"))
        return rows[:6]

    def _build_upcoming_lessons(self, schedules: list[dict], student_map: dict[int, str], course_map: dict[int, str]) -> list[dict[str, str]]:
        today = date.today()
        tomorrow = today.fromordinal(today.toordinal() + 1)
        now = datetime.now()
        upcoming: list[tuple[datetime, dict[str, str]]] = []

        for record in schedules:
            if not self._is_active_record(record):
                continue

            lesson_date = self._parse_date(record.get("plan_tarihi"))
            if lesson_date is None or lesson_date < today:
                continue

            start_dt = self._parse_time(record.get("baslangic_saati"))
            if start_dt is None:
                continue

            lesson_start = datetime(
                lesson_date.year,
                lesson_date.month,
                lesson_date.day,
                start_dt.hour,
                start_dt.minute,
            )
            if lesson_start < now:
                continue

            if lesson_date == tomorrow:
                remaining = "Yarin"
            else:
                minutes = int((lesson_start - now).total_seconds() // 60)
                if minutes < 60:
                    remaining = f"{minutes} dk"
                else:
                    hours = max(1, round(minutes / 60))
                    remaining = "1 Saat" if hours == 1 else f"{hours} Saat"

            student_id = self._safe_int(record.get("student_id"))
            course_id = self._safe_int(record.get("course_id"))
            upcoming.append(
                (
                    lesson_start,
                    {
                        "time": str(record.get("baslangic_saati") or "--:--").strip() or "--:--",
                        "student": student_map.get(student_id, f"Ogrenci {student_id}"),
                        "course": course_map.get(course_id, "Kurs"),
                        "remaining": remaining,
                    },
                )
            )

        upcoming.sort(key=lambda item: item[0])
        return [record for _, record in upcoming[:6]]

    def _build_latest_measurements(
        self,
        measurements: list[dict],
        courses: list[dict],
        students: list[dict],
        lessons: list[dict],
    ) -> list[dict]:
        student_map = {self._safe_int(row.get("id")): str(row.get("ad_soyad") or "-") for row in students}
        course_student_map = {self._safe_int(row.get("id")): self._safe_int(row.get("student_id")) for row in courses}
        lesson_course_map = {
            self._safe_int(row.get("id")): self._safe_int(row.get("course_id")) for row in lessons
        }
        lesson_date_map = {
            self._safe_int(row.get("id")): str(row.get("tarih") or "-") for row in lessons
        }

        ordered = sorted(measurements, key=lambda row: self._safe_int(row.get("id")), reverse=True)
        speed_cache_by_student: dict[int, float] = {}
        rows: list[dict] = []

        for record in ordered:
            lesson_id = self._safe_int(record.get("lesson_id"))
            course_id = lesson_course_map.get(lesson_id, 0)
            student_id = course_student_map.get(course_id, 0)

            speed = self._safe_float(record.get("okuma_hizi"), 0.0)
            understanding = self._safe_int(round(self._safe_float(record.get("anlama"), 0.0)), 0)

            previous_speed = speed_cache_by_student.get(student_id)
            if previous_speed is None:
                trend = "flat"
            elif speed > previous_speed:
                trend = "up"
            elif speed < previous_speed:
                trend = "down"
            else:
                trend = "flat"

            speed_cache_by_student[student_id] = speed

            rows.append(
                {
                    "date": lesson_date_map.get(lesson_id, str(record.get("created_at") or "-")[:10]),
                    "student": student_map.get(student_id, f"Ogrenci {student_id}"),
                    "speed": str(int(speed)) if speed else "0",
                    "speed_trend": trend,
                    "understanding": max(0, min(100, understanding)),
                }
            )

            if len(rows) >= 6:
                break

        return rows

    def _build_action_items(self) -> list[dict]:
        def go(route: str):
            return lambda _: self._on_navigate(route)

        actions = build_dashboard_action_panel_placeholders()
        route_map = {
            "new-student": "/students",
            "new-lesson": "/lesson-records",
            "new-measurement": "/measurements",
            "new-report": "/progress-reports",
        }

        for action in actions:
            key = str(action.get("key") or "")
            route = route_map.get(key)
            if route:
                action["on_click"] = go(route)
        return actions

    def _build_statistic_area(self, students: list[dict], courses: list[dict], schedules: list[dict]) -> ft.Control:
        cards = self._build_dashboard_statistics(students, courses, schedules)
        return ft.ResponsiveRow(
            spacing=16,
            run_spacing=16,
            controls=[ft.Container(col={"xs": 12, "sm": 6, "md": 6, "lg": 3}, content=card) for card in cards],
        )

    def _build_chart_area(self) -> ft.Control:
        cards = build_dashboard_chart_card_placeholders()
        return ft.ResponsiveRow(
            spacing=24,
            run_spacing=24,
            controls=[ft.Container(col={"xs": 12, "md": 12, "lg": 6}, content=card) for card in cards],
        )

    def _build_lessons_area(self, schedules: list[dict], student_map: dict[int, str], course_map: dict[int, str]) -> ft.Control:
        todays_rows = self._build_todays_lessons(schedules, student_map, course_map)
        upcoming_rows = self._build_upcoming_lessons(schedules, student_map, course_map)

        return ft.ResponsiveRow(
            spacing=24,
            run_spacing=24,
            controls=[
                ft.Container(
                    col={"xs": 12, "md": 12, "lg": 6},
                    content=build_todays_lessons_card(todays_rows),
                ),
                ft.Container(
                    col={"xs": 12, "md": 12, "lg": 6},
                    content=build_upcoming_lessons_card(upcoming_rows),
                ),
            ],
        )

    def _build_bottom_area(
        self,
        measurements: list[dict],
        courses: list[dict],
        students: list[dict],
        lessons: list[dict],
    ) -> ft.Control:
        measurement_rows = self._build_latest_measurements(measurements, courses, students, lessons)

        return ft.ResponsiveRow(
            spacing=24,
            run_spacing=24,
            controls=[
                ft.Container(
                    col={"xs": 12, "md": 12, "lg": 6},
                    content=build_latest_measurements_card(measurement_rows),
                ),
                ft.Container(
                    col={"xs": 12, "md": 12, "lg": 6},
                    content=build_action_panel(
                        title="Hizli Islemler",
                        subtitle="Sik kullanilan islemler",
                        actions=self._build_action_items(),
                    ),
                ),
            ],
        )

    def _build_content(self) -> ft.Control:
        spacing = THEME_TOKENS["spacing"]
        data = self._load_dashboard_data()

        students = data["students"]
        courses = data["courses"]
        schedules = data["schedules"]
        measurements = data["measurements"]
        lessons = data["lessons"]

        student_map = {self._safe_int(row.get("id")): str(row.get("ad_soyad") or "-") for row in students}
        course_map = {self._safe_int(row.get("id")): f"Kur {self._safe_int(row.get('kur_no'), 0)}" for row in courses}

        return ft.Container(
            expand=True,
            padding=spacing["lg"],
            content=ft.Column(
                spacing=spacing["lg"],
                controls=[
                    self._build_statistic_area(students, courses, schedules),
                    self._build_chart_area(),
                    self._build_lessons_area(schedules, student_map, course_map),
                    self._build_bottom_area(measurements, courses, students, lessons),
                ],
            ),
        )

    def build(self, viewport_width: int | float | None = None) -> ft.Control:
        colors = THEME_TOKENS["colors"]

        width = viewport_width if viewport_width is not None else DESKTOP_BREAKPOINT

        main_column = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                build_topbar_component(route="/dashboard", notification_count=3),
                self._build_content(),
            ],
        )

        if width < TABLET_BREAKPOINT:
            return ft.Container(expand=True, bgcolor=colors["background"], content=main_column)

        return ft.Row(
            spacing=0,
            expand=True,
            controls=[
                build_sidebar_component(active_route="/dashboard", on_navigate=self._on_navigate),
                ft.Container(
                    expand=True,
                    bgcolor=colors["background"],
                    content=main_column,
                ),
            ],
        )
