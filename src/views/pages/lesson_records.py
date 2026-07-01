"""Dynamic daily lesson records page for Sprint LR-3."""

from __future__ import annotations

import flet as ft

from components import AppCard, AppDropdown, AppInput, AppTextArea, ContentCard, PageContainer, PrimaryButton, TwoColumnLayout
from controllers import build_lesson_controller, build_text_controller
from localization.tr import tr_error_message
from theme.theme import THEME_TOKENS


DAYS_PER_COURSE = 8


def _as_text(value: object) -> str:
    return str(value or "").strip()


def _as_float(value: object) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value).strip().replace(",", "."))
    except (TypeError, ValueError):
        return None


def _format_number(value: object) -> str:
    number = _as_float(value)
    if number is None:
        return ""
    return str(int(number)) if number.is_integer() else str(round(number, 1))


def _average(values: list[object]) -> str:
    numbers = [number for number in (_as_float(value) for value in values) if number is not None]
    if not numbers:
        return "-"
    result = sum(numbers) / len(numbers)
    return str(int(round(result)))


def _metric(label: str, value: str) -> ft.Control:
    colors = THEME_TOKENS["colors"]
    return ft.Row(
        spacing=4,
        controls=[
            ft.Text(f"{label}:", size=12, color=colors["text_secondary"], weight=ft.FontWeight.W_600),
            ft.Text(value or "-", size=12, color=colors["text_primary"]),
        ],
    )


