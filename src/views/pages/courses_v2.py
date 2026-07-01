"""Courses V2 page – Design System + Component Library + CourseController.

Sprint: Screen Library Sprint / Courses-5 – Courses V2 Search & Filter
Real SQLite via CourseController only.  No Service/Repository/SQLite direct imports.

DB schema (courses table):
    id, student_id, kur_no, baslangic, bitis, durum, hedef_ders_sayisi, is_active
    durum CHECK: Aktif | Beklemede | Tamamlandi | Iptal
    UNIQUE (student_id, kur_no, is_active)
    hedef_ders_sayisi always 16
"""

from __future__ import annotations

from datetime import date

import flet as ft

from components import (
    PageContainer,
    build_action_panel,
    build_app_dropdown,
    build_app_header,
    build_badge,
    build_danger_button,
    build_empty_state,
    build_error_state,
    build_filter_bar,
    build_form_card,
    build_loading_state,
    build_primary_button,
    build_search_bar,
    build_secondary_button,
    build_table_card,
    build_text_field,
)
from controllers import build_course_controller
from controllers.course_controller import CourseController


# ---------------------------------------------------------------------------
# Turkish error message mapper
# ---------------------------------------------------------------------------


def _friendly_error(exc: Exception) -> str:
    message = str(exc)
    if "course name cannot be empty" in message:
        return "Kur numarasi ve ogrenci kimlik bilgisi zorunludur."
    if "course level must be between" in message:
        return "Kur numarasi 1 ile 12 arasinda olmalidir."
    if "course duration must be a positive value" in message:
        return "Hedef ders sayisi pozitif bir sayi olmalidir."
    if "an active course with the same name already exists" in message:
        return "Ayni ogrenciye ayni kur ikinci kez atanamaz."
    if "UNIQUE constraint failed" in message:
        return "Bu ogrenciye ayni kur zaten atanmis."
    if "FOREIGN KEY constraint failed" in message:
        return "Gecersiz ogrenci kimlik numarasi."
    if "no such table" in message:
        return "Veri tabani hazir degil. Lutfen kurulum adimlarini kontrol edin."
    if "course data must be a mapping" in message:
        return "Form verisi gecersiz format."
    if "Bu kursun kontenjanı dolmuştur" in message or "Bu kursun kontenjanı dolmuştur." in message:
        return "Bu kursun kontenjanı dolmuştur."
    if "Pasif kurslara öğrenci atanamaz" in message or "Pasif kurslara ogrenci atanamaz" in message:
        return "Pasif kurslara ogrenci atanamaz."
    if "Tamamlanan kurslara" in message:
        return "Tamamlanan kurslara ogrenci atanamaz."
    if "zaten atanmışsınız" in message or "zaten atanmissiniz" in message:
        return "Bu kursa zaten atanmissiniz."
    return "Islem tamamlanamadi. Lutfen tekrar deneyin."


# ---------------------------------------------------------------------------
# Status helpers
# ---------------------------------------------------------------------------

_DURUM_OPTIONS = ["Aktif", "Beklemede", "Tamamlandi", "Iptal"]


def _status_variant(status: str) -> str:
    normalized = (status or "").strip().lower()
    if normalized == "aktif":
        return "success"
    if normalized == "beklemede" or normalized == "pasif":
        return "warning"
    if normalized == "tamamlandi" or normalized == "tamamlandı":
        return "primary"
    if normalized == "kontenjan dolu":
        return "danger"
    return "passive"


# ---------------------------------------------------------------------------
# Local filter (search/filter stay in-memory per sprint scope)
# ---------------------------------------------------------------------------


