"""Canonical Students V3 professional management screen."""

from __future__ import annotations

from typing import Any

import flet as ft

from components import (
    build_app_datepicker,
    build_app_dropdown,
    build_badge,
    build_card,
    build_danger_button,
    build_empty_state,
    build_primary_button,
    build_search_box,
    build_secondary_button,
    build_text_field,
)
from controllers import build_course_controller, build_student_controller
from controllers.course_controller import CourseController
from controllers.student_controller import StudentController
from theme.theme import THEME_TOKENS


STATUS_ALL = "Tumu"
STATUS_ACTIVE = "Aktif"
STATUS_PASSIVE = "Pasif"
STATUS_COMPLETED = "Tamamlanan"
PAGE_SIZE = 8


def students_v3_responsive_profile(width: int) -> str:
    """Classify the target desktop widths used by sprint validation."""

    if width >= 1800:
        return "1920x1080"
    if width >= 1500:
        return "1600x900"
    if width >= 1320:
        return "1366x768"
    if width >= 768:
        return "Tablet"
    return "Mobile"


def _safe_text(value: object) -> str:
    return str(value or "").strip()


def _course_label(student_id: int, courses: list[dict[str, Any]]) -> str:
    student_courses = [
        course
        for course in courses
        if int(course.get("student_id", 0) or 0) == student_id
        and int(course.get("is_active", 1) or 0) == 1
    ]
    if not student_courses:
        return "-"

    student_courses.sort(key=lambda course: int(course.get("id", 0) or 0), reverse=True)
    kur_no = int(student_courses[0].get("kur_no", 0) or 0)
    return f"Kur {kur_no}" if kur_no else "-"


def _student_status(record: dict[str, Any], courses: list[dict[str, Any]] | None = None) -> str:
    student_id = int(record.get("id", 0) or 0)
    for course in courses or []:
        if int(course.get("student_id", 0) or 0) != student_id:
            continue
        if int(course.get("is_active", 1) or 0) != 1:
            continue
        if _safe_text(course.get("durum")) in {"Tamamlandi", "Tamamlanan", "Iptal"}:
            return STATUS_COMPLETED

    if "Tamamlandi" in _safe_text(record.get("notlar")) or "Tamamlanan" in _safe_text(record.get("notlar")):
        return STATUS_COMPLETED

    raw_status = _safe_text(record.get("durum"))
    if raw_status == "Aktif":
        return STATUS_ACTIVE
    if raw_status in {"Pasif", "Beklemede"}:
        return STATUS_PASSIVE
    if raw_status in {"Tamamlandi", "Tamamlanan", "Egitimi Tamamlandi"}:
        return STATUS_COMPLETED
    return STATUS_PASSIVE


def _status_badge_variant(status: str) -> str:
    if status == STATUS_ACTIVE:
        return "success"
    if status == STATUS_COMPLETED:
        return "completed"
    return "warning"


def _initials(name: str) -> str:
    parts = [part for part in name.split() if part]
    if not parts:
        return "--"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return f"{parts[0][0]}{parts[-1][0]}".upper()


def students_v3_filter_students(
    students: list[dict[str, Any]],
    courses: list[dict[str, Any]],
    query: str,
    status_filter: str,
) -> list[dict[str, Any]]:
    """Filter SQLite-backed student rows for the management list."""

    normalized_query = _safe_text(query).casefold()
    filtered: list[dict[str, Any]] = []

    for student in students:
        status = _student_status(student, courses)
        if status_filter != STATUS_ALL and status != status_filter:
            continue

        student_id = int(student.get("id", 0) or 0)
        searchable = " ".join(
            [
                _safe_text(student.get("ad_soyad")),
                _safe_text(student.get("sinif")),
                _safe_text(student.get("telefon")),
                _safe_text(student.get("veli_adi")),
                _safe_text(student.get("kullanici_adi")),
                _course_label(student_id, courses),
                status,
            ]
        ).casefold()
        if normalized_query and normalized_query not in searchable:
            continue

        filtered.append(student)

    return filtered


