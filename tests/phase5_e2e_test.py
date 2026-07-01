"""FAZ 5 end-to-end chain test.

Flow:
new screen -> controller -> service -> repository -> SQLite -> E2E assertions
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = ROOT / "tests" / ".tmp"
TMP_DB_PATH = TMP_DIR / "phase5_e2e.db"
SCHEMA_PATH = ROOT / "database" / "schema.sql"

if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


def _prepare_database() -> None:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    if TMP_DB_PATH.exists():
        TMP_DB_PATH.unlink()

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with sqlite3.connect(TMP_DB_PATH) as conn:
        conn.executescript(schema_sql)


def _build_chain():
    # Set env before project imports that may read DB config defaults.
    os.environ["IDIL_DB_PATH"] = str(TMP_DB_PATH)

    from database.config import DatabaseConfig
    from database.connection_manager import SQLiteConnectionManager
    from controllers.course_controller import CourseController
    from controllers.lesson_controller import LessonController
    from controllers.student_controller import StudentController
    from repositories.course_repository import CourseRepository
    from repositories.lesson_repository import LessonRepository
    from repositories.student_repository import StudentRepository
    from services.course_service import CourseService
    from services.lesson_service import LessonService
    from services.student_service import StudentService

    manager = SQLiteConnectionManager(config=DatabaseConfig(db_path=TMP_DB_PATH))

    student_repo = StudentRepository(connection_manager=manager)
    course_repo = CourseRepository(connection_manager=manager)
    lesson_repo = LessonRepository(connection_manager=manager)

    student_service = StudentService(student_repository=student_repo)
    course_service = CourseService(course_repository=course_repo)
    lesson_service = LessonService(
        lesson_repository=lesson_repo,
        student_repository=student_repo,
        course_repository=course_repo,
    )

    return (
        manager,
        StudentController(student_service=student_service),
        CourseController(course_service=course_service),
        LessonController(lesson_service=lesson_service),
    )


def run_phase5_e2e() -> None:
    _prepare_database()

    # New screen smoke: ensure v2 screen can be constructed.
    from views.pages_v2.lesson_records_page_v2 import build_lesson_records_page_v2

    screen = build_lesson_records_page_v2()
    assert screen is not None

    manager, student_controller, course_controller, lesson_controller = _build_chain()

    student_id = student_controller.create_student(
        {
            "ad_soyad": "Faz Bes Ogrenci",
            "sinif": "5-A",
            "baslangic_tarihi": "2026-06-30",
            "veli_adi": "Veli Test",
            "telefon": "5551112233",
            "email": "faz5@example.com",
            "kullanici_adi": "faz5_user",
            "sifre": "1234",
            "durum": "Aktif",
            "notlar": "E2E seed",
        }
    )
    assert isinstance(student_id, int) and student_id > 0

    course_id = course_controller.create_course(
        {
            "course_name": "Kur Programi",
            "student_id": student_id,
            "kur_no": 1,
            "baslangic": "2026-06-30",
            "bitis": "2026-07-30",
            "durum": "Aktif",
            "total_lessons": 16,
        }
    )
    assert isinstance(course_id, int) and course_id > 0

    lesson_payload = {
        "student_id": student_id,
        "course_id": course_id,
        "lesson_no": 1,
        "tarih": "2026-06-30",
        "metin": "Deneme metni",
        "word_count": 120,
        "duration": 10,
        "comprehension": 80,
        "durum": "Planlandi",
    }

    lesson_id = lesson_controller.create_lesson(lesson_payload)
    assert isinstance(lesson_id, int) and lesson_id > 0

    lesson_row = lesson_controller.get_lesson(lesson_id)
    assert lesson_row is not None
    assert int(lesson_row["course_id"]) == course_id
    assert int(lesson_row["lesson_no"]) == 1

    listed = lesson_controller.list_lessons(limit=50, offset=0)
    assert any(int(row.get("id", 0)) == lesson_id for row in listed)

    updated = lesson_controller.update_lesson(
        lesson_id,
        {
            "student_id": student_id,
            "course_id": course_id,
            "lesson_no": 1,
            "tarih": "2026-06-30",
            "metin": "Guncellenmis metin",
            "word_count": 150,
            "duration": 12,
            "comprehension": 88,
            "durum": "Tamamlandi",
        },
    )
    assert updated is True

    after_update = lesson_controller.get_lesson(lesson_id)
    assert after_update is not None
    assert str(after_update.get("durum")) == "Tamamlandi"

    # SQLite-level verification.
    with manager.connection_scope() as connection:
        count = int(
            connection.execute(
                "SELECT COUNT(*) AS cnt FROM lessons WHERE id = ?",
                (lesson_id,),
            ).fetchone()["cnt"]
        )
    assert count == 1

    deleted = lesson_controller.delete_lesson(lesson_id)
    assert deleted is True

    with manager.connection_scope() as connection:
        remaining = int(
            connection.execute(
                "SELECT COUNT(*) AS cnt FROM lessons WHERE id = ?",
                (lesson_id,),
            ).fetchone()["cnt"]
        )
    assert remaining == 0

    print("PHASE5-E2E: PASS")


if __name__ == "__main__":
    run_phase5_e2e()
