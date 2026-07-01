"""App table component aligned with theme tokens."""

from __future__ import annotations

import flet as ft

from theme.theme import THEME_TOKENS


def build_app_table(
    columns: list[str],
    rows: list[list[str | ft.Control]],
    heading_row_height: int = 44,
    data_row_min_height: int = 44,
    data_row_max_height: int = 52,
) -> ft.Container:
    """Build a simple themed table wrapper."""
    colors = THEME_TOKENS["colors"]
    typography = THEME_TOKENS["typography"]
    spacing = THEME_TOKENS["spacing"]
    radius = THEME_TOKENS["radius"]

    table_columns = [
        ft.DataColumn(
            label=ft.Text(
                value=column,
                size=typography["caption"]["max_size"],
                weight=ft.FontWeight.W_600,
                color=colors["text_secondary"],
            )
        )
        for column in columns
    ]

    table_rows: list[ft.DataRow] = []
    for row in rows:
        cells: list[ft.DataCell] = []
        for value in row:
            if isinstance(value, ft.Control):
                cells.append(ft.DataCell(value))
            else:
                cells.append(
                    ft.DataCell(
                        ft.Text(
                            value=value,
                            size=typography["body"]["max_size"],
                            color=colors["text_primary"],
                        )
                    )
                )
        table_rows.append(ft.DataRow(cells=cells))

    table = ft.DataTable(
        columns=table_columns,
        rows=table_rows,
        heading_row_height=heading_row_height,
        data_row_min_height=data_row_min_height,
        data_row_max_height=data_row_max_height,
        horizontal_lines=ft.BorderSide(1, colors["border"]),
        heading_row_color=f"{colors['primary']}0F",
        column_spacing=spacing["16"],
    )

    return ft.Container(
        bgcolor=colors["surface"],
        border_radius=radius["card"],
        padding=spacing["16"],
        border=ft.Border(
            top=ft.BorderSide(1, colors["border"]),
            right=ft.BorderSide(1, colors["border"]),
            bottom=ft.BorderSide(1, colors["border"]),
            left=ft.BorderSide(1, colors["border"]),
        ),
        content=table,
    )
