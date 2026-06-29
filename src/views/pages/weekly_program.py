"""Weekly program page skeleton."""

import flet as ft

from components.badge import build_badge
from components.button import build_button
from components.card import build_card, build_lesson_card
from components.text_field import build_text_field
from theme.theme import THEME_TOKENS


WEIGHT_MAP = {
    400: ft.FontWeight.W_400,
    600: ft.FontWeight.W_600,
    700: ft.FontWeight.W_700,
}


STATIC_LESSON_SLOTS = {
    (0, 0): {
        "student_name": "Ayse Demir",
        "class_name": "5-A",
        "level_no": "2",
        "progress_text": "6 / 16",
        "status_text": "Planlandi",
        "status_variant": "primary",
    },
    (1, 3): {
        "student_name": "Mehmet Kaya",
        "class_name": "6-B",
        "level_no": "1",
        "progress_text": "3 / 14",
        "status_text": "Devam Ediyor",
        "status_variant": "success",
    },
    (2, 5): {
        "student_name": "Zeynep Aras",
        "class_name": "7-C",
        "level_no": "3",
        "progress_text": "9 / 18",
        "status_text": "Riskli",
        "status_variant": "warning",
    },
    (4, 2): {
        "student_name": "Ali Can",
        "class_name": "8-A",
        "level_no": "4",
        "progress_text": "12 / 20",
        "status_text": "Gecikme",
        "status_variant": "danger",
    },
}


def _font_weight(token_weight: int) -> ft.FontWeight:
    return WEIGHT_MAP.get(token_weight, ft.FontWeight.W_400)


