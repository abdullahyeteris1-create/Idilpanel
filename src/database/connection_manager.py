"""Shared SQLite connection manager for repository layer consumption."""

from __future__ import annotations

import shutil
import sqlite3
from contextlib import contextmanager
from datetime import datetime
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
        """Ensure DB file, schema, and runtime diagnostics exist."""
        if self._is_initialized:
            return

        with self._init_lock:
            if self._is_initialized:
                return

            self._config.db_path.parent.mkdir(parents=True, exist_ok=True)
            if not self._config.db_path.exists():
                self._bootstrap_database()

            self._ensure_schema_compatibility()
            self._write_runtime_log()

            self._is_initialized = True

    def _bootstrap_database(self) -> None:
        bundled_db_path = self._config.bundled_db_path
        if bundled_db_path.exists() and bundled_db_path.resolve() != self._config.db_path.resolve():
            shutil.copy2(bundled_db_path, self._config.db_path)
            return

        connection = sqlite3.connect(self._config.db_path, timeout=self._config.timeout_seconds)
        try:
            schema_path = self._config.schema_path
            if schema_path.exists():
                connection.executescript(schema_path.read_text(encoding="utf-8"))
            connection.commit()
        finally:
            connection.close()

    def _ensure_schema_compatibility(self) -> None:
        connection = sqlite3.connect(self._config.db_path, timeout=self._config.timeout_seconds)
        connection.row_factory = sqlite3.Row
        try:
            schema_path = self._config.schema_path
            has_students = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'students'"
            ).fetchone()
            if not has_students and schema_path.exists():
                connection.executescript(schema_path.read_text(encoding="utf-8"))

            self._ensure_texts_table(connection)
            self._ensure_student_columns(connection)
            self._ensure_lesson_columns(connection)
            self._ensure_weekly_schedule_columns(connection)
            connection.commit()
        finally:
            connection.close()

    def _ensure_texts_table(self, connection: sqlite3.Connection) -> None:
        connection.execute(
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
        connection.execute("CREATE INDEX IF NOT EXISTS idx_texts_title ON texts(title)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_texts_course_level ON texts(course_level)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_texts_is_active ON texts(is_active)")

    def _ensure_student_columns(self, connection: sqlite3.Connection) -> None:
        if not self._table_exists(connection, "students"):
            return
        columns = self._columns(connection, "students")
        for column in ("email", "kullanici_adi", "sifre", "bitis_tarihi"):
            if column not in columns:
                connection.execute(f"ALTER TABLE students ADD COLUMN {column} TEXT")
        connection.execute(
            """
            UPDATE students
            SET email = eposta
            WHERE (email IS NULL OR email = '')
              AND (eposta IS NOT NULL AND eposta <> '')
            """
        )

    def _ensure_lesson_columns(self, connection: sqlite3.Connection) -> None:
        if not self._table_exists(connection, "lessons"):
            return
        columns = self._columns(connection, "lessons")
        if "okuma_hizi" not in columns:
            connection.execute("ALTER TABLE lessons ADD COLUMN okuma_hizi REAL")
        if "anlama_algi" not in columns:
            connection.execute("ALTER TABLE lessons ADD COLUMN anlama_algi REAL")
        if "gun_no" not in columns:
            connection.execute("ALTER TABLE lessons ADD COLUMN gun_no INTEGER NOT NULL DEFAULT 1")
        if "focus_percent" not in columns:
            connection.execute("ALTER TABLE lessons ADD COLUMN focus_percent REAL")

    def _ensure_weekly_schedule_columns(self, connection: sqlite3.Connection) -> None:
        if not self._table_exists(connection, "weekly_schedule"):
            return
        columns = self._columns(connection, "weekly_schedule")
        if "progress_day" not in columns:
            connection.execute("ALTER TABLE weekly_schedule ADD COLUMN progress_day INTEGER NOT NULL DEFAULT 0")

    def _table_exists(self, connection: sqlite3.Connection, table_name: str) -> bool:
        return (
            connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
                (table_name,),
            ).fetchone()
            is not None
        )

    def _columns(self, connection: sqlite3.Connection, table_name: str) -> set[str]:
        return {row["name"] for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()}

    def _table_count(self, connection: sqlite3.Connection, table_name: str) -> int | None:
        if not self._table_exists(connection, table_name):
            return None
        return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])

    def _write_runtime_log(self) -> None:
        connection = sqlite3.connect(self._config.db_path, timeout=self._config.timeout_seconds)
        try:
            stats = {
                "students": self._table_count(connection, "students"),
                "weekly_schedule": self._table_count(connection, "weekly_schedule"),
                "lesson_records": self._table_count(connection, "lesson_records"),
                "lessons": self._table_count(connection, "lessons"),
                "texts": self._table_count(connection, "texts"),
            }
        finally:
            connection.close()

        db_path = self._config.db_path
        lines = [
            f"time={datetime.now().isoformat(timespec='seconds')}",
            f"db_path={db_path.resolve()}",
            f"db_exists={db_path.exists()}",
            f"db_size={db_path.stat().st_size if db_path.exists() else 0}",
            f"schema_path={self._config.schema_path.resolve()}",
            f"schema_exists={self._config.schema_path.exists()}",
            f"bundled_db_path={self._config.bundled_db_path.resolve()}",
            f"bundled_db_exists={self._config.bundled_db_path.exists()}",
            f"students_count={stats['students']}",
            f"weekly_schedule_count={stats['weekly_schedule']}",
            f"lesson_records_count={stats['lesson_records']}",
            f"lessons_count={stats['lessons']}",
            f"texts_count={stats['texts']}",
            "",
        ]
        with self._config.runtime_log_path.open("a", encoding="utf-8") as log_file:
            log_file.write("\n".join(lines))

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
