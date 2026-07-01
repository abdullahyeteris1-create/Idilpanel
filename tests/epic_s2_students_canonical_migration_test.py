"""EPIC S-2 Students canonical migration checks.

Validates that /students is the canonical Students V3 route while legacy
Students pages remain present but inactive.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = ROOT / "tests" / ".tmp"
TMP_DB_PATH = TMP_DIR / "epic_s2_students_canonical.db"
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


def test_router_uses_students_v3() -> bool:
    from views.pages.students_v3 import build_students_v3_page
    from views.router import ROUTE_REGISTRY, resolve_route

    assert resolve_route("/students") == "/students"
    assert ROUTE_REGISTRY["/students"]["builder"] is build_students_v3_page
    assert "/students-v2" not in ROUTE_REGISTRY
    assert "/students-v3" not in ROUTE_REGISTRY
    return True


def test_sidebar_students_navigation() -> bool:
    from views.sidebar import build_sidebar

    captured_routes: list[str] = []
    sidebar = build_sidebar(
        active_route="/students",
        on_navigate=lambda route: captured_routes.append(route),
        compact=False,
    )

    student_items = []
    for control in _walk_controls(sidebar):
        content = getattr(control, "content", None)
        if getattr(control, "on_click", None) is None or content is None:
            continue
        labels = [
            getattr(item, "value", "")
            for item in _walk_controls(content)
            if getattr(item, "value", "") == "Ogrenciler"
        ]
        if labels:
            student_items.append(control)

    assert len(student_items) == 1
    assert student_items[0].on_click is not None
    student_items[0].on_click(None)
    assert captured_routes == ["/students"]
    return True


def test_students_navigation_builds_canonical_page() -> bool:
    import flet as ft
    from views.router import build_route_content

    content = build_route_content("/students")
    assert isinstance(content, ft.Container)
    assert getattr(content, "expand", None) is True
    return True


def test_legacy_pages_are_marked() -> bool:
    from views.pages import students, students_v2

    assert students.IS_LEGACY_STUDENTS_PAGE is True
    assert students_v2.IS_LEGACY_STUDENTS_PAGE is True
    assert students.CANONICAL_STUDENTS_MODULE == "views.pages.students_v3"
    assert students_v2.CANONICAL_STUDENTS_MODULE == "views.pages.students_v3"
    return True


def test_student_crud_sqlite_path() -> bool:
    from controllers import build_student_controller

    controller = build_student_controller()
    payload = {
        "ad_soyad": "EPIC S2 Student",
        "sinif": "5-A",
        "veli_adi": "EPIC S2 Parent",
        "telefon": "05551234567",
        "email": "epic-s2@example.com",
        "kullanici_adi": "epic_s2_user",
        "sifre": "test-pass",
        "baslangic_tarihi": date.today().isoformat(),
        "durum": "Aktif",
        "notlar": "Canonical migration CRUD check",
    }

    student_id = controller.create_student(payload)
    assert isinstance(student_id, int) and student_id > 0

    created = controller.get_student(student_id)
    assert created is not None
    assert created["ad_soyad"] == "EPIC S2 Student"

    updated_payload = dict(payload)
    updated_payload["ad_soyad"] = "EPIC S2 Student Updated"
    assert controller.update_student(student_id, updated_payload) is True
    updated = controller.get_student(student_id)
    assert updated is not None
    assert updated["ad_soyad"] == "EPIC S2 Student Updated"

    listed = controller.list_students(limit=100, offset=0)
    assert any(int(row["id"]) == student_id for row in listed)

    assert controller.delete_student(student_id) is True
    assert controller.get_student(student_id) is None
    return True


def run_all() -> None:
    _prepare_database()

    checks = [
        ("Router Test", test_router_uses_students_v3),
        ("Sidebar Test", test_sidebar_students_navigation),
        ("Students Navigation Test", test_students_navigation_builds_canonical_page),
        ("Legacy Marker Test", test_legacy_pages_are_marked),
        ("CRUD + SQLite Test", test_student_crud_sqlite_path),
    ]

    for name, check in checks:
        result = check()
        print(f"{name}: {result}")


if __name__ == "__main__":
    run_all()
