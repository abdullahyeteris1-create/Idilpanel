"""Student service skeleton for student domain operations."""

from __future__ import annotations

from typing import Any

from repositories.student_repository import StudentRepository

from .base_service import BaseService


class StudentService(BaseService):
    """Service entry point for student-related operations."""

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
        return self.get_repository("student").create(data)

    def get_student(self, record_id):
        return self.get_repository("student").get_by_id(record_id)

    def list_students(self, limit: int = 100, offset: int = 0):
        return self.get_repository("student").list_all(limit, offset)

    def update_student(self, record_id, data):
        return self.get_repository("student").update(record_id, data)

    def delete_student(self, record_id):
        return self.get_repository("student").delete(record_id)

    def validate_student(self, data):
        self.get_repository("student")
        return data
