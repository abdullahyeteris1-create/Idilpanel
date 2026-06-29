"""Weekly program page skeleton."""

import flet as ft

from components.badge import build_badge
from components.button import build_button
from components.card import build_card, build_lesson_card
from components.text_field import build_text_field
from controllers.student_controller import StudentController
from repositories.student_repository import StudentRepository
from services.student_service import StudentService
from theme.theme import THEME_TOKENS


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


DAY_COUNT = 7
SLOTS_PER_DAY = 9
TOTAL_SLOTS = DAY_COUNT * SLOTS_PER_DAY


def _status_variant_for_index(index: int) -> str:
    variants = ["primary", "success", "warning", "secondary"]
    return variants[index % len(variants)]


def _build_slots_from_students(student_rows: list[dict]) -> dict[tuple[int, int], dict[str, str]]:
    slots: dict[tuple[int, int], dict[str, str]] = {}
    for index, student in enumerate(student_rows[:TOTAL_SLOTS]):
        day_index = index // SLOTS_PER_DAY
        slot_index = index % SLOTS_PER_DAY

        full_name = str(student.get("ad_soyad") or "-").strip() or "-"
        class_name = str(student.get("sinif") or "-").strip() or "-"
        status_text = str(student.get("durum") or "Aktif").strip() or "Aktif"
        start_date = str(student.get("baslangic_tarihi") or "-").strip() or "-"

        slots[(day_index, slot_index)] = {
            "student_name": full_name,
            "class_name": class_name,
            "level_no": "-",
            "progress_text": start_date,
            "status_text": status_text,
            "status_variant": _status_variant_for_index(index),
        }
    return slots


def _load_weekly_student_slots() -> dict[tuple[int, int], dict[str, str]]:
    controller = StudentController(StudentService(student_repository=StudentRepository()))
    try:
        students = controller.list_students(limit=TOTAL_SLOTS, offset=0)
    except Exception:
        return {}
    return _build_slots_from_students(students)


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def _with_alpha(color: str, alpha: str = "1A") -> str:
    if len(color) == 7:
        return f"{color}{alpha}"
    return color