def _build_slot() -> ft.Container:
    colors = THEME_TOKENS["colors"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]
    typography = THEME_TOKENS["typography"]

    return ft.Container(
        bgcolor=colors["background"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border_neutral"]),
            right=ft.BorderSide(1, colors["border_neutral"]),
            bottom=ft.BorderSide(1, colors["border_neutral"]),
            left=ft.BorderSide(1, colors["border_neutral"]),
        ),
        border_radius=radius["input"],
        padding=spacing["sm"],
        content=ft.Row(
            controls=[
                ft.Text(
                    value="+",
                    size=typography["subtitle"]["min_size"],
                    weight=_font_weight(typography["subtitle"]["weight"]),
                    color=colors["text_secondary"],
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


def _build_lesson_slot(
    lesson_data: dict[str, str],
    slot_key: tuple[int, int],
    selected_slot_key: tuple[int, int],
    on_select,
) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    radius = THEME_TOKENS["radius"]

    return ft.Container(
        border=ft.Border(
            top=ft.BorderSide(
                2,
                colors["primary"] if slot_key == selected_slot_key else colors["background"],
            ),
            right=ft.BorderSide(
                2,
                colors["primary"] if slot_key == selected_slot_key else colors["background"],
            ),
            bottom=ft.BorderSide(
                2,
                colors["primary"] if slot_key == selected_slot_key else colors["background"],
            ),
            left=ft.BorderSide(
                2,
                colors["primary"] if slot_key == selected_slot_key else colors["background"],
            ),
        ),
        border_radius=radius["input"],
        on_click=lambda e, key=slot_key: on_select(key, e),
        content=build_lesson_card(
            student_name=lesson_data["student_name"],
            class_name=lesson_data["class_name"],
            level_no=lesson_data["level_no"],
            progress_text=lesson_data["progress_text"],
            status_text=lesson_data["status_text"],
            status_variant=lesson_data["status_variant"],
        ),
    )


def _build_day_column(
    day_name: str,
    day_index: int,
    selected_slot_key: tuple[int, int],
    on_select,
    lesson_slot_refs: dict[tuple[int, int], ft.Container],
) -> ft.Container:
    spacing = THEME_TOKENS["spacing"]

    slot_controls: list[ft.Control] = []
    for slot_index in range(9):
        slot_key = (day_index, slot_index)
        lesson_data = STATIC_LESSON_SLOTS.get(slot_key)
        if lesson_data:
            lesson_slot = _build_lesson_slot(
                lesson_data=lesson_data,
                slot_key=slot_key,
                selected_slot_key=selected_slot_key,
                on_select=on_select,
            )
            lesson_slot_refs[slot_key] = lesson_slot
            slot_controls.append(lesson_slot)
        else:
            slot_controls.append(_build_slot())

    return ft.Container(
        expand=True,
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
    selected_slot_key: tuple[int, int],
    on_select,
    lesson_slot_refs: dict[tuple[int, int], ft.Container],
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
        subtitle="7 gun, 9 slot ve secili statik ders kartlari",
        content=ft.Row(
            controls=[
                _build_day_column(
                    day_name=day_name,
                    day_index=day_index,
                    selected_slot_key=selected_slot_key,
                    on_select=on_select,
                    lesson_slot_refs=lesson_slot_refs,
                )
                for day_index, day_name in enumerate(day_names)
            ],
            spacing=spacing["sm"],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )


def _build_summary_card(title: str, value: str) -> ft.Container:
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]

    return ft.Container(
        expand=True,
        content=build_card(
            title=title,
            content=ft.Text(
                value=value,
                size=typography["card_title"]["max_size"],
                weight=_font_weight(typography["card_title"]["weight"]),
                color=colors["text_primary"],
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
        border=ft.Border(
            top=ft.BorderSide(1, colors["border_neutral"]),
            right=ft.BorderSide(1, colors["border_neutral"]),
            bottom=ft.BorderSide(1, colors["border_neutral"]),
            left=ft.BorderSide(1, colors["border_neutral"]),
        ),
        border_radius=radius["input"],
        padding=spacing["sm"],
        content=ft.Column(
            controls=[
                ft.Text(
                    value=title,
                    size=typography["body"]["max_size"],
                    weight=ft.FontWeight.W_600,
                    color=colors["text_primary"],
                ),
                ft.Column(controls=content, spacing=spacing["sm"]),
            ],
            spacing=spacing["sm"],
        ),
    )


def build_weekly_program_page() -> ft.Control:
    """Build static weekly-program skeleton content without business logic."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    selected_slot_state = {"value": next(iter(STATIC_LESSON_SLOTS.keys()))}
    lesson_slot_refs: dict[tuple[int, int], ft.Container] = {}

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
            status_badge_container,
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
        subtitle="Secilen ders kartinin statik bilgileri",
        content=ft.Column(
            controls=[
                student_group,
                academic_group,
                notes_group,
            ],
            spacing=spacing["sm"],
        ),
    )

    def _apply_selected_lesson(slot_key: tuple[int, int]) -> None:
        lesson_data = STATIC_LESSON_SLOTS[slot_key]
        student_value.value = lesson_data["student_name"]
        class_value.value = lesson_data["class_name"]
        level_value.value = lesson_data["level_no"]
        progress_value.value = lesson_data["progress_text"]
        status_badge_container.content = build_badge(
            text=lesson_data["status_text"],
            variant=lesson_data["status_variant"],
        )

        for item_key, lesson_container in lesson_slot_refs.items():
            lesson_container.border = ft.Border(
                top=ft.BorderSide(2, colors["primary"] if item_key == slot_key else colors["background"]),
                right=ft.BorderSide(2, colors["primary"] if item_key == slot_key else colors["background"]),
                bottom=ft.BorderSide(2, colors["primary"] if item_key == slot_key else colors["background"]),
                left=ft.BorderSide(2, colors["primary"] if item_key == slot_key else colors["background"]),
            )

    def _on_lesson_select(slot_key: tuple[int, int], e: ft.ControlEvent) -> None:
        selected_slot_state["value"] = slot_key
        _apply_selected_lesson(slot_key)
        e.page.update()

    schedule_grid = _build_schedule_grid(
        selected_slot_key=selected_slot_state["value"],
        on_select=_on_lesson_select,
        lesson_slot_refs=lesson_slot_refs,
    )
    _apply_selected_lesson(selected_slot_state["value"])

    top_section = ft.Row(
        controls=[
            ft.Container(expand=4, content=schedule_grid),
            ft.Container(expand=2, content=detail_panel),
        ],
        spacing=spacing["md"],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    summary_section = ft.Row(
        controls=[
            _build_summary_card("Toplam Ders", "0"),
            _build_summary_card("Bos Saat", "0"),
            _build_summary_card("Haftalik Sure", "0 dk"),
        ],
        spacing=spacing["md"],
    )

    return ft.Column(
        controls=[top_section, summary_section],
        spacing=spacing["md"],
        expand=True,
    )
