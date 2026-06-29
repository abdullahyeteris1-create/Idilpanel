"""Lesson records page with end-to-end Lesson module integration."""

from __future__ import annotations

import flet as ft

from controllers import build_lesson_controller


def build_lesson_records_page() -> ft.Control:
    """Build lesson records page and wire UI -> controller -> service -> repository -> SQLite."""
    controller = build_lesson_controller()

    student_dropdown = ft.Dropdown(label="Ogrenci", width=260)
    course_dropdown = ft.Dropdown(label="Kurs", width=220)
    lesson_dropdown = ft.Dropdown(label="Kayitli Ders", width=340)
    date_field = ft.TextField(label="Tarih (YYYY-MM-DD)", width=220)
    text_field = ft.TextField(label="Metin", width=260)
    word_count_field = ft.TextField(label="Kelime Sayisi", width=180)
    duration_field = ft.TextField(label="Sure", width=140)
    comprehension_field = ft.TextField(label="Anlama %", width=160)

    result_text = ft.Text(value="Hazir", selectable=True)
    lessons_list = ft.Column(spacing=6)
    lesson_cache: dict[int, dict] = {}

    def _selected_lesson_id() -> int | None:
        selected = (lesson_dropdown.value or "").strip()
        if not selected:
            return None
        return int(selected)

    def _validate_before_save() -> tuple[bool, int | None, int | None]:
        student_value = (student_dropdown.value or "").strip()
        course_value = (course_dropdown.value or "").strip()

        if not student_value:
            result_text.value = "Hata: Ogrenci seciniz."
            return False, None, None

        if not course_value:
            result_text.value = "Hata: Kurs seciniz."
            return False, None, None

        student_id = int(student_value)
        course_id = int(course_value)
        if not controller.is_course_available_for_student(student_id, course_id):
            result_text.value = "Hata: Secilen kurs bu ogrenciye ait degil."
            return False, None, None

        if not (date_field.value or "").strip():
            result_text.value = "Hata: Tarih zorunludur."
            return False, None, None

        return True, student_id, course_id

    def payload() -> dict[str, str]:
        _, student_id, course_id = _validate_before_save()
        next_lesson_no = controller.suggest_next_lesson_no(int(course_id or 0))
        return {
            "course_id": str(course_id or ""),
            "lesson_no": str(next_lesson_no),
            "tarih": (date_field.value or "").strip(),
            "metin": (text_field.value or "").strip(),
            "ogretmen_notu": (
                f"Ogrenci ID: {student_id or ''} | "
                f"Kelime: {(word_count_field.value or '').strip()} | "
                f"Sure: {(duration_field.value or '').strip()} | "
                f"Anlama: {(comprehension_field.value or '').strip()}"
            ),
            "durum": "Planlandi",
        }

    def refresh_students() -> None:
        records = controller.list_students(limit=200, offset=0)
        student_dropdown.options = [
            ft.dropdown.Option(str(record.get("id")), str(record.get("ad_soyad")))
            for record in records
        ]

    def refresh_courses(selected_student_id: int | None = None) -> None:
        records = controller.list_courses(student_id=selected_student_id, limit=200, offset=0)
        course_dropdown.options = [
            ft.dropdown.Option(str(record.get("id")), f"Kur {record.get('kur_no')} (Ogrenci {record.get('student_id')})")
            for record in records
        ]

    def refresh_lessons() -> None:
        records = controller.list_lessons(limit=50, offset=0)
        lesson_cache.clear()
        lessons_list.controls = []
        lesson_dropdown.options = []
        for record in records:
            record_id = int(record.get("id", 0))
            lesson_cache[record_id] = record
            lesson_dropdown.options.append(
                ft.dropdown.Option(
                    str(record_id),
                    f"Kurs {record.get('course_id')} | Ders {record.get('lesson_no')} | {record.get('tarih')}",
                )
            )
            lessons_list.controls.append(
                ft.Text(
                    f"{record_id} | Kurs:{record.get('course_id')} | Ders:{record.get('lesson_no')} | "
                    f"Tarih:{record.get('tarih')} | Durum:{record.get('durum')}"
                )
            )

    def on_student_change(e: ft.ControlEvent) -> None:
        selected_student_id = int((student_dropdown.value or "0").strip()) if student_dropdown.value else None
        refresh_courses(selected_student_id)
        course_dropdown.value = None
        e.page.update()

    student_dropdown.on_change = on_student_change

    def handle_create(e: ft.ControlEvent) -> None:
        is_valid, _, _ = _validate_before_save()
        if not is_valid:
            e.page.update()
            return
        try:
            record_id = controller.create_lesson(payload())
            lesson_dropdown.value = str(record_id)
            result_text.value = f"Olusturuldu: {record_id}"
            refresh_lessons()
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            if "FOREIGN KEY constraint failed" in str(exc):
                result_text.value = "Hata: Gecersiz kurs secimi."
            else:
                result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    def handle_get(e: ft.ControlEvent) -> None:
        lesson_id = _selected_lesson_id()
        if lesson_id is None:
            result_text.value = "Hata: Kayitli ders seciniz."
            e.page.update()
            return
        try:
            record = controller.get_lesson(lesson_id)
            if not record:
                result_text.value = "Hata: Kayit bulunamadi."
                e.page.update()
                return
            course_dropdown.value = str(record.get("course_id"))
            date_field.value = str(record.get("tarih") or "")
            text_field.value = str(record.get("metin") or "")
            result_text.value = f"Getirildi: {record}"
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    def handle_list(e: ft.ControlEvent) -> None:
        try:
            refresh_lessons()
            result_text.value = "Liste guncellendi"
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    def handle_update(e: ft.ControlEvent) -> None:
        lesson_id = _selected_lesson_id()
        if lesson_id is None:
            result_text.value = "Hata: Guncellenecek dersi seciniz."
            e.page.update()
            return

        is_valid, _, course_id = _validate_before_save()
        if not is_valid:
            e.page.update()
            return

        try:
            existing = controller.get_lesson(lesson_id) or {}
            updated_payload = {
                "course_id": str(course_id or ""),
                "lesson_no": str(existing.get("lesson_no") or controller.suggest_next_lesson_no(int(course_id or 0))),
                "tarih": (date_field.value or "").strip(),
                "metin": (text_field.value or "").strip(),
                "ogretmen_notu": existing.get("ogretmen_notu") or "",
                "durum": existing.get("durum") or "Planlandi",
            }
            updated = controller.update_lesson(lesson_id, updated_payload)
            result_text.value = f"Guncellendi: {updated}"
            refresh_lessons()
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            if "FOREIGN KEY constraint failed" in str(exc):
                result_text.value = "Hata: Gecersiz kurs secimi."
            else:
                result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    def handle_delete(e: ft.ControlEvent) -> None:
        lesson_id = _selected_lesson_id()
        if lesson_id is None:
            result_text.value = "Hata: Silinecek dersi seciniz."
            e.page.update()
            return
        try:
            deleted = controller.delete_lesson(lesson_id)
            result_text.value = f"Silindi: {deleted}"
            lesson_dropdown.value = None
            refresh_lessons()
        except ValueError as exc:
            result_text.value = f"Hata: {exc}"
        except Exception as exc:
            result_text.value = f"Islem hatasi: {exc}"
        e.page.update()

    try:
        refresh_students()
        refresh_courses()
        refresh_lessons()
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
                        student_dropdown,
                        course_dropdown,
                        lesson_dropdown,
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
                        ft.ElevatedButton("Dersi Kaydet", on_click=handle_create),
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
