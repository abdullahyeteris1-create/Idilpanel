"""Weekly program page migrated to shared design system components."""

from __future__ import annotations

import flet as ft

from components import AppCard, ContentCard, PageContainer, PrimaryButton, SecondaryButton, ThreeColumnLayout, TwoColumnLayout
from controllers.student_controller import StudentController
from repositories.student_repository import StudentRepository
from services.student_service import StudentService
from theme.theme import THEME_TOKENS


DAY_COUNT = 7
SLOTS_PER_DAY = 9
TOTAL_SLOTS = DAY_COUNT * SLOTS_PER_DAY


def _status_variant_for_index(index: int) -> str:
    variants = ["Aktif", "Tamamlandi", "Pasif", "Aktif"]
    return variants[index % len(variants)]


def _build_slots_from_students(student_rows: list[dict]) -> dict[tuple[int, int], dict[str, str]]:
    slots: dict[tuple[int, int], dict[str, str]] = {}
    for index, student in enumerate(student_rows[:TOTAL_SLOTS]):
        day_index = index // SLOTS_PER_DAY
        slot_index = index % SLOTS_PER_DAY

        full_name = str(student.get("ad_soyad") or "-").strip() or "-"
        class_name = str(student.get("sinif") or "-").strip() or "-"
        start_date = str(student.get("baslangic_tarihi") or "-").strip() or "-"

        slots[(day_index, slot_index)] = {
            "student_name": full_name,
            "class_name": class_name,
            "level_no": str((slot_index % 4) + 1),
            "progress_text": start_date,
            "status_text": _status_variant_for_index(index),
        }
    return slots


def _load_weekly_student_slots() -> dict[tuple[int, int], dict[str, str]]:
    controller = StudentController(StudentService(student_repository=StudentRepository()))
    try:
        students = controller.list_students(limit=TOTAL_SLOTS, offset=0)
    except Exception:
        return {}
    return _build_slots_from_students(students)


def _status_chip(status: str) -> ft.Control:
    if status == "Aktif":
        bg, fg = "#DCFCE7", "#166534"
    elif status == "Pasif":
        bg, fg = "#FEF3C7", "#92400E"
    else:
        bg, fg = "#DBEAFE", "#1E3A8A"
    return ft.Container(
        padding=ft.Padding(10, 4, 10, 4),
        border_radius=999,
        bgcolor=bg,
        content=ft.Text(status, size=12, color=fg, weight=ft.FontWeight.W_600),
    )


def _summary_card(title: str, value: str) -> ft.Control:
    colors = THEME_TOKENS["colors"]
    return AppCard(
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, size=13, color=colors["text_secondary"]),
                ft.Text(value, size=28, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
            ],
        )
    )


