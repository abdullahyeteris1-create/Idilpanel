"""Simple, stable MVP student management screen.

This page intentionally avoids the professional Students V3 layout. It uses
plain Flet controls and direct SQLite access so the app is usable immediately.
"""

from __future__ import annotations

from datetime import date
from typing import Any

import flet as ft

from database.connection_manager import db_manager


def _text(value: object) -> str:
    return str(value or "").strip()


def _course_number(value: object) -> int:
    digits = "".join(ch for ch in _text(value) if ch.isdigit())
    if not digits:
        return 1
    return max(1, int(digits))


def _border(color: str = "#D1D5DB") -> ft.Border:
    return ft.Border(
        top=ft.BorderSide(1, color),
        right=ft.BorderSide(1, color),
        bottom=ft.BorderSide(1, color),
        left=ft.BorderSide(1, color),
    )


def _parse_date(value: object) -> date:
    try:
        return date.fromisoformat(_text(value))
    except ValueError:
        return date.today()


def _ensure_schema() -> None:
    schema_path = db_manager.config.schema_path
    with db_manager.connection_scope() as connection:
        has_students = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'students'"
        ).fetchone()
        if has_students:
            return
        connection.executescript(schema_path.read_text(encoding="utf-8"))


def _load_students() -> list[dict[str, Any]]:
    _ensure_schema()
    query = """
        SELECT
            s.*,
            (
                SELECT c.kur_no
                FROM courses c
                WHERE c.student_id = s.id AND c.is_active = 1
                ORDER BY c.id DESC
                LIMIT 1
            ) AS kur_no
        FROM students s
        WHERE s.is_active = 1
        ORDER BY s.id DESC
    """
    with db_manager.connection_scope() as connection:
        rows = connection.execute(query).fetchall()
        return [dict(row) for row in rows]


def _save_course(connection, student_id: int, kur_no: int, start_date: str) -> None:
    existing = connection.execute(
        """
        SELECT id FROM courses
        WHERE student_id = ? AND kur_no = ? AND is_active = 1
        LIMIT 1
        """,
        (student_id, kur_no),
    ).fetchone()
    if existing:
        connection.execute(
            "UPDATE courses SET baslangic = ?, durum = 'Aktif', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (start_date, int(existing["id"])),
        )
        return

    connection.execute(
        """
        INSERT OR IGNORE INTO courses (student_id, kur_no, baslangic, durum, hedef_ders_sayisi, is_active)
        VALUES (?, ?, ?, 'Aktif', 16, 1)
        """,
        (student_id, kur_no, start_date),
    )


def _create_student(payload: dict[str, str]) -> int:
    _ensure_schema()
    kur_no = _course_number(payload.pop("kurs", "1"))
    with db_manager.connection_scope() as connection:
        cursor = connection.execute(
            """
            INSERT INTO students (
                ad_soyad, sinif, veli_adi, telefon, baslangic_tarihi,
                kullanici_adi, sifre, notlar, durum, is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Aktif', 1)
            """,
            (
                payload["ad_soyad"],
                payload["sinif"],
                payload["veli_adi"],
                payload["telefon"],
                payload["baslangic_tarihi"],
                payload["kullanici_adi"],
                payload["sifre"],
                payload["notlar"],
            ),
        )
        student_id = int(cursor.lastrowid)
        _save_course(connection, student_id, kur_no, payload["baslangic_tarihi"])
        return student_id


