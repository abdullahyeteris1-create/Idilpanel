"""Measurement controller skeleton for UI-to-service request orchestration."""

from __future__ import annotations

from services.measurement_service import MeasurementService


class MeasurementController:
    """Bridge UI requests to MeasurementService without business logic."""

    def __init__(self, measurement_service: MeasurementService) -> None:
        self._measurement_service = measurement_service

    def create_measurement(self, data):
        return self._measurement_service.create_measurement(data)

    def get_measurement(self, record_id):
        return self._measurement_service.get_measurement(record_id)

    def list_measurements(self, limit: int = 100, offset: int = 0):
        return self._measurement_service.list_measurements(limit, offset)

    def update_measurement(self, record_id, data):
        return self._measurement_service.update_measurement(record_id, data)

    def delete_measurement(self, record_id):
        return self._measurement_service.delete_measurement(record_id)
