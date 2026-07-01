"""Controller for text library UI operations."""

from __future__ import annotations

from services.text_service import TextService


class TextController:
    """Bridge UI requests to TextService."""

    def __init__(self, text_service: TextService) -> None:
        self._text_service = text_service

    def create_text(self, data):
        return self._text_service.create_text(data)

    def get_text(self, record_id):
        return self._text_service.get_text(record_id)

    def list_texts(self, limit: int = 500, offset: int = 0):
        return self._text_service.list_texts(limit, offset)

    def search_texts(self, query: str = "", course_level: int | None = None, limit: int = 500, offset: int = 0):
        return self._text_service.search_texts(query=query, course_level=course_level, limit=limit, offset=offset)

    def update_text(self, record_id, data):
        return self._text_service.update_text(record_id, data)

    def delete_text(self, record_id):
        return self._text_service.delete_text(record_id)

    def import_texts_from_xlsx(self, file_path: str):
        return self._text_service.import_texts_from_xlsx(file_path)

    def export_texts_xlsx_bytes(self) -> bytes:
        return self._text_service.export_texts_xlsx_bytes()