def _build_slot(
    slot_key: tuple[int, int],
    selected_slot_key: tuple[int, int],
    focused_slot_key: tuple[int, int] | None,
    hovered_empty_slot_key: tuple[int, int] | None,
    on_hover,
    on_focus,
    empty_slot_refs: dict[tuple[int, int], ft.Container],
) -> ft.GestureDetector:
    colors = THEME_TOKENS["colors"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]
    typography = THEME_TOKENS["typography"]

    is_selected = slot_key == selected_slot_key
    is_focused = slot_key == focused_slot_key
    is_hovered = slot_key == hovered_empty_slot_key

    border_color = colors["border_neutral"]
    if is_hovered:
        border_color = colors["secondary"]
    if is_focused:
        border_color = colors["secondary"]
    if is_selected:
        border_color = colors["primary"]

    slot_container = ft.Container(
        bgcolor=_with_alpha(colors["surface"], "CC") if is_hovered else colors["background"],
        border=ft.Border(
            top=ft.BorderSide(2 if is_focused or is_selected else 1, border_color),
            right=ft.BorderSide(2 if is_focused or is_selected else 1, border_color),
            bottom=ft.BorderSide(2 if is_focused or is_selected else 1, border_color),
            left=ft.BorderSide(2 if is_focused or is_selected else 1, border_color),
        ),
        border_radius=radius["input"],
        padding=spacing["sm"],
        animate=120,
        content=ft.Row(
            controls=[
                ft.Text(
                    value="+",
                    size=typography["subtitle"]["min_size"],
                    weight=_font_weight(typography["subtitle"]["weight"]),
                    color=colors["secondary"] if is_hovered else colors["text_secondary"],
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    empty_slot_refs[slot_key] = slot_container

    return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.CLICK,
        on_hover=lambda e, key=slot_key: on_hover(key, e),
        on_tap_down=lambda e, key=slot_key: on_focus(key, e),
        content=slot_container,
    )


def _build_lesson_slot(
    lesson_data: dict[str, str],
    slot_key: tuple[int, int],
    selected_slot_key: tuple[int, int],
    focused_slot_key: tuple[int, int] | None,
    hovered_lesson_slot_key: tuple[int, int] | None,
    on_select,
    on_hover,
    on_focus,
    lesson_slot_refs: dict[tuple[int, int], ft.Container],
) -> ft.GestureDetector:
    colors = THEME_TOKENS["colors"]
    radius = THEME_TOKENS["radius"]
    shadows = THEME_TOKENS["shadows"]

    is_selected = slot_key == selected_slot_key
    is_focused = slot_key == focused_slot_key
    is_hovered = slot_key == hovered_lesson_slot_key

    border_color = colors["background"]
    border_width = 2
    background = colors["surface"]
    shadow = None

    if is_hovered:
        border_color = _with_alpha(colors["primary"], "80")
        background = _with_alpha(colors["primary"], "08")

    if is_focused:
        border_color = colors["secondary"]

    if is_selected:
        border_color = colors["primary"]
        background = _with_alpha(colors["primary"], "12")
        shadow = shadows["card"]

    lesson_container = ft.Container(
        bgcolor=background,
        shadow=shadow,
        animate=120,
        animate_scale=120,
        scale=1.0,
        border=ft.Border(
            top=ft.BorderSide(border_width, border_color),
            right=ft.BorderSide(border_width, border_color),
            bottom=ft.BorderSide(border_width, border_color),
            left=ft.BorderSide(border_width, border_color),
        ),
        border_radius=radius["input"],
        content=build_lesson_card(
            student_name=lesson_data["student_name"],
            class_name=lesson_data["class_name"],
            level_no=lesson_data["level_no"],
            progress_text=lesson_data["progress_text"],
            status_text=lesson_data["status_text"],
            status_variant=lesson_data["status_variant"],
        ),
    )

    lesson_slot_refs[slot_key] = lesson_container

    return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.CLICK,
        on_hover=lambda e, key=slot_key: on_hover(key, e),
        on_tap_down=lambda e, key=slot_key: on_focus(key, e),
        on_tap=lambda e, key=slot_key: on_select(key, e),
        content=lesson_container,
    )


def _build_day_column(
    day_name: str,
    day_index: int,
    lesson_slots: dict[tuple[int, int], dict[str, str]],
    selected_slot_key: tuple[int, int],
    focused_slot_key: tuple[int, int] | None,
    hovered_lesson_slot_key: tuple[int, int] | None,
    hovered_empty_slot_key: tuple[int, int] | None,
    on_select,
    on_lesson_hover,
    on_empty_hover,
    on_focus,
    lesson_slot_refs: dict[tuple[int, int], ft.Container],
    empty_slot_refs: dict[tuple[int, int], ft.Container],
) -> ft.Container:
    spacing = THEME_TOKENS["spacing"]

    slot_controls: list[ft.Control] = []
    for slot_index in range(SLOTS_PER_DAY):
        slot_key = (day_index, slot_index)
        lesson_data = lesson_slots.get(slot_key)
        if lesson_data:
            lesson_slot = _build_lesson_slot(
                lesson_data=lesson_data,
                slot_key=slot_key,
                selected_slot_key=selected_slot_key,
                focused_slot_key=focused_slot_key,
                hovered_lesson_slot_key=hovered_lesson_slot_key,
                on_select=on_select,
                on_hover=on_lesson_hover,
                on_focus=on_focus,
                lesson_slot_refs=lesson_slot_refs,
            )
            slot_controls.append(lesson_slot)
        else:
            slot_controls.append(
                _build_slot(
                    slot_key=slot_key,
                    selected_slot_key=selected_slot_key,
                    focused_slot_key=focused_slot_key,
                    hovered_empty_slot_key=hovered_empty_slot_key,
                    on_hover=on_empty_hover,
                    on_focus=on_focus,
                    empty_slot_refs=empty_slot_refs,
                )
            )

    return ft.Container(
        width=spacing["xxxl"] * 3 + spacing["xl"],
        content=build_card(
            title=day_name,
            content=ft.Column(
                controls=slot_controls,
                spacing=spacing["xs"],
            ),
            padding_size="sm",
        ),
    )


def _build_schedule_grid(
    lesson_slots: dict[tuple[int, int], dict[str, str]],
    selected_slot_key: tuple[int, int],
    focused_slot_key: tuple[int, int] | None,
    hovered_lesson_slot_key: tuple[int, int] | None,
    hovered_empty_slot_key: tuple[int, int] | None,
    on_select,
    on_lesson_hover,
    on_empty_hover,
    on_focus,
    lesson_slot_refs: dict[tuple[int, int], ft.Container],
    empty_slot_refs: dict[tuple[int, int], ft.Container],
) -> ft.Control:
    spacing = THEME_TOKENS["spacing"]

    day_names = [
        "Pazartesi",
        "Sali",
        "Carsamba",
        "Persembe",
        "Cuma",
        "Cumartesi",
        "Pazar",
    ]

    return build_card(
        title="Haftalik Program",
        subtitle=f"7 gun, 9 slot, salt okunur ogrenci kartlari ({len(lesson_slots)} kayit)",
        content=ft.Row(
            controls=[
                _build_day_column(
                    day_name=day_name,
                    day_index=day_index,
                    lesson_slots=lesson_slots,
                    selected_slot_key=selected_slot_key,
                    focused_slot_key=focused_slot_key,
                    hovered_lesson_slot_key=hovered_lesson_slot_key,
                    hovered_empty_slot_key=hovered_empty_slot_key,
                    on_select=on_select,
                    on_lesson_hover=on_lesson_hover,
                    on_empty_hover=on_empty_hover,
                    on_focus=on_focus,
                    lesson_slot_refs=lesson_slot_refs,
                    empty_slot_refs=empty_slot_refs,
                )
                for day_index, day_name in enumerate(day_names)
            ],
            spacing=spacing["sm"],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False,
            scroll=ft.ScrollMode.AUTO,
        ),
    )


def _build_summary_card(title: str, value: str) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]

    return ft.Container(
        expand=True,
        content=build_card(
            title=title,
            content=ft.Column(
                controls=[
                    ft.Text(
                        value=value,
                        size=typography["page_title"]["min_size"],
                        weight=ft.FontWeight.W_700,
                        color=colors["text_primary"],
                    ),
                ],
                spacing=spacing["xs"],
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
        ),
    )


def _build_detail_group(
    title: str,
    content: list[ft.Control],
) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]
    typography = THEME_TOKENS["typography"]

    return ft.Container(
        bgcolor=_with_alpha(colors["surface"], "E6"),
        border=ft.Border(
            top=ft.BorderSide(1, colors["border_neutral"]),
            right=ft.BorderSide(1, colors["border_neutral"]),
            bottom=ft.BorderSide(1, colors["border_neutral"]),
            left=ft.BorderSide(1, colors["border_neutral"]),
        ),
        border_radius=radius["input"],
        padding=spacing["md"],
        content=ft.Column(
            controls=[
                ft.Text(
                    value=title,
                    size=typography["subtitle"]["min_size"],
                    weight=ft.FontWeight.W_600,
                    color=colors["text_primary"],
                ),
                ft.Column(controls=content, spacing=spacing["xs"]),
            ],
            spacing=spacing["sm"],
        ),
    )


def build_weekly_program_page() -> ft.Control:
    """Build static weekly-program skeleton content without business logic."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    lesson_slots = _load_weekly_student_slots()
    selected_slot_state = {"value": next(iter(lesson_slots.keys()), (0, 0))}
    focused_slot_state = {"value": selected_slot_state["value"]}
    hovered_lesson_slot_state = {"value": None}
    hovered_empty_slot_state = {"value": None}
    lesson_slot_refs: dict[tuple[int, int], ft.Container] = {}
    empty_slot_refs: dict[tuple[int, int], ft.Container] = {}

    student_value = ft.Text(
        value="-",
        size=typography["body"]["max_size"],
        weight=ft.FontWeight.W_600,
        color=colors["text_primary"],
    )
    class_value = ft.Text(
        value="-",
        size=typography["body"]["max_size"],
        weight=ft.FontWeight.W_600,
        color=colors["text_primary"],
    )
    level_value = ft.Text(
        value="-",
        size=typography["body"]["max_size"],
        weight=ft.FontWeight.W_600,
        color=colors["text_primary"],
    )
    progress_value = ft.Text(
        value="-",
        size=typography["body"]["max_size"],
        weight=ft.FontWeight.W_600,
        color=colors["text_primary"],
    )
    status_badge_container = ft.Container(content=build_badge(text="-", variant="secondary"))

    note_field = build_text_field(
        label="Not",
        hint_text="Not alani salt okunur placeholder.",
        multiline=True,
        min_lines=3,
        max_lines=3,
    )
    note_field.read_only = True

    student_group = _build_detail_group(
        title="Ogrenci Bilgileri",
        content=[
            ft.Text("Ogrenci Adi", size=typography["small"]["max_size"], color=colors["text_secondary"]),
            student_value,
        ],
    )

    academic_group = _build_detail_group(
        title="Akademik Durum",
        content=[
            ft.Text("Sinif", size=typography["small"]["max_size"], color=colors["text_secondary"]),
            class_value,
            ft.Text("Kur No", size=typography["small"]["max_size"], color=colors["text_secondary"]),
            level_value,
            ft.Text("Ilerleme", size=typography["small"]["max_size"], color=colors["text_secondary"]),
            progress_value,
            ft.Text("Durum", size=typography["small"]["max_size"], color=colors["text_secondary"]),
            ft.Container(alignment=ft.Alignment(-1, 0), content=status_badge_container),
        ],
    )

    notes_group = _build_detail_group(
        title="Notlar",
        content=[
            note_field,
            build_button(label="Kaydet", disabled=True, expand=True),
        ],
    )

    detail_panel = build_card(
        title="Detay Paneli",
        subtitle="Secilen kartin salt okunur ogrenci bilgileri",
        content=ft.Column(
            controls=[
                student_group,
                academic_group,
                notes_group,
            ],
            spacing=spacing["md"],
        ),
    )

    def _apply_selected_lesson(slot_key: tuple[int, int]) -> None:
        lesson_data = lesson_slots.get(slot_key)
        if lesson_data is None:
            student_value.value = "-"
            class_value.value = "-"
            level_value.value = "-"
            progress_value.value = "-"
            status_badge_container.content = build_badge(text="-", variant="secondary")
            return

        student_value.value = lesson_data["student_name"]
        class_value.value = lesson_data["class_name"]
        level_value.value = lesson_data["level_no"]
        progress_value.value = lesson_data["progress_text"]
        status_badge_container.content = build_badge(
            text=lesson_data["status_text"],
            variant=lesson_data["status_variant"],
        )

    def _apply_interaction_styles() -> None:
        for item_key, lesson_container in lesson_slot_refs.items():
            is_selected = item_key == selected_slot_state["value"]
            is_focused = item_key == focused_slot_state["value"]
            is_hovered = item_key == hovered_lesson_slot_state["value"]

            border_color = colors["background"]
            bg_color = colors["surface"]
            shadow = None

            if is_hovered:
                border_color = _with_alpha(colors["primary"], "80")
                bg_color = _with_alpha(colors["primary"], "08")
                shadow = THEME_TOKENS["shadows"]["card"]

            if is_focused:
                border_color = colors["secondary"]

            if is_selected:
                border_color = colors["primary"]
                bg_color = _with_alpha(colors["primary"], "12")
                shadow = THEME_TOKENS["shadows"]["card"]

            lesson_container.bgcolor = bg_color
            lesson_container.shadow = shadow
            lesson_container.scale = 1.01 if is_hovered or is_selected else 1.0
            lesson_container.border = ft.Border(
                top=ft.BorderSide(2, border_color),
                right=ft.BorderSide(2, border_color),
                bottom=ft.BorderSide(2, border_color),
                left=ft.BorderSide(2, border_color),
            )

        for item_key, empty_container in empty_slot_refs.items():
            is_selected = item_key == selected_slot_state["value"]
            is_focused = item_key == focused_slot_state["value"]
            is_hovered = item_key == hovered_empty_slot_state["value"]

            border_color = colors["border_neutral"]
            border_width = 1

            if is_hovered:
                border_color = colors["secondary"]

            if is_focused:
                border_color = colors["secondary"]
                border_width = 2

            if is_selected:
                border_color = colors["primary"]
                border_width = 2

            empty_container.bgcolor = _with_alpha(colors["surface"], "CC") if is_hovered else colors["background"]
            empty_container.border = ft.Border(
                top=ft.BorderSide(border_width, border_color),
                right=ft.BorderSide(border_width, border_color),
                bottom=ft.BorderSide(border_width, border_color),
                left=ft.BorderSide(border_width, border_color),
            )

            if isinstance(empty_container.content, ft.Row) and empty_container.content.controls:
                plus_control = empty_container.content.controls[0]
                if isinstance(plus_control, ft.Text):
                    plus_control.color = colors["secondary"] if is_hovered else colors["text_secondary"]

    def _on_lesson_select(slot_key: tuple[int, int], e: ft.ControlEvent) -> None:
        selected_slot_state["value"] = slot_key
        focused_slot_state["value"] = slot_key
        _apply_selected_lesson(slot_key)
        _apply_interaction_styles()
        e.page.update()

    def _on_lesson_hover(slot_key: tuple[int, int], e) -> None:
        hovered_lesson_slot_state["value"] = slot_key if str(e.data).lower() == "true" else None
        _apply_interaction_styles()
        e.page.update()

    def _on_empty_hover(slot_key: tuple[int, int], e) -> None:
        hovered_empty_slot_state["value"] = slot_key if str(e.data).lower() == "true" else None
        _apply_interaction_styles()
        e.page.update()

    def _on_slot_focus(slot_key: tuple[int, int], e) -> None:
        focused_slot_state["value"] = slot_key
        _apply_interaction_styles()
        e.page.update()

    schedule_grid = _build_schedule_grid(
        lesson_slots=lesson_slots,
        selected_slot_key=selected_slot_state["value"],
        focused_slot_key=focused_slot_state["value"],
        hovered_lesson_slot_key=hovered_lesson_slot_state["value"],
        hovered_empty_slot_key=hovered_empty_slot_state["value"],
        on_select=_on_lesson_select,
        on_lesson_hover=_on_lesson_hover,
        on_empty_hover=_on_empty_hover,
        on_focus=_on_slot_focus,
        lesson_slot_refs=lesson_slot_refs,
        empty_slot_refs=empty_slot_refs,
    )
    _apply_selected_lesson(selected_slot_state["value"])
    _apply_interaction_styles()

    top_section = ft.ResponsiveRow(
        columns=12,
        controls=[
            ft.Container(
                col={"xs": 12, "sm": 12, "md": 12, "lg": 9, "xl": 9, "xxl": 9},
                content=schedule_grid,
            ),
            ft.Container(
                col={"xs": 12, "sm": 12, "md": 12, "lg": 3, "xl": 3, "xxl": 3},
                content=detail_panel,
            ),
        ],
        spacing=spacing["md"],
        run_spacing=spacing["md"],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    summary_section = ft.ResponsiveRow(
        columns=12,
        controls=[
            ft.Container(
                col={"xs": 12, "sm": 12, "md": 6, "lg": 4, "xl": 4},
                content=_build_summary_card("Toplam Kart", str(len(lesson_slots))),
            ),
            ft.Container(
                col={"xs": 12, "sm": 12, "md": 6, "lg": 4, "xl": 4},
                content=_build_summary_card("Bos Slot", str(TOTAL_SLOTS - len(lesson_slots))),
            ),
            ft.Container(
                col={"xs": 12, "sm": 12, "md": 12, "lg": 4, "xl": 4},
                content=_build_summary_card("Kaynak", "SQLite / Student"),
            ),
        ],
        spacing=spacing["md"],
        run_spacing=spacing["md"],
    )

    return ft.Column(
        controls=[top_section, summary_section],
        spacing=spacing["md"],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
