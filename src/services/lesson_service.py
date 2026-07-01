"""Lesson service skeleton for lesson domain operations."""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from datetime import date, datetime
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

    def save_course_day_lesson(self, data):
        return self.create_course_day_entry(data)

    def create_course_day_entry(self, data):
        prepared_data = dict(data or {})
        day_no = self._require_day_no(prepared_data.get("day_no") or prepared_data.get("gun_no"))
        prepared_data["gun_no"] = day_no
        prepared_data["lesson_no"] = self._next_day_lesson_no(
            self._require_positive_int(prepared_data.get("course_id"), "course"),
            day_no,
        )
        validated_data = self.validate_lesson(prepared_data)
        validated_data["gun_no"] = day_no
        validated_data["lesson_no"] = prepared_data["lesson_no"]
        try:
            return self.get_repository("lesson").create(validated_data)
        except sqlite3.IntegrityError:
            validated_data["lesson_no"] = self.suggest_next_lesson_no(validated_data["course_id"])
            return self.get_repository("lesson").create(validated_data)

    def get_course_day_lesson(self, course_id: int, day_no: int, lesson_slot: int):
        lesson_no = self.lesson_no_from_day_slot(day_no, lesson_slot)
        return self.get_repository("lesson").get_by_course_lesson(course_id, lesson_no)

    def list_course_lessons(self, course_id: int):
        return self.get_repository("lesson").list_by_course(course_id)

    def list_student_lessons(self, student_id: int):
        student_id = self._require_positive_int(student_id, "student")
        return self.get_repository("lesson").list_by_student(student_id)

    def list_course_day_lessons(self, course_id: int, day_no: int):
        return self.get_repository("lesson").list_by_course_day(course_id, self._require_day_no(day_no))

    def delete_lesson(self, record_id):
        return self.get_repository("lesson").delete(record_id)

    def list_students(self, limit: int = 200, offset: int = 0):
        return self.get_repository("student").list_all(limit, offset)

    def list_active_students(self, limit: int = 200, offset: int = 0):
        repository = self.get_repository("student")
        if hasattr(repository, "list_active"):
            return repository.list_active(limit, offset)
        return [
            record
            for record in repository.list_all(limit, offset)
            if int(record.get("is_active", 1) or 0) == 1
            and not record.get("deleted_at")
            and str(record.get("durum") or "").strip() == "Aktif"
        ]

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

    def _next_day_lesson_no(self, course_id: int, day_no: int) -> int:
        records = self.get_repository("lesson").list_by_course_day(course_id, day_no)
        return len(records) + 1

    @staticmethod
    def _require_day_no(value: Any) -> int:
        try:
            day_no = int(str(value).strip())
        except (TypeError, ValueError) as exc:
            raise ValueError("day_no is required") from exc
        if day_no < 1 or day_no > 8:
            raise ValueError("day_no must be between 1 and 8")
        return day_no

    @staticmethod
    def lesson_no_from_day_slot(day_no: int, lesson_slot: int) -> int:
        day = int(day_no)
        slot = int(lesson_slot)
        if day < 1 or day > 8:
            raise ValueError("day_no must be between 1 and 8")
        if slot not in (1, 2):
            raise ValueError("lesson_slot must be 1 or 2")
        return ((day - 1) * 2) + slot

    @staticmethod
    def day_slot_from_lesson_no(lesson_no: int) -> tuple[int, int]:
        value = int(lesson_no)
        if value < 1 or value > 16:
            raise ValueError("lesson_no must be between 1 and 16")
        return ((value - 1) // 2) + 1, 1 if value % 2 else 2

    # Validation
    def validate_lesson(self, data: Any | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("lesson data must be a mapping")

        student_id = self._require_positive_int(data.get("student_id"), "student")
        course_id = self._require_positive_int(data.get("course_id"), "course")
        day_no = self._require_day_no(data.get("gun_no") or data.get("day_no") or 1)

        if data.get("lesson_no") not in (None, ""):
            lesson_no = self._require_positive_int(data.get("lesson_no"), "lesson_no")
        else:
            lesson_slot = self._require_positive_int(data.get("lesson_slot"), "lesson_slot")
            lesson_no = self.lesson_no_from_day_slot(day_no, lesson_slot)

        if not self.student_exists(student_id):
            raise ValueError("student not found")

        if not self.is_course_available_for_student(student_id, course_id):
            raise ValueError("selected course does not belong to selected student")

        if lesson_no > 16:
            raise ValueError("lesson_no must be between 1 and 16")

        text_name = str(data.get("metin") or "").strip()
        if not text_name:
            raise ValueError("text_name is required")

        date_value = str(data.get("tarih") or "").strip() or date.today().isoformat()
        self._validate_iso_date(date_value)

        speed = self._optional_positive_float(data.get("okuma_hizi"), "okuma_hizi")
        comprehension = self._optional_float_in_range(data.get("anlama_algi"), "anlama_algi", 0.0, 100.0)
        focus_percent = self._optional_float_in_range(data.get("focus_percent"), "focus_percent", 0.0, 100.0)

        validated_payload: dict[str, Any] = {
            "course_id": course_id,
            "gun_no": day_no,
            "lesson_no": lesson_no,
            "tarih": date_value,
            "metin": text_name,
            "okuma_hizi": speed,
            "anlama_algi": comprehension,
            "focus_percent": focus_percent,
            "ogretmen_notu": str(data.get("ogretmen_notu") or data.get("notlar") or "").strip() or None,
            "durum": str(data.get("durum") or "Tamamlandi").strip() or "Tamamlandi",
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
    def _optional_positive_float(value: Any, field_name: str) -> float | None:
        if value is None or str(value).strip() == "":
            return None
        try:
            parsed = float(str(value).strip().replace(",", "."))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be numeric") from exc

        if parsed < 0:
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

    @staticmethod
    def _optional_float_in_range(value: Any, field_name: str, min_value: float, max_value: float) -> float | None:
        if value is None or str(value).strip() == "":
            return None
        try:
            parsed = float(str(value).strip().replace(",", "."))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be numeric") from exc

        if not (min_value <= parsed <= max_value):
            raise ValueError(f"{field_name} must be between {min_value:g} and {max_value:g}")
        return parsed

    # Business Operations
    # Epic 4.1B scope: intentionally left empty.
