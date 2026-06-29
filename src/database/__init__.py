"""Database foundation package for shared SQLite infrastructure."""

from .config import DatabaseConfig
from .connection_manager import SQLiteConnectionManager, db_manager

__all__ = ["DatabaseConfig", "SQLiteConnectionManager", "db_manager"]
