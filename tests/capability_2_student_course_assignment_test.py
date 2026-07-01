"""Capability 2.0 test: Student Course Assignment.

Checks:
- Student can be assigned to a course (Kur)
- Same course cannot be assigned twice
- SQLite relation is persisted
- Passive-course selection validation path is blocked
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = ROOT / "tests" / ".tmp"
TMP_DB_PATH = TMP_DIR / "capability_2_assignment.db"
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


def run_capability_2_assignment_test() -> None:
    _prepare_database()
    os.environ["IDIL_DB_PATH"] = str(TMP_DB_PATH)

    from controllers import build_course_controller, build_student_controller
    from views.pages.students_v2 import students_v2_active_course_label, students_v2_validate_course_assignment

    student_controller = build_student_controller()
    course_controller = build_course_controller()

    student_id = student_controller.create_student(
        {
            "ad_soyad": "Capability Test Ogrenci",
            "sinif": "5-A",
            "veli_adi": "Test Veli",
            "telefon": "05551234567",
            "email": "cap2@example.com",
            "kullanici_adi": "cap2_user",
            "sifre": "1234",
            "baslangic_tarihi": "2026-06-30",
            "durum": "Aktif",
            "notlar": "Kur: 1",
        }
    )
    assert isinstance(student_id, int) and student_id > 0

    valid, msg = students_v2_validate_course_assignment(student_id, "Kur 3", [])
    assert valid is True and msg == ""

    assignment_payload = {
        "student_id": student_id,
        "course_name": f"Ogrenci {student_id} Kur 3",
        "kur_no": 3,
        "baslangic": "2026-06-30",
        "bitis": "",
        "total_lessons": 16,
        "durum": "Aktif",
    }
    course_id = course_controller.create_course(assignment_payload)
    assert isinstance(course_id, int) and course_id > 0

    courses = course_controller.list_courses(limit=200, offset=0)
    active_label = students_v2_active_course_label(student_id, courses)
    assert active_label == "Kur 3"

    with sqlite3.connect(TMP_DB_PATH) as conn:
        row = conn.execute(
            "SELECT student_id, kur_no, durum FROM courses WHERE id = ?",
            (course_id,),
        ).fetchone()
    assert row is not None
    assert int(row[0]) == int(student_id)
    assert int(row[1]) == 3
    assert str(row[2]) == "Aktif"

    valid_dup, msg_dup = students_v2_validate_course_assignment(student_id, "Kur 3", courses)
    assert valid_dup is False
    assert msg_dup == "Ayni kurs ikinci kez atanamaz."

    passive_courses = [dict(item) for item in courses]
    passive_courses[0]["durum"] = "Beklemede"
    valid_passive, msg_passive = students_v2_validate_course_assignment(student_id, "Kur 3", passive_courses)
    assert valid_passive is False
    assert msg_passive == "Pasif kurs secilemez."

    print("CAPABILITY_2_ASSIGNMENT_TEST_OK", True)


if __name__ == "__main__":
    run_capability_2_assignment_test()
