"""Text Library page for Sprint TX-1."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import traceback

import flet as ft

from components import AppCard, AppDropdown, AppInput, ContentCard, PageContainer, PrimaryButton, SecondaryButton, TwoColumnLayout
from controllers import build_text_controller
from localization.tr import tr_error_message
from theme.theme import THEME_TOKENS


COURSE_LEVELS = list(range(1, 13))


def _as_text(value: object) -> str:
    return str(value or "").strip()


def _active_label(value: object) -> str:
    return "Aktif" if int(value or 0) == 1 else "Pasif"


def _selected_int(value: object) -> int | None:
    text = _as_text(value)
    return int(text) if text else None


def _log_import_exception(exc: Exception, file_path: str | None = None) -> None:
    tb = traceback.format_exc()
    traceback_tail = traceback.extract_tb(exc.__traceback__)[-1:] if exc.__traceback__ else []
    location = traceback_tail[0] if traceback_tail else None
    with open("debug_text_library_import.log", "a", encoding="utf-8") as handle:
        handle.write("=" * 80 + "\n")
        handle.write(f"TEXT LIBRARY IMPORT ERROR: {datetime.now().isoformat(timespec='seconds')}\n")
        handle.write(f"file_path: {file_path or '-'}\n")
        handle.write(f"exception_type: {type(exc).__name__}\n")
        handle.write(f"exception_message: {exc}\n")
        if location is not None:
            handle.write(f"error_location: {location.filename}:{location.lineno} in {location.name}\n")
            handle.write(f"error_line: {location.line}\n")
        handle.write("traceback:\n")
        handle.write(tb)
        handle.write("\n")


def build_text_library_page() -> ft.Control:
    """Build central text library CRUD screen."""
    controller = build_text_controller()
    colors = THEME_TOKENS["colors"]

    state: dict[str, object] = {
        "selected_id": None,
        "records": [],
    }

    title_field = AppInput(label="Metin Adi", hint_text="Ornek: Daginik Cocuk", required=True)
    course_level_dropdown = AppDropdown(
        label="Kur",
        options=[(str(level), f"{level}. Kur") for level in COURSE_LEVELS],
        value="1",
        required=True,
    )
    category_field = AppInput(label="Kategori", hint_text="Opsiyonel")
    word_count_field = AppInput(label="Kelime Sayisi", hint_text="Opsiyonel")
    status_dropdown = AppDropdown(
        label="Durum",
        options=[("1", "Aktif"), ("0", "Pasif")],
        value="1",
    )

    search_field = AppInput(label="", hint_text="Metin veya kategori ara...")
    search_field.prefix_icon = ft.Icons.SEARCH
    course_filter = AppDropdown(
        label="Kur Filtresi",
        options=[("", "Tumu"), *[(str(level), f"{level}. Kur") for level in COURSE_LEVELS]],
        value="",
    )

    result_text = ft.Text("Yeni metin eklemek icin formu doldurun.", color=colors["text_secondary"], selectable=True)
    selected_text = ft.Text("Secili kayit yok", color=colors["text_secondary"], size=13)
    list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    file_picker = ft.FilePicker()

    def _selected_id() -> int | None:
        value = state.get("selected_id")
        return int(value) if value else None

    def _payload() -> dict[str, object]:
        return {
            "title": title_field.value,
            "course_level": course_level_dropdown.value,
            "category": category_field.value,
            "word_count": word_count_field.value,
            "is_active": status_dropdown.value,
        }

    def _clear_form() -> None:
        state["selected_id"] = None
        title_field.value = ""
        course_level_dropdown.value = "1"
        category_field.value = ""
        word_count_field.value = ""
        status_dropdown.value = "1"
        selected_text.value = "Secili kayit yok"

    def _fill_form(record: dict) -> None:
        state["selected_id"] = int(record.get("id") or 0)
        title_field.value = _as_text(record.get("title"))
        course_level_dropdown.value = str(record.get("course_level") or "1")
        category_field.value = _as_text(record.get("category"))
        word_count_field.value = _as_text(record.get("word_count"))
        status_dropdown.value = str(record.get("is_active") if record.get("is_active") is not None else 1)
        selected_text.value = f"Secili kayit: #{record.get('id')}"

    def _empty_list(message: str) -> ft.Control:
        return AppCard(
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.INBOX_OUTLINED, color=colors["text_secondary"]),
                    ft.Text(message, color=colors["text_secondary"]),
                ],
            )
        )

    def _build_text_card(record: dict) -> ft.Control:
        record_id = int(record.get("id") or 0)
        is_selected = _selected_id() == record_id
        status = _active_label(record.get("is_active"))
        status_bg = "#DCFCE7" if status == "Aktif" else "#F1F5F9"
        status_fg = "#166534" if status == "Aktif" else colors["text_secondary"]

        def _select(e: ft.ControlEvent) -> None:
            _fill_form(record)
            result_text.value = "Kayit forma getirildi."
            e.page.update()

        card = ft.Container(
            padding=14,
            border_radius=8,
            bgcolor="#F8FAFC" if is_selected else colors["surface"],
            border=ft.Border(
                top=ft.BorderSide(1, colors["primary"] if is_selected else colors["border"]),
                right=ft.BorderSide(1, colors["primary"] if is_selected else colors["border"]),
                bottom=ft.BorderSide(1, colors["primary"] if is_selected else colors["border"]),
                left=ft.BorderSide(1, colors["primary"] if is_selected else colors["border"]),
            ),
            on_click=_select,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(_as_text(record.get("title")), size=15, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
                                    ft.Text(
                                        f"{record.get('course_level')}. Kur"
                                        + (f" | {_as_text(record.get('category'))}" if _as_text(record.get("category")) else ""),
                                        size=12,
                                        color=colors["text_secondary"],
                                    ),
                                ],
                            ),
                            ft.Container(
                                padding=ft.Padding(8, 3, 8, 3),
                                border_radius=999,
                                bgcolor=status_bg,
                                content=ft.Text(status, size=11, weight=ft.FontWeight.W_600, color=status_fg),
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.FORMAT_LIST_NUMBERED, size=16, color=colors["text_secondary"]),
                            ft.Text(f"Kelime: {_as_text(record.get('word_count')) or '-'}", size=12, color=colors["text_secondary"]),
                            ft.Text(f"ID: {record_id}", size=12, color=colors["text_secondary"]),
                        ],
                    ),
                ],
            ),
        )
        return card

    def _refresh_list() -> None:
        query = _as_text(search_field.value)
        level = _selected_int(course_filter.value)
        records = list(controller.search_texts(query=query, course_level=level, limit=500, offset=0))
        state["records"] = records
        list_column.controls = [_build_text_card(record) for record in records]
        if not records:
            list_column.controls = [_empty_list("Metin bulunamadi.")]

    def _handle_create(e: ft.ControlEvent) -> None:
        try:
            record_id = controller.create_text(_payload())
            result_text.value = f"Metin eklendi. Kayit ID: {record_id}"
            _clear_form()
            _refresh_list()
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def _handle_update(e: ft.ControlEvent) -> None:
        record_id = _selected_id()
        if record_id is None:
            result_text.value = "Guncellemek icin listeden bir metin secin."
            e.page.update()
            return
        try:
            updated = controller.update_text(record_id, _payload())
            result_text.value = "Metin guncellendi." if updated else "Kayit bulunamadi."
            _refresh_list()
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def _handle_delete(e: ft.ControlEvent) -> None:
        record_id = _selected_id()
        if record_id is None:
            result_text.value = "Silmek icin listeden bir metin secin."
            e.page.update()
            return
        try:
            deleted = controller.delete_text(record_id)
            result_text.value = "Metin silindi." if deleted else "Kayit bulunamadi."
            _clear_form()
            _refresh_list()
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        e.page.update()

    def _handle_clear(e: ft.ControlEvent) -> None:
        _clear_form()
        result_text.value = "Form temizlendi."
        _refresh_list()
        e.page.update()

    def _handle_filter_change(e: ft.ControlEvent) -> None:
        _refresh_list()
        e.page.update()

    def _ensure_file_picker(page: ft.Page | None) -> bool:
        if page is None:
            result_text.value = "Dosya secici acilamadi."
            return False
        if file_picker not in page.services:
            page.services.append(file_picker)
            page.update()
        return True

    def _write_export_file(directory: str, content: bytes) -> str:
        export_dir = Path(directory)
        export_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = export_dir / f"metin_kutuphanesi_{timestamp}.xlsx"
        file_path.write_bytes(content)
        return str(file_path)

    async def _handle_import_pick(e: ft.ControlEvent) -> None:
        if not _ensure_file_picker(e.page):
            if e.page:
                e.page.update()
            return
        selected_path: str | None = None
        try:
            selected_files = await file_picker.pick_files(
                dialog_title="Excel dosyasi sec",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["xlsx"],
                allow_multiple=False,
            )
            selected_file = selected_files[0] if selected_files else None
            if selected_file is None or not selected_file.path:
                result_text.value = "Excel dosyasi secilmedi."
                return

            selected_path = selected_file.path
            summary = controller.import_texts_from_xlsx(selected_path)
            result_text.value = (
                f"{summary['processed']} kayit islendi | "
                f"{summary['inserted']} yeni kayit eklendi | "
                f"{summary['skipped']} kayit zaten vardi, atlandi"
            )
            _refresh_list()
        except ValueError as exc:
            _log_import_exception(exc, selected_path)
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            _log_import_exception(exc, selected_path)
            result_text.value = tr_error_message(exc)
        finally:
            if e.page:
                e.page.update()

    async def _handle_export_pick(e: ft.ControlEvent) -> None:
        if not _ensure_file_picker(e.page):
            if e.page:
                e.page.update()
            return
        try:
            export_path = await file_picker.get_directory_path(
                dialog_title="Excel disa aktarma klasoru sec"
            )
            if not export_path:
                result_text.value = "Disa aktarma klasoru secilmedi."
                return

            file_path = _write_export_file(export_path, controller.export_texts_xlsx_bytes())
            result_text.value = f"Excel disa aktarildi: {file_path}"
        except ValueError as exc:
            result_text.value = tr_error_message(exc)
        except Exception as exc:
            result_text.value = tr_error_message(exc)
        finally:
            if e.page:
                e.page.update()

    search_field.on_change = _handle_filter_change
    course_filter.on_select = _handle_filter_change

    form_fields = ft.ResponsiveRow(
        columns=12,
        spacing=12,
        run_spacing=12,
        controls=[
            ft.Container(col={"xs": 12}, content=title_field),
            ft.Container(col={"xs": 12, "sm": 6}, content=course_level_dropdown),
            ft.Container(col={"xs": 12, "sm": 6}, content=status_dropdown),
            ft.Container(col={"xs": 12}, content=category_field),
            ft.Container(col={"xs": 12}, content=word_count_field),
        ],
    )

    actions = ft.ResponsiveRow(
        columns=12,
        spacing=8,
        run_spacing=8,
        controls=[
            ft.Container(col={"xs": 12, "sm": 6}, content=PrimaryButton("Kaydet", on_click=_handle_create, icon=ft.Icons.SAVE, expand=True)),
            ft.Container(col={"xs": 12, "sm": 6}, content=SecondaryButton("Guncelle", on_click=_handle_update, icon=ft.Icons.EDIT, expand=True)),
            ft.Container(col={"xs": 12, "sm": 6}, content=SecondaryButton("Sil", on_click=_handle_delete, icon=ft.Icons.DELETE_OUTLINE, expand=True)),
            ft.Container(col={"xs": 12, "sm": 6}, content=SecondaryButton("Temizle", on_click=_handle_clear, icon=ft.Icons.CLEAR, expand=True)),
        ],
    )

    form_panel = ContentCard(
        title="Metin Formu",
        subtitle="Metinleri merkezi kutuphanede yonetin",
        content=ft.Column(spacing=16, controls=[selected_text, form_fields, actions, result_text]),
    )
    form_panel.width = 480

    filters = ft.ResponsiveRow(
        columns=12,
        spacing=12,
        run_spacing=12,
        controls=[
            ft.Container(col={"xs": 12, "md": 8}, content=search_field),
            ft.Container(col={"xs": 12, "md": 4}, content=course_filter),
        ],
    )

    import_export_actions = ft.ResponsiveRow(
        columns=12,
        spacing=8,
        run_spacing=8,
        controls=[
            ft.Container(
                col={"xs": 12, "sm": 6},
                content=SecondaryButton("Excel'den Ice Aktar", on_click=_handle_import_pick, icon=ft.Icons.UPLOAD_FILE, expand=True),
            ),
            ft.Container(
                col={"xs": 12, "sm": 6},
                content=SecondaryButton("Excel'e Disa Aktar", on_click=_handle_export_pick, icon=ft.Icons.DOWNLOAD, expand=True),
            ),
        ],
    )

    list_panel = ContentCard(
        title="Metin Listesi",
        subtitle="Arama ve kur filtresiyle metinleri bulun",
        content=ft.Column(spacing=12, expand=True, controls=[import_export_actions, filters, list_column]),
    )
    list_panel.expand = True

    try:
        _refresh_list()
    except Exception as exc:
        result_text.value = tr_error_message(exc)
        list_column.controls = [_empty_list("Metin listesi yuklenemedi.")]

    layout = ft.Column(
        spacing=16,
        expand=True,
        controls=[
            ft.Text("Metin Kutuphanesi", size=24, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
            TwoColumnLayout(left=form_panel, right=list_panel, left_flex=0, right_flex=1, spacing=24),
        ],
    )

    return PageContainer(content=layout, max_width=1888, padding=24)
