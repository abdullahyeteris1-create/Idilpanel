"""Lesson records page with end-to-end Lesson module integration."""

from __future__ import annotations

import flet as ft

from controllers.lesson_controller import LessonController
from repositories.lesson_repository import LessonRepository
from services.lesson_service import LessonService


def _build_lesson_controller() -> LessonController:
    lesson_repository = LessonRepository()
    lesson_service = LessonService(lesson_repository=lesson_repository)
    return LessonController(lesson_service=lesson_service)


def build_lesson_records_page() -> ft.Control:
    """Build lesson records page and wire UI -> controller -> service -> repository -> SQLite."""
    controller = _build_lesson_controller()

    lesson_id_field = ft.TextField(label="Lesson ID", width=160)
    student_field = ft.TextField(label="Ogrenci", width=220)
    course_id_field = ft.TextField(label="Kurs ID", width=180)
    lesson_no_field = ft.TextField(label="Ders No", width=140)
    date_field = ft.TextField(label="Tarih (YYYY-MM-DD)", width=220)
    text_field = ft.TextField(label="Metin", width=260)
    word_count_field = ft.TextField(label="Kelime Sayisi", width=180)
    duration_field = ft.TextField(label="Sure", width=140)
    comprehension_field = ft.TextField(label="Anlama %", width=160)

    result_text = ft.Text(value="Hazir", selectable=True)
    lessons_list = ft.Column(spacing=6)

    def payload() -> dict[str, str]:
        return {
            "course_id": (course_id_field.value or "").strip(),
            "lesson_no": (lesson_no_field.value or "").strip(),
            "tarih": (date_field.value or "").strip(),
            "metin": (text_field.value or "").strip(),
            "ogretmen_notu": (
                f"Ogrenci: {(student_field.value or '').strip()} | "
                f"Kelime: {(word_count_field.value or '').strip()} | "
                f"Sure: {(duration_field.value or '').strip()} | "
                f"Anlama: {(comprehension_field.value or '').strip()}"
            ),
            "durum": "Planlandi",
        }

    def refresh_list() -> None:
        records = controller.list_lessons(limit=50, offset=0)
        lessons_list.controls = [
            ft.Text(
                f"{record.get('id')} | Kurs:{record.get('course_id')} | Ders:{record.get('lesson_no')} | "
                f"Tarih:{record.get('tarih')} | Durum:{record.get('durum')}"
            )
            for record in records
        ]

    def handle_create(e: ft.ControlEvent) -> None:
        try:
            record_id = controller.create_lesson(payload())
            lesson_id_field.value = str(record_id)
            result_text.value = f"Olusturuldu: {record_id}"
            refresh_list()
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    def handle_get(e: ft.ControlEvent) -> None:
        try:
            record_id = int((lesson_id_field.value or "0").strip())
            record = controller.get_lesson(record_id)
            result_text.value = f"Getirildi: {record}"
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    def handle_list(e: ft.ControlEvent) -> None:
        try:
            refresh_list()
            result_text.value = "Liste guncellendi"
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    def handle_update(e: ft.ControlEvent) -> None:
        try:
            record_id = int((lesson_id_field.value or "0").strip())
            updated = controller.update_lesson(record_id, payload())
            result_text.value = f"Guncellendi: {updated}"
            refresh_list()
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    def handle_delete(e: ft.ControlEvent) -> None:
        try:
            record_id = int((lesson_id_field.value or "0").strip())
            deleted = controller.delete_lesson(record_id)
            result_text.value = f"Silindi: {deleted}"
            refresh_list()
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    try:
        refresh_list()
    except Exception:
        lessons_list.controls = [ft.Text("Liste alinamadi. Once veri tabanini hazirlayin.")]

    return ft.Container(
        padding=16,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Ders Kayitlari", size=24, weight=ft.FontWeight.W_600),
                ft.Row(
                    wrap=True,
                    controls=[
                        lesson_id_field,
                        student_field,
                        course_id_field,
                        lesson_no_field,
                        date_field,
                        text_field,
                        word_count_field,
                        duration_field,
                        comprehension_field,
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
                lessons_list,
            ],
        ),
    )
