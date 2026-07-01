"""EPIC S-3 Students professional management UI checks."""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = ROOT / "tests" / ".tmp"
TMP_DB_PATH = TMP_DIR / "epic_s3_students_ui.db"
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

    os.environ["IDIL_DB_PATH"] = str(TMP_DB_PATH)


def _walk_controls(control):
    yield control

    content = getattr(control, "content", None)
    if content is not None:
        yield from _walk_controls(content)

    for child in getattr(control, "controls", []) or []:
        yield from _walk_controls(child)


def _all_text_values(control) -> list[str]:
    return [
        str(getattr(item, "value", ""))
        for item in _walk_controls(control)
        if getattr(item, "value", None) not in (None, "")
    ]


def _seed_students() -> tuple[int, int, int]:
    from controllers import build_course_controller, build_student_controller

    student_controller = build_student_controller()
    course_controller = build_course_controller()

    active_id = student_controller.create_student(
        {
            "ad_soyad": "S3 Active Student",
            "sinif": "5-A",
            "telefon": "05551234567",
            "baslangic_tarihi": "2026-06-30",
            "durum": "Aktif",
        }
    )
    passive_id = student_controller.create_student(
        {
            "ad_soyad": "S3 Passive Student",
            "sinif": "6-B",
            "telefon": "05557654321",
            "baslangic_tarihi": "2026-06-30",
            "durum": "Beklemede",
        }
    )
    completed_id = student_controller.create_student(
        {
            "ad_soyad": "S3 Completed Student",
            "sinif": "7-C",
            "telefon": "05550000000",
            "baslangic_tarihi": "2026-06-30",
            "durum": "Aktif",
        }
    )

    course_controller.assign_course_to_student(active_id, 3)
    course_controller.assign_course_to_student(passive_id, 4)
    completed_course = course_controller.assign_course_to_student(completed_id, 5)
    with sqlite3.connect(TMP_DB_PATH) as conn:
        conn.execute(
            "UPDATE courses SET durum = ? WHERE id = ?",
            ("Tamamlandi", completed_course["id"]),
        )
        conn.commit()

    return active_id, passive_id, completed_id


def test_real_sqlite_list_renders() -> bool:
    from views.pages.students_v3 import build_students_v3_page

    page = build_students_v3_page()
    values = _all_text_values(page)

    assert "Student Management List" in values
    assert "S3 Active Student" in values
    assert "S3 Passive Student" in values
    assert "S3 Completed Student" in values
    assert "Kur 3" in values
    return True


def test_search_and_filters_use_sqlite_rows() -> bool:
    from controllers import build_course_controller, build_student_controller
    from views.pages.students_v3 import STATUS_ACTIVE, STATUS_COMPLETED, STATUS_PASSIVE, students_v3_filter_students

    students = build_student_controller().list_students(limit=1000, offset=0)
    courses = build_course_controller().list_courses(limit=1000, offset=0)

    assert len(students_v3_filter_students(students, courses, "Active", "Tumu")) == 1
    assert len(students_v3_filter_students(students, courses, "Kur 4", "Tumu")) == 1
    assert len(students_v3_filter_students(students, courses, "", STATUS_ACTIVE)) == 1
    assert len(students_v3_filter_students(students, courses, "", STATUS_PASSIVE)) == 1
    assert len(students_v3_filter_students(students, courses, "", STATUS_COMPLETED)) == 1
    return True


def test_responsive_profiles() -> bool:
    from views.pages.students_v3 import students_v3_responsive_profile

    assert students_v3_responsive_profile(1366) == "1366x768"
    assert students_v3_responsive_profile(1600) == "1600x900"
    assert students_v3_responsive_profile(1920) == "1920x1080"
    return True


def test_crud_sqlite_refresh_path() -> bool:
    from controllers import build_student_controller

    controller = build_student_controller()
    student_id = controller.create_student(
        {
            "ad_soyad": "S3 CRUD Student",
            "sinif": "8-D",
            "telefon": "05559998877",
            "baslangic_tarihi": "2026-06-30",
            "durum": "Aktif",
        }
    )
    assert student_id > 0
    assert controller.get_student(student_id)["ad_soyad"] == "S3 CRUD Student"

    updated = {
        "ad_soyad": "S3 CRUD Student Updated",
        "sinif": "8-D",
        "telefon": "05559998877",
        "baslangic_tarihi": "2026-06-30",
        "durum": "Aktif",
    }
    assert controller.update_student(student_id, updated) is True
    assert controller.get_student(student_id)["ad_soyad"] == "S3 CRUD Student Updated"

    assert controller.delete_student(student_id) is True
    assert controller.get_student(student_id) is None
    return True


def run_all() -> None:
    _prepare_database()
    _seed_students()

    checks = [
        ("Real SQLite Student List Test", test_real_sqlite_list_renders),
        ("Search + Filter Test", test_search_and_filters_use_sqlite_rows),
        ("Responsive 1366/1600/1920 Test", test_responsive_profiles),
        ("CRUD SQLite Refresh Path Test", test_crud_sqlite_refresh_path),
    ]

    for name, check in checks:
        print(f"{name}: {check()}")


if __name__ == "__main__":
    run_all()
