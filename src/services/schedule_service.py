"""Schedule service skeleton for schedule domain operations."""

from __future__ import annotations

from typing import Any

from repositories.schedule_repository import ScheduleRepository

from .base_service import BaseService


class ScheduleService(BaseService):
    """Service entry point for schedule-related operations."""

    def __init__(
        self,
        schedule_repository: ScheduleRepository | None = None,
        repositories: dict[str, Any] | None = None,
    ) -> None:
        merged_repositories = dict(repositories or {})
        if schedule_repository is not None:
            merged_repositories["schedule"] = schedule_repository
        super().__init__(merged_repositories)

    # CRUD Operations
    def create_schedule(self, data):
        return self.get_repository("schedule").create(data)

    def get_schedule(self, record_id):
        return self.get_repository("schedule").get_by_id(record_id)

    def list_schedules(self, limit: int = 100, offset: int = 0):
        return self.get_repository("schedule").list_all(limit, offset)

    def update_schedule(self, record_id, data):
        return self.get_repository("schedule").update(record_id, data)

    def delete_schedule(self, record_id):
        return self.get_repository("schedule").delete(record_id)

    # Validation
    def validate_schedule(self, data: Any | None = None):
        self.get_repository("schedule")
        return data
