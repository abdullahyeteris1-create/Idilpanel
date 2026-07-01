"""Simple visual weekly schedule MVP screen with direct SQLite persistence."""

from __future__ import annotations

from typing import Any

import flet as ft

from database.connection_manager import db_manager


DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
SLOT_COUNT = 9
TIME_OPTIONS = [
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
    "21:30",
    "22:00",
]
DAY_COLORS: dict[str, dict[str, str]] = {
    "Pazartesi": {"header": "#DBEAFE", "card": "#EFF6FF", "border": "#93C5FD", "text": "#1D4ED8"},
    "Salı": {"header": "#DCFCE7", "card": "#F0FDF4", "border": "#86EFAC", "text": "#15803D"},
    "Çarşamba": {"header": "#FEF3C7", "card": "#FFFBEB", "border": "#FCD34D", "text": "#B45309"},
    "Perşembe": {"header": "#EDE9FE", "card": "#F5F3FF", "border": "#C4B5FD", "text": "#6D28D9"},
    "Cuma": {"header": "#CCFBF1", "card": "#F0FDFA", "border": "#5EEAD4", "text": "#0F766E"},
    "Cumartesi": {"header": "#FFEDD5", "card": "#FFF7ED", "border": "#FDBA74", "text": "#C2410C"},
    "Pazar": {"header": "#FCE7F3", "card": "#FDF2F8", "border": "#F9A8D4", "text": "#BE185D"},
}


def _text(value: object) -> str:
    return str(value or "").strip()


def _border(color: str = "#D1D5DB", width: int = 1) -> ft.Border:
    return ft.Border(
        top=ft.BorderSide(width, color),
        right=ft.BorderSide(width, color),
        bottom=ft.BorderSide(width, color),
        left=ft.BorderSide(width, color),
    )


def _ensure_schema() -> None:
    schema_path = db_manager.config.db_path.parent / "schema.sql"
    with db_manager.connection_scope() as connection:
        has_students = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'students'"
        ).fetchone()
        if not has_students:
            connection.executescript(schema_path.read_text(encoding="utf-8"))

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS weekly_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_name TEXT NOT NULL,
                slot_index INTEGER NOT NULL,
                student_id INTEGER,
                student_name TEXT,
                lesson_time TEXT,
                note TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def _load_students() -> list[dict[str, Any]]:
    _ensure_schema()
    with db_manager.connection_scope() as connection:
        rows = connection.execute(
            """
            SELECT id, ad_soyad, sinif
            FROM students
            WHERE is_active = 1
            ORDER BY ad_soyad ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def _load_schedule() -> dict[tuple[str, int], dict[str, Any]]:
    _ensure_schema()
    with db_manager.connection_scope() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM weekly_schedule
            ORDER BY day_name ASC, slot_index ASC, id DESC
            """
        ).fetchall()

    schedule: dict[tuple[str, int], dict[str, Any]] = {}
    for row in rows:
        record = dict(row)
        key = (_text(record.get("day_name")), int(record.get("slot_index") or 0))
        if key not in schedule:
            schedule[key] = record
    return schedule


def _student_name(student_id: int, students: list[dict[str, Any]]) -> str:
    for student in students:
        if int(student.get("id") or 0) == student_id:
            return _text(student.get("ad_soyad"))
    return ""


