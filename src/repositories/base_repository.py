"""Base repository with shared connection and execute helpers."""

from __future__ import annotations

from collections.abc import Sequence
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

    def execute_insert(self, query: str, params: Sequence[Any] | None = None) -> int:
        """Execute insert statement and return inserted row id."""
        resolved_params = tuple(params or ())
        with self._connection_manager.connection_scope() as connection:
            cursor = connection.execute(query, resolved_params)
            return int(cursor.lastrowid)

    def execute_write(self, query: str, params: Sequence[Any] | None = None) -> int:
        """Execute update/delete-like statement and return affected row count."""
        resolved_params = tuple(params or ())
        with self._connection_manager.connection_scope() as connection:
            cursor = connection.execute(query, resolved_params)
            return int(cursor.rowcount)

    def execute_fetchone(self, query: str, params: Sequence[Any] | None = None) -> dict[str, Any] | None:
        """Execute select-like statement and return the first row as a dict."""
        resolved_params = tuple(params or ())
        with self._connection_manager.connection_scope() as connection:
            row = connection.execute(query, resolved_params).fetchone()
            return dict(row) if row else None

    def execute_fetchall(self, query: str, params: Sequence[Any] | None = None) -> list[dict[str, Any]]:
        """Execute select-like statement and return rows as dict list."""
        resolved_params = tuple(params or ())
        with self._connection_manager.connection_scope() as connection:
            rows = connection.execute(query, resolved_params).fetchall()
            return [dict(row) for row in rows]
