"""Simple visual weekly schedule MVP screen with direct SQLite persistence."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import flet as ft

from database.connection_manager import db_manager


DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
SLOT_COUNT = 9
SLOT_HEIGHT = 72
DEBUG_LOG_PATH = Path(__file__).resolve().parents[3] / "debug_weekly_progress.log"
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


def _debug_progress(message: str, **values: object) -> None:
    parts = [f"{key}={value}" for key, value in values.items()]
    line = f"{datetime.now().isoformat(timespec='seconds')} {message}"
    if parts:
        line = f"{line} | {'; '.join(parts)}"
    DEBUG_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DEBUG_LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{line}\n")


def _ensure_schema() -> None:
    schema_path = db_manager.config.db_path.parent / "schema.sql"
    if not schema_path.exists():
        schema_path = Path(__file__).resolve().parents[3] / "database" / "schema.sql"
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
                progress_day INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(weekly_schedule)").fetchall()
        }
        if "progress_day" not in columns:
            connection.execute("ALTER TABLE weekly_schedule ADD COLUMN progress_day INTEGER NOT NULL DEFAULT 0")


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


def _reload_slot_progress(
    schedule_id: int | None,
    day_name: str,
    slot_index: int,
) -> int | None:
    _ensure_schema()
    with db_manager.connection_scope() as connection:
        row = None
        if schedule_id:
            row = connection.execute(
                "SELECT progress_day FROM weekly_schedule WHERE id = ?",
                (schedule_id,),
            ).fetchone()
        if row is None:
            row = connection.execute(
                """
                SELECT progress_day
                FROM weekly_schedule
                WHERE day_name = ? AND slot_index = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (day_name, slot_index),
            ).fetchone()
    return int(row["progress_day"]) if row else None


def _student_name(student_id: int, students: list[dict[str, Any]]) -> str:
    for student in students:
        if int(student.get("id") or 0) == student_id:
            return _text(student.get("ad_soyad"))
    return ""


def _progress_label(progress_day: int) -> str:
    day = max(0, min(8, int(progress_day or 0)))
    return "Başlamadı" if day == 0 else f"{day}. Gün tamamlandı"


def _progress_options() -> list[ft.dropdown.Option]:
    return [ft.dropdown.Option("0", "Başlamadı")] + [
        ft.dropdown.Option(str(day), f"{day}. Gün tamamlandı") for day in range(1, 9)
    ]


