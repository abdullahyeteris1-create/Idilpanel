"""Students page with end-to-end Student module integration."""

from __future__ import annotations

import flet as ft

from controllers.student_controller import StudentController
from repositories.student_repository import StudentRepository
from services.student_service import StudentService


def _build_student_controller() -> StudentController:
    student_repository = StudentRepository()
    student_service = StudentService(student_repository=student_repository)
    return StudentController(student_service=student_service)


def build_students_page() -> ft.Control:
    """Build students page and wire UI -> controller -> service -> repository -> SQLite."""
    controller = _build_student_controller()

    id_field = ft.TextField(label="Ogrenci ID", width=180)
    name_field = ft.TextField(label="Ad Soyad", width=320)
    class_field = ft.TextField(label="Sinif", width=180)
    course_id_field = ft.TextField(label="Kurs ID", width=180)
    start_date_field = ft.TextField(label="Baslangic Tarihi (YYYY-MM-DD)", width=260)

    result_text = ft.Text(value="Hazir", selectable=True)
    students_list = ft.Column(spacing=6)

    def payload() -> dict[str, str]:
        return {
            "ad_soyad": name_field.value or "",
            "sinif": class_field.value or "",
            "course_id": course_id_field.value or "",
            "baslangic_tarihi": start_date_field.value or "",
        }

    def refresh_list() -> None:
        records = controller.list_students(limit=50, offset=0)
        students_list.controls = [
            ft.Text(f"{record.get('id')} | {record.get('ad_soyad')} | {record.get('sinif')} | {record.get('baslangic_tarihi')}")
            for record in records
        ]

    def handle_create(_: ft.ControlEvent) -> None:
        try:
            record_id = controller.create_student(payload())
            result_text.value = f"Olusturuldu: {record_id}"
            id_field.value = str(record_id)
            refresh_list()
        except Exception as exc:
            result_text.value = f"Hata: {exc}"
        _.page.update()

    def handle_get(_: ft.ControlEvent) -> None:
        try:
            record_id = int((id_field.value or "0").strip())
            record = controller.get_student(record_id)
            result_text.value = f"Getirildi: {record}"
        except Exception as exc:
            result_text.value = f"Hata: {exc}"
        _.page.update()

    def handle_list(_: ft.ControlEvent) -> None:
        try:
            refresh_list()
            result_text.value = "Liste guncellendi"
        except Exception as exc:
            result_text.value = f"Hata: {exc}"
        _.page.update()

    def handle_update(_: ft.ControlEvent) -> None:
        try:
            record_id = int((id_field.value or "0").strip())
            updated = controller.update_student(record_id, payload())
            result_text.value = f"Guncellendi: {updated}"
            refresh_list()
        except Exception as exc:
            result_text.value = f"Hata: {exc}"
        _.page.update()

    def handle_delete(_: ft.ControlEvent) -> None:
        try:
            record_id = int((id_field.value or "0").strip())
            deleted = controller.delete_student(record_id)
            result_text.value = f"Silindi: {deleted}"
            refresh_list()
        except Exception as exc:
            result_text.value = f"Hata: {exc}"
        _.page.update()

    try:
        refresh_list()
    except Exception:
        students_list.controls = [ft.Text("Liste alinamadi. Once veri tabanini hazirlayin.")]

    return ft.Container(
        padding=16,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Ogrenciler", size=24, weight=ft.FontWeight.W_600),
                ft.Row(wrap=True, controls=[id_field, name_field, class_field, course_id_field, start_date_field]),
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
                students_list,
            ],
        ),
    )
