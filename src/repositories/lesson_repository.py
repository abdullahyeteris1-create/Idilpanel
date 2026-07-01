"""Lesson repository skeleton for lesson table operations."""

from __future__ import annotations

from .base_repository import BaseRepository


class LessonRepository(BaseRepository):
    """Repository entry point for lessons table access."""

    table_name: str = "lessons"
    id_column: str = "id"

    def ensure_lr_columns(self) -> None:
        """Add lesson-record optional columns for existing local SQLite files."""
        columns = {
            row["name"]
            for row in self.execute_fetchall(f"PRAGMA table_info({self.table_name})")
        }
        if "gun_no" not in columns:
            self.execute_write(f"ALTER TABLE {self.table_name} ADD COLUMN gun_no INTEGER NOT NULL DEFAULT 1")
        if "okuma_hizi" not in columns:
            self.execute_write(f"ALTER TABLE {self.table_name} ADD COLUMN okuma_hizi REAL")
        if "anlama_algi" not in columns:
            self.execute_write(f"ALTER TABLE {self.table_name} ADD COLUMN anlama_algi REAL")

    def create(self, data):
        self.ensure_lr_columns()
        return self._insert_from_mapping(self.table_name, data)

    def get_by_id(self, record_id):
        self.ensure_lr_columns()
        return self._select_by_id(self.table_name, self.id_column, record_id)

    def list_all(self, limit: int = 100, offset: int = 0):
        self.ensure_lr_columns()
        return self._select_all(self.table_name, self.id_column, limit, offset)

    def update(self, record_id, data):
        self.ensure_lr_columns()
        return self._update_from_mapping(self.table_name, self.id_column, record_id, data)

    def delete(self, record_id):
        return self._delete_by_id(self.table_name, self.id_column, record_id)

    def get_by_course_lesson(self, course_id: int, lesson_no: int):
        self.ensure_lr_columns()
        return self.execute_fetchone(
            """
            SELECT *
            FROM lessons
            WHERE course_id = ? AND lesson_no = ? AND is_active = 1
            LIMIT 1
            """,
            (course_id, lesson_no),
        )

    def list_by_course(self, course_id: int):
        self.ensure_lr_columns()
        return self.execute_fetchall(
            """
            SELECT *
            FROM lessons
            WHERE course_id = ? AND is_active = 1
            ORDER BY gun_no ASC, lesson_no ASC, id ASC
            """,
            (course_id,),
        )

    def list_by_course_day(self, course_id: int, day_no: int):
        self.ensure_lr_columns()
        return self.execute_fetchall(
            """
            SELECT *
            FROM lessons
            WHERE course_id = ? AND gun_no = ? AND is_active = 1
            ORDER BY lesson_no ASC, id ASC
            """,
            (course_id, day_no),
        )
