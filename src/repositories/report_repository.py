"""Report repository skeleton for report table operations."""

from __future__ import annotations

from typing import Any, Mapping

from .base_repository import BaseRepository


class ReportRepository(BaseRepository):
    """Repository entry point for reports table access."""

    table_name = "reports"
    id_column = "id"

    def create(self, data: Mapping[str, Any]) -> int:
        if not data:
            raise ValueError("data must not be empty")

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        return self.execute_insert(query, tuple(data.values()))

    def get_by_id(self, record_id: int) -> dict[str, Any] | None:
        query = f"SELECT * FROM {self.table_name} WHERE {self.id_column} = ? LIMIT 1"
        return self.execute_fetchone(query, (record_id,))

    def list_all(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} ORDER BY {self.id_column} ASC LIMIT ? OFFSET ?"
        return self.execute_fetchall(query, (limit, offset))

    def update(self, record_id: int, data: Mapping[str, Any]) -> bool:
        if not data:
            return False

        set_clause = ", ".join([f"{column} = ?" for column in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.id_column} = ?"
        params = tuple(data.values()) + (record_id,)
        return self.execute_write(query, params) > 0

    def delete(self, record_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE {self.id_column} = ?"
        return self.execute_write(query, (record_id,)) > 0