def build_lesson_records_page() -> ft.Control:
    """Build the LR-3 dynamic daily lesson records screen."""
    controller = build_lesson_controller()
    text_controller = build_text_controller()
    colors = THEME_TOKENS["colors"]

    state: dict[str, object] = {
        "students": [],
        "courses": [],
        "records_by_day": {},
        "text_titles": [],
    }

    student_dropdown = AppDropdown(label="Ogrenci", options=[], hint_text="Ogrenci secin", required=True)
    course_dropdown = AppDropdown(label="Kur", options=[], hint_text="Kur secin", required=True, disabled=True)
    day_dropdown = AppDropdown(
        label="Gun",
        options=[(str(day), f"{day}. Gun") for day in range(1, DAYS_PER_COURSE + 1)],
        value="1",
        required=True,
    )

    text_dropdown = AppDropdown(label="Metin adi", options=[], hint_text="Metin kutuphanesinden secin")
    text_field = AppInput(label="Metin adi", hint_text="Listede yoksa elle yazin", required=True)
    speed_field = AppInput(label="Hiz", hint_text="Opsiyonel")
    comprehension_field = AppInput(label="Anlama / Algi %", hint_text="Opsiyonel")
    focus_field = AppInput(label="Odaklanma %", hint_text="Opsiyonel")
    notes_field = AppTextArea(label="Notlar", hint_text="Opsiyonel", min_height=104, min_lines=3, max_lines=5)

    result_text = ft.Text(value="Ogrenci ve kur secerek baslayin.", color=colors["text_secondary"], selectable=True)
    selected_info = ft.Text(value="Her gun icin istediginiz kadar metin kaydi ekleyin.", color=colors["text_secondary"], size=13)
    history_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)

    def _selected_student_id() -> int | None:
        value = _as_text(student_dropdown.value)
        return int(value) if value else None

    def _selected_course_id() -> int | None:
        value = _as_text(course_dropdown.value)
        return int(value) if value else None

    def _selected_day() -> int:
        return int(day_dropdown.value or "1")

    def _clear_entry_fields() -> None:
        text_dropdown.value = None
        text_field.value = ""
        speed_field.value = ""
        comprehension_field.value = ""
        focus_field.value = ""
        notes_field.value = ""

    def _empty_history(message: str) -> ft.Control:
        return AppCard(
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.INBOX_OUTLINED, color=colors["text_secondary"]),
                    ft.Text(message, color=colors["text_secondary"]),
                ],
            )
        )

    def _refresh_students() -> None:
        students = list(controller.list_active_students(limit=500, offset=0))
        state["students"] = students
        student_dropdown.options = [
            ft.dropdown.Option(key=str(record.get("id")), text=_as_text(record.get("ad_soyad")) or f"Ogrenci {record.get('id')}")
            for record in students
        ]

    def _refresh_texts() -> None:
        records = list(text_controller.search_texts(query="", course_level=None, limit=5000, offset=0))
        titles = sorted(
            {
                _as_text(record.get("title"))
                for record in records
                if int(record.get("is_active", 1) or 0) == 1 and _as_text(record.get("title"))
            },
            key=lambda value: value.casefold(),
        )
        state["text_titles"] = titles
        text_dropdown.options = [ft.dropdown.Option(key=title, text=title) for title in titles]

    def _refresh_courses() -> None:
        student_id = _selected_student_id()
        if student_id is None:
            state["courses"] = []
            course_dropdown.options = []
            course_dropdown.value = None
            course_dropdown.disabled = True
            return

        courses = list(controller.list_courses(student_id=student_id, limit=200, offset=0))
        state["courses"] = courses
        course_dropdown.options = [
            ft.dropdown.Option(key=str(record.get("id")), text=f"{record.get('kur_no')}. Kur")
            for record in courses
        ]
        course_dropdown.disabled = False
        if course_dropdown.value and not any(str(record.get("id")) == str(course_dropdown.value) for record in courses):
            course_dropdown.value = None

    def _refresh_records() -> None:
        course_id = _selected_course_id()
        if course_id is None:
            state["records_by_day"] = {}
            selected_info.value = "Her gun icin istediginiz kadar metin kaydi ekleyin."
            history_column.controls = [_empty_history("Kur secildiginde gunluk kayitlar burada gorunur.")]
            return

        records = list(controller.list_course_lessons(course_id))
        records_by_day: dict[int, list[dict]] = {day: [] for day in range(1, DAYS_PER_COURSE + 1)}
        for record in records:
            day_no = int(record.get("gun_no") or 1)
            if 1 <= day_no <= DAYS_PER_COURSE:
                records_by_day[day_no].append(record)

        state["records_by_day"] = records_by_day
        history_column.controls = [_build_day_section(day_no) for day_no in range(1, DAYS_PER_COURSE + 1)]

        selected_course = next((record for record in state["courses"] if str(record.get("id")) == str(course_id)), {})
        selected_info.value = f"{selected_course.get('kur_no', '-')}. Kur | Toplam {len(records)} metin kaydi"

    def _select_day(day_no: int, page: ft.Page | None) -> None:
        day_dropdown.value = str(day_no)
        result_text.value = f"{day_no}. Gun secildi."
        if page is not None:
            page.update()

    def _build_record_row(index: int, record: dict) -> ft.Control:
        note = _as_text(record.get("ogretmen_notu"))
        controls: list[ft.Control] = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text(
                        f"{index}) {_as_text(record.get('metin'))}",
                        size=14,
                        weight=ft.FontWeight.W_700,
                        color=colors["text_primary"],
                    ),
                    ft.Text(f"ID {record.get('id')}", size=11, color=colors["text_secondary"]),
                ],
            ),
            ft.Row(
                spacing=12,
                controls=[
                    _metric("Hiz", _format_number(record.get("okuma_hizi"))),
                    _metric("Anlama", _format_number(record.get("anlama_algi"))),
                    _metric("Odak", _format_number(record.get("focus_percent"))),
                ],
            ),
        ]
        if note:
            controls.append(ft.Text(note, size=12, color=colors["text_secondary"], selectable=True))

        return ft.Container(
            padding=12,
            border_radius=8,
            bgcolor=colors["surface"],
            border=ft.Border(
                top=ft.BorderSide(1, colors["border"]),
                right=ft.BorderSide(1, colors["border"]),
                bottom=ft.BorderSide(1, colors["border"]),
                left=ft.BorderSide(1, colors["border"]),
            ),
            content=ft.Column(spacing=6, controls=controls),
        )

    def _build_average_block(records: list[dict]) -> ft.Control:
        speed_average = _average([record.get("okuma_hizi") for record in records])
        comprehension_average = _average([record.get("anlama_algi") for record in records])
        focus_average = _average([record.get("focus_percent") for record in records])
        return ft.Container(
            padding=12,
            border_radius=8,
            bgcolor="#F8FAFC",
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text("Gun Ortalamasi", size=13, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
                    _metric("Hiz", speed_average),
                    _metric("Anlama", comprehension_average),
                    _metric("Odak", focus_average),
                ],
            ),
        )

    def _build_day_section(day_no: int) -> ft.Control:
        records = list(dict(state["records_by_day"]).get(day_no, []))
        record_controls = [_build_record_row(index, record) for index, record in enumerate(records, start=1)]
        if not record_controls:
            record_controls = [
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor="#F8FAFC",
                    content=ft.Text("Ders kaydi yok", size=13, color=colors["text_secondary"]),
                )
            ]

        card = AppCard(
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(f"{day_no}. Gun", size=16, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
                            ft.Text(f"{len(records)} kayit", size=12, color=colors["text_secondary"]),
                        ],
                    ),
                    *record_controls,
                    _build_average_block(records),
                ],
            )
        )
        card.on_click = lambda e: _select_day(day_no, e.page)
        return card

    def _handle_student_change(e: ft.ControlEvent) -> None:
        course_dropdown.value = None
        _refresh_courses()
        _refresh_records()
        result_text.value = "Kur secin."
        e.page.update()

    def _handle_course_change(e: ft.ControlEvent) -> None:
        _refresh_records()
        result_text.value = "Gun secip metin kaydi ekleyin."
        e.page.update()

    def _handle_day_change(e: ft.ControlEvent) -> None:
        result_text.value = f"{_selected_day()}. Gun icin yeni kayit ekleyebilirsiniz."
        e.page.update()

    def _handle_text_change(e: ft.ControlEvent) -> None:
        text_field.value = _as_text(text_dropdown.value)
        e.page.update()

    def _handle_save(e: ft.ControlEvent) -> None:
        student_id = _selected_student_id()
        course_id = _selected_course_id()
        day_no = _selected_day()

        if student_id is None:
            result_text.value = "Lutfen ogrenci secin."
            e.page.update()
            return
        if course_id is None:
            result_text.value = "Lutfen kur secin."
            e.page.update()
            return
        if not _as_text(text_field.value):
            result_text.value = "Metin adi zorunludur."
            e.page.update()
            return

        payload = {
            "student_id": student_id,
            "course_id": course_id,
            "day_no": day_no,
            "metin": text_field.value,
            "okuma_hizi": speed_field.value,
            "anlama_algi": comprehension_field.value,
            "focus_percent": focus_field.value,
            "notlar": notes_field.value,
        }

        try:
            record_id = controller.create_course_day_entry(payload)
            _refresh_records()
            _clear_entry_fields()
            result_text.value = f"{day_no}. Gun icin yeni kayit eklendi. Kayit ID: {record_id}"
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    student_dropdown.on_select = _handle_student_change
    course_dropdown.on_select = _handle_course_change
    day_dropdown.on_select = _handle_day_change
    text_dropdown.on_select = _handle_text_change

    form_fields = ft.ResponsiveRow(
        columns=12,
        spacing=16,
        run_spacing=18,
        controls=[
            ft.Container(col={"xs": 12}, content=student_dropdown),
            ft.Container(col={"xs": 12, "sm": 6}, content=course_dropdown),
            ft.Container(col={"xs": 12, "sm": 6}, content=day_dropdown),
            ft.Container(col={"xs": 12}, content=text_dropdown),
            ft.Container(col={"xs": 12}, content=text_field),
            ft.Container(col={"xs": 12, "sm": 6}, content=speed_field),
            ft.Container(col={"xs": 12, "sm": 6}, content=comprehension_field),
            ft.Container(col={"xs": 12, "sm": 6}, content=focus_field),
            ft.Container(col={"xs": 12}, content=notes_field),
        ],
    )

    form_panel = ContentCard(
        title="Ders Kaydi",
        subtitle="Gun bazli dinamik metin kaydi",
        content=ft.Column(
            spacing=16,
            controls=[
                selected_info,
                form_fields,
                PrimaryButton("Dersi Kaydet", on_click=_handle_save, icon=ft.Icons.SAVE),
                result_text,
            ],
        ),
    )
    form_panel.width = 560

    history_panel = ContentCard(
        title="Gunluk Kayitlar",
        subtitle="Her gunun metinleri ve ortalamalari",
        content=history_column,
    )
    history_panel.expand = True

    try:
        _refresh_texts()
        _refresh_students()
        _refresh_courses()
        _refresh_records()
    except Exception as exc:
        result_text.value = tr_error_message(exc)
        history_column.controls = [_empty_history("Kayitlar yuklenemedi.")]

    layout = ft.Column(
        spacing=16,
        expand=True,
        controls=[
            ft.Text("Ders Kayitlari", size=24, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
            TwoColumnLayout(left=form_panel, right=history_panel, left_flex=0, right_flex=1, spacing=24),
        ],
    )

    return PageContainer(content=layout, max_width=1888, padding=24)
