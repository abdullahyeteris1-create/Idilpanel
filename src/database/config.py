"""Database configuration primitives for SQLite foundation."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path


APP_DATA_DIR_NAME = "IDIL_HIZLI_OKUMA"


@dataclass(frozen=True)
class DatabaseConfig:
    """Resolve DB file path from config with safe project defaults."""

    db_path: Path
    resource_root: Path = field(default_factory=lambda: DatabaseConfig._resource_root())
    timeout_seconds: float = 5.0

    @property
    def schema_path(self) -> Path:
        return self.resource_root / "database" / "schema.sql"

    @property
    def bundled_db_path(self) -> Path:
        return self.resource_root / "database" / "idilpanel.db"

    @property
    def migrations_dir(self) -> Path:
        return self.resource_root / "database" / "migrations"

    @property
    def runtime_log_path(self) -> Path:
        return self.db_path.parent / "db_runtime.log"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        resource_root = cls._resource_root()
        configured_path = os.getenv("IDIL_DB_PATH")

        if configured_path:
            db_path = Path(configured_path).expanduser()
        elif cls._is_frozen():
            local_app_data = Path(os.getenv("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
            db_path = local_app_data / APP_DATA_DIR_NAME / "idilpanel.db"
        else:
            db_path = resource_root / "database" / "idilpanel.db"

        return cls(db_path=db_path, resource_root=resource_root)

    @staticmethod
    def _is_frozen() -> bool:
        return bool(getattr(sys, "frozen", False))

    @classmethod
    def _resource_root(cls) -> Path:
        if cls._is_frozen():
            return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
        return Path(__file__).resolve().parents[2]