def _courses_v2_apply_filters(
    records: list[dict],
    search_query: str,
    status_filter: str,
    kur_filter: str,
    sort_field: str = "student_id",
    sort_direction: str = "Artan",
) -> list[dict]:
    query = (search_query or "").strip().lower()
    status_value = (status_filter or "Tumu").strip()
    kur_value = (kur_filter or "Tumu").strip()

    filtered = list(records)

    if query:
        def _matches(item: dict) -> bool:
            haystack = " ".join([
                str(item.get("student_id") or ""),
                str(item.get("kur_no") or ""),
                str(item.get("baslangic") or ""),
                str(item.get("durum") or ""),
            ]).lower()
            return query in haystack

        filtered = [item for item in filtered if _matches(item)]

    if status_value != "Tumu":
        filtered = [
            item for item in filtered
            if (item.get("durum") or "").strip() == status_value
        ]

    if kur_value != "Tumu":
        try:
            kur_int = int(kur_value)
            filtered = [
                item for item in filtered
                if int(item.get("kur_no", 0) or 0) == kur_int
            ]
        except ValueError:
            pass

    # Apply sorting
    reverse = sort_direction == "Azalan"

    if sort_field == "Kur":
        filtered.sort(key=lambda x: int(x.get("kur_no", 0) or 0), reverse=reverse)
    elif sort_field == "Baslangic":
        filtered.sort(key=lambda x: str(x.get("baslangic", "")), reverse=reverse)
    else:  # "Ogrenci ID" default
        filtered.sort(key=lambda x: int(x.get("student_id", 0) or 0), reverse=reverse)

    return filtered


# ---------------------------------------------------------------------------
# Responsive profile
# ---------------------------------------------------------------------------


def courses_v2_responsive_profile(width: int) -> str:
    """Classify viewport width using Courses V2 target breakpoints."""
    if width >= 1800:
        return "1920 px"
    if width >= 1500:
        return "1600 px"
    if width >= 1320:
        return "1366 px"
    if width >= 1200:
        return "1280 px"
    if width >= 768:
        return "Tablet"
    return "Mobil"


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------


