"""Repository for text library table operations."""

from __future__ import annotations

from typing import Any

from .base_repository import BaseRepository


class TextRepository(BaseRepository):
    """Repository entry point for the texts table."""

    table_name = "texts"
    id_column = "id"

    def ensure_table(self) -> None:
        self.execute_write(
            """
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                course_level INTEGER NOT NULL CHECK (course_level >= 1),
                category TEXT,
                word_count INTEGER CHECK (word_count IS NULL OR word_count >= 0),
                is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.execute_write("CREATE INDEX IF NOT EXISTS idx_texts_title ON texts(title)")
        self.execute_write("CREATE INDEX IF NOT EXISTS idx_texts_course_level ON texts(course_level)")
        self.execute_write("CREATE INDEX IF NOT EXISTS idx_texts_is_active ON texts(is_active)")

    def create(self, data):
        self.ensure_table()
        return self._insert_from_mapping(self.table_name, data)

    def get_by_id(self, record_id):
        self.ensure_table()
        return self._select_by_id(self.table_name, self.id_column, record_id)

    def list_all(self, limit: int = 100, offset: int = 0):
        self.ensure_table()
        return self._select_all(self.table_name, self.id_column, limit, offset)

    def update(self, record_id, data):
        self.ensure_table()
        return self._update_from_mapping(self.table_name, self.id_column, record_id, data)

    def delete(self, record_id):
        self.ensure_table()
        return self._delete_by_id(self.table_name, self.id_column, record_id)

    def search(self, query: str = "", course_level: int | None = None, limit: int = 500, offset: int = 0) -> list[dict[str, Any]]:
        self.ensure_table()
        clauses: list[str] = []
        params: list[Any] = []

        cleaned_query = str(query or "").strip()
        if cleaned_query:
            clauses.append("(LOWER(title) LIKE ? OR LOWER(COALESCE(category, '')) LIKE ?)")
            like_value = f"%{cleaned_query.lower()}%"
            params.extend([like_value, like_value])

        if course_level is not None:
            clauses.append("course_level = ?")
            params.append(course_level)

        where_clause = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        params.extend([limit, offset])

        return self.execute_fetchall(
            f"""
            SELECT *
            FROM texts
            {where_clause}
            ORDER BY course_level ASC, title COLLATE NOCASE ASC, id ASC
            LIMIT ? OFFSET ?
            """,
            tuple(params),
        )

    def find_by_level_title(self, course_level: int, title: str):
        self.ensure_table()
        return self.execute_fetchone(
            """
            SELECT *
            FROM texts
            WHERE course_level = ? AND LOWER(title) = LOWER(?)
            LIMIT 1
            """,
            (course_level, title.strip()),
        )
