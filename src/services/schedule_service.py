"""Schedule service skeleton for schedule domain operations."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, time
from typing import Any

from repositories.schedule_repository import ScheduleRepository

from .base_service import BaseService


class ScheduleService(BaseService):
    """Service entry point for schedule-related operations."""

    _STUDENT_FIELDS = ("student_id",)
    _COURSE_FIELDS = ("course_id",)
    _DAY_FIELDS = ("day", "gun", "weekday")
    _START_TIME_FIELDS = ("start_time", "baslangic_saati")
    _END_TIME_FIELDS = ("end_time", "bitis_saati")

    _VALID_WEEK_DAYS = {
        "pazartesi",
        "sali",
        "salı",
        "carsamba",
        "çarşamba",
        "persembe",
        "perşembe",
        "cuma",
        "cumartesi",
        "pazar",
    }

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
        validated_data = self.validate_schedule(data)
        return self.get_repository("schedule").create(validated_data)

    def get_schedule(self, record_id):
        return self.get_repository("schedule").get_by_id(record_id)

    def list_schedules(self, limit: int = 100, offset: int = 0):
        return self.get_repository("schedule").list_all(limit, offset)

    def update_schedule(self, record_id, data):
        validated_data = self.validate_schedule(data)
        return self.get_repository("schedule").update(record_id, validated_data)

    def delete_schedule(self, record_id):
        return self.get_repository("schedule").delete(record_id)

    # Validation
    def validate_schedule(self, data: Any | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("schedule data must be a mapping")

        student_id = self._get_field_value(data, self._STUDENT_FIELDS)
        if student_id is None or not student_id:
            raise ValueError("student must be selected")

        course_id = self._get_field_value(data, self._COURSE_FIELDS)
        if course_id is None or not course_id:
            raise ValueError("course must be selected")

        day_value = self._get_field_value(data, self._DAY_FIELDS)
        if day_value is None or not day_value:
            raise ValueError("lesson day cannot be empty")
        if day_value.casefold() not in self._VALID_WEEK_DAYS:
            raise ValueError("lesson day must be a valid weekday")

        start_time_value = self._get_field_value(data, self._START_TIME_FIELDS)
        if start_time_value is None or not start_time_value:
            raise ValueError("start time cannot be empty")

        end_time_value = self._get_field_value(data, self._END_TIME_FIELDS)
        if end_time_value is None or not end_time_value:
            raise ValueError("end time cannot be empty")

        start_time = self._parse_time(start_time_value, "start time")
        end_time = self._parse_time(end_time_value, "end time")
        if start_time >= end_time:
            raise ValueError("start time must be earlier than end time")

        self.get_repository("schedule")
        return data

    def _get_field_value(self, data: Mapping[str, Any], field_names: tuple[str, ...]) -> str | None:
        for field_name in field_names:
            if field_name in data:
                value = data[field_name]
                if value is None:
                    return ""
                return str(value).strip()
        return None

    def _parse_time(self, value: str, field_label: str) -> time:
        value = value.strip()

        for parser in (time.fromisoformat, self._parse_time_via_datetime):
            try:
                return parser(value)
            except ValueError:
                continue

        raise ValueError(f"{field_label} must be a valid time")

    def _parse_time_via_datetime(self, value: str) -> time:
        return datetime.strptime(value, "%H:%M").time()