def build_courses_v2_page() -> ft.Control:
    """Build Courses V2 page – real CRUD via CourseController."""

    controller: CourseController = build_course_controller()

    state: dict = {
        "courses": [],
        "filtered": [],
        "view_state": "loading",
        "edit_target": None,
        "selected_id": None,     # row currently selected in table
        "search_query": "",
        "status_filter": "Tumu",
        "kur_filter": "Tumu",
        "sort_field": "Ogrenci ID",
        "sort_direction": "Artan",
        "error_message": "",
    }

    # ------------------------------------------------------------------
    # Form fields
    # ------------------------------------------------------------------
    student_id_field = build_text_field("Ogrenci ID", required=True)
    # Mark first field for autofocus so keyboard lands there when form opens
    student_id_field.data["field"].autofocus = True
    kur_dropdown = build_app_dropdown(
        "Kur",
        options=[str(i) for i in range(1, 13)],
    )
    baslangic_field = build_text_field("Baslangic Tarihi (YYYY-AA-GG)", required=True)
    bitis_field = build_text_field("Bitis Tarihi (opsiyonel)")
    durum_dropdown = build_app_dropdown(
        "Durum",
        options=_DURUM_OPTIONS,
        value="Aktif",
    )

    form_error_host = ft.Container(visible=False)

    def _set_form_error(message: str) -> None:
        if message:
            form_error_host.content = build_badge(message, variant="danger")
            form_error_host.visible = True
        else:
            form_error_host.content = None
            form_error_host.visible = False

    # ------------------------------------------------------------------
    # Result info display
    # ------------------------------------------------------------------
    result_info_text = ft.Text("", size=13, color="#6B7280")

    def _update_result_info() -> None:
        total = len(state["courses"])
        filtered = len(state["filtered"])
        result_info_text.value = f"{total} kurstan {filtered} kayit gosteriliyor."

    # ------------------------------------------------------------------
    # Active filters display
    # ------------------------------------------------------------------
    active_filters_row = ft.Row(spacing=8, wrap=True)

    def _refresh_active_filters() -> None:
        controls: list[ft.Control] = []
        if state["search_query"]:
            controls.append(
                build_badge(f"Arama: {state['search_query']}", variant="primary")
            )
        if state["status_filter"] != "Tumu":
            controls.append(
                build_badge(f"Durum: {state['status_filter']}", variant="success")
            )
        if state["kur_filter"] != "Tumu":
            controls.append(
                build_badge(f"Kur: {state['kur_filter']}", variant="primary")
            )
        if state["sort_field"] != "Ogrenci ID" or state["sort_direction"] != "Artan":
            sort_label = f"{state['sort_field']} ({state['sort_direction']})"
            controls.append(
                build_badge(f"Siralama: {sort_label}", variant="warning")
            )
        active_filters_row.controls = controls

    # ------------------------------------------------------------------
    # Feedback helpers
    # ------------------------------------------------------------------
    table_host = ft.Column(spacing=10)
    feedback_tag_host = ft.Container(content=build_badge("Bilgi", variant="primary"))
    feedback_text = ft.Text("Hazir")
    feedback_row = ft.Row(spacing=8, controls=[feedback_tag_host, feedback_text])

    def _set_feedback(kind: str, message: str) -> None:
        variant = {
            "success": "success",
            "info": "primary",
            "warning": "warning",
            "error": "danger",
        }.get(kind, "primary")
        label = {
            "success": "Basari",
            "info": "Bilgi",
            "warning": "Uyari",
            "error": "Hata",
        }.get(kind, "Bilgi")
        feedback_tag_host.content = build_badge(label, variant=variant)
        feedback_text.value = message

    # ------------------------------------------------------------------
    # Active count
    # ------------------------------------------------------------------
    def _count_active() -> int:
        return sum(
            1 for item in state["courses"]
            if (item.get("durum") or "").strip() == "Aktif"
        )

    # ------------------------------------------------------------------
    # Data loader
    # ------------------------------------------------------------------
    def _load_courses() -> None:
        try:
            records = controller.list_courses(limit=500, offset=0)
            state["courses"] = list(records)
            state["error_message"] = ""
        except Exception as exc:
            state["courses"] = []
            state["error_message"] = _friendly_error(exc)

    # ------------------------------------------------------------------
    # State renderers
    # ------------------------------------------------------------------
    def _render_loading() -> None:
        table_host.controls = [build_loading_state("Kurslar yukleniyor...")]

    def _render_error(message: str) -> None:
        table_host.controls = [
            build_error_state(
                title="Hata",
                message=message or "Kurslar yuklenemedi.",
                action=build_secondary_button(
                    "Yenile",
                    on_click=lambda e: _reload_and_render(e.page),
                ),
            )
        ]

    def _render_table() -> None:
        records = list(state["filtered"])

        if not records:
            table_host.controls = [
                build_empty_state(
                    title="Kurs Bulunamadi",
                    message="Arama kriterlerine uygun kurs bulunamadi.",
                    primary_action=build_primary_button(
                        "Yeni Kurs",
                        on_click=lambda e: _open_form(e.page),
                    ),
                    icon=ft.Icons.SCHOOL_OUTLINED,
                )
            ]
            return

        rows: list[list] = []
        for item in records:
            item_id = int(item.get("id") or 0)
            is_selected = state["selected_id"] == item_id
            kur_no = int(item.get("kur_no") or 0)
            
            # Get capacity info for this kur level
            try:
                capacity_info = controller.get_course_capacity_info(kur_no)
                current_count = capacity_info.get("current_count", 0)
                max_capacity = capacity_info.get("max_capacity", 30)
                occupancy_rate = capacity_info.get("occupancy_rate", 0)
                effective_status = capacity_info.get("status", "Pasif")
            except Exception:
                current_count = 0
                max_capacity = 30
                occupancy_rate = 0
                effective_status = "Pasif"
            
            status_badge = build_badge(effective_status, variant=_status_variant(effective_status))

            # Selection indicator in ID column
            id_cell: ft.Control
            if is_selected:
                id_cell = ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.RADIO_BUTTON_CHECKED, size=16, color="#6366F1"),
                        ft.Text(str(item_id), weight=ft.FontWeight.W_600),
                    ],
                    spacing=4,
                    tight=True,
                )
            else:
                id_cell = ft.Text(str(item_id))

            select_btn = build_secondary_button(
                "Sec",
                on_click=lambda e, rec=item: _select_row(e.page, rec),
            )
            detail_btn = build_secondary_button(
                "Kurs Detayi",
                on_click=lambda e, rec=item: _open_course_detail_drawer(e.page, rec),
            )
            edit_btn = build_secondary_button(
                "Duzenle",
                on_click=lambda e, rec=item: _open_form(e.page, rec),
            )
            delete_btn = build_danger_button(
                "Sil",
                on_click=lambda e, rec=item: _confirm_delete(e.page, rec),
            )
            actions_row = ft.Row(controls=[select_btn, detail_btn, edit_btn, delete_btn], spacing=6)

            rows.append([
                id_cell,
                str(item.get("student_id") or "-"),
                f"Kur {item.get('kur_no', '-')}",
                str(item.get("baslangic") or "-"),
                f"{current_count}/{max_capacity}",
                f"%{occupancy_rate}",
                status_badge,
                actions_row,
            ])

        table_host.controls = [
            build_table_card(
                columns=["ID", "Ogrenci ID", "Kur", "Baslangic", "Mevcut/Max", "Doluluk", "Durum", "Islemler"],
                rows=rows,
                title="Kurs Listesi",
                subtitle=f"{len(records)} kurs listeleniyor",
            )
        ]

    # ------------------------------------------------------------------
    # Filter + reload
    # ------------------------------------------------------------------
    def _apply_and_render(page) -> None:
        state["filtered"] = _courses_v2_apply_filters(
            state["courses"],
            state["search_query"],
            state["status_filter"],
            state["kur_filter"],
            state["sort_field"],
            state["sort_direction"],
        )
        _update_result_info()
        _refresh_active_filters()
        _render_table()
        if page:
            page.update()

    def _reload_and_render(page) -> None:
        _load_courses()
        if state["error_message"]:
            state["view_state"] = "error"
            _render_error(state["error_message"])
            if page:
                page.update()
            return
        state["view_state"] = "list"
        _apply_and_render(page)

    # ------------------------------------------------------------------
    # Form helpers
    # ------------------------------------------------------------------
    def _get_field_value(container) -> str:
        return str(container.data["field"].value or "").strip()

    def _clear_form() -> None:
        student_id_field.data["field"].value = ""
        kur_dropdown.value = None
        baslangic_field.data["field"].value = date.today().isoformat()
        bitis_field.data["field"].value = ""
        durum_dropdown.value = "Aktif"
        _set_form_error("")

    def _populate_form(record: dict) -> None:
        student_id_field.data["field"].value = str(record.get("student_id") or "")
        kur_dropdown.value = str(record.get("kur_no") or "")
        baslangic_field.data["field"].value = str(record.get("baslangic") or "")
        bitis_field.data["field"].value = str(record.get("bitis") or "")
        durum_dropdown.value = str(record.get("durum") or "Aktif")
        _set_form_error("")

    def _open_form(page, record=None) -> None:
        state["edit_target"] = record
        if record:
            _populate_form(record)
            state["selected_id"] = int(record.get("id") or 0)
        else:
            _clear_form()
            state["selected_id"] = None
        state["view_state"] = "form"
        _refresh_view(page)

    def _select_row(page, record: dict) -> None:
        """Select a row in the table and auto-populate the form."""
        state["selected_id"] = int(record.get("id") or 0)
        _populate_form(record)
        state["edit_target"] = record
        state["view_state"] = "form"
        _refresh_view(page)

    def _close_form(page) -> None:
        _clear_form()
        state["edit_target"] = None
        state["selected_id"] = None
        state["view_state"] = "list"
        _reload_and_render(page)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def _validate_form():
        student_id_raw = _get_field_value(student_id_field)
        if not student_id_raw:
            return "Ogrenci ID zorunludur."
        try:
            student_id_int = int(student_id_raw)
            if student_id_int <= 0:
                raise ValueError
        except ValueError:
            return "Ogrenci ID gecerli bir tam sayi olmalidir."

        if not (kur_dropdown.value or "").strip():
            return "Kur secimi zorunludur."

        baslangic_raw = _get_field_value(baslangic_field)
        if not baslangic_raw:
            return "Baslangic tarihi zorunludur."
        try:
            date.fromisoformat(baslangic_raw)
        except ValueError:
            return "Baslangic tarihi YYYY-AA-GG formatinda olmalidir."

        bitis_raw = _get_field_value(bitis_field)
        if bitis_raw:
            try:
                date.fromisoformat(bitis_raw)
            except ValueError:
                return "Bitis tarihi YYYY-AA-GG formatinda olmalidir."

        return None

    def _build_payload() -> dict:
        student_id_raw = _get_field_value(student_id_field)
        kur_raw = (kur_dropdown.value or "").strip()
        return {
            "course_name": f"Ogrenci {student_id_raw} Kur {kur_raw}",
            "student_id": int(student_id_raw),
            "kur_no": int(kur_raw),
            "baslangic": _get_field_value(baslangic_field),
            "bitis": _get_field_value(bitis_field),
            "total_lessons": 16,
            "durum": (durum_dropdown.value or "Aktif").strip(),
        }

    # ------------------------------------------------------------------
    # Save handler
    # ------------------------------------------------------------------
    def _save_form(e) -> None:
        err = _validate_form()
        if err:
            _set_form_error(err)
            e.page.update()
            return

        payload = _build_payload()
        edit_target = state.get("edit_target")

        try:
            if edit_target:
                record_id = int(edit_target.get("id", 0))
                controller.update_course(record_id, payload)
                _set_feedback("success", "Kurs basariyla guncellendi.")
                # UPDATE: close form, go back to list
                _close_form(e.page)
            else:
                controller.create_course(payload)
                _set_feedback("success", "Kurs basariyla olusturuldu.")
                # CREATE: stay in form, clear fields, focus first field
                _load_courses()
                state["filtered"] = _courses_v2_apply_filters(
                    state["courses"],
                    state["search_query"],
                    state["status_filter"],
                    state["kur_filter"],
                )
                _clear_form()
                _set_form_error("")
                if e.page:
                    try:
                        e.page.set_focus(student_id_field.data["field"])
                    except Exception:
                        pass
                    e.page.update()
        except Exception as exc:
            _set_form_error(_friendly_error(exc))
            e.page.update()
            return

    # ------------------------------------------------------------------
    # Delete handler
    # ------------------------------------------------------------------
    def _confirm_delete(page, record: dict) -> None:
        if page is None:
            return

        record_id = int(record.get("id", 0))
        label = f"Ogrenci {record.get('student_id', '?')} – Kur {record.get('kur_no', '?')}"

        def _do_delete(ev) -> None:
            try:
                controller.delete_course(record_id)
                _set_feedback("success", "Kurs basariyla silindi.")
            except Exception as exc:
                _set_feedback("error", _friendly_error(exc))
            ev.page.close(modal)
            state["selected_id"] = None
            _reload_and_render(ev.page)

        def _cancel_delete(ev) -> None:
            ev.page.close(modal)

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Kursu Sil"),
            content=ft.Text(f"'{label}' kaydini silmek istediginizden emin misiniz?"),
            actions=[
                build_secondary_button("Vazgec", on_click=_cancel_delete),
                build_danger_button("Sil", on_click=_do_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(modal)
        page.update()

    # ------------------------------------------------------------------
    # Course detail drawer
    # ------------------------------------------------------------------
    def _open_course_detail_drawer(page, course_record: dict) -> None:
        """Open a drawer showing course details and enrolled students."""
        if page is None:
            _set_feedback("warning", "Sayfa hazir degil.")
            return
        
        course_id = int(course_record.get("id", 0) or 0)
        if not course_id:
            _set_feedback("warning", "Kurs secimi gecersiz.")
            return
        
        try:
            # Get the course information
            course_info = controller.get_course(course_id)
            if not course_info:
                _set_feedback("warning", "Kurs bulunamadi.")
                return
            
            # Try to get students for this course
            students = []
            try:
                students = list(controller.get_students_for_course(course_id))
            except Exception:
                students = []
            
            # Build course details
            kur_no = int(course_info.get("kur_no", 0) or 0)
            baslangic = str(course_info.get("baslangic") or "-")
            durum = str(course_info.get("durum") or "-")
            
            # Get capacity info
            try:
                capacity_info = controller.get_course_capacity_info(kur_no)
                current_count = capacity_info.get("current_count", 0)
                max_capacity = capacity_info.get("max_capacity", 30)
                occupancy_rate = capacity_info.get("occupancy_rate", 0)
                effective_status = capacity_info.get("status", "Pasif")
            except Exception:
                current_count = 0
                max_capacity = 30
                occupancy_rate = 0
                effective_status = durum
            
            detail_content_controls = [
                ft.Text("Kurs Bilgileri", size=16, weight=ft.FontWeight.W_600),
                ft.Divider(),
                ft.Row([
                    ft.Column(controls=[
                        ft.Text("Kur Numarasi:", weight=ft.FontWeight.W_600, size=12),
                        ft.Text(f"Kur {kur_no}", size=14),
                    ], spacing=2),
                    ft.Column(controls=[
                        ft.Text("Durum:", weight=ft.FontWeight.W_600, size=12),
                        build_badge(effective_status, variant=_status_variant(effective_status)),
                    ], spacing=2),
                ], spacing=16),
                ft.Row([
                    ft.Column(controls=[
                        ft.Text("Baslangic Tarihi:", weight=ft.FontWeight.W_600, size=12),
                        ft.Text(baslangic, size=14),
                    ], spacing=2),
                    ft.Column(controls=[
                        ft.Text("Hedef Ders Sayisi:", weight=ft.FontWeight.W_600, size=12),
                        ft.Text("16", size=14),
                    ], spacing=2),
                ], spacing=16),
                ft.Row([
                    ft.Column(controls=[
                        ft.Text("Mevcut Ogrenci:", weight=ft.FontWeight.W_600, size=12),
                        ft.Text(str(current_count), size=14),
                    ], spacing=2),
                    ft.Column(controls=[
                        ft.Text("Maksimum Ogrenci:", weight=ft.FontWeight.W_600, size=12),
                        ft.Text(str(max_capacity), size=14),
                    ], spacing=2),
                    ft.Column(controls=[
                        ft.Text("Doluluk Orani:", weight=ft.FontWeight.W_600, size=12),
                        ft.Text(f"%{occupancy_rate}", size=14),
                    ], spacing=2),
                ], spacing=16),
                ft.Divider(),
                ft.Text("Kayitli Ogrenciler", size=16, weight=ft.FontWeight.W_600),
            ]
            
            # Build student list
            if not students:
                detail_content_controls.append(
                    build_empty_state(
                        title="Ogrenci Yok",
                        message="Bu kursa henuz ogrenci atanmadi.",
                    )
                )
            else:
                # Build student table
                student_rows = []
                for student in students:
                    # Skip deleted students (deleted_at is not NULL)
                    if student.get("deleted_at"):
                        continue
                    
                    student_durum = str(student.get("durum") or "Aktif")
                    durum_badge = build_badge(student_durum, variant=_status_variant(student_durum))
                    
                    student_rows.append([
                        str(student.get("ad_soyad") or "-"),
                        str(student.get("sinif") or "-"),
                        str(student.get("telefon") or "-"),
                        str(student.get("baslangic_tarihi") or "-"),
                        durum_badge,
                    ])
                
                from components import build_table_card
                detail_content_controls.append(
                    build_table_card(
                        columns=["Ad Soyad", "Sinif", "Telefon", "Baslangic Tarihi", "Durum"],
                        rows=student_rows,
                    )
                )
            
            # Build drawer content
            drawer = ft.NavigationDrawer(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row([
                                    ft.Text(f"Kurs {kur_no} Detaylari", 
                                           size=18, weight=ft.FontWeight.W_600),
                                    ft.IconButton(
                                        ft.Icons.CLOSE,
                                        on_click=lambda e: _close_drawer(page, drawer),
                                    ),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ] + detail_content_controls,
                            scroll=ft.ScrollMode.AUTO,
                            spacing=12,
                        ),
                        padding=20,
                    )
                ]
            )
            
            page.drawer = drawer
            page.drawer.open = True
            page.update()
            
        except Exception as exc:
            _set_feedback("error", _friendly_error(exc))
            page.update()
    
    def _close_drawer(page, drawer) -> None:
        """Close the course detail drawer."""
        drawer.open = False
        page.update()

    # ------------------------------------------------------------------
    # Search / Filter handlers
    # ------------------------------------------------------------------
    def _on_search_change(e) -> None:
        state["search_query"] = str(e.control.value or "").strip()
        _apply_and_render(e.page)

    def _on_search_submit(e) -> None:
        state["search_query"] = str(e.control.value or "").strip()
        _apply_and_render(e.page)

    def _on_status_filter_change(e) -> None:
        state["status_filter"] = str(e.control.value or "Tumu").strip()
        _apply_and_render(e.page)

    def _on_kur_filter_change(e) -> None:
        state["kur_filter"] = str(e.control.value or "Tumu").strip()
        _apply_and_render(e.page)

    def _on_sort_field_change(e) -> None:
        state["sort_field"] = str(e.control.value or "Ogrenci ID").strip()
        _apply_and_render(e.page)

    def _on_sort_direction_change(e) -> None:
        state["sort_direction"] = str(e.control.value or "Artan").strip()
        _apply_and_render(e.page)

    def _clear_all_filters(page) -> None:
        """Clear search, filters, and sort to defaults."""
        state["search_query"] = ""
        state["status_filter"] = "Tumu"
        state["kur_filter"] = "Tumu"
        state["sort_field"] = "Ogrenci ID"
        state["sort_direction"] = "Artan"
        search_bar.content.content.value = ""  # clear search box
        filter_status.value = "Tumu"
        filter_kur.value = "Tumu"
        sort_field_dropdown.value = "Ogrenci ID"
        sort_direction_dropdown.value = "Artan"
        _apply_and_render(page)
        _set_feedback("info", "Filtreler temizlendi.")

    # ------------------------------------------------------------------
    # Filter controls (including sort and clear button)
    # ------------------------------------------------------------------
    filter_status = build_app_dropdown(
        label="Durum",
        options=["Tumu"] + _DURUM_OPTIONS,
        value="Tumu",
        on_change=_on_status_filter_change,
    )
    filter_kur = build_app_dropdown(
        label="Kur",
        options=["Tumu"] + [str(i) for i in range(1, 13)],
        value="Tumu",
        on_change=_on_kur_filter_change,
    )
    sort_field_dropdown = build_app_dropdown(
        label="Siralama",
        options=["Ogrenci ID", "Kur", "Baslangic"],
        value="Ogrenci ID",
        on_change=_on_sort_field_change,
    )
    sort_direction_dropdown = build_app_dropdown(
        label="Yon",
        options=["Artan", "Azalan"],
        value="Artan",
        on_change=_on_sort_direction_change,
    )
    filter_status.col = {"xs": 12, "sm": 6, "md": 4}
    filter_kur.col = {"xs": 12, "sm": 6, "md": 4}
    sort_field_dropdown.col = {"xs": 12, "sm": 6, "md": 4}
    sort_direction_dropdown.col = {"xs": 12, "sm": 6, "md": 2}

    clear_filters_btn = build_secondary_button(
        "Filtreleri Temizle",
        on_click=lambda e: _clear_all_filters(e.page),
    )
    clear_filters_btn.col = {"xs": 12, "sm": 6, "md": 2}

    def _show_only_status(page, durum: str) -> None:
        state["status_filter"] = durum
        filter_status.value = durum
        _apply_and_render(page)
        if page:
            page.update()

    # ------------------------------------------------------------------
    # View switcher
    # ------------------------------------------------------------------
    form_host = ft.Column(spacing=12)
    content_host = ft.Column(spacing=16)

    def _refresh_view(page) -> None:
        view = state["view_state"]

        if view == "loading":
            _render_loading()
            content_host.controls = [table_host]

        elif view == "error":
            _render_error(state.get("error_message", ""))
            content_host.controls = [table_host]

        elif view == "form":
            edit_target = state.get("edit_target")
            form_title = "Kursu Duzenle" if edit_target else "Yeni Kurs"
            form_subtitle = (
                "Bilgileri guncelleyiniz." if edit_target else "Kurs bilgilerini giriniz."
            )

            student_id_field.col = {"xs": 12, "sm": 6, "md": 3}
            kur_dropdown.col = {"xs": 12, "sm": 6, "md": 3}
            baslangic_field.col = {"xs": 12, "sm": 6, "md": 3}
            bitis_field.col = {"xs": 12, "sm": 6, "md": 3}
            durum_dropdown.col = {"xs": 12, "sm": 6, "md": 3}

            form_host.controls = [
                ft.Row(
                    controls=[
                        build_primary_button("Kaydet", on_click=_save_form),
                        build_secondary_button(
                            "Temizle",
                            on_click=lambda e: (_clear_form(), e.page.update()),
                        ),
                        build_secondary_button(
                            "Iptal", on_click=lambda e: _close_form(e.page)
                        ),
                    ],
                    spacing=8,
                ),
                form_error_host,
                build_form_card(
                    fields=[
                        student_id_field,
                        kur_dropdown,
                        baslangic_field,
                        bitis_field,
                        durum_dropdown,
                    ],
                    title=form_title,
                    subtitle=form_subtitle,
                ),
            ]
            content_host.controls = [form_host]

        else:
            _apply_and_render(page)
            content_host.controls = [table_host]

        if page:
            page.update()

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    header = build_app_header(
        title="Kurslar",
        subtitle="Kurs yonetimi",
        actions=[
            build_primary_button(
                "➕  Yeni Kurs",
                on_click=lambda e: _open_form(e.page),
            )
        ],
    )

    # ------------------------------------------------------------------
    # Action panel
    # ------------------------------------------------------------------
    action_panel = build_action_panel(
        title="Hizli Islemler",
        subtitle="Kurs yonetimi akislari",
        actions=[
            {
                "key": "new_course",
                "title": "Yeni Kurs",
                "subtitle": "Yeni bir kurs olustur",
                "icon": ft.Icons.ADD_CIRCLE_OUTLINE,
                "on_click": lambda e: _open_form(e.page),
            },
            {
                "key": "active_courses",
                "title": "Aktif Kurslar",
                "subtitle": "Yalnizca aktif kurslari goster",
                "icon": ft.Icons.CHECK_CIRCLE_OUTLINE,
                "on_click": lambda e: _show_only_status(e.page, "Aktif"),
            },
            {
                "key": "all_courses",
                "title": "Tum Kurslar",
                "subtitle": "Tum kurs kayitlari",
                "icon": ft.Icons.LIST_ALT_OUTLINED,
                "on_click": lambda e: _show_only_status(e.page, "Tumu"),
            },
        ],
    )

    # ------------------------------------------------------------------
    # Search bar (store reference for clearing)
    # ------------------------------------------------------------------
    search_bar_ref = None

    search_bar = build_search_bar(
        title="Arama",
        subtitle="Ogrenci ID, Kur No, Baslangic, Durum",
        hint_text="Kurs ara...",
        on_change=_on_search_change,
        on_submit=_on_search_submit,
    )
    search_bar_ref = search_bar

    # ------------------------------------------------------------------
    # Filter bar (with sort + clear)
    # ------------------------------------------------------------------
    filter_bar = build_filter_bar(
        filters=[filter_status, filter_kur, sort_field_dropdown, sort_direction_dropdown, clear_filters_btn],
        title="Filtreler & Siralama",
        subtitle="Listeyi filtreleyin ve siralayın",
    )

    # ------------------------------------------------------------------
    # Initial data load
    # ------------------------------------------------------------------
    _render_loading()
    _load_courses()
    if state["error_message"]:
        state["view_state"] = "error"
        _render_error(state["error_message"])
    else:
        state["view_state"] = "list"
        state["filtered"] = _courses_v2_apply_filters(
            state["courses"],
            state["search_query"],
            state["status_filter"],
            state["kur_filter"],
            state["sort_field"],
            state["sort_direction"],
        )
        _update_result_info()
        _refresh_active_filters()
        _render_table()

    content_host.controls = [table_host]

    # ------------------------------------------------------------------
    # Assemble page
    # ------------------------------------------------------------------
    return PageContainer(
        content=ft.Column(
            spacing=16,
            controls=[
                header,
                feedback_row,
                action_panel,
                search_bar,
                result_info_text,
                active_filters_row,
                filter_bar,
                content_host,
            ],
        )
    )
