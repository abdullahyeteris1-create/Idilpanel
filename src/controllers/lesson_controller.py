"""Lesson controller skeleton for UI-to-service request orchestration."""

from __future__ import annotations

from services.lesson_service import LessonService


class LessonController:
    """Bridge UI requests to LessonService without business logic."""

    def __init__(self, lesson_service: LessonService) -> None:
        self._lesson_service = lesson_service

    def create_lesson(self, data):
        return self._lesson_service.create_lesson(data)

    def get_lesson(self, record_id):
        return self._lesson_service.get_lesson(record_id)

    def list_lessons(self, limit: int = 100, offset: int = 0):
        return self._lesson_service.list_lessons(limit, offset)

    def update_lesson(self, record_id, data):
        return self._lesson_service.update_lesson(record_id, data)

    def delete_lesson(self, record_id):
        return self._lesson_service.delete_lesson(record_id)

    def list_students(self, limit: int = 200, offset: int = 0):
        return self._lesson_service.list_students(limit, offset)

    def list_courses(self, student_id: int | None = None, limit: int = 200, offset: int = 0):
        return self._lesson_service.list_courses(student_id, limit, offset)

    def is_course_available_for_student(self, student_id: int, course_id: int) -> bool:
        return self._lesson_service.is_course_available_for_student(student_id, course_id)

    def suggest_next_lesson_no(self, course_id: int) -> int:
        return self._lesson_service.suggest_next_lesson_no(course_id)
