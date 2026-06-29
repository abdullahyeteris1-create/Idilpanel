"""Schedule repository skeleton for schedule table operations."""

from __future__ import annotations

from .base_repository import BaseRepository


class ScheduleRepository(BaseRepository):
    """Repository entry point for schedules table access."""

    table_name = "schedules"
    id_column = "id"

    def create(self, data):
        return self._insert_from_mapping(self.table_name, data)

    def get_by_id(self, record_id):
        return self._select_by_id(self.table_name, self.id_column, record_id)

    def list_all(self, limit: int = 100, offset: int = 0):
        return self._select_all(self.table_name, self.id_column, limit, offset)

    def update(self, record_id, data):
        return self._update_from_mapping(self.table_name, self.id_column, record_id, data)

    def delete(self, record_id):
        return self._delete_by_id(self.table_name, self.id_column, record_id)
