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

    def save_course_day_lesson(self, data):
        return self._lesson_service.save_course_day_lesson(data)

    def create_course_day_entry(self, data):
        return self._lesson_service.create_course_day_entry(data)

    def get_course_day_lesson(self, course_id: int, day_no: int, lesson_slot: int):
        return self._lesson_service.get_course_day_lesson(course_id, day_no, lesson_slot)

    def list_course_lessons(self, course_id: int):
        return self._lesson_service.list_course_lessons(course_id)

    def list_student_lessons(self, student_id: int):
        return self._lesson_service.list_student_lessons(student_id)

    def list_course_day_lessons(self, course_id: int, day_no: int):
        return self._lesson_service.list_course_day_lessons(course_id, day_no)

    def day_slot_from_lesson_no(self, lesson_no: int) -> tuple[int, int]:
        return self._lesson_service.day_slot_from_lesson_no(lesson_no)

    def delete_lesson(self, record_id):
        return self._lesson_service.delete_lesson(record_id)

    def list_students(self, limit: int = 200, offset: int = 0):
        return self._lesson_service.list_students(limit, offset)

    def list_active_students(self, limit: int = 200, offset: int = 0):
        return self._lesson_service.list_active_students(limit, offset)

    def list_courses(self, student_id: int | None = None, limit: int = 200, offset: int = 0):
        return self._lesson_service.list_courses(student_id, limit, offset)

    def is_course_available_for_student(self, student_id: int, course_id: int) -> bool:
        return self._lesson_service.is_course_available_for_student(student_id, course_id)

    def suggest_next_lesson_no(self, course_id: int) -> int:
        return self._lesson_service.suggest_next_lesson_no(course_id)