def _update_student(student_id: int, payload: dict[str, str]) -> None:
    _ensure_schema()
    kur_no = _course_number(payload.pop("kurs", "1"))
    with db_manager.connection_scope() as connection:
        connection.execute(
            """
            UPDATE students
            SET ad_soyad = ?,
                sinif = ?,
                veli_adi = ?,
                telefon = ?,
                baslangic_tarihi = ?,
                kullanici_adi = ?,
                sifre = ?,
                notlar = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                payload["ad_soyad"],
                payload["sinif"],
                payload["veli_adi"],
                payload["telefon"],
                payload["baslangic_tarihi"],
                payload["kullanici_adi"],
                payload["sifre"],
                payload["notlar"],
                student_id,
            ),
        )
        _save_course(connection, student_id, kur_no, payload["baslangic_tarihi"])


def _delete_student(student_id: int) -> None:
    _ensure_schema()
    with db_manager.connection_scope() as connection:
        connection.execute(
            "UPDATE students SET is_active = 0, deleted_at = CURRENT_TIMESTAMP WHERE id = ?",
            (student_id,),
        )
        connection.execute(
            "UPDATE courses SET is_active = 0, deleted_at = CURRENT_TIMESTAMP WHERE student_id = ?",
            (student_id,),
        )


def build_students_mvp_page() -> ft.Control:
    selected_id: dict[str, int | None] = {"value": None}

    title = ft.Text("Ogrenci Yonetimi", size=24, weight=ft.FontWeight.BOLD)
    message = ft.Text("", color="#374151")

    name_field = ft.TextField(label="Ad Soyad", height=48)
    class_field = ft.TextField(label="Sinif", height=48)
    parent_field = ft.TextField(label="Veli", height=48)
    phone_field = ft.TextField(label="Telefon", height=48)
    start_field = ft.TextField(
        label="Baslangic Tarihi",
        value=date.today().isoformat(),
        height=48,
        read_only=True,
    )
    username_field = ft.TextField(label="Kullanici Adi", height=48)
    password_field = ft.TextField(label="Sifre", password=True, can_reveal_password=True, height=48)
    course_field = ft.Dropdown(
        label="Kurs",
        value="1",
        options=[ft.dropdown.Option(str(number), f"Kur {number}") for number in range(1, 17)],
        height=48,
    )
    notes_field = ft.TextField(label="Notlar", multiline=True, min_lines=3, max_lines=5)

    students_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def handle_date_change(e: ft.ControlEvent) -> None:
        picked = getattr(e.control, "value", None)
        if isinstance(picked, date):
            start_field.value = picked.isoformat()
        elif picked:
            start_field.value = _parse_date(picked).isoformat()
        if e.page:
            e.page.update()

    start_date_picker = ft.DatePicker(on_change=handle_date_change)

    def open_start_date_picker(e: ft.ControlEvent) -> None:
        if not e.page:
            return
        start_date_picker.value = _parse_date(start_field.value)
        if start_date_picker not in e.page.overlay:
            e.page.overlay.append(start_date_picker)
        start_date_picker.open = True
        e.page.update()

    start_field.on_click = open_start_date_picker
    start_date_input = ft.Row(
        spacing=8,
        controls=[
            ft.Container(expand=True, content=start_field, on_click=open_start_date_picker),
            ft.IconButton(
                icon=ft.Icons.CALENDAR_MONTH,
                tooltip="Tarih sec",
                width=48,
                height=48,
                on_click=open_start_date_picker,
            ),
        ],
    )

    def payload() -> dict[str, str]:
        return {
            "ad_soyad": _text(name_field.value),
            "sinif": _text(class_field.value),
            "veli_adi": _text(parent_field.value),
            "telefon": _text(phone_field.value),
            "baslangic_tarihi": _text(start_field.value) or date.today().isoformat(),
            "kullanici_adi": _text(username_field.value),
            "sifre": _text(password_field.value),
            "kurs": _text(course_field.value) or "1",
            "notlar": _text(notes_field.value),
        }

    def clear_form() -> None:
        selected_id["value"] = None
        name_field.value = ""
        class_field.value = ""
        parent_field.value = ""
        phone_field.value = ""
        start_field.value = date.today().isoformat()
        username_field.value = ""
        password_field.value = ""
        course_field.value = "1"
        notes_field.value = ""

    def fill_form(record: dict[str, Any]) -> None:
        selected_id["value"] = int(record["id"])
        name_field.value = _text(record.get("ad_soyad"))
        class_field.value = _text(record.get("sinif"))
        parent_field.value = _text(record.get("veli_adi"))
        phone_field.value = _text(record.get("telefon"))
        start_field.value = _text(record.get("baslangic_tarihi")) or date.today().isoformat()
        username_field.value = _text(record.get("kullanici_adi"))
        password_field.value = _text(record.get("sifre"))
        course_field.value = str(record.get("kur_no") or "1")
        notes_field.value = _text(record.get("notlar"))

    def show_message(text: str) -> None:
        message.value = text

    def refresh(page: ft.Page | None = None) -> None:
        records = _load_students()
        if not records:
            students_list.controls = [ft.Text("Henuz kayitli ogrenci yok.")]
        else:
            students_list.controls = [student_card(record) for record in records]
        if page:
            page.update()

    def handle_save(e: ft.ControlEvent) -> None:
        data = payload()
        if not data["ad_soyad"] or not data["sinif"]:
            show_message("Ad Soyad ve Sinif zorunludur.")
            e.page.update()
            return
        try:
            if selected_id["value"]:
                _update_student(int(selected_id["value"]), data)
                show_message("Ogrenci guncellendi.")
            else:
                selected_id["value"] = _create_student(data)
                show_message("Ogrenci kaydedildi.")
            clear_form()
            refresh(e.page)
        except Exception as exc:
            show_message(f"Hata: {exc}")
            e.page.update()

    def handle_clear(e: ft.ControlEvent) -> None:
        clear_form()
        show_message("Form temizlendi.")
        e.page.update()

    def handle_edit(record: dict[str, Any]):
        def _handler(e: ft.ControlEvent) -> None:
            fill_form(record)
            show_message("Duzenleme icin forma yuklendi.")
            e.page.update()

        return _handler

    def handle_delete(record_id: int):
        def _handler(e: ft.ControlEvent) -> None:
            try:
                _delete_student(record_id)
                if selected_id["value"] == record_id:
                    clear_form()
                show_message("Ogrenci silindi.")
                refresh(e.page)
            except Exception as exc:
                show_message(f"Hata: {exc}")
                e.page.update()

        return _handler

    def handle_lesson(record_id: int):
        def _handler(e: ft.ControlEvent) -> None:
            e.page.go("/lesson-records")

        return _handler

    def student_card(record: dict[str, Any]) -> ft.Control:
        record_id = int(record["id"])
        course_label = f"Kur {record.get('kur_no') or '-'}"
        return ft.Container(
            bgcolor="#FFFFFF",
            border=_border(),
            border_radius=6,
            padding=12,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(_text(record.get("ad_soyad")) or "-", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Sinif: {_text(record.get('sinif')) or '-'}"),
                    ft.Text(f"Veli: {_text(record.get('veli_adi')) or '-'}"),
                    ft.Text(f"Kurs: {course_label}"),
                    ft.Row(
                        wrap=True,
                        spacing=8,
                        controls=[
                            ft.ElevatedButton("Ders Yap", on_click=handle_lesson(record_id)),
                            ft.ElevatedButton("Duzenle", on_click=handle_edit(record)),
                            ft.ElevatedButton("Sil", on_click=handle_delete(record_id), bgcolor="#DC2626", color="#FFFFFF"),
                        ],
                    ),
                ],
            ),
        )

    form_panel = ft.Container(
        width=360,
        bgcolor="#FFFFFF",
        border=_border(),
        border_radius=6,
        padding=16,
        content=ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Ogrenci Formu", size=18, weight=ft.FontWeight.BOLD),
                name_field,
                class_field,
                parent_field,
                phone_field,
                start_date_input,
                username_field,
                password_field,
                course_field,
                notes_field,
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.ElevatedButton("Kaydet", on_click=handle_save, bgcolor="#2563EB", color="#FFFFFF"),
                        ft.ElevatedButton("Temizle", on_click=handle_clear),
                    ],
                ),
            ],
        ),
    )

    list_panel = ft.Container(
        expand=True,
        bgcolor="#F9FAFB",
        border=_border(),
        border_radius=6,
        padding=16,
        content=ft.Column(
            expand=True,
            spacing=12,
            controls=[
                ft.Text("Kayitli Ogrenciler", size=18, weight=ft.FontWeight.BOLD),
                students_list,
            ],
        ),
    )

    page = ft.Container(
        expand=True,
        bgcolor="#F3F4F6",
        padding=16,
        content=ft.Column(
            expand=True,
            spacing=12,
            controls=[
                title,
                message,
                ft.Row(
                    expand=True,
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[form_panel, list_panel],
                ),
            ],
        ),
    )
    page.data = {"canonical": "students_mvp"}
    refresh()
    return page
