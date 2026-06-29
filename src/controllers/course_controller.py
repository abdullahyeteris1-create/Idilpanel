"""Course controller skeleton for UI-to-service request orchestration."""

from __future__ import annotations

from services.course_service import CourseService


class CourseController:
    """Bridge UI requests to CourseService without business logic."""

    def __init__(self, course_service: CourseService) -> None:
        self._course_service = course_service

    def create_course(self, data):
        return self._course_service.create_course(data)

    def get_course(self, record_id):
        return self._course_service.get_course(record_id)

    def list_courses(self, limit: int = 100, offset: int = 0):
        return self._course_service.list_courses(limit, offset)

    def update_course(self, record_id, data):
        return self._course_service.update_course(record_id, data)

    def delete_course(self, record_id):
        return self._course_service.delete_course(record_id)
