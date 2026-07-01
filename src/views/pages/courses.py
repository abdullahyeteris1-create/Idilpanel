"""Courses page with end-to-end Course module integration."""

from __future__ import annotations

import flet as ft

from controllers.course_controller import CourseController
from localization.tr import tr_error_message, tr_text
from repositories.course_repository import CourseRepository
from services.course_service import CourseService


def _build_course_controller() -> CourseController:
    course_repository = CourseRepository()
    course_service = CourseService(course_repository=course_repository)
    return CourseController(course_service=course_service)


def build_courses_page() -> ft.Control:
    """Build courses page and wire UI -> controller -> service -> repository -> SQLite."""
    controller = _build_course_controller()

    id_field = ft.TextField(label="Kurs ID", width=160)
    student_id_field = ft.TextField(label="Ogrenci ID", width=180)
    course_name_field = ft.TextField(label="Kurs Adi", width=260)
    level_field = ft.TextField(label="Kur No", width=140)
    start_field = ft.TextField(label="Baslangic (YYYY-MM-DD)", width=240)
    end_field = ft.TextField(label="Bitis (opsiyonel)", width=220)
    total_lessons_field = ft.TextField(label="Hedef Ders Sayisi", width=200, value="16")
    status_field = ft.TextField(label="Durum", width=180, value="Aktif")

    result_text = ft.Text(value=tr_text("ready"), selectable=True)
    courses_list = ft.Column(spacing=6)

    def payload() -> dict[str, str]:
        return {
            "student_id": student_id_field.value or "",
            "course_name": course_name_field.value or "",
            "kur_no": level_field.value or "",
            "baslangic": start_field.value or "",
            "bitis": end_field.value or "",
            "total_lessons": total_lessons_field.value or "",
            "durum": status_field.value or "",
        }

    def refresh_list() -> None:
        records = controller.list_courses(limit=50, offset=0)
        courses_list.controls = [
            ft.Text(
                f"{record.get('id')} | Ogrenci:{record.get('student_id')} | Kur:{record.get('kur_no')} | "
                f"Baslangic:{record.get('baslangic')} | Durum:{record.get('durum')}"
            )
            for record in records
        ]

    def handle_create(e: ft.ControlEvent) -> None:
        try:
            record_id = controller.create_course(payload())
            id_field.value = str(record_id)
            result_text.value = tr_text("created")
            refresh_list()
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def handle_get(e: ft.ControlEvent) -> None:
        try:
            record_id = int((id_field.value or "0").strip())
            record = controller.get_course(record_id)
            result_text.value = tr_text("get_success") if record else tr_text("record_not_found")
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def handle_list(e: ft.ControlEvent) -> None:
        try:
            refresh_list()
            result_text.value = tr_text("list_refresh")
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def handle_update(e: ft.ControlEvent) -> None:
        try:
            record_id = int((id_field.value or "0").strip())
            updated = controller.update_course(record_id, payload())
            result_text.value = tr_text("updated") if updated else tr_text("record_not_found")
            refresh_list()
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def handle_delete(e: ft.ControlEvent) -> None:
        try:
            record_id = int((id_field.value or "0").strip())
            deleted = controller.delete_course(record_id)
            result_text.value = tr_text("deleted") if deleted else tr_text("record_not_found")
            refresh_list()
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    try:
        refresh_list()
    except Exception:
        courses_list.controls = [ft.Text(tr_text("list_unavailable"))]

    return ft.Container(
        padding=16,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Kurslar", size=24, weight=ft.FontWeight.W_600),
                ft.Row(
                    wrap=True,
                    controls=[
                        id_field,
                        student_id_field,
                        course_name_field,
                        level_field,
                        start_field,
                        end_field,
                        total_lessons_field,
                        status_field,
                    ],
                ),
                ft.Row(
                    wrap=True,
                    controls=[
                        ft.ElevatedButton("Olustur", on_click=handle_create),
                        ft.ElevatedButton("Getir", on_click=handle_get),
                        ft.ElevatedButton("Listele", on_click=handle_list),
                        ft.ElevatedButton("Guncelle", on_click=handle_update),
                        ft.ElevatedButton("Sil", on_click=handle_delete),
                    ],
                ),
                result_text,
                ft.Divider(),
                ft.Text("Kayitlar", weight=ft.FontWeight.W_600),
                courses_list,
            ],
        ),
    )
