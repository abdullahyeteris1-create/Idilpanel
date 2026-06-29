"""Lesson service skeleton for lesson domain operations."""

from __future__ import annotations

from collections.abc import Mapping
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

        return data

    # Business Operations
    # Epic 4.1B scope: intentionally left empty.
