"""Courses V2 Sprint-3 real CRUD test."""
import sys, os, sqlite3
sys.path.insert(0, "src")

TMP_DB = "tests/.tmp/courses3_crud_test.db"
os.makedirs("tests/.tmp", exist_ok=True)
if os.path.exists(TMP_DB):
    os.unlink(TMP_DB)

schema_sql = open("database/schema.sql", encoding="utf-8").read()
with sqlite3.connect(TMP_DB) as conn:
    conn.executescript(schema_sql)
os.environ["IDIL_DB_PATH"] = TMP_DB

# Seed a student so FK is satisfied
with sqlite3.connect(TMP_DB) as conn:
    conn.execute(
        "INSERT INTO students (ad_soyad, baslangic_tarihi, durum) VALUES (?, ?, ?)",
        ("Test Ogrenci", "2026-01-01", "Aktif"),
    )
    student_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

from controllers import build_course_controller

ctrl = build_course_controller()

# CREATE
cid = ctrl.create_course({
    "course_name": f"Ogrenci {student_id} Kur 3",
    "student_id": student_id,
    "kur_no": 3,
    "baslangic": "2026-06-30",
    "total_lessons": 16,
    "durum": "Aktif",
})
assert isinstance(cid, int) and cid > 0, "create fail"
print(f"CREATE: OK – id={cid}")

# READ
record = ctrl.get_course(cid)
assert record is not None, "get fail"
assert int(record["kur_no"]) == 3
assert int(record["student_id"]) == student_id
print(f"READ: OK – kur_no={record['kur_no']} student_id={record['student_id']}")

# LIST
courses = ctrl.list_courses(limit=100, offset=0)
assert any(int(c["id"]) == cid for c in courses), "list fail"
print(f"LIST: OK – {len(courses)} record(s)")

# UPDATE
ctrl.update_course(cid, {
    "course_name": f"Ogrenci {student_id} Kur 3",
    "student_id": student_id,
    "kur_no": 3,
    "baslangic": "2026-06-30",
    "total_lessons": 16,
    "durum": "Beklemede",
})
updated = ctrl.get_course(cid)
assert updated["durum"] == "Beklemede", "update fail"
print(f"UPDATE: OK – durum={updated['durum']}")

# DELETE
result = ctrl.delete_course(cid)
assert result is True, "delete fail"
deleted = ctrl.get_course(cid)
assert deleted is None, "delete verify fail"
print("DELETE: OK – record gone")

# SQLite direct verify
with sqlite3.connect(TMP_DB) as conn:
    row = conn.execute("SELECT id FROM courses WHERE id=?", (cid,)).fetchone()
    assert row is None, "SQLite verify fail"
print("SQLite verify: OK")

print("COURSES3_CRUD_TEST: ALL PASSED")
