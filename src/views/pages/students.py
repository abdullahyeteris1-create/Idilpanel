"""LEGACY Students page.

Canonical Students page: views.pages.students_v3.build_students_v3_page.
This module is retained for reference only and must not receive new feature work.
"""

from __future__ import annotations

import flet as ft

from components import (
    AppCard,
    AppDatePicker,
    AppDropdown,
    AppInput,
    AppTextArea,
    ContentCard,
    PageContainer,
    PasswordInput,
    PrimaryButton,
    SecondaryButton,
    TwoColumnLayout,
)
from controllers.student_controller import StudentController
from repositories.student_repository import StudentRepository
from services.student_service import StudentService
from theme.theme import THEME_TOKENS


IS_LEGACY_STUDENTS_PAGE = True
CANONICAL_STUDENTS_MODULE = "views.pages.students_v3"


def _build_student_controller() -> StudentController:
    student_repository = StudentRepository()
    student_service = StudentService(student_repository=student_repository)
    return StudentController(student_service=student_service)


def build_students_page() -> ft.Control:
    """Build students page and wire UI -> controller -> service -> repository -> SQLite."""
    controller = _build_student_controller()
    colors = THEME_TOKENS["colors"]

    active_filter = {"value": "Tumu"}
    pagination_state = {"page": 1, "page_size": 6}
    student_cache: dict[int, dict] = {}
    filter_counts = {"Aktif": 0, "Pasif": 0, "Tamamlanan": 0, "Tumu": 0}

    student_dropdown = AppDropdown(
        label="Kayitli Ogrenci",
        options=[],
        hint_text="Listeden bir ogrenci secin",
    )
    name_field = AppInput(label="Ad Soyad", hint_text="Ogrenci adi ve soyadi", required=True)
    class_field = AppInput(label="Sinif", hint_text="Sinif secin", required=True)
    parent_name_field = AppInput(label="Veli Adi", hint_text="Veli adi ve soyadi")
    username_field = AppInput(label="Kullanici Adi", hint_text="Sisteme giris icin kullanici adi")
    password_field = PasswordInput(label="Sifre", hint_text="Sifre girin")
    phone_field = AppInput(label="Telefon", hint_text="5XX XXX XX XX")
    email_field = AppInput(label="E-posta", hint_text="ornek@email.com")

    start_date_state = {"value": ""}
    end_date_state = {"value": ""}
    start_date_picker = AppDatePicker(
        label="Baslangic Tarihi",
        value="",
        required=True,
        on_date_change=lambda value: start_date_state.update({"value": value}),
    )
    end_date_picker = AppDatePicker(
        label="Bitis Tarihi",
        value="",
        on_date_change=lambda value: end_date_state.update({"value": value}),
    )

    kur_dropdown = AppDropdown(
        label="Kur",
        options=[str(index) for index in range(1, 17)],
        hint_text="Kur secin",
        required=True,
    )
    notes_field = AppTextArea(
        label="Notlar",
        hint_text="Ogrenci hakkinda notlarinizi buraya yazabilirsiniz...",
        min_height=140,
        min_lines=6,
        max_lines=10,
    )

    result_text = ft.Text(value="Hazir", selectable=True, color=colors["text_secondary"])
    search_field = AppInput(label="", hint_text="Ara...")
    search_field.prefix_icon = ft.Icons.SEARCH
    search_field.width = 280

    page_info_text = ft.Text(value="Sayfa 1/1", color=colors["text_secondary"], size=15)
    total_info_text = ft.Text(value="Toplam 0 ogrenci", color=colors["text_secondary"], size=15)
    page_chip_text = ft.Text("1", size=12, weight=ft.FontWeight.W_600, color=colors["primary"])
    students_list = ft.Column(spacing=24, scroll=ft.ScrollMode.AUTO, expand=True)

    def _date_value(date_control: ft.Control) -> str:
        field = date_control.data["field"]
        return str(field.value or "").strip()

    def _set_date_value(date_control: ft.Control, value: str) -> None:
        field = date_control.data["field"]
        field.value = value

    def _extract_meta_value(note_text: str, key: str) -> str:
        for line in (note_text or "").splitlines():
            if line.startswith(f"{key}:"):
                return line.split(":", 1)[1].strip()
        return ""

    def _upsert_meta(note_text: str, key: str, value: str) -> str:
        lines = [line for line in (note_text or "").splitlines() if not line.startswith(f"{key}:")]
        if value:
            lines.append(f"{key}: {value}")
        return "\n".join(lines).strip()

    def _plain_notes(note_text: str) -> str:
        kept_lines: list[str] = []
        for line in (note_text or "").splitlines():
            if line.startswith("Kur:") or line.startswith("Durum:"):
                continue
            kept_lines.append(line)
        return "\n".join(kept_lines).strip()

    def _status_from_record(record: dict) -> str:
        note_text = str(record.get("notlar") or "")
        note_status = _extract_meta_value(note_text, "Durum")
        if note_status == "Tamamlandi":
            return "Tamamlandı"

        raw_status = str(record.get("durum") or "").strip()
        if raw_status == "Tamamlandi":
            return "Tamamlandı"
        if raw_status in {"Pasif", "Beklemede"}:
            return "Pasif"
        is_active = int(record.get("is_active", 1) or 1)
        return "Aktif" if is_active == 1 else "Pasif"

    def _initials(value: str) -> str:
        parts = [item for item in value.strip().split() if item]
        if not parts:
            return "--"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return f"{parts[0][0]}{parts[-1][0]}".upper()

    def _friendly_error(exc: Exception) -> str:
        message = str(exc)
        if "cannot be empty" in message:
            return "Lutfen zorunlu alanlari doldurun."
        if "must be a valid date" in message:
            return "Lutfen gecerli bir tarih secin."
        if "end date cannot be before start date" in message:
            return "Bitis tarihi baslangic tarihinden once olamaz."
        if "email must be valid" in message:
            return "E-posta adresi gecersiz."
        if "not found" in message:
            return "Kayit bulunamadi."
        return "Islem su an tamamlanamadi. Lutfen tekrar deneyin."

    def _validate_ui() -> bool:
        if not (name_field.value or "").strip():
            result_text.value = "Ad Soyad zorunludur."
            return False
        if not (class_field.value or "").strip():
            result_text.value = "Sinif bilgisi zorunludur."
            return False
        if not (kur_dropdown.value or "").strip():
            result_text.value = "Kur secimi zorunludur."
            return False
        if not _date_value(start_date_picker):
            result_text.value = "Baslangic tarihi zorunludur."
            return False
        return True

    def _build_notes_payload() -> str:
        lines: list[str] = []
        plain_notes = (notes_field.value or "").strip()
        if plain_notes:
            lines.append(plain_notes)

        kur_value = (kur_dropdown.value or "").strip()
        if kur_value:
            lines.append(f"Kur: {kur_value}")

        return "\n".join(lines)

    def payload() -> dict[str, str]:
        return {
            "ad_soyad": (name_field.value or "").strip(),
            "sinif": (class_field.value or "").strip(),
            "baslangic_tarihi": _date_value(start_date_picker),
            "bitis_tarihi": _date_value(end_date_picker),
            "veli_adi": (parent_name_field.value or "").strip(),
            "telefon": (phone_field.value or "").strip(),
            "email": (email_field.value or "").strip(),
            "kullanici_adi": (username_field.value or "").strip(),
            "sifre": (password_field.value or "").strip(),
            "durum": "Aktif",
            "notlar": _build_notes_payload(),
        }

    def _fill_form(record: dict) -> None:
        note_text = str(record.get("notlar") or "")
        name_field.value = str(record.get("ad_soyad") or "")
        class_field.value = str(record.get("sinif") or "")
        _set_date_value(start_date_picker, str(record.get("baslangic_tarihi") or ""))
        _set_date_value(end_date_picker, str(record.get("bitis_tarihi") or ""))
        start_date_state["value"] = _date_value(start_date_picker)
        end_date_state["value"] = _date_value(end_date_picker)
        parent_name_field.value = str(record.get("veli_adi") or "")
        phone_field.value = str(record.get("telefon") or "")
        email_field.value = str(record.get("email") or record.get("eposta") or "")
        username_field.value = str(record.get("kullanici_adi") or "")
        password_field.value = str(record.get("sifre") or "")
        kur_dropdown.value = _extract_meta_value(note_text, "Kur")
        notes_field.value = _plain_notes(note_text)

    def _is_visible_by_filter(record: dict) -> bool:
        filter_value = active_filter["value"]
        if filter_value == "Tumu":
            return True
        status = _status_from_record(record)
        if filter_value == "Tamamlanan":
            return status == "Tamamlandı"
        return status == filter_value

    def _matches_search(record: dict, query: str) -> bool:
        if not query:
            return True

        note_text = str(record.get("notlar") or "")
        kur_value = _extract_meta_value(note_text, "Kur")
        searchable = " ".join(
            [
                str(record.get("ad_soyad") or ""),
                str(record.get("sinif") or ""),
                str(kur_value or ""),
                str(_status_from_record(record)),
            ]
        ).lower()
        return query.lower() in searchable

    def _status_badge(status: str) -> ft.Control:
        if status == "Aktif":
            bg = "#DCFCE7"
            fg = "#166534"
        elif status == "Pasif":
            bg = "#FEF3C7"
            fg = "#92400E"
        else:
            bg = "#DBEAFE"
            fg = "#1E3A8A"
        return ft.Container(
            padding=ft.Padding(10, 4, 10, 4),
            border_radius=999,
            bgcolor=bg,
            content=ft.Text(status, size=12, weight=ft.FontWeight.W_600, color=fg),
        )

    def _filter_tone(value: str) -> tuple[str, str]:
        if value == "Aktif":
            return "#DCFCE7", "#166534"
        if value == "Pasif":
            return "#FEF3C7", "#92400E"
        if value == "Tamamlanan":
            return "#DBEAFE", "#1E3A8A"
        return "#EEF2FF", "#4338CA"

    def _build_student_card(record: dict) -> ft.Control:
        record_id = int(record.get("id", 0) or 0)
        status = _status_from_record(record)
        note_text = str(record.get("notlar") or "")
        kur_value = _extract_meta_value(note_text, "Kur") or "-"

        def _select(e: ft.ControlEvent) -> None:
            student_dropdown.value = str(record_id)
            _fill_form(record)
            result_text.value = "Kayit forma yuklendi."
            e.page.update()

        def _update_status(e: ft.ControlEvent, target: str) -> None:
            try:
                updated_notes = str(record.get("notlar") or "")
                updated_status = str(record.get("durum") or "Aktif")

                if target == "passive":
                    updated_status = "Beklemede"
                    updated_notes = _upsert_meta(updated_notes, "Durum", "")
                    result_text.value = "Kayit pasife alindi."
                elif target == "completed":
                    updated_notes = _upsert_meta(updated_notes, "Durum", "Tamamlandi")
                    result_text.value = "Egitim tamamlandi olarak isaretlendi."

                update_payload = {
                    "ad_soyad": str(record.get("ad_soyad") or ""),
                    "sinif": str(record.get("sinif") or ""),
                    "baslangic_tarihi": str(record.get("baslangic_tarihi") or ""),
                    "bitis_tarihi": str(record.get("bitis_tarihi") or ""),
                    "veli_adi": str(record.get("veli_adi") or ""),
                    "telefon": str(record.get("telefon") or ""),
                    "email": str(record.get("email") or record.get("eposta") or ""),
                    "kullanici_adi": str(record.get("kullanici_adi") or ""),
                    "sifre": str(record.get("sifre") or ""),
                    "durum": updated_status,
                    "notlar": updated_notes,
                }
                controller.update_student(record_id, update_payload)
                refresh_list()
            except Exception as exc:
                result_text.value = _friendly_error(exc)
            e.page.update()

        def _delete_from_menu(e: ft.ControlEvent) -> None:
            try:
                deleted = controller.delete_student(record_id)
                result_text.value = "Ogrenci kaydi silindi." if deleted else "Kayit bulunamadi."
                refresh_list()
            except Exception as exc:
                result_text.value = _friendly_error(exc)
            e.page.update()

        menu_button = ft.PopupMenuButton(
            icon=ft.Icons.MORE_VERT,
            items=[
                ft.PopupMenuItem(text="Duzenle", on_click=_select),
                ft.PopupMenuItem(text="Pasife Al", on_click=lambda e: _update_status(e, "passive")),
                ft.PopupMenuItem(text="Egitimi Tamamlandi", on_click=lambda e: _update_status(e, "completed")),
                ft.PopupMenuItem(text="Sil", on_click=_delete_from_menu),
            ],
        )

        row_content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=36,
                            height=36,
                            border_radius=18,
                            bgcolor=f"{colors['primary']}1F",
                            alignment=ft.Alignment(0, 0),
                            content=ft.Text(_initials(str(record.get('ad_soyad') or "")), size=12, weight=ft.FontWeight.W_600, color=colors["primary"]),
                        ),
                        ft.Column(
                            spacing=1,
                            controls=[
                                ft.TextButton(
                                    content=ft.Text(str(record.get("ad_soyad") or "-"), size=15, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                                    on_click=_select,
                                    style=ft.ButtonStyle(
                                        padding=ft.Padding(0, 0, 0, 0),
                                        overlay_color=ft.Colors.TRANSPARENT,
                                    ),
                                ),
                                ft.Text(f"{record.get('sinif') or '-'} • {kur_value}. Kur", size=12, color=colors["text_secondary"]),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[_status_badge(status), menu_button],
                ),
            ],
        )

        card = AppCard(content=row_content)
        card.height = 72
        card.padding = ft.Padding(14, 8, 14, 8)
        card.on_click = _select
        return card

    def _build_status_section(title: str, records: list[dict]) -> ft.Control:
        if not records:
            return ft.Container(
                padding=ft.Padding(0, 24, 0, 24),
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                    controls=[
                        ft.Icon(ft.Icons.INBOX_OUTLINED, color=colors["text_secondary"], size=24),
                        ft.Text(f"{title} listesi bos", size=16, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                        ft.Text("Bu bolumde henuz kayit bulunamadi.", color=colors["text_secondary"]),
                    ],
                ),
            )
        return ft.Column(spacing=12, controls=[_build_student_card(record) for record in records])

    def refresh_list() -> None:
        records = controller.list_students(limit=100, offset=0)
        student_cache.clear()
        dropdown_options: list[tuple[str, str]] = []
        searched_records: list[dict] = []
        filtered_records: list[dict] = []

        for record in records:
            record_id = int(record.get("id", 0) or 0)
            student_cache[record_id] = record
            dropdown_options.append((str(record_id), str(record.get("ad_soyad") or "Kayit")))
            if _matches_search(record, (search_field.value or "").strip()):
                searched_records.append(record)

        student_dropdown.options = [ft.dropdown.Option(key=key, text=text) for key, text in dropdown_options]

        for record in searched_records:
            if _is_visible_by_filter(record):
                filtered_records.append(record)

        page_size = int(pagination_state["page_size"])
        total_items = len(filtered_records)
        filter_counts["Tumu"] = len(searched_records)
        filter_counts["Aktif"] = sum(1 for r in searched_records if _status_from_record(r) == "Aktif")
        filter_counts["Pasif"] = sum(1 for r in searched_records if _status_from_record(r) == "Pasif")
        filter_counts["Tamamlanan"] = sum(1 for r in searched_records if _status_from_record(r) == "Tamamlandı")
        total_info_text.value = f"Toplam {total_items} ogrenci"

        total_pages = max(1, (total_items + page_size - 1) // page_size)
        if pagination_state["page"] > total_pages:
            pagination_state["page"] = total_pages

        current_page = int(pagination_state["page"])
        start = (current_page - 1) * page_size
        end = start + page_size
        paged_records = filtered_records[start:end]
        page_info_text.value = f"Sayfa {current_page}/{total_pages}"
        page_chip_text.value = str(current_page)

        if not paged_records:
            students_list.controls = [_build_status_section(active_filter["value"], [])]
            return

        students_list.controls = [_build_student_card(record) for record in paged_records]

    def _set_filter(filter_name: str) -> None:
        active_filter["value"] = filter_name
        pagination_state["page"] = 1
        refresh_list()

    def _go_prev_page(e: ft.ControlEvent) -> None:
        if pagination_state["page"] > 1:
            pagination_state["page"] -= 1
            refresh_list()
        e.page.update()

    def _go_next_page(e: ft.ControlEvent) -> None:
        pagination_state["page"] += 1
        refresh_list()
        e.page.update()

    def _on_search_change(e: ft.ControlEvent) -> None:
        pagination_state["page"] = 1
        refresh_list()
        e.page.update()

    def _filter_button(label: str, value: str) -> ft.Control:
        count = filter_counts.get(value, 0)
        bg, fg = _filter_tone(value)
        selected = active_filter["value"] == value
        return ft.TextButton(
            on_click=lambda e: (_set_filter(value), e.page.update()),
            style=ft.ButtonStyle(
                padding=ft.Padding(10, 0, 10, 0),
                shape=ft.RoundedRectangleBorder(radius=999),
                overlay_color=ft.Colors.TRANSPARENT,
            ),
            content=ft.Container(
                height=30,
                padding=ft.Padding(10, 0, 10, 0),
                border_radius=999,
                bgcolor=bg if selected else colors["surface"],
                border=ft.Border(
                    top=ft.BorderSide(1, bg if selected else colors["border"]),
                    right=ft.BorderSide(1, bg if selected else colors["border"]),
                    bottom=ft.BorderSide(1, bg if selected else colors["border"]),
                    left=ft.BorderSide(1, bg if selected else colors["border"]),
                ),
                alignment=ft.Alignment(0, 0),
                content=ft.Row(
                    spacing=6,
                    controls=[
                        ft.Text(label, size=12, color=fg if selected else colors["text_secondary"], weight=ft.FontWeight.W_600),
                        ft.Container(
                            padding=ft.Padding(6, 1, 6, 1),
                            border_radius=999,
                            bgcolor=colors["surface"] if selected else f"{colors['primary']}14",
                            content=ft.Text(str(count), size=11, color=fg if selected else colors["primary"], weight=ft.FontWeight.W_600),
                        ),
                    ],
                ),
            ),
        )

    def _selected_student_id() -> int | None:
        selected = (student_dropdown.value or "").strip()
        if not selected:
            return None
        return int(selected)

    def _reset_form(e: ft.ControlEvent) -> None:
        student_dropdown.value = None
        name_field.value = ""
        class_field.value = ""
        parent_name_field.value = ""
        username_field.value = ""
        password_field.value = ""
        phone_field.value = ""
        email_field.value = ""
        _set_date_value(start_date_picker, "")
        _set_date_value(end_date_picker, "")
        start_date_state["value"] = ""
        end_date_state["value"] = ""
        kur_dropdown.value = None
        notes_field.value = ""
        result_text.value = "Form temizlendi."
        e.page.update()

    def on_student_change(e: ft.ControlEvent) -> None:
        selected_id = _selected_student_id()
        if selected_id is None:
            e.page.update()
            return
        record = student_cache.get(selected_id) or controller.get_student(selected_id)
        if not record:
            result_text.value = "Kayit bulunamadi."
            e.page.update()
            return
        _fill_form(record)
        e.page.update()

    student_dropdown.on_change = on_student_change
    search_field.on_change = _on_search_change

    def handle_create(e: ft.ControlEvent) -> None:
        if not _validate_ui():
            e.page.update()
            return
        try:
            record_id = controller.create_student(payload())
            student_dropdown.value = str(record_id)
            result_text.value = "Ogrenci kaydi olusturuldu."
            refresh_list()
        except Exception as exc:
            result_text.value = _friendly_error(exc)
        e.page.update()

    def handle_get(e: ft.ControlEvent) -> None:
        selected_id = _selected_student_id()
        if selected_id is None:
            result_text.value = "Lutfen kayitli bir ogrenci secin."
            e.page.update()
            return
        try:
            record = controller.get_student(selected_id)
            if not record:
                result_text.value = "Kayit bulunamadi."
                e.page.update()
                return
            _fill_form(record)
            result_text.value = "Kayit getirildi."
        except Exception as exc:
            result_text.value = _friendly_error(exc)
        e.page.update()

    def handle_update(e: ft.ControlEvent) -> None:
        selected_id = _selected_student_id()
        if selected_id is None:
            result_text.value = "Lutfen guncellenecek kaydi secin."
            e.page.update()
            return
        if not _validate_ui():
            e.page.update()
            return
        try:
            updated = controller.update_student(selected_id, payload())
            result_text.value = "Ogrenci kaydi guncellendi." if updated else "Kayit bulunamadi."
            refresh_list()
        except Exception as exc:
            result_text.value = _friendly_error(exc)
        e.page.update()

    def handle_delete(e: ft.ControlEvent) -> None:
        selected_id = _selected_student_id()
        if selected_id is None:
            result_text.value = "Lutfen silinecek kaydi secin."
            e.page.update()
            return
        try:
            deleted = controller.delete_student(selected_id)
            result_text.value = "Ogrenci kaydi silindi." if deleted else "Kayit bulunamadi."
            student_dropdown.value = None
            refresh_list()
        except Exception as exc:
            result_text.value = _friendly_error(exc)
        e.page.update()

    form_fields = ft.ResponsiveRow(
        columns=12,
        spacing=12,
        run_spacing=12,
        controls=[
            ft.Container(col={"xs": 12, "sm": 12, "md": 12}, content=student_dropdown),
            ft.Container(col={"xs": 12, "sm": 12, "md": 12}, content=name_field),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=class_field),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=parent_name_field),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=username_field),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=password_field),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=phone_field),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=email_field),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=start_date_picker),
            ft.Container(col={"xs": 12, "sm": 6, "md": 6}, content=end_date_picker),
            ft.Container(col={"xs": 12, "sm": 12, "md": 12}, content=kur_dropdown),
            ft.Container(col={"xs": 12, "sm": 12, "md": 12}, content=notes_field),
        ],
    )

    form_actions = ft.Row(
        spacing=8,
        controls=[
            SecondaryButton("Temizle", on_click=_reset_form, icon=ft.Icons.RESTART_ALT),
            PrimaryButton("Kaydet", on_click=handle_create, icon=ft.Icons.SAVE),
            SecondaryButton("Getir", on_click=handle_get, icon=ft.Icons.DOWNLOAD_DONE),
            SecondaryButton("Guncelle", on_click=handle_update, icon=ft.Icons.EDIT),
            SecondaryButton("Sil", on_click=handle_delete, icon=ft.Icons.DELETE_OUTLINE),
        ],
    )

    form_panel = ContentCard(
        title="Ogrenci Bilgileri",
        subtitle="Yeni ogrenci bilgilerini girin",
        content=ft.Column(
            spacing=16,
            controls=[form_fields, form_actions, result_text],
        ),
    )
    form_panel.width = 420

    list_header_action = ft.Row(
        spacing=8,
        controls=[
            search_field,
            PrimaryButton("Yeni Ogrenci", on_click=_reset_form, icon=ft.Icons.ADD),
        ],
    )

    list_filters = ft.Row(
        spacing=8,
        controls=[
            _filter_button("Tumu", "Tumu"),
            _filter_button("Aktif", "Aktif"),
            _filter_button("Pasif", "Pasif"),
            _filter_button("Tamamlanan", "Tamamlanan"),
        ],
    )

    list_footer = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Row(
                spacing=8,
                controls=[
                    SecondaryButton("", on_click=_go_prev_page, icon=ft.Icons.CHEVRON_LEFT),
                    ft.Container(
                        width=28,
                        height=28,
                        border_radius=8,
                        alignment=ft.Alignment(0, 0),
                        bgcolor="#EEF2FF",
                        content=page_chip_text,
                    ),
                    SecondaryButton("", on_click=_go_next_page, icon=ft.Icons.CHEVRON_RIGHT),
                ],
            ),
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.END,
                spacing=2,
                controls=[page_info_text, total_info_text],
            ),
        ],
    )

    list_panel = ContentCard(
        title="Ogrenci Listesi",
        subtitle="Tum ogrencileri goruntuleyin",
        action=list_header_action,
        content=ft.Column(
            spacing=16,
            expand=True,
            controls=[
                list_filters,
                AppCard(content=students_list),
                list_footer,
            ],
        ),
    )
    list_panel.expand = True

    try:
        refresh_list()
    except Exception:
        students_list.controls = [ft.Text("Liste alinamadi. Once veri tabanini hazirlayin.")]

    layout = ft.Column(
        spacing=16,
        expand=True,
        controls=[
            ft.Text("Ogrenci Ekle", size=24, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
            TwoColumnLayout(left=form_panel, right=list_panel, left_flex=0, right_flex=1, spacing=24),
        ],
    )

    return PageContainer(content=layout, max_width=1888, padding=24)
