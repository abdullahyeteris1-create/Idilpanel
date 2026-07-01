"""Student service skeleton for student domain operations."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from typing import Any

from repositories.student_repository import StudentRepository

from .base_service import BaseService


class StudentService(BaseService):
    """Service entry point for student-related operations."""

    _FULL_NAME_FIELDS = ("full_name", "ad_soyad", "name")
    _FIRST_NAME_FIELDS = ("first_name", "ad")
    _LAST_NAME_FIELDS = ("last_name", "soyad")
    _CLASS_FIELDS = ("class_name", "class", "sinif")
    _START_DATE_FIELDS = ("start_date", "baslangic_tarihi")
    _END_DATE_FIELDS = ("end_date", "bitis_tarihi")
    _PARENT_NAME_FIELDS = ("parent_name", "veli_adi")
    _PHONE_FIELDS = ("phone", "telefon")
    _EMAIL_FIELDS = ("email", "eposta")
    _USERNAME_FIELDS = ("username", "kullanici_adi")
    _PASSWORD_FIELDS = ("password", "sifre")
    _STATUS_FIELDS = ("status", "durum")
    _NOTES_FIELDS = ("notes", "notlar")

    def __init__(
        self,
        student_repository: StudentRepository | None = None,
        repositories: dict[str, Any] | None = None,
    ) -> None:
        merged_repositories = dict(repositories or {})
        if student_repository is not None:
            merged_repositories["student"] = student_repository
        super().__init__(merged_repositories)

    def create_student(self, data):
        validated_data = self.validate_student(data)
        repository_payload = self._to_repository_payload(validated_data)
        return self.get_repository("student").create(repository_payload)

    def get_student(self, record_id):
        self.validate_student()
        return self.get_repository("student").get_by_id(record_id)

    def list_students(self, limit: int = 100, offset: int = 0):
        self.validate_student()
        return self.get_repository("student").list_all(limit, offset)

    def list_active_students(self, limit: int = 100, offset: int = 0):
        self.validate_student()
        repository = self.get_repository("student")
        if hasattr(repository, "list_active"):
            return repository.list_active(limit, offset)
        return [
            record
            for record in repository.list_all(limit, offset)
            if int(record.get("is_active", 1) or 0) == 1
            and not record.get("deleted_at")
            and str(record.get("durum") or "").strip() == "Aktif"
        ]

    def update_student(self, record_id, data):
        validated_data = self.validate_student(data)
        repository_payload = self._to_repository_payload(validated_data)
        return self.get_repository("student").update(record_id, repository_payload)

    def delete_student(self, record_id):
        self.validate_student()
        return self.get_repository("student").delete(record_id)

    def validate_student(self, data: Mapping[str, Any] | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("student data must be a mapping")

        full_name = self._get_field_value(data, self._FULL_NAME_FIELDS)
        first_name = self._get_field_value(data, self._FIRST_NAME_FIELDS)
        last_name = self._get_field_value(data, self._LAST_NAME_FIELDS)

        if full_name is not None:
            if not full_name:
                raise ValueError("student name cannot be empty")
        else:
            if first_name is None or last_name is None:
                raise ValueError("student name cannot be empty")
            if not first_name:
                raise ValueError("student first name cannot be empty")
            if not last_name:
                raise ValueError("student last name cannot be empty")

        class_value = self._get_field_value(data, self._CLASS_FIELDS)
        if class_value is None or not class_value:
            raise ValueError("student class information cannot be empty")

        start_date_value = self._get_field_value(data, self._START_DATE_FIELDS)
        if start_date_value is None or not start_date_value:
            raise ValueError("student start date cannot be empty")

        start_date = self._parse_date(start_date_value)

        end_date_value = self._get_field_value(data, self._END_DATE_FIELDS)
        if end_date_value:
            end_date = self._parse_date(end_date_value, "student end date must be a valid date")
            if end_date < start_date:
                raise ValueError("student end date cannot be before start date")

        email_value = self._get_field_value(data, self._EMAIL_FIELDS)
        if email_value and "@" not in email_value:
            raise ValueError("student email must be valid")

        status_value = self._get_field_value(data, self._STATUS_FIELDS)
        if status_value and status_value not in {"Aktif", "Beklemede"}:
            raise ValueError("student status must be Aktif or Beklemede")

        return data

    def _get_field_value(self, data: Mapping[str, Any], field_names: tuple[str, ...]) -> str | None:
        for field_name in field_names:
            if field_name in data:
                value = data[field_name]
                if value is None:
                    return ""

                text = str(value).strip()
                return text
        return None

    def _parse_date(self, value: Any, error_message: str = "student start date must be a valid date") -> date:
        if isinstance(value, date):
            return value

        if isinstance(value, datetime):
            return value.date()

        if not isinstance(value, str):
            raise ValueError(error_message)

        cleaned_value = value.strip()
        try:
            return date.fromisoformat(cleaned_value)
        except ValueError as first_error:
            try:
                return datetime.fromisoformat(cleaned_value).date()
            except ValueError as second_error:
                raise ValueError(error_message) from second_error

    def _to_repository_payload(self, data: Mapping[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {}

        full_name = self._get_field_value(data, self._FULL_NAME_FIELDS)
        if full_name is not None:
            payload["ad_soyad"] = full_name

        class_value = self._get_field_value(data, self._CLASS_FIELDS)
        if class_value is not None:
            payload["sinif"] = class_value

        start_date_value = self._get_field_value(data, self._START_DATE_FIELDS)
        if start_date_value is not None:
            payload["baslangic_tarihi"] = start_date_value

        parent_name_value = self._get_field_value(data, self._PARENT_NAME_FIELDS)
        if parent_name_value is not None:
            payload["veli_adi"] = parent_name_value

        phone_value = self._get_field_value(data, self._PHONE_FIELDS)
        if phone_value is not None:
            payload["telefon"] = phone_value

        email_value = self._get_field_value(data, self._EMAIL_FIELDS)
        if email_value is not None:
            payload["email"] = email_value
            payload["eposta"] = email_value

        username_value = self._get_field_value(data, self._USERNAME_FIELDS)
        if username_value is not None:
            payload["kullanici_adi"] = username_value

        password_value = self._get_field_value(data, self._PASSWORD_FIELDS)
        if password_value is not None:
            payload["sifre"] = password_value

        end_date_value = self._get_field_value(data, self._END_DATE_FIELDS)
        if end_date_value is not None:
            payload["bitis_tarihi"] = end_date_value

        status_value = self._get_field_value(data, self._STATUS_FIELDS)
        if status_value is not None:
            payload["durum"] = status_value

        notes_value = self._get_field_value(data, self._NOTES_FIELDS)
        if notes_value is not None:
            payload["notlar"] = notes_value

        return payload
