"""Base service infrastructure for service-layer implementations."""

from __future__ import annotations

from typing import Any


class BaseService:
    """Provide shared service-layer dependency management helpers."""

    def __init__(self, repositories: dict[str, Any] | None = None) -> None:
        self._repositories: dict[str, Any] = dict(repositories or {})

    def register_repository(self, name: str, repository: Any) -> None:
        if not name:
            raise ValueError("name must not be empty")

        self._repositories[name] = repository

    def get_repository(self, name: str, default: Any | None = None) -> Any:
        repository = self._repositories.get(name, default)
        if repository is None:
            raise LookupError(f"Repository not registered: {name}")
        return repository

    def has_repository(self, name: str) -> bool:
        return name in self._repositories
