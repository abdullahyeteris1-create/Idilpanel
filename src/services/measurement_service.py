"""Measurement service skeleton for measurement domain operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from repositories.measurement_repository import MeasurementRepository

from .base_service import BaseService


class MeasurementService(BaseService):
    """Service entry point for measurement-related operations."""

    def __init__(
        self,
        measurement_repository: MeasurementRepository | None = None,
        repositories: dict[str, Any] | None = None,
    ) -> None:
        merged_repositories = dict(repositories or {})
        if measurement_repository is not None:
            merged_repositories["measurement"] = measurement_repository
        super().__init__(merged_repositories)

    def create_measurement(self, data):
        validated_data = self.validate_measurement(data)
        return self.get_repository("measurement").create(validated_data)

    def get_measurement(self, record_id):
        return self.get_repository("measurement").get_by_id(record_id)

    def list_measurements(self, limit: int = 100, offset: int = 0):
        return self.get_repository("measurement").list_all(limit, offset)

    def update_measurement(self, record_id, data):
        validated_data = self.validate_measurement(data)
        return self.get_repository("measurement").update(record_id, validated_data)

    def delete_measurement(self, record_id):
        return self.get_repository("measurement").delete(record_id)

    def validate_measurement(self, data: Any | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("measurement data must be a mapping")

        return data
