"""Lesson service skeleton for lesson domain operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from repositories.lesson_repository import LessonRepository

from .base_service import BaseService


class LessonService(BaseService):
    """Service entry point for lesson-related operations."""

    def __init__(
        self,
        lesson_repository: LessonRepository | None = None,
        repositories: dict[str, Any] | None = None,
    ) -> None:
        merged_repositories = dict(repositories or {})
        if lesson_repository is not None:
            merged_repositories["lesson"] = lesson_repository
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

    # Validation
    def validate_lesson(self, data: Any | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("lesson data must be a mapping")

        return data

    # Business Operations
    # Epic 4.1B scope: intentionally left empty.
