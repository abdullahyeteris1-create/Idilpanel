"""Progress reports built from lesson records."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import flet as ft

from components import AppDropdown, ContentCard, PageContainer, SecondaryButton
from controllers import build_lesson_controller
from localization.tr import tr_error_message
from theme.theme import THEME_TOKENS


ALL_COURSES = "all"
DAYS_PER_COURSE = 8
EMPTY_LESSON_MESSAGE = "Bu öğrenci için henüz ders kaydı bulunmuyor."


def _text(value: object) -> str:
    return str(value or "").strip()


def _number(value: object) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).strip().replace(",", "."))
    except (TypeError, ValueError):
        return None


def _average(values: list[object]) -> float | None:
    numbers = [number for number in (_number(value) for value in values) if number is not None]
    return sum(numbers) / len(numbers) if numbers else None


def _format_number(value: float | None, suffix: str = "") -> str:
    if value is None:
        return "-"
    rounded = round(value, 1)
    text = str(int(rounded)) if rounded.is_integer() else str(rounded)
    return f"{text}{suffix}"


def _format_speed(value: float | None) -> str:
    formatted = _format_number(value)
    return "-" if formatted == "-" else f"{formatted} kelime/dk"


def _format_percent(value: float | None) -> str:
    formatted = _format_number(value)
    return "-" if formatted == "-" else f"%{formatted}"


def _metric_card(title: str, value: str, subtitle: str = "") -> ft.Control:
    colors = THEME_TOKENS["colors"]
    return ft.Container(
        col={"xs": 12, "sm": 6, "lg": 2},
        content=ContentCard(
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(title, size=12, color=colors["text_secondary"], weight=ft.FontWeight.W_600),
                    ft.Text(value, size=22, color=colors["text_primary"], weight=ft.FontWeight.W_700),
                    ft.Text(subtitle, size=11, color=colors["text_secondary"]),
                ],
            )
        ),
    )


def _empty_state(message: str) -> ft.Control:
    colors = THEME_TOKENS["colors"]
    return ContentCard(
        content=ft.Container(
            height=180,
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.QUERY_STATS, size=38, color=colors["text_secondary"]),
                    ft.Text(message, size=14, color=colors["text_secondary"], text_align=ft.TextAlign.CENTER),
                ],
            ),
        )
    )


def _chart_empty_state(message: str) -> ft.Control:
    colors = THEME_TOKENS["colors"]
    return ft.Container(
        height=180,
        alignment=ft.Alignment(0, 0),
        border_radius=8,
        bgcolor=colors["background"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        content=ft.Text(message, size=13, color=colors["text_secondary"], text_align=ft.TextAlign.CENTER),
    )


def _progress_chart(
    title: str,
    subtitle: str,
    points: list[dict[str, Any]],
    field: str,
    color: str,
    suffix: str = "",
    fixed_max: float | None = None,
) -> ft.Control:
    colors = THEME_TOKENS["colors"]
    values = [float(point[field]) for point in points if point.get(field) is not None]
    if not values:
        return ContentCard(title=title, subtitle=subtitle, content=_chart_empty_state("Bu grafik icin yeterli veri yok."))

    maximum = fixed_max or max(values)
    minimum = 0.0
    if maximum <= 0:
        maximum = 1.0

    columns: list[ft.Control] = []
    for point in points:
        raw_value = point.get(field)
        value = float(raw_value) if raw_value is not None else 0.0
        ratio = 0.0 if raw_value is None else (value - minimum) / (maximum - minimum)
        height = max(10, int(min(1.0, max(0.0, ratio)) * 132))
        value_label = _format_number(value, suffix) if raw_value is not None else "-"
        columns.append(
            ft.Container(
                expand=True,
                content=ft.Column(
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Text(value_label, size=10, color=colors["text_secondary"], no_wrap=True),
                        ft.Container(
                            height=144,
                            alignment=ft.Alignment(0, 1),
                            content=ft.Container(
                                width=28,
                                height=height,
                                border_radius=ft.BorderRadius(6, 6, 3, 3),
                                bgcolor=color if raw_value is not None else colors["border"],
                            ),
                        ),
                        ft.Container(
                            width=48,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Text(f"{point['day']}. Gün", size=10, color=colors["text_secondary"], no_wrap=True),
                        ),
                    ],
                ),
            )
        )

    chart_body = ft.Column(
        spacing=8,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(_format_number(maximum, suffix), size=10, color=colors["text_secondary"]),
                    ft.Text("Günlük ortalama", size=10, color=colors["text_secondary"]),
                ],
            ),
            ft.Container(
                height=208,
                padding=ft.Padding(8, 10, 8, 4),
                border_radius=8,
                bgcolor=colors["background"],
                border=ft.Border(
                    top=ft.BorderSide(1, colors["border"]),
                    right=ft.BorderSide(1, colors["border"]),
                    bottom=ft.BorderSide(1, colors["border"]),
                    left=ft.BorderSide(1, colors["border"]),
                ),
                content=ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    controls=columns,
                ),
            ),
        ],
    )
    return ContentCard(title=title, subtitle=subtitle, content=chart_body)


def _daily_points(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        try:
            day = int(record.get("gun_no") or 1)
        except (TypeError, ValueError):
            day = 1
        if day > 0:
            grouped[day].append(record)

    points: list[dict[str, Any]] = []
    for day in sorted(grouped):
        day_records = grouped[day]
        points.append(
            {
                "day": day,
                "count": len(day_records),
                "speed": _average([record.get("okuma_hizi") for record in day_records]),
                "comprehension": _average([record.get("anlama_algi") for record in day_records]),
                "focus": _average([record.get("focus_percent") for record in day_records]),
            }
        )
    return points


def _summaries(points: list[dict[str, Any]]) -> dict[str, str]:
    speed_points = [point for point in points if point.get("speed") is not None]
    first_speed = speed_points[0]["speed"] if speed_points else None
    last_speed = speed_points[-1]["speed"] if speed_points else None
    speed_growth = None
    if first_speed and last_speed is not None:
        speed_growth = ((float(last_speed) - float(first_speed)) / float(first_speed)) * 100

    return {
        "days": f"{len(points)} / {DAYS_PER_COURSE}",
        "first_speed": _format_speed(first_speed),
        "last_speed": _format_speed(last_speed),
        "speed_growth": _format_percent(speed_growth),
        "avg_comprehension": _format_percent(_average([point.get("comprehension") for point in points])),
        "avg_focus": _format_percent(_average([point.get("focus") for point in points])),
    }


def build_progress_reports_page() -> ft.Control:
    """Build progress reports from saved lesson records."""
    controller = build_lesson_controller()
    colors = THEME_TOKENS["colors"]

    state: dict[str, Any] = {
        "students": [],
        "courses": [],
        "records": [],
    }

    student_dropdown = AppDropdown(label="Öğrenci Seç", options=[], hint_text="Öğrenci seçin")
    course_dropdown = AppDropdown(label="Kur Seç", options=[], hint_text="Tüm kurlar", disabled=True)
    status_text = ft.Text("", size=12, color=colors["text_secondary"])
    metrics_row = ft.ResponsiveRow(columns=12, spacing=12, run_spacing=12)
    charts_column = ft.Column(spacing=16, expand=True)

    def _selected_student_id() -> int | None:
        value = _text(student_dropdown.value)
        return int(value) if value else None

    def _selected_course_id() -> int | None:
        value = _text(course_dropdown.value)
        if not value or value == ALL_COURSES:
            return None
        return int(value)

    def _refresh_students() -> None:
        students = list(controller.list_active_students(limit=500, offset=0))
        state["students"] = students
        student_dropdown.options = [
            ft.dropdown.Option(
                key=str(record.get("id")),
                text=_text(record.get("ad_soyad")) or f"Öğrenci {record.get('id')}",
            )
            for record in students
        ]
        if not student_dropdown.value and students:
            student_dropdown.value = str(students[0].get("id"))

    def _refresh_courses() -> None:
        student_id = _selected_student_id()
        if student_id is None:
            state["courses"] = []
            course_dropdown.options = []
            course_dropdown.value = None
            course_dropdown.disabled = True
            return

        courses = list(controller.list_courses(student_id=student_id, limit=500, offset=0))
        state["courses"] = courses
        if not courses:
            course_dropdown.options = []
            course_dropdown.value = None
            course_dropdown.disabled = True
            return

        options = [ft.dropdown.Option(key=ALL_COURSES, text="Tüm kurlar")]
        options.extend(
            ft.dropdown.Option(key=str(record.get("id")), text=f"{record.get('kur_no')}. Kur")
            for record in courses
        )
        course_dropdown.options = options
        course_dropdown.disabled = False
        if not course_dropdown.value or not any(option.key == course_dropdown.value for option in options):
            course_dropdown.value = ALL_COURSES

    def _load_records() -> list[dict[str, Any]]:
        student_id = _selected_student_id()
        if student_id is None:
            return []

        course_id = _selected_course_id()
        if course_id is not None:
            return list(controller.list_course_lessons(course_id))
        return list(controller.list_student_lessons(student_id))

    def _render() -> None:
        records = _load_records()
        state["records"] = records
        points = _daily_points(records)
        summary = _summaries(points)

        metrics_row.controls = [
            _metric_card("Tamamlanan Gün", summary["days"], "Ders kaydı olan gün"),
            _metric_card("İlk Okuma Hızı", summary["first_speed"], "İlk gün ortalaması"),
            _metric_card("Son Okuma Hızı", summary["last_speed"], "Son gün ortalaması"),
            _metric_card("Hız Artış Oranı", summary["speed_growth"], "İlk-son hız farkı"),
            _metric_card("Ortalama Anlama", summary["avg_comprehension"], "Günlük ortalama"),
            _metric_card("Ortalama Odaklanma", summary["avg_focus"], "Günlük ortalama"),
        ]

        if not records:
            charts_column.controls = [_empty_state(EMPTY_LESSON_MESSAGE)]
        else:
            charts_column.controls = [
                _progress_chart(
                    "Okuma Hızı Gelişim Grafiği",
                    "Günlere göre kelime/dk değişimi",
                    points,
                    "speed",
                    colors["primary"],
                ),
                _progress_chart(
                    "Anlama Oranı Grafiği",
                    "Günlere göre anlama yüzdesi",
                    points,
                    "comprehension",
                    colors["secondary"],
                    "%",
                    fixed_max=100,
                ),
                _progress_chart(
                    "Odaklanma Grafiği",
                    "Günlere göre odaklanma yüzdesi",
                    points,
                    "focus",
                    colors["purple"],
                    "%",
                    fixed_max=100,
                ),
            ]

        status_text.value = f"{len(records)} ders kaydı | {len(points)} gün"

    def _update_page(page: ft.Page | None) -> None:
        if page is not None:
            page.update()

    def _handle_student_change(e: ft.ControlEvent) -> None:
        course_dropdown.value = None
        _refresh_courses()
        _render()
        _update_page(e.page)

    def _handle_course_change(e: ft.ControlEvent) -> None:
        _render()
        _update_page(e.page)

    def _handle_refresh(e: ft.ControlEvent) -> None:
        _refresh_students()
        _refresh_courses()
        _render()
        _update_page(e.page)

    student_dropdown.on_select = _handle_student_change
    course_dropdown.on_select = _handle_course_change

    try:
        _refresh_students()
        _refresh_courses()
        _render()
    except Exception as exc:
        status_text.value = tr_error_message(exc)
        metrics_row.controls = []
        charts_column.controls = [_empty_state("Gelişim verileri yüklenemedi.")]

    filters = ContentCard(
        title="Filtreler",
        subtitle="Veriler Ders Kayıtları ekranındaki kayıtlardan otomatik hesaplanır.",
        action=SecondaryButton(label="Yenile", icon=ft.Icons.REFRESH, on_click=_handle_refresh),
        content=ft.ResponsiveRow(
            columns=12,
            spacing=12,
            run_spacing=12,
            controls=[
                ft.Container(col={"xs": 12, "md": 5}, content=student_dropdown),
                ft.Container(col={"xs": 12, "md": 4}, content=course_dropdown),
                ft.Container(col={"xs": 12, "md": 3}, alignment=ft.Alignment(0, 0), content=status_text),
            ],
        ),
    )

    body = ft.Column(
        spacing=16,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("Gelişim Raporları", size=24, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
            filters,
            metrics_row,
            charts_column,
        ],
    )

    return PageContainer(content=body, max_width=1888, padding=24)
