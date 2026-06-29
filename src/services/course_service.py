"""Course service skeleton for course domain operations."""

from __future__ import annotations

from typing import Any

from repositories.course_repository import CourseRepository

from .base_service import BaseService


class CourseService(BaseService):
    """Service entry point for course-related operations."""

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
        return self.get_repository("course").create(data)

    def get_course(self, record_id):
        return self.get_repository("course").get_by_id(record_id)

    def list_courses(self, limit: int = 100, offset: int = 0):
        return self.get_repository("course").list_all(limit, offset)

    def update_course(self, record_id, data):
        return self.get_repository("course").update(record_id, data)

    def delete_course(self, record_id):
        return self.get_repository("course").delete(record_id)

    # Validation
    def validate_course(self, data: Any | None = None):
        self.get_repository("course")
        return data
