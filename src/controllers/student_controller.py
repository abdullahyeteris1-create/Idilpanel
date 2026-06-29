"""Student controller skeleton for UI-to-service request orchestration."""

from __future__ import annotations

from services.student_service import StudentService


class StudentController:
    """Bridge UI requests to StudentService without business logic."""

    def __init__(self, student_service: StudentService) -> None:
        self._student_service = student_service

    def create_student(self, data):
        return self._student_service.create_student(data)

    def get_student(self, record_id):
        return self._student_service.get_student(record_id)

    def list_students(self, limit: int = 100, offset: int = 0):
        return self._student_service.list_students(limit, offset)

    def update_student(self, record_id, data):
        return self._student_service.update_student(record_id, data)

    def delete_student(self, record_id):
        return self._student_service.delete_student(record_id)