def _save_slot(day_name: str, slot_index: int, student_id: int, lesson_time: str, note: str = "") -> None:
    _ensure_schema()
    students = _load_students()
    name = _student_name(student_id, students)
    with db_manager.connection_scope() as connection:
        connection.execute(
            "DELETE FROM weekly_schedule WHERE day_name = ? AND slot_index = ?",
            (day_name, slot_index),
        )
        connection.execute(
            """
            INSERT INTO weekly_schedule (day_name, slot_index, student_id, student_name, lesson_time, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (day_name, slot_index, student_id, name, lesson_time, note),
        )


def _clear_slot(day_name: str, slot_index: int) -> None:
    _ensure_schema()
    with db_manager.connection_scope() as connection:
        connection.execute(
            "DELETE FROM weekly_schedule WHERE day_name = ? AND slot_index = ?",
            (day_name, slot_index),
        )


def build_weekly_program_mvp_page() -> ft.Control:
    students = _load_students()
    schedule = _load_schedule()
    message = ft.Text("", size=12, color="#374151")

    student_options = [
        ft.dropdown.Option(str(student["id"]), _text(student.get("ad_soyad")) or f"Öğrenci {student['id']}")
        for student in students
    ]

    def show_message(text: str, page: ft.Page | None = None) -> None:
        message.value = text
        if page:
            page.update()

    def build_slot(day_name: str, slot_index: int) -> ft.Container:
        colors = DAY_COLORS[day_name]
        slot_key = (day_name, slot_index)
        slot = ft.Container(height=64)

        def render_empty() -> None:
            slot.height = 64
            slot.bgcolor = "#F9FAFB"
            slot.border = _border("#E5E7EB")
            slot.border_radius = 8
            slot.padding = 6
            slot.alignment = ft.Alignment(0, 0)
            slot.on_click = lambda e: render_editor(e.page)
            slot.content = ft.Column(
                tight=True,
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.ADD, size=18, color="#6B7280"),
                    ft.Text("Ders Ekle", size=11, color="#6B7280", weight=ft.FontWeight.W_600),
                ],
            )

        def render_filled(record: dict[str, Any]) -> None:
            slot.height = 64
            slot.bgcolor = colors["card"]
            slot.border = _border(colors["border"])
            slot.border_radius = 8
            slot.padding = ft.Padding(7, 5, 5, 5)
            slot.alignment = ft.Alignment(-1, 0)
            slot.on_click = None
            slot.content = ft.Row(
                spacing=3,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            tight=True,
                            spacing=2,
                            controls=[
                                ft.Text(
                                    _text(record.get("student_name")) or "Öğrenci",
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color="#111827",
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(
                                    _text(record.get("lesson_time")) or "-",
                                    size=12,
                                    color=colors["text"],
                                    weight=ft.FontWeight.W_600,
                                ),
                            ],
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_size=16,
                        tooltip="Düzenle",
                        on_click=lambda e: render_editor(e.page, record),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_size=16,
                        icon_color="#DC2626",
                        tooltip="Sil",
                        on_click=handle_clear,
                    ),
                ],
            )

        def render_editor(page: ft.Page | None = None, record: dict[str, Any] | None = None) -> None:
            record = record or schedule.get(slot_key, {})
            student_dropdown = ft.Dropdown(
                value=str(record.get("student_id") or "") or None,
                options=list(student_options),
                height=34,
                text_size=11,
                content_padding=ft.Padding(7, 2, 7, 2),
            )
            time_field = ft.Dropdown(
                hint_text="Saat",
                value=_text(record.get("lesson_time")) or None,
                options=[ft.dropdown.Option(value) for value in TIME_OPTIONS],
                height=32,
                text_size=12,
                content_padding=ft.Padding(7, 2, 7, 2),
            )

            def handle_save(e: ft.ControlEvent) -> None:
                raw_student_id = _text(student_dropdown.value)
                lesson_time = _text(time_field.value)
                if not raw_student_id:
                    show_message("Öğrenci seçin.", e.page)
                    return
                if not lesson_time:
                    show_message("Saat seçin.", e.page)
                    return
                try:
                    student_id = int(raw_student_id)
                    _save_slot(day_name, slot_index, student_id, lesson_time)
                    saved_record = {
                        "day_name": day_name,
                        "slot_index": slot_index,
                        "student_id": student_id,
                        "student_name": _student_name(student_id, students),
                        "lesson_time": lesson_time,
                        "note": "",
                    }
                    schedule[slot_key] = saved_record
                    render_filled(saved_record)
                    show_message(f"{day_name} {slot_index}. slot kaydedildi.", e.page)
                except Exception as exc:
                    show_message(f"Hata: {exc}", e.page)

            def handle_cancel(e: ft.ControlEvent) -> None:
                existing = schedule.get(slot_key)
                if existing:
                    render_filled(existing)
                else:
                    render_empty()
                if e.page:
                    e.page.update()

            slot.height = 118
            slot.bgcolor = "#FFFFFF"
            slot.border = _border(colors["border"], 2)
            slot.border_radius = 8
            slot.padding = 5
            slot.alignment = ft.Alignment(0, 0)
            slot.on_click = None
            slot.content = ft.Column(
                spacing=4,
                controls=[
                    student_dropdown,
                    time_field,
                    ft.Row(
                        spacing=2,
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.IconButton(icon=ft.Icons.SAVE, icon_size=16, tooltip="Kaydet", on_click=handle_save),
                            ft.IconButton(icon=ft.Icons.CLOSE, icon_size=16, tooltip="Vazgeç", on_click=handle_cancel),
                        ],
                    ),
                ],
            )
            if page:
                page.update()

        def handle_clear(e: ft.ControlEvent) -> None:
            try:
                _clear_slot(day_name, slot_index)
                schedule.pop(slot_key, None)
                render_empty()
                show_message(f"{day_name} {slot_index}. slot silindi.", e.page)
            except Exception as exc:
                show_message(f"Hata: {exc}", e.page)

        saved = schedule.get(slot_key)
        if saved:
            render_filled(saved)
        else:
            render_empty()
        return slot

    def build_day(day_name: str) -> ft.Control:
        colors = DAY_COLORS[day_name]
        return ft.Container(
            expand=True,
            bgcolor="#FFFFFF",
            border=_border("#D1D5DB"),
            border_radius=8,
            padding=5,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Container(
                        height=30,
                        bgcolor=colors["header"],
                        border_radius=6,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(day_name, size=13, weight=ft.FontWeight.BOLD, color=colors["text"]),
                    ),
                    *[build_slot(day_name, slot_index) for slot_index in range(1, SLOT_COUNT + 1)],
                ],
            ),
        )

    schedule_grid = ft.Row(
        expand=True,
        spacing=7,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[build_day(day_name) for day_name in DAYS],
    )

    empty_warning = ft.Text(
        "Kayıtlı aktif öğrenci yok. Önce Öğrenci Yönetimi ekranından öğrenci ekleyin.",
        size=12,
        color="#B45309",
        visible=not bool(students),
    )

    page = ft.Container(
        expand=True,
        bgcolor="#F3F4F6",
        padding=10,
        content=ft.Column(
            expand=True,
            spacing=7,
            controls=[
                ft.Text("Haftalık Ders Programı", size=22, weight=ft.FontWeight.BOLD),
                empty_warning,
                message,
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[schedule_grid],
                    ),
                ),
            ],
        ),
    )
    page.data = {"canonical": "weekly_program_mvp", "days": len(DAYS), "slots_per_day": SLOT_COUNT}
    return page
