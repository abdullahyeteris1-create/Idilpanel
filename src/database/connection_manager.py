"""Shared SQLite connection manager for repository layer consumption."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from threading import Lock

from .config import DatabaseConfig


class SQLiteConnectionManager:
    """Manage SQLite DB file lifecycle and connection open/close operations."""

    def __init__(self, config: DatabaseConfig | None = None) -> None:
        self._config = config or DatabaseConfig.from_env()
        self._init_lock = Lock()
        self._is_initialized = False

    @property
    def config(self) -> DatabaseConfig:
        return self._config

    def initialize(self) -> None:
        """Ensure DB file and parent directory exist without creating schema."""
        if self._is_initialized:
            return

        with self._init_lock:
            if self._is_initialized:
                return

            self._config.db_path.parent.mkdir(parents=True, exist_ok=True)
            if not self._config.db_path.exists():
                connection = sqlite3.connect(self._config.db_path, timeout=self._config.timeout_seconds)
                connection.close()

            self._is_initialized = True

    def connect(self) -> sqlite3.Connection:
        """Open a new SQLite connection prepared for repository layer usage."""
        self.initialize()
        connection = sqlite3.connect(self._config.db_path, timeout=self._config.timeout_seconds)
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.row_factory = sqlite3.Row
        return connection

    def close(self, connection: sqlite3.Connection) -> None:
        """Close connection safely."""
        connection.close()

    @contextmanager
    def connection_scope(self):
        """Provide transactional connection scope with rollback safety."""
        connection = self.connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            self.close(connection)


# Shared instance intended for future repository layer usage.
db_manager = SQLiteConnectionManager()
