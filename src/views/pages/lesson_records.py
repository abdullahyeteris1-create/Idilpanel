"""Lesson records page with end-to-end Lesson module integration."""

from __future__ import annotations

import flet as ft

from components import AppCard, AppDatePicker, AppDropdown, AppInput, ContentCard, PageContainer, PrimaryButton, SecondaryButton, TwoColumnLayout
from controllers import build_lesson_controller
from localization.tr import tr_error_message, tr_text
from theme.theme import THEME_TOKENS


def _status_chip(status: str) -> ft.Control:
    status_text = status or "Planlandi"
    if status_text == "Tamamlandi":
        bg, fg = "#DBEAFE", "#1E3A8A"
    elif status_text == "Iptal":
        bg, fg = "#FEE2E2", "#991B1B"
    else:
        bg, fg = "#FEF3C7", "#92400E"

    return ft.Container(
        padding=ft.Padding(10, 4, 10, 4),
        border_radius=999,
        bgcolor=bg,
        content=ft.Text(status_text, size=12, color=fg, weight=ft.FontWeight.W_600),
    )


def build_lesson_records_page() -> ft.Control:
    """Build lesson records page and wire UI -> controller -> service -> repository -> SQLite."""
    controller = build_lesson_controller()
    colors = THEME_TOKENS["colors"]

    lesson_cache: dict[int, dict] = {}

    student_dropdown = AppDropdown(label="Ogrenci", options=[], hint_text="Ogrenci secin")
    course_dropdown = AppDropdown(label="Kurs", options=[], hint_text="Kurs secin")
    lesson_dropdown = AppDropdown(label="Kayitli Ders", options=[], hint_text="Kayit secin")

    date_state = {"value": ""}
    date_picker = AppDatePicker(
        label="Tarih",
        required=True,
        on_date_change=lambda value: date_state.update({"value": value}),
    )

    text_field = AppInput(label="Metin", hint_text="Ders metni")
    word_count_field = AppInput(label="Kelime Sayisi", hint_text="Ornek: 120")
    duration_field = AppInput(label="Sure", hint_text="Dakika")
    comprehension_field = AppInput(label="Anlama %", hint_text="0-100")

    search_field = AppInput(label="", hint_text="Kayit ara...")
    search_field.prefix_icon = ft.Icons.SEARCH
    search_field.width = 280

    result_text = ft.Text(value=tr_text("ready"), selectable=True, color=colors["text_secondary"])
    lessons_list = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
    total_info_text = ft.Text(value="Toplam 0 ders", color=colors["text_secondary"], size=15)

    def _date_value() -> str:
        field = date_picker.data["field"]
        return str(field.value or "").strip()

    def _set_date_value(value: str) -> None:
        field = date_picker.data["field"]
        field.value = value
        date_state["value"] = value

    def _selected_lesson_id() -> int | None:
        selected = (lesson_dropdown.value or "").strip()
        if not selected:
            return None
        return int(selected)

    def _validate_before_save() -> tuple[bool, int | None, int | None]:
        student_value = (student_dropdown.value or "").strip()
        course_value = (course_dropdown.value or "").strip()

        if not student_value:
            result_text.value = "Lütfen öğrenci seçin."
            return False, None, None

        if not course_value:
            result_text.value = "Lütfen kurs seçin."
            return False, None, None

        student_id = int(student_value)
        course_id = int(course_value)
        if not controller.is_course_available_for_student(student_id, course_id):
            result_text.value = "Seçilen kurs bu öğrenciye ait değil."
            return False, None, None

        if not _date_value():
            result_text.value = "Bu alan zorunludur."
            return False, None, None

        return True, student_id, course_id

    def payload(lesson_no_override: int | None = None) -> dict[str, str]:
        _, student_id, course_id = _validate_before_save()
        resolved_lesson_no = lesson_no_override
        if resolved_lesson_no is None:
            resolved_lesson_no = controller.suggest_next_lesson_no(int(course_id or 0))
        return {
            "student_id": str(student_id or ""),
            "course_id": str(course_id or ""),
            "lesson_no": str(resolved_lesson_no),
            "tarih": _date_value(),
            "metin": (text_field.value or "").strip(),
            "word_count": (word_count_field.value or "").strip(),
            "duration": (duration_field.value or "").strip(),
            "comprehension": (comprehension_field.value or "").strip(),
            "durum": "Planlandi",
        }

    def _matches_search(record: dict, query: str) -> bool:
        if not query:
            return True
        target = " ".join(
            [
                str(record.get("id") or ""),
                str(record.get("course_id") or ""),
                str(record.get("lesson_no") or ""),
                str(record.get("tarih") or ""),
                str(record.get("durum") or ""),
            ]
        ).lower()
        return query.lower() in target

    def _fill_form_from_record(record: dict) -> None:
        course_records = controller.list_courses(limit=500, offset=0)
        matched_course = next(
            (item for item in course_records if int(item.get("id", 0)) == int(record.get("course_id", 0))),
            None,
        )
        if matched_course:
            student_dropdown.value = str(matched_course.get("student_id"))
            refresh_courses(int(matched_course.get("student_id")))

        course_dropdown.value = str(record.get("course_id") or "")
        _set_date_value(str(record.get("tarih") or ""))
        text_field.value = str(record.get("metin") or "")
        word_count_field.value = str(record.get("word_count") or "")
        duration_field.value = str(record.get("duration") or "")
        comprehension_field.value = str(record.get("comprehension") or "")

    def refresh_students() -> None:
        records = controller.list_students(limit=200, offset=0)
        student_dropdown.options = [
            ft.dropdown.Option(key=str(record.get("id")), text=str(record.get("ad_soyad")))
            for record in records
        ]

    def refresh_courses(selected_student_id: int | None = None) -> None:
        records = controller.list_courses(student_id=selected_student_id, limit=200, offset=0)
        course_dropdown.options = [
            ft.dropdown.Option(key=str(record.get("id")), text=f"Kur {record.get('kur_no')} (Ogrenci {record.get('student_id')})")
            for record in records
        ]

    def _build_lesson_card(record: dict) -> ft.Control:
        record_id = int(record.get("id", 0) or 0)

        def _select(e: ft.ControlEvent) -> None:
            lesson_dropdown.value = str(record_id)
            _fill_form_from_record(record)
            result_text.value = tr_text("get_success")
            e.page.update()

        card = AppCard(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                f"Kurs {record.get('course_id')} • Ders {record.get('lesson_no')}",
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=colors["text_primary"],
                            ),
                            ft.Text(
                                f"Tarih: {record.get('tarih') or '-'}",
                                size=12,
                                color=colors["text_secondary"],
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            _status_chip(str(record.get("durum") or "Planlandi")),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, size=18, color=colors["text_secondary"]),
                        ],
                    ),
                ],
            )
        )
        card.on_click = _select
        return card

    def refresh_lessons() -> None:
        records = controller.list_lessons(limit=200, offset=0)
        lesson_cache.clear()
        lesson_dropdown.options = []

        filtered_records: list[dict] = []
        for record in records:
            record_id = int(record.get("id", 0))
            lesson_cache[record_id] = record
            lesson_dropdown.options.append(
                ft.dropdown.Option(
                    key=str(record_id),
                    text=f"Kurs {record.get('course_id')} | Ders {record.get('lesson_no')} | {record.get('tarih')}",
                )
            )
            if _matches_search(record, (search_field.value or "").strip()):
                filtered_records.append(record)

        lessons_list.controls = [_build_lesson_card(record) for record in filtered_records]
        total_info_text.value = f"Toplam {len(filtered_records)} ders"

        if not filtered_records:
            lessons_list.controls = [
                AppCard(
                    content=ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon(ft.Icons.INBOX_OUTLINED, color=colors["text_secondary"]),
                            ft.Text(tr_text("list_unavailable"), color=colors["text_secondary"]),
                        ],
                    )
                )
            ]

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
            result_text.value = tr_text("created")
            refresh_lessons()
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def handle_get(e: ft.ControlEvent) -> None:
        lesson_id = _selected_lesson_id()
        if lesson_id is None:
            result_text.value = "Lütfen kayıtlı ders seçin."
            e.page.update()
            return
        try:
            record = controller.get_lesson(lesson_id)
            if not record:
                result_text.value = tr_text("record_not_found")
                e.page.update()
                return

            _fill_form_from_record(record)
            result_text.value = tr_text("get_success")
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def handle_list(e: ft.ControlEvent) -> None:
        try:
            refresh_lessons()
            result_text.value = tr_text("list_refresh")
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def handle_update(e: ft.ControlEvent) -> None:
        lesson_id = _selected_lesson_id()
        if lesson_id is None:
            result_text.value = "Lütfen güncellenecek dersi seçin."
            e.page.update()
            return

        is_valid, _, course_id = _validate_before_save()
        if not is_valid:
            e.page.update()
            return

        try:
            existing = controller.get_lesson(lesson_id) or {}
            existing_lesson_no = int(existing.get("lesson_no") or controller.suggest_next_lesson_no(int(course_id or 0)))
            updated_payload = payload(lesson_no_override=existing_lesson_no)
            updated = controller.update_lesson(lesson_id, updated_payload)
            result_text.value = tr_text("updated") if updated else tr_text("record_not_found")
            refresh_lessons()
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def handle_delete(e: ft.ControlEvent) -> None:
        lesson_id = _selected_lesson_id()
        if lesson_id is None:
            result_text.value = "Lütfen silinecek dersi seçin."
            e.page.update()
            return
        try:
            deleted = controller.delete_lesson(lesson_id)
            result_text.value = tr_text("deleted") if deleted else tr_text("record_not_found")
            lesson_dropdown.value = None
            refresh_lessons()
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def _on_search_change(e: ft.ControlEvent) -> None:
        refresh_lessons()
        e.page.update()

    search_field.on_change = _on_search_change

    form_fields = ft.ResponsiveRow(
        columns=12,
        spacing=12,
        run_spacing=12,
        controls=[
            ft.Container(col={"xs": 12, "sm": 12, "md": 12}, content=student_dropdown),
            ft.Container(col={"xs": 12, "sm": 12, "md": 12}, content=course_dropdown),
            ft.Container(col={"xs": 12, "sm": 12, "md": 12}, content=lesson_dropdown),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=date_picker),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=text_field),
            ft.Container(col={"xs": 12, "sm": 4, "md": 4}, content=word_count_field),
            ft.Container(col={"xs": 12, "sm": 4, "md": 4}, content=duration_field),
            ft.Container(col={"xs": 12, "sm": 4, "md": 4}, content=comprehension_field),
        ],
    )

    form_actions = ft.Row(
        spacing=8,
        controls=[
            PrimaryButton("Dersi Kaydet", on_click=handle_create, icon=ft.Icons.SAVE),
            SecondaryButton("Getir", on_click=handle_get, icon=ft.Icons.DOWNLOAD_DONE),
            SecondaryButton("Listele", on_click=handle_list, icon=ft.Icons.LIST),
            SecondaryButton("Guncelle", on_click=handle_update, icon=ft.Icons.EDIT),
            SecondaryButton("Sil", on_click=handle_delete, icon=ft.Icons.DELETE_OUTLINE),
        ],
    )

    form_panel = ContentCard(
        title="Ders Bilgileri",
        subtitle="Ders kaydi olustur ve yonet",
        content=ft.Column(
            spacing=16,
            controls=[form_fields, form_actions, result_text],
        ),
    )
    form_panel.width = 520

    list_panel = ContentCard(
        title="Ders Listesi",
        subtitle="Tum kayitlari goruntuleyin",
        action=search_field,
        content=ft.Column(
            spacing=12,
            expand=True,
            controls=[lessons_list, total_info_text],
        ),
    )
    list_panel.expand = True

    try:
        refresh_students()
        refresh_courses()
        refresh_lessons()
    except Exception:
        lessons_list.controls = [ft.Text(tr_text("list_unavailable"))]

    layout = ft.Column(
        spacing=16,
        expand=True,
        controls=[
            ft.Text("Ders Kayitlari", size=24, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
            TwoColumnLayout(left=form_panel, right=list_panel, left_flex=0, right_flex=1, spacing=24),
        ],
    )

    return PageContainer(content=layout, max_width=1888, padding=24)
