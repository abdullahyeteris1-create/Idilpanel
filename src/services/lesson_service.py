"""Lesson service skeleton for lesson domain operations."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any

from repositories.course_repository import CourseRepository
from repositories.lesson_repository import LessonRepository
from repositories.student_repository import StudentRepository

from .base_service import BaseService


class LessonService(BaseService):
    """Service entry point for lesson-related operations."""

    def __init__(
        self,
        lesson_repository: LessonRepository | None = None,
        student_repository: StudentRepository | None = None,
        course_repository: CourseRepository | None = None,
        repositories: dict[str, Any] | None = None,
    ) -> None:
        merged_repositories = dict(repositories or {})
        if lesson_repository is not None:
            merged_repositories["lesson"] = lesson_repository
        if student_repository is not None:
            merged_repositories["student"] = student_repository
        if course_repository is not None:
            merged_repositories["course"] = course_repository
        super().__init__(merged_repositories)

    # CRUD Operations
    def create_lesson(self, data):
        validated_data = self.validate_lesson(data)
        return self.get_repository("lesson").create(validated_data)

    def get_lesson(self, record_id):
        return self.get_repository("lesson").get_by_id(record_id)

    def list_lessons(self, limit: int = 100, offset: int = 0):
        return self.get_repository("lesson").list_all(limit, offset)

    def update_lesson(self, record_id, data):
        validated_data = self.validate_lesson(data)
        return self.get_repository("lesson").update(record_id, validated_data)

    def delete_lesson(self, record_id):
        return self.get_repository("lesson").delete(record_id)

    def list_students(self, limit: int = 200, offset: int = 0):
        return self.get_repository("student").list_all(limit, offset)

    def student_exists(self, student_id: int) -> bool:
        student = self.get_repository("student").get_by_id(student_id)
        return bool(student)

    def list_courses(self, student_id: int | None = None, limit: int = 200, offset: int = 0):
        records = self.get_repository("course").list_all(limit, offset)
        if student_id is None:
            return records
        return [record for record in records if int(record.get("student_id", 0)) == int(student_id)]

    def is_course_available_for_student(self, student_id: int, course_id: int) -> bool:
        return any(
            int(record.get("id", 0)) == int(course_id)
            for record in self.list_courses(student_id=student_id, limit=500, offset=0)
        )

    def suggest_next_lesson_no(self, course_id: int) -> int:
        records = self.list_lessons(limit=500, offset=0)
        lesson_numbers = [
            int(record.get("lesson_no", 0))
            for record in records
            if int(record.get("course_id", 0)) == int(course_id)
        ]
        return max(lesson_numbers, default=0) + 1

    # Validation
    def validate_lesson(self, data: Any | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("lesson data must be a mapping")

        student_id = self._require_positive_int(data.get("student_id"), "student")
        course_id = self._require_positive_int(data.get("course_id"), "course")
        lesson_no = self._require_positive_int(data.get("lesson_no"), "lesson_no")
        word_count = self._require_positive_int(data.get("word_count"), "word_count")
        duration = self._require_positive_float(data.get("duration"), "duration")
        comprehension = self._require_float_in_range(data.get("comprehension"), "comprehension", 0.0, 100.0)

        if not self.student_exists(student_id):
            raise ValueError("student not found")

        if not self.is_course_available_for_student(student_id, course_id):
            raise ValueError("selected course does not belong to selected student")

        if lesson_no > 16:
            raise ValueError("lesson_no must be between 1 and 16")

        date_value = str(data.get("tarih") or "").strip()
        if not date_value:
            raise ValueError("lesson_date is required")
        self._validate_iso_date(date_value)

        note = (
            f"Ogrenci: {self._student_label(student_id)} | "
            f"Kelime: {word_count} | "
            f"Sure: {duration} | "
            f"Anlama: {comprehension}"
        )

        validated_payload: dict[str, Any] = {
            "course_id": course_id,
            "lesson_no": lesson_no,
            "tarih": date_value,
            "metin": str(data.get("metin") or "").strip() or None,
            "ogretmen_notu": note,
            "durum": str(data.get("durum") or "Planlandi").strip() or "Planlandi",
        }

        return validated_payload

    def _student_label(self, student_id: int) -> str:
        student = self.get_repository("student").get_by_id(student_id)
        if not student:
            return str(student_id)
        return str(student.get("ad_soyad") or student_id)

    @staticmethod
    def _validate_iso_date(value: str) -> None:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("lesson_date must be YYYY-MM-DD") from exc

    @staticmethod
    def _require_positive_int(value: Any, field_name: str) -> int:
        try:
            parsed = int(str(value).strip())
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} is required") from exc

        if parsed <= 0:
            raise ValueError(f"{field_name} must be positive")
        return parsed

    @staticmethod
    def _require_positive_float(value: Any, field_name: str) -> float:
        try:
            parsed = float(str(value).strip())
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} is required") from exc

        if parsed <= 0:
            raise ValueError(f"{field_name} must be positive")
        return parsed

    @staticmethod
    def _require_float_in_range(value: Any, field_name: str, min_value: float, max_value: float) -> float:
        try:
            parsed = float(str(value).strip())
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} is required") from exc

        if not (min_value <= parsed <= max_value):
            raise ValueError(f"{field_name} must be between {min_value:g} and {max_value:g}")
        return parsed

    # Business Operations
    # Epic 4.1B scope: intentionally left empty.