def build_students_v3_page() -> ft.Container:
    """Build the canonical Students management page."""

    colors = THEME_TOKENS["colors"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    student_controller: StudentController = build_student_controller()
    course_controller: CourseController = build_course_controller()

    state: dict[str, Any] = {
        "students": [],
        "courses": [],
        "selected_id": None,
        "selected_snapshot": None,
        "query": "",
        "status_filter": STATUS_ALL,
        "page": 1,
        "view_state": "loading",
    }

    feedback_area = ft.Container(height=0)
    student_list = ft.Column(spacing=spacing["sm"], scroll=ft.ScrollMode.AUTO, expand=True)
    result_text = ft.Text("0 kayit", color=colors["text_secondary"])
    page_text = ft.Text("Sayfa 1/1", color=colors["text_secondary"])

    name_field = build_text_field("Ad Soyad", required=True)
    class_field = build_text_field("Sinif", required=True)
    parent_field = build_text_field("Veli Adi")
    username_field = build_text_field("Kullanici Adi")
    password_field = build_text_field("Sifre", password=True)
    phone_field = build_text_field("Telefon")
    email_field = build_text_field("E-posta")
    start_date = build_app_datepicker("Baslangic", required=True)
    end_date = build_app_datepicker("Bitis")
    status_dropdown = build_app_dropdown(
        "Durum",
        options=["Aktif", "Beklemede"],
        value="Aktif",
        required=True,
    )
    notes_field = build_text_field("Notlar", multiline=True, min_lines=4, max_lines=6)

    def _set_feedback(level: str, message: str) -> None:
        variant_color = {
            "success": colors["success"],
            "warning": colors["warning"],
            "error": colors["danger"],
            "info": colors["primary"],
        }.get(level, colors["primary"])
        feedback_area.content = ft.Container(
            padding=ft.Padding(spacing["md"], spacing["sm"], spacing["md"], spacing["sm"]),
            bgcolor=variant_color,
            border_radius=radius["input"],
            content=ft.Text(message, color=colors["surface"]),
        )
        feedback_area.height = 44

    def _date_value(control: ft.Control) -> str:
        return _safe_text(getattr(control, "value", ""))

    def _set_date_value(control: ft.Control, value: str) -> None:
        control.value = value

    def _clear_form() -> None:
        state["selected_id"] = None
        state["selected_snapshot"] = None
        for field in [name_field, class_field, parent_field, username_field, password_field, phone_field, email_field, notes_field]:
            field.value = ""
        _set_date_value(start_date, "")
        _set_date_value(end_date, "")
        status_dropdown.value = "Aktif"

    def _payload() -> dict[str, str]:
        return {
            "ad_soyad": _safe_text(name_field.value),
            "sinif": _safe_text(class_field.value),
            "veli_adi": _safe_text(parent_field.value),
            "telefon": _safe_text(phone_field.value),
            "email": _safe_text(email_field.value),
            "kullanici_adi": _safe_text(username_field.value),
            "sifre": _safe_text(password_field.value),
            "baslangic_tarihi": _date_value(start_date),
            "bitis_tarihi": _date_value(end_date),
            "durum": _safe_text(status_dropdown.value) or "Aktif",
            "notlar": _safe_text(notes_field.value),
        }

    def _fill_form(record: dict[str, Any]) -> None:
        state["selected_id"] = int(record.get("id", 0) or 0)
        state["selected_snapshot"] = dict(record)
        name_field.value = _safe_text(record.get("ad_soyad"))
        class_field.value = _safe_text(record.get("sinif"))
        parent_field.value = _safe_text(record.get("veli_adi"))
        username_field.value = _safe_text(record.get("kullanici_adi"))
        password_field.value = _safe_text(record.get("sifre"))
        phone_field.value = _safe_text(record.get("telefon"))
        email_field.value = _safe_text(record.get("email") or record.get("eposta"))
        _set_date_value(start_date, _safe_text(record.get("baslangic_tarihi")))
        _set_date_value(end_date, _safe_text(record.get("bitis_tarihi")))
        status_dropdown.value = _safe_text(record.get("durum")) or "Aktif"
        notes_field.value = _safe_text(record.get("notlar"))

    def _validate_payload(payload: dict[str, str]) -> str:
        if not payload["ad_soyad"]:
            return "Ad Soyad zorunludur."
        if not payload["sinif"]:
            return "Sinif zorunludur."
        if not payload["baslangic_tarihi"]:
            return "Baslangic tarihi zorunludur."
        return ""

    def _load_students_from_sqlite() -> None:
        try:
            state["students"] = list(student_controller.list_students(limit=1000, offset=0))
            state["courses"] = list(course_controller.list_courses(limit=1000, offset=0))
            state["view_state"] = "ready"
        except Exception as exc:
            state["students"] = []
            state["courses"] = []
            state["view_state"] = "error"
            _set_feedback("error", f"Ogrenci listesi yuklenemedi: {exc}")

    def _filtered_rows() -> list[dict[str, Any]]:
        return students_v3_filter_students(
            students=list(state["students"]),
            courses=list(state["courses"]),
            query=_safe_text(state["query"]),
            status_filter=_safe_text(state["status_filter"]) or STATUS_ALL,
        )

    def _select_record(record: dict[str, Any], page: ft.Page | None) -> None:
        _fill_form(record)
        _set_feedback("info", "Ogrenci forma yuklendi.")
        _render_list(page)
        if page:
            page.update()

    def _student_card(record: dict[str, Any], page: ft.Page | None) -> ft.Control:
        student_id = int(record.get("id", 0) or 0)
        selected = int(state.get("selected_id") or 0) == student_id
        status = _student_status(record, state["courses"])
        name = _safe_text(record.get("ad_soyad")) or "-"

        avatar = ft.Container(
            width=44,
            height=44,
            border_radius=22,
            bgcolor=f"{colors['primary']}1F",
            alignment=ft.Alignment(0, 0),
            content=ft.Text(_initials(name), weight=ft.FontWeight.W_600, color=colors["primary"]),
        )

        details = ft.Column(
            expand=True,
            spacing=2,
            controls=[
                ft.Text(name, size=15, weight=ft.FontWeight.W_600, color=colors["text_primary"], overflow=ft.TextOverflow.ELLIPSIS),
                ft.Row(
                    wrap=True,
                    spacing=spacing["sm"],
                    controls=[
                        ft.Text(_safe_text(record.get("sinif")) or "-", size=12, color=colors["text_secondary"]),
                        ft.Text(_course_label(student_id, state["courses"]), size=12, color=colors["text_secondary"]),
                        ft.Text(_safe_text(record.get("telefon")) or "-", size=12, color=colors["text_secondary"]),
                    ],
                ),
            ],
        )

        return ft.Container(
            bgcolor=f"{colors['primary']}0F" if selected else colors["surface"],
            border=ft.Border(
                top=ft.BorderSide(1, colors["primary"] if selected else colors["border_neutral"]),
                right=ft.BorderSide(1, colors["primary"] if selected else colors["border_neutral"]),
                bottom=ft.BorderSide(1, colors["primary"] if selected else colors["border_neutral"]),
                left=ft.BorderSide(3 if selected else 1, colors["primary"] if selected else colors["border_neutral"]),
            ),
            border_radius=radius["card"],
            padding=spacing["md"],
            on_click=lambda _: _select_record(record, page),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=spacing["md"],
                controls=[
                    avatar,
                    details,
                    build_badge(status, variant=_status_badge_variant(status)),
                ],
            ),
        )

    def _render_list(page: ft.Page | None = None) -> None:
        if state["view_state"] == "error":
            student_list.controls = [
                build_empty_state(
                    title="Liste yuklenemedi",
                    message="SQLite ogrenci verisi okunamadi.",
                    primary_action=build_secondary_button("Tekrar Dene", on_click=_handle_refresh),
                    icon=ft.Icons.ERROR_OUTLINE,
                )
            ]
            return

        rows = _filtered_rows()
        total = len(rows)
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        if state["page"] > total_pages:
            state["page"] = total_pages
        if state["page"] < 1:
            state["page"] = 1

        start = (int(state["page"]) - 1) * PAGE_SIZE
        page_rows = rows[start : start + PAGE_SIZE]
        result_text.value = f"{total} kayit"
        page_text.value = f"Sayfa {state['page']}/{total_pages}"
        prev_button.disabled = state["page"] <= 1
        next_button.disabled = state["page"] >= total_pages

        if not page_rows:
            student_list.controls = [
                build_empty_state(
                    title="Ogrenci bulunamadi",
                    message="Arama veya filtre kriterlerine uygun kayit yok.",
                    primary_action=build_primary_button("Yeni Ogrenci", icon=ft.Icons.PERSON_ADD, on_click=_handle_new),
                    secondary_action=build_secondary_button("Filtreleri Temizle", on_click=_handle_clear_filters),
                    icon=ft.Icons.GROUP_OFF,
                )
            ]
            return

        student_list.controls = [_student_card(record, page) for record in page_rows]

    def _refresh_from_sqlite(page: ft.Page | None = None) -> None:
        _load_students_from_sqlite()
        _render_list(page)

    def _handle_new(e: ft.ControlEvent) -> None:
        _clear_form()
        _set_feedback("info", "Yeni ogrenci formu hazir.")
        _render_list(e.page)
        e.page.update()

    def _handle_clear(e: ft.ControlEvent) -> None:
        _clear_form()
        _set_feedback("info", "Form temizlendi.")
        _render_list(e.page)
        e.page.update()

    def _handle_refresh(e: ft.ControlEvent) -> None:
        _refresh_from_sqlite(e.page)
        _set_feedback("info", "Liste SQLite verisinden yenilendi.")
        e.page.update()

    def _handle_save(e: ft.ControlEvent) -> None:
        payload = _payload()
        validation_error = _validate_payload(payload)
        if validation_error:
            _set_feedback("warning", validation_error)
            e.page.update()
            return

        try:
            student_id = student_controller.create_student(payload)
            _refresh_from_sqlite(e.page)
            for record in state["students"]:
                if int(record.get("id", 0) or 0) == int(student_id):
                    _fill_form(record)
                    break
            _set_feedback("success", "Ogrenci kaydedildi ve listede secildi.")
            _render_list(e.page)
        except Exception as exc:
            _set_feedback("error", str(exc))
        e.page.update()

    def _handle_update(e: ft.ControlEvent) -> None:
        selected_id = int(state.get("selected_id") or 0)
        if not selected_id:
            _set_feedback("warning", "Guncellemek icin listeden ogrenci secin.")
            e.page.update()
            return

        payload = _payload()
        validation_error = _validate_payload(payload)
        if validation_error:
            _set_feedback("warning", validation_error)
            e.page.update()
            return

        try:
            if student_controller.update_student(selected_id, payload):
                _refresh_from_sqlite(e.page)
                for record in state["students"]:
                    if int(record.get("id", 0) or 0) == selected_id:
                        _fill_form(record)
                        break
                _set_feedback("success", "Ogrenci guncellendi.")
            else:
                _set_feedback("warning", "Guncellenecek kayit bulunamadi.")
            _render_list(e.page)
        except Exception as exc:
            _set_feedback("error", str(exc))
        e.page.update()

    def _handle_delete(e: ft.ControlEvent) -> None:
        selected_id = int(state.get("selected_id") or 0)
        if not selected_id:
            _set_feedback("warning", "Silmek icin listeden ogrenci secin.")
            e.page.update()
            return

        try:
            student_controller.delete_student(selected_id)
            _clear_form()
            _refresh_from_sqlite(e.page)
            _set_feedback("success", "Ogrenci silindi.")
        except Exception as exc:
            _set_feedback("error", str(exc))
        e.page.update()

    def _handle_search(e: ft.ControlEvent) -> None:
        state["query"] = _safe_text(e.control.value)
        state["page"] = 1
        _refresh_from_sqlite(e.page)
        e.page.update()

    def _handle_filter(status: str):
        def handler(e: ft.ControlEvent) -> None:
            state["status_filter"] = status
            state["page"] = 1
            _refresh_from_sqlite(e.page)
            e.page.update()

        return handler

    def _handle_clear_filters(e: ft.ControlEvent) -> None:
        state["query"] = ""
        state["status_filter"] = STATUS_ALL
        state["page"] = 1
        if hasattr(search_input, "value"):
            search_input.value = ""
        _refresh_from_sqlite(e.page)
        e.page.update()

    def _previous_page(e: ft.ControlEvent) -> None:
        if state["page"] > 1:
            state["page"] -= 1
            _render_list(e.page)
            e.page.update()

    def _next_page(e: ft.ControlEvent) -> None:
        total = len(_filtered_rows())
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        if state["page"] < total_pages:
            state["page"] += 1
            _render_list(e.page)
            e.page.update()

    form_fields = ft.Column(
        controls=[
            name_field,
            class_field,
            parent_field,
            phone_field,
            email_field,
            username_field,
            password_field,
            start_date,
            end_date,
            status_dropdown,
            notes_field,
        ],
        spacing=spacing["sm"],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    form_footer = ft.Container(
        padding=ft.Padding(0, spacing["md"], 0, 0),
        border=ft.Border(top=ft.BorderSide(1, colors["border_neutral"])),
        content=ft.Row(
            wrap=True,
            spacing=spacing["sm"],
            controls=[
                build_secondary_button("Temizle", icon=ft.Icons.RESTART_ALT, on_click=_handle_clear),
                build_danger_button("Sil", icon=ft.Icons.DELETE_OUTLINE, on_click=_handle_delete),
                build_secondary_button("Guncelle", icon=ft.Icons.EDIT, on_click=_handle_update),
                build_primary_button("Kaydet", icon=ft.Icons.SAVE, on_click=_handle_save),
            ],
        ),
    )

    left_panel_content = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.Container(content=form_fields, expand=True),
            form_footer,
        ],
    )
    left_panel = build_card(
        title="Ogrenci Formu",
        subtitle="Kayit bilgileri",
        content=left_panel_content,
    )
    left_panel.expand = True
    search_input = build_search_box(
        hint_text="Ad, sinif, kur, telefon veya veli ara...",
        on_change=_handle_search,
    )

    filter_buttons = ft.Row(
        wrap=True,
        spacing=spacing["sm"],
        controls=[
            build_secondary_button("Tumu", on_click=_handle_filter(STATUS_ALL)),
            build_secondary_button("Aktif", on_click=_handle_filter(STATUS_ACTIVE)),
            build_secondary_button("Pasif", on_click=_handle_filter(STATUS_PASSIVE)),
            build_secondary_button("Tamamlanan", on_click=_handle_filter(STATUS_COMPLETED)),
        ],
    )

    prev_button = build_secondary_button("Onceki", icon=ft.Icons.CHEVRON_LEFT, on_click=_previous_page)
    next_button = build_secondary_button("Sonraki", icon=ft.Icons.CHEVRON_RIGHT, on_click=_next_page)

    list_footer = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        wrap=True,
        controls=[
            result_text,
            ft.Row(spacing=spacing["sm"], controls=[prev_button, page_text, next_button]),
        ],
    )

    right_panel_content = ft.Column(
        expand=True,
        spacing=spacing["md"],
        controls=[
            search_input,
            filter_buttons,
            ft.Container(content=student_list, expand=True),
            list_footer,
        ],
    )
    right_panel = build_card(
        title="Student Management List",
        subtitle="SQLite ogrenci kayitlari",
        action=build_primary_button("Yeni Ogrenci", icon=ft.Icons.PERSON_ADD, on_click=_handle_new),
        content=right_panel_content,
    )
    right_panel.expand = True
    main_content = ft.ResponsiveRow(
        columns=12,
        spacing=spacing["md"],
        run_spacing=spacing["md"],
        expand=True,
        controls=[
            ft.Container(col={"xs": 12, "md": 5, "xl": 4}, expand=True, content=left_panel),
            ft.Container(col={"xs": 12, "md": 7, "xl": 8}, expand=True, content=right_panel),
        ],
    )
    body = ft.Column(
        expand=True,
        spacing=spacing["md"],
        controls=[
            feedback_area,
            main_content,
        ],
    )

    _refresh_from_sqlite()
    _set_feedback("info", "Hazir")

    return ft.Container(
        expand=True,
        padding=spacing["lg"],
        content=body,
        data={
            "canonical": "students_v3",
            "features": ["crud", "search", "filters", "sqlite", "pagination", "responsive"],
        },
    )
