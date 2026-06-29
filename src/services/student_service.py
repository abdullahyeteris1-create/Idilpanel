"""Student service skeleton for student domain operations."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from typing import Any

from repositories.student_repository import StudentRepository

from .base_service import BaseService


class StudentService(BaseService):
    """Service entry point for student-related operations."""

    _FULL_NAME_FIELDS = ("full_name", "ad_soyad", "name")
    _FIRST_NAME_FIELDS = ("first_name", "ad")
    _LAST_NAME_FIELDS = ("last_name", "soyad")
    _CLASS_FIELDS = ("class_name", "class", "sinif")
    _COURSE_FIELDS = ("course_id", "kurs_id", "course", "kurs")
    _START_DATE_FIELDS = ("start_date", "baslangic_tarihi")

    def __init__(
        self,
        student_repository: StudentRepository | None = None,
        repositories: dict[str, Any] | None = None,
    ) -> None:
        merged_repositories = dict(repositories or {})
        if student_repository is not None:
            merged_repositories["student"] = student_repository
        super().__init__(merged_repositories)

    def create_student(self, data):
        validated_data = self.validate_student(data)
        return self.get_repository("student").create(validated_data)

    def get_student(self, record_id):
        self.validate_student()
        return self.get_repository("student").get_by_id(record_id)

    def list_students(self, limit: int = 100, offset: int = 0):
        self.validate_student()
        return self.get_repository("student").list_all(limit, offset)

    def update_student(self, record_id, data):
        validated_data = self.validate_student(data)
        return self.get_repository("student").update(record_id, validated_data)

    def delete_student(self, record_id):
        self.validate_student()
        return self.get_repository("student").delete(record_id)

    def validate_student(self, data: Mapping[str, Any] | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("student data must be a mapping")

        full_name = self._get_field_value(data, self._FULL_NAME_FIELDS)
        first_name = self._get_field_value(data, self._FIRST_NAME_FIELDS)
        last_name = self._get_field_value(data, self._LAST_NAME_FIELDS)

        if full_name is not None:
            if not full_name:
                raise ValueError("student name cannot be empty")
        else:
            if first_name is None or last_name is None:
                raise ValueError("student name cannot be empty")
            if not first_name:
                raise ValueError("student first name cannot be empty")
            if not last_name:
                raise ValueError("student last name cannot be empty")

        class_value = self._get_field_value(data, self._CLASS_FIELDS)
        if class_value is None or not class_value:
            raise ValueError("student class information cannot be empty")

        course_value = self._get_field_value(data, self._COURSE_FIELDS)
        if course_value is None or not course_value:
            raise ValueError("student must be assigned to a course")

        start_date_value = self._get_field_value(data, self._START_DATE_FIELDS)
        if start_date_value is None or not start_date_value:
            raise ValueError("student start date cannot be empty")

        self._parse_date(start_date_value)
        return data

    def _get_field_value(self, data: Mapping[str, Any], field_names: tuple[str, ...]) -> str | None:
        for field_name in field_names:
            if field_name in data:
                value = data[field_name]
                if value is None:
                    return ""

                text = str(value).strip()
                return text
        return None

    def _parse_date(self, value: Any) -> date:
        if isinstance(value, date):
            return value

        if isinstance(value, datetime):
            return value.date()

        if not isinstance(value, str):
            raise ValueError("student start date must be a valid date")

        cleaned_value = value.strip()
        try:
            return date.fromisoformat(cleaned_value)
        except ValueError as first_error:
            try:
                return datetime.fromisoformat(cleaned_value).date()
            except ValueError as second_error:
                raise ValueError("student start date must be a valid date") from second_error
