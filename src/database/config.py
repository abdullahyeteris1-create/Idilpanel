"""Database configuration primitives for SQLite foundation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatabaseConfig:
    """Resolve DB file path from config with safe project defaults."""

    db_path: Path
    timeout_seconds: float = 5.0

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        project_root = Path(__file__).resolve().parents[2]
        default_path = project_root / "database" / "idilpanel.db"
        configured_path = os.getenv("IDIL_DB_PATH")

        db_path = Path(configured_path).expanduser() if configured_path else default_path
        return cls(db_path=db_path)
