"""Base repository with shared connection and execute helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from typing import Any

from database.connection_manager import SQLiteConnectionManager, db_manager


class BaseRepository:
    """Provide common connection, transaction, and execute helpers."""

    def __init__(self, connection_manager: SQLiteConnectionManager | None = None) -> None:
        self._connection_manager = connection_manager or db_manager

    @contextmanager
    def connection_scope(self):
        """Expose transaction-safe connection scope to repositories."""
        with self._connection_manager.connection_scope() as connection:
            yield connection

    def _validate_payload(self, data: Mapping[str, Any]) -> None:
        if not data:
            raise ValueError("data must not be empty")

    def _insert_from_mapping(self, table_name: str, data: Mapping[str, Any]) -> int:
        self._validate_payload(data)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute_insert(query, tuple(data.values()))

    def _select_by_id(self, table_name: str, id_column: str, record_id: int) -> dict[str, Any] | None:
        query = f"SELECT * FROM {table_name} WHERE {id_column} = ? LIMIT 1"
        return self.execute_fetchone(query, (record_id,))

    def _select_all(self, table_name: str, id_column: str, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        query = f"SELECT * FROM {table_name} ORDER BY {id_column} ASC LIMIT ? OFFSET ?"
        return self.execute_fetchall(query, (limit, offset))

    def _update_from_mapping(self, table_name: str, id_column: str, record_id: int, data: Mapping[str, Any]) -> bool:
        if not data:
            return False

        set_clause = ", ".join([f"{column} = ?" for column in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = ?"
        params = tuple(data.values()) + (record_id,)
        return self.execute_write(query, params) > 0

    def _delete_by_id(self, table_name: str, id_column: str, record_id: int) -> bool:
        query = f"DELETE FROM {table_name} WHERE {id_column} = ?"
        return self.execute_write(query, (record_id,)) > 0

    def execute_insert(self, query: str, params: Sequence[Any] | None = None) -> int:
        """Execute insert statement and return inserted row id."""
        resolved_params = tuple(params or ())
        with self.connection_scope() as connection:
            cursor = connection.execute(query, resolved_params)
            return int(cursor.lastrowid)

    def execute_write(self, query: str, params: Sequence[Any] | None = None) -> int:
        """Execute update/delete-like statement and return affected row count."""
        resolved_params = tuple(params or ())
        with self.connection_scope() as connection:
            cursor = connection.execute(query, resolved_params)
            return int(cursor.rowcount)

    def execute_fetchone(self, query: str, params: Sequence[Any] | None = None) -> dict[str, Any] | None:
        """Execute select-like statement and return the first row as a dict."""
        resolved_params = tuple(params or ())
        with self.connection_scope() as connection:
            row = connection.execute(query, resolved_params).fetchone()
            return dict(row) if row else None

    def execute_fetchall(self, query: str, params: Sequence[Any] | None = None) -> list[dict[str, Any]]:
        """Execute select-like statement and return rows as dict list."""
        resolved_params = tuple(params or ())
        with self.connection_scope() as connection:
            rows = connection.execute(query, resolved_params).fetchall()
            return [dict(row) for row in rows]