def build_weekly_program_page() -> ft.Control:
    """Build weekly program page with design-system-aligned UI."""
    colors = THEME_TOKENS["colors"]

    lesson_slots = _load_weekly_student_slots()
    selected_slot = {"value": next(iter(lesson_slots.keys()), (0, 0))}

    student_value = ft.Text("-", size=15, weight=ft.FontWeight.W_600, color=colors["text_primary"])
    class_value = ft.Text("-", size=15, weight=ft.FontWeight.W_600, color=colors["text_primary"])
    level_value = ft.Text("-", size=15, weight=ft.FontWeight.W_600, color=colors["text_primary"])
    progress_value = ft.Text("-", size=15, weight=ft.FontWeight.W_600, color=colors["text_primary"])
    status_holder = ft.Container(content=_status_chip("-"))

    day_names = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]

    schedule_columns = ft.Row(spacing=12, scroll=ft.ScrollMode.AUTO)

    def _apply_details(slot_key: tuple[int, int]) -> None:
        lesson_data = lesson_slots.get(slot_key)
        if lesson_data is None:
            student_value.value = "-"
            class_value.value = "-"
            level_value.value = "-"
            progress_value.value = "-"
            status_holder.content = _status_chip("-")
            return

        student_value.value = lesson_data["student_name"]
        class_value.value = lesson_data["class_name"]
        level_value.value = lesson_data["level_no"]
        progress_value.value = lesson_data["progress_text"]
        status_holder.content = _status_chip(lesson_data["status_text"])

    def _build_slot_card(slot_key: tuple[int, int]) -> ft.Control:
        lesson_data = lesson_slots.get(slot_key)
        is_selected = slot_key == selected_slot["value"]

        border_color = colors["primary"] if is_selected else colors["border"]
        background = "#EEF2FF" if is_selected else colors["surface"]

        if lesson_data is None:
            card = AppCard(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.Text("+", size=18, color=colors["text_secondary"])],
                )
            )
            card.height = 72
            card.padding = ft.Padding(10, 8, 10, 8)
            card.bgcolor = background
            card.border = ft.Border(
                top=ft.BorderSide(1, border_color),
                right=ft.BorderSide(1, border_color),
                bottom=ft.BorderSide(1, border_color),
                left=ft.BorderSide(1, border_color),
            )

            def _select_empty(ev: ft.ControlEvent) -> None:
                selected_slot["value"] = slot_key
                _render_schedule()
                _apply_details(slot_key)
                ev.page.update()

            card.on_click = _select_empty
            return card

        initials = "".join(part[0] for part in lesson_data["student_name"].split()[:2]).upper()
        row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=32,
                            height=32,
                            border_radius=16,
                            bgcolor=f"{colors['primary']}1F",
                            alignment=ft.Alignment(0, 0),
                            content=ft.Text(initials or "--", size=11, weight=ft.FontWeight.W_700, color=colors["primary"]),
                        ),
                        ft.Column(
                            spacing=1,
                            controls=[
                                ft.Text(lesson_data["student_name"], size=13, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                                ft.Text(f"{lesson_data['class_name']} • {lesson_data['level_no']}. Kur", size=11, color=colors["text_secondary"]),
                            ],
                        ),
                    ],
                ),
                _status_chip(lesson_data["status_text"]),
            ],
        )

        card = AppCard(content=row)
        card.height = 72
        card.padding = ft.Padding(10, 8, 10, 8)
        card.bgcolor = background
        card.border = ft.Border(
            top=ft.BorderSide(1, border_color),
            right=ft.BorderSide(1, border_color),
            bottom=ft.BorderSide(1, border_color),
            left=ft.BorderSide(1, border_color),
        )

        def _select_lesson(ev: ft.ControlEvent) -> None:
            selected_slot["value"] = slot_key
            _render_schedule()
            _apply_details(slot_key)
            ev.page.update()

        card.on_click = _select_lesson
        return card

    def _render_schedule() -> None:
        schedule_columns.controls = []
        for day_index, day_name in enumerate(day_names):
            slot_controls: list[ft.Control] = []
            for slot_index in range(SLOTS_PER_DAY):
                slot_key = (day_index, slot_index)
                slot_controls.append(_build_slot_card(slot_key))

            day_card = ContentCard(
                title=day_name,
                subtitle=f"{SLOTS_PER_DAY} slot",
                content=ft.Column(spacing=8, controls=slot_controls),
            )
            day_card.width = 260
            schedule_columns.controls.append(day_card)

    detail_panel = ContentCard(
        title="Detay Paneli",
        subtitle="Secilen kartin salt okunur ogrenci bilgileri",
        content=ft.Column(
            spacing=16,
            controls=[
                AppCard(content=ft.Column(spacing=6, controls=[ft.Text("Ogrenci Adi", size=12, color=colors["text_secondary"]), student_value])),
                AppCard(content=ft.Column(spacing=6, controls=[ft.Text("Sinif", size=12, color=colors["text_secondary"]), class_value])),
                AppCard(content=ft.Column(spacing=6, controls=[ft.Text("Kur", size=12, color=colors["text_secondary"]), level_value])),
                AppCard(content=ft.Column(spacing=6, controls=[ft.Text("Ilerleme", size=12, color=colors["text_secondary"]), progress_value])),
                AppCard(content=ft.Column(spacing=6, controls=[ft.Text("Durum", size=12, color=colors["text_secondary"]), status_holder])),
                SecondaryButton("Kaydet", disabled=True),
            ],
        ),
    )
    detail_panel.width = 360

    schedule_panel = ContentCard(
        title="Haftalik Program",
        subtitle=f"7 gun, 9 slot, salt okunur ogrenci kartlari ({len(lesson_slots)} kayit)",
        action=PrimaryButton("Dersi Ac", on_click=lambda e: e.page.go("/lesson-records"), icon=ft.Icons.OPEN_IN_NEW),
        content=schedule_columns,
    )

    summary = ThreeColumnLayout(
        first=_summary_card("Toplam Kart", str(len(lesson_slots))),
        second=_summary_card("Bos Slot", str(TOTAL_SLOTS - len(lesson_slots))),
        third=_summary_card("Kaynak", "SQLite / Student"),
        spacing=24,
    )

    body = ft.Column(
        spacing=24,
        expand=True,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    ft.Text("Haftalik Program", size=24, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
                    ft.Text("Haftalik slotlar ve ogrenci yerlesimi", size=15, color=colors["text_secondary"]),
                ],
            ),
            TwoColumnLayout(left=schedule_panel, right=detail_panel, left_flex=2, right_flex=1, spacing=24),
            summary,
        ],
    )

    _render_schedule()
    _apply_details(selected_slot["value"])
    return PageContainer(content=body, max_width=1888, padding=24)
