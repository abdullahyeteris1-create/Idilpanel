"""Schedule controller skeleton for UI-to-service request orchestration."""

from __future__ import annotations

from services.schedule_service import ScheduleService


class ScheduleController:
    """Bridge UI requests to ScheduleService without business logic."""

    def __init__(self, schedule_service: ScheduleService) -> None:
        self._schedule_service = schedule_service

    def create_schedule(self, data):
        return self._schedule_service.create_schedule(data)

    def get_schedule(self, record_id):
        return self._schedule_service.get_schedule(record_id)

    def list_schedules(self, limit: int = 100, offset: int = 0):
        return self._schedule_service.list_schedules(limit, offset)

    def update_schedule(self, record_id, data):
        return self._schedule_service.update_schedule(record_id, data)

    def delete_schedule(self, record_id):
        return self._schedule_service.delete_schedule(record_id)