def _save_slot(
    day_name: str,
    slot_index: int,
    student_id: int,
    lesson_time: str,
    note: str = "",
    progress_day: int = 0,
) -> int:
    _ensure_schema()
    students = _load_students()
    name = _student_name(student_id, students)
    resolved_progress_day = max(0, min(8, int(progress_day or 0)))
    with db_manager.connection_scope() as connection:
        connection.execute(
            "DELETE FROM weekly_schedule WHERE day_name = ? AND slot_index = ?",
            (day_name, slot_index),
        )
        cursor = connection.execute(
            """
            INSERT INTO weekly_schedule (day_name, slot_index, student_id, student_name, lesson_time, note, progress_day)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (day_name, slot_index, student_id, name, lesson_time, note, resolved_progress_day),
        )
        return int(cursor.lastrowid)


def _update_slot_progress(
    schedule_id: int | None,
    day_name: str,
    slot_index: int,
    progress_day: int,
) -> dict[str, int | None]:
    _ensure_schema()
    resolved_progress_day = max(0, min(8, int(progress_day or 0)))
    affected_rows = 0
    with db_manager.connection_scope() as connection:
        if schedule_id:
            cursor = connection.execute(
                """
                UPDATE weekly_schedule
                SET progress_day = ?
                WHERE id = ?
                """,
                (resolved_progress_day, schedule_id),
            )
            affected_rows = cursor.rowcount

        if affected_rows == 0:
            cursor = connection.execute(
                """
                UPDATE weekly_schedule
                SET progress_day = ?
                WHERE day_name = ? AND slot_index = ?
                """,
                (resolved_progress_day, day_name, slot_index),
            )
            affected_rows = cursor.rowcount

    reloaded_progress_day = _reload_slot_progress(schedule_id, day_name, slot_index)
    _debug_progress(
        "progress_change",
        schedule_id=schedule_id,
        day_name=day_name,
        slot_index=slot_index,
        selected_progress_day=resolved_progress_day,
        update_affected_rows=affected_rows,
        reloaded_progress_day=reloaded_progress_day,
    )
    return {
        "affected_rows": affected_rows,
        "reloaded_progress_day": reloaded_progress_day,
    }


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
        slot = ft.Container(height=SLOT_HEIGHT)

        def render_empty() -> None:
            slot.height = SLOT_HEIGHT
            slot.bgcolor = "#F9FAFB"
            slot.border = _border("#E5E7EB")
            slot.border_radius = 8
            slot.padding = 4
            slot.alignment = ft.Alignment(0, 0)
            slot.on_click = lambda e: render_editor(e.page)
            slot.content = ft.Column(
                tight=True,
                spacing=1,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.ADD, size=16, color="#6B7280"),
                    ft.Text("Ders Ekle", size=10, color="#6B7280", weight=ft.FontWeight.W_600),
                ],
            )

        def render_filled(record: dict[str, Any]) -> None:
            progress_dropdown = ft.Dropdown(
                value=str(int(record.get("progress_day") or 0)),
                options=_progress_options(),
                height=24,
                text_size=9,
                dense=True,
                content_padding=ft.Padding(4, 0, 4, 0),
                border_radius=999,
                border_color="#86EFAC" if int(record.get("progress_day") or 0) else "#D1D5DB",
                focused_border_color="#22C55E",
                bgcolor="#DCFCE7" if int(record.get("progress_day") or 0) else "#F3F4F6",
            )

            def handle_progress_save(e: ft.ControlEvent) -> None:
                progress_day = int(progress_dropdown.value or "0")
                schedule_id = int(record.get("id") or 0) or None
                result = _update_slot_progress(schedule_id, day_name, slot_index, progress_day)
                reloaded_progress_day = result.get("reloaded_progress_day")
                record["progress_day"] = (
                    int(reloaded_progress_day) if reloaded_progress_day is not None else progress_day
                )
                schedule[slot_key] = record
                progress_dropdown.value = str(record["progress_day"])
                progress_dropdown.border_color = "#86EFAC" if record["progress_day"] else "#D1D5DB"
                progress_dropdown.bgcolor = "#DCFCE7" if record["progress_day"] else "#F3F4F6"
                show_message("İlerleme kaydedildi.", e.page)

            slot.height = SLOT_HEIGHT
            slot.bgcolor = colors["card"]
            slot.border = _border(colors["border"])
            slot.border_radius = 8
            slot.padding = ft.Padding(6, 4, 4, 4)
            slot.alignment = ft.Alignment(-1, 0)
            slot.on_click = None
            slot.content = ft.Row(
                spacing=2,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            tight=True,
                            spacing=1,
                            controls=[
                                ft.Text(
                                    _text(record.get("student_name")) or "Öğrenci",
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color="#111827",
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(
                                    _text(record.get("lesson_time")) or "-",
                                    size=10,
                                    color=colors["text"],
                                    weight=ft.FontWeight.W_600,
                                ),
                                ft.Row(
                                    spacing=2,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(expand=True, content=progress_dropdown),
                                        ft.IconButton(
                                            icon=ft.Icons.CHECK,
                                            icon_size=14,
                                            width=24,
                                            height=24,
                                            tooltip="İlerlemeyi kaydet",
                                            on_click=handle_progress_save,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_size=15,
                        width=26,
                        height=26,
                        tooltip="Düzenle",
                        on_click=lambda e: render_editor(e.page, record),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_size=15,
                        width=26,
                        height=26,
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
                height=28,
                text_size=10,
                content_padding=ft.Padding(6, 1, 6, 1),
            )
            time_field = ft.Dropdown(
                hint_text="Saat",
                value=_text(record.get("lesson_time")) or None,
                options=[ft.dropdown.Option(value) for value in TIME_OPTIONS],
                height=28,
                text_size=10,
                content_padding=ft.Padding(6, 1, 6, 1),
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
                    progress_day = int(record.get("progress_day") or 0)
                    schedule_id = _save_slot(day_name, slot_index, student_id, lesson_time, progress_day=progress_day)
                    saved_record = {
                        "id": schedule_id,
                        "day_name": day_name,
                        "slot_index": slot_index,
                        "student_id": student_id,
                        "student_name": _student_name(student_id, students),
                        "lesson_time": lesson_time,
                        "note": "",
                        "progress_day": progress_day,
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

            slot.height = SLOT_HEIGHT
            slot.bgcolor = "#FFFFFF"
            slot.border = _border(colors["border"], 2)
            slot.border_radius = 8
            slot.padding = 4
            slot.alignment = ft.Alignment(0, 0)
            slot.on_click = None
            slot.content = ft.Column(
                spacing=3,
                controls=[
                    student_dropdown,
                    ft.Row(
                        spacing=2,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(expand=True, content=time_field),
                            ft.IconButton(
                                icon=ft.Icons.SAVE,
                                icon_size=15,
                                width=26,
                                height=26,
                                tooltip="Kaydet",
                                on_click=handle_save,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_size=15,
                                width=26,
                                height=26,
                                tooltip="Vazgeç",
                                on_click=handle_cancel,
                            ),
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
            padding=4,
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Container(
                        height=28,
                        bgcolor=colors["header"],
                        border_radius=6,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(day_name, size=12, weight=ft.FontWeight.BOLD, color=colors["text"]),
                    ),
                    *[build_slot(day_name, slot_index) for slot_index in range(1, SLOT_COUNT + 1)],
                ],
            ),
        )

    schedule_grid = ft.Row(
        expand=True,
        spacing=6,
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
        padding=8,
        content=ft.Column(
            expand=True,
            spacing=5,
            controls=[
                ft.Text("Haftalık Ders Programı", size=20, weight=ft.FontWeight.BOLD),
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
