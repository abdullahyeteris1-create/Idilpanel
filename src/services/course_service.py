"""Course service skeleton for course domain operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from repositories.course_repository import CourseRepository

from .base_service import BaseService


class CourseService(BaseService):
    """Service entry point for course-related operations."""

    _NAME_FIELDS = ("course_name", "name", "kurs_adi")
    _ACTIVE_FIELDS = ("is_active", "active", "durum", "status")
    _LEVEL_FIELDS = ("course_level", "level", "kur_no", "kur")
    _DURATION_FIELDS = ("duration", "duration_weeks", "sure", "total_lessons")

    _LEVEL_MIN = 1
    _LEVEL_MAX = 12

    def __init__(
        self,
        course_repository: CourseRepository | None = None,
        repositories: dict[str, Any] | None = None,
    ) -> None:
        merged_repositories = dict(repositories or {})
        if course_repository is not None:
            merged_repositories["course"] = course_repository
        super().__init__(merged_repositories)

    # CRUD Operations
    def create_course(self, data):
        validated_data = self.validate_course(data)
        repository_payload = self._to_repository_payload(validated_data)
        return self.get_repository("course").create(repository_payload)

    def get_course(self, record_id):
        return self.get_repository("course").get_by_id(record_id)

    def list_courses(self, limit: int = 100, offset: int = 0):
        return self.get_repository("course").list_all(limit, offset)

    def update_course(self, record_id, data):
        validated_data = self.validate_course(data, current_course_id=record_id)
        repository_payload = self._to_repository_payload(validated_data)
        return self.get_repository("course").update(record_id, repository_payload)

    def delete_course(self, record_id):
        return self.get_repository("course").delete(record_id)

    # Validation
    def validate_course(self, data: Any | None = None, current_course_id: int | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("course data must be a mapping")

        repository = self.get_repository("course")

        course_name = self._get_field_value(data, self._NAME_FIELDS)
        if course_name is None or not course_name:
            raise ValueError("course name cannot be empty")

        if hasattr(repository, "list_all"):
            self._ensure_unique_active_name(repository, course_name, current_course_id)

        level_value = self._get_field_value(data, self._LEVEL_FIELDS)
        if level_value is not None and level_value:
            level = self._parse_int(level_value, "course level")
            if level < self._LEVEL_MIN or level > self._LEVEL_MAX:
                raise ValueError(
                    f"course level must be between {self._LEVEL_MIN} and {self._LEVEL_MAX}"
                )

        duration_value = self._get_field_value(data, self._DURATION_FIELDS)
        if duration_value is not None and duration_value:
            duration = self._parse_float(duration_value, "course duration")
            if duration <= 0:
                raise ValueError("course duration must be a positive value")

        return data

    def _get_field_value(self, data: Mapping[str, Any], field_names: tuple[str, ...]) -> str | None:
        for field_name in field_names:
            if field_name in data:
                value = data[field_name]
                if value is None:
                    return ""
                return str(value).strip()
        return None

    def _ensure_unique_active_name(
        self,
        repository: CourseRepository,
        course_name: str,
        current_course_id: int | None = None,
    ) -> None:
        existing_courses = repository.list_all(limit=1000, offset=0)
        for existing_course in existing_courses:
            if not isinstance(existing_course, Mapping):
                continue

            existing_name = self._get_field_value(existing_course, self._NAME_FIELDS)
            if existing_name is None:
                continue

            if existing_name.casefold() != course_name.casefold():
                continue

            existing_id = existing_course.get("id")
            if current_course_id is not None and existing_id == current_course_id:
                continue

            if self._is_active(existing_course):
                raise ValueError("an active course with the same name already exists")

    def _is_active(self, data: Mapping[str, Any]) -> bool:
        for field_name in self._ACTIVE_FIELDS:
            if field_name not in data:
                continue

            value = data[field_name]
            if isinstance(value, bool):
                return value

            text = str(value).strip().casefold()
            return text in {"1", "true", "aktif", "active", "yes"}

        return True

    def _parse_int(self, value: str, field_label: str) -> int:
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(f"{field_label} must be a valid integer") from exc

    def _parse_float(self, value: str, field_label: str) -> float:
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(f"{field_label} must be a valid number") from exc

    def _to_repository_payload(self, data: Mapping[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {}

        if "student_id" in data:
            payload["student_id"] = data["student_id"]

        level_value = self._get_field_value(data, self._LEVEL_FIELDS)
        if level_value is not None and level_value:
            payload["kur_no"] = self._parse_int(level_value, "course level")

        start_date = data.get("baslangic")
        if start_date is not None:
            payload["baslangic"] = str(start_date).strip()

        end_date = data.get("bitis")
        if end_date is not None:
            cleaned_end_date = str(end_date).strip()
            if cleaned_end_date:
                payload["bitis"] = cleaned_end_date

        status_value = data.get("durum")
        if status_value is not None:
            payload["durum"] = str(status_value).strip()

        duration_value = self._get_field_value(data, self._DURATION_FIELDS)
        if duration_value is not None and duration_value:
            payload["hedef_ders_sayisi"] = self._parse_int(duration_value, "course duration")

        if "is_active" in data:
            payload["is_active"] = data["is_active"]

        return payload
