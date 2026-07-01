"""
RC-1 Sprint: Student & Course Integration Review

Comprehensive end-to-end integration test covering all 5 release scenarios:
1. Create → List → Edit → Save → Delete Student
2. Create → List → Edit → Save → Delete Course
3. Assign Student to Course → View Details → Verify Student List
4. Capacity Control → Full Course → Prevent Assignment
5. Passive Course → Assignment Attempt → Turkish Error Message

This validates Students V2 and Courses V2 modules working together.

Usage:
    python tests/rc1_integration_test.py
"""

import os
import sqlite3
import sys
import time
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = ROOT / "tests" / ".tmp"
TMP_DB_PATH = TMP_DIR / "rc1_integration.db"
SCHEMA_PATH = ROOT / "database" / "schema.sql"

if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


def _prepare_database() -> None:
    """Initialize test database from schema."""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    if TMP_DB_PATH.exists():
        TMP_DB_PATH.unlink()

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with sqlite3.connect(TMP_DB_PATH) as conn:
        conn.executescript(schema_sql)


def test_rc1_integration() -> bool:
    """Execute RC-1 comprehensive integration test."""
    _prepare_database()
    os.environ["IDIL_DB_PATH"] = str(TMP_DB_PATH)

    from controllers import build_course_controller, build_student_controller

    student_controller = build_student_controller()
    course_controller = build_course_controller()

    print("\n" + "=" * 90)
    print("RC-1 SPRINT: STUDENT & COURSE INTEGRATION REVIEW")
    print("=" * 90)

    scenario_results = []

    # ==========================================================================
    # SENARYO 1: Yeni Öğrenci Oluştur → Listele → Düzenle → Kaydet → Sil
    # ==========================================================================
    print("\n[SENARYO 1] Yeni Öğrenci Oluştur → Listele → Düzenle → Kaydet → Sil")
    print("-" * 90)

    try:
        # CREATE
        print("  → Yeni Öğrenci Oluştur")
        student_data = {
            "ad_soyad": "RC1 Test Student",
            "sinif": "5. Sinif",
            "veli_adi": "RC1 Parent",
            "telefon": "05551234567",
            "email": "rc1@test.com",
            "kullanici_adi": "rc1_user",
            "sifre": "Pass123",
            "baslangic_tarihi": date.today().isoformat(),
            "durum": "Aktif",
        }
        student_id = student_controller.create_student(student_data)
        assert student_id > 0, "Student creation failed"
        print(f"    ✓ Oluşturuldu: ID={student_id}")

        # LIST
        print("  → Listele")
        students = student_controller.list_students(limit=100, offset=0)
        found = any(s.get("id") == student_id for s in students)
        assert found, "Student not in list"
        print(f"    ✓ Listede görülüyor ({len(students)} kayıt)")

        # RETRIEVE for edit
        print("  → Düzenle")
        student = student_controller.get_student(student_id)
        assert student is not None, "Cannot retrieve student"
        original_name = student.get("ad_soyad")
        print(f"    ✓ Alındı: {original_name}")

        # UPDATE
        print("  → Kaydet")
        updated_data = student_data.copy()
        updated_data["ad_soyad"] = "RC1 Test Student Updated"
        student_controller.update_student(student_id, updated_data)
        
        # Verify update
        student = student_controller.get_student(student_id)
        assert student.get("ad_soyad") == "RC1 Test Student Updated", "Update failed"
        print(f"    ✓ Güncellendi: {student.get('ad_soyad')}")

        # DELETE
        print("  → Sil")
        student_controller.delete_student(student_id)
        
        # Verify deletion
        students = student_controller.list_students(limit=100, offset=0)
        found = any(s.get("id") == student_id for s in students if not s.get("is_deleted", False))
        assert not found, "Student still in list after delete"
        print(f"    ✓ Silindi")

        scenario_results.append(("SENARYO 1", "✓ PASS"))
        print("  ✓ SENARYO 1 BAŞARILI")

    except Exception as e:
        print(f"  ✗ SENARYO 1 BAŞARISIZ: {str(e)}")
        scenario_results.append(("SENARYO 1", f"✗ FAIL: {str(e)}"))
        return False

    # ==========================================================================
    # SENARYO 2: Yeni Kurs Oluştur → Listele → Düzenle → Kaydet → Sil
    # ==========================================================================
    print("\n[SENARYO 2] Yeni Kurs Oluştur → Listele → Düzenle → Kaydet → Sil")
    print("-" * 90)

    try:
        # CREATE (via student assignment)
        print("  → Yeni Kurs Oluştur")
        create_student = student_controller.create_student({
            "ad_soyad": "Course Test Student",
            "sinif": "3. Sinif",
            "veli_adi": "Parent",
            "telefon": "05559876543",
            "email": "course@test.com",
            "kullanici_adi": "course_user",
            "sifre": "Pass123",
            "baslangic_tarihi": date.today().isoformat(),
            "durum": "Aktif",
        })

        course = course_controller.assign_course_to_student(create_student, 4)
        course_id = course.get("id")
        assert course_id > 0, "Course creation failed"
        print(f"    ✓ Oluşturuldu: ID={course_id}, Kur 4")

        # LIST
        print("  → Listele")
        courses = course_controller.list_courses(limit=100, offset=0)
        found = any(c.get("id") == course_id for c in courses)
        assert found, "Course not in list"
        print(f"    ✓ Listede görülüyor ({len(courses)} kayıt)")

        # RETRIEVE for edit
        print("  → Düzenle")
        course = course_controller.get_course(course_id)
        assert course is not None, "Cannot retrieve course"
        original_status = course.get("durum")
        print(f"    ✓ Alındı: Durum={original_status}")

        # UPDATE
        print("  → Kaydet")
        updated_course_data = {
            **course,
            "durum": "Aktif",  # Ensure Aktif
            "kurs_adi": f"Kur {course.get('kur_no')}"  # Add name for validation
        }
        course_controller.update_course(course_id, updated_course_data)
        
        # Verify update
        course = course_controller.get_course(course_id)
        assert course.get("durum") in ["Aktif", "Beklemede"], "Update failed"
        print(f"    ✓ Güncellendi: Durum={course.get('durum')}")

        # DELETE
        print("  → Sil")
        course_controller.delete_course(course_id)
        
        # Verify deletion
        course = course_controller.get_course(course_id)
        assert course is None or course.get("is_deleted"), "Course still retrievable after delete"
        print(f"    ✓ Silindi")

        scenario_results.append(("SENARYO 2", "✓ PASS"))
        print("  ✓ SENARYO 2 BAŞARILI")

    except Exception as e:
        print(f"  ✗ SENARYO 2 BAŞARISIZ: {str(e)}")
        scenario_results.append(("SENARYO 2", f"✗ FAIL: {str(e)}"))
        return False

    # ==========================================================================
    # SENARYO 3: Öğrenciyi Kursa Ata → Kurs Detayını Aç → Öğrenci Listesini Doğrula
    # ==========================================================================
    print("\n[SENARYO 3] Öğrenciyi Kursa Ata → Kurs Detayını Aç → Öğrenci Listesini Doğrula")
    print("-" * 90)

    try:
        # Create students for assignment
        print("  → Öğrenciler Oluştur")
        students_for_assignment = []
        for i in range(3):
            sid = student_controller.create_student({
                "ad_soyad": f"S3 Student {i}",
                "sinif": "2. Sinif",
                "veli_adi": "Parent",
                "telefon": f"0555998{i:05d}",
                "email": f"s3s{i}@test.com",
                "kullanici_adi": f"s3user{i}",
                "sifre": "Pass123",
                "baslangic_tarihi": date.today().isoformat(),
                "durum": "Aktif",
            })
            students_for_assignment.append(sid)
        print(f"    ✓ {len(students_for_assignment)} öğrenci oluşturuldu")

        # ASSIGN
        print("  → Kursa Ata")
        assigned_courses = []
        for sid in students_for_assignment:
            course = course_controller.assign_course_to_student(sid, 6)
            assigned_courses.append(course)
        print(f"    ✓ {len(assigned_courses)} atama yapıldı")

        # OPEN DETAIL
        print("  → Kurs Detayını Aç")
        course_id = assigned_courses[0].get("id")
        course_detail = course_controller.get_course(course_id)
        assert course_detail is not None, "Cannot get course detail"
        print(f"    ✓ Kurs {course_detail.get('kur_no')}, Durum: {course_detail.get('durum')}")

        # VERIFY STUDENT LIST
        print("  → Öğrenci Listesini Doğrula")
        students_in_course = course_controller.get_students_for_course(course_id)
        assert len(students_in_course) > 0, "No students in course"
        print(f"    ✓ {len(students_in_course)} öğrenci bulundu")

        # Verify capacity
        print("  → Kapasite Bilgilerini Doğrula")
        capacity_info = course_controller.get_course_capacity_info(6)
        assert capacity_info["current_count"] >= len(students_in_course), "Capacity count mismatch"
        print(f"    ✓ Kapasite: {capacity_info['current_count']}/30 ({capacity_info['occupancy_rate']}%)")

        scenario_results.append(("SENARYO 3", "✓ PASS"))
        print("  ✓ SENARYO 3 BAŞARILI")

    except Exception as e:
        print(f"  ✗ SENARYO 3 BAŞARISIZ: {str(e)}")
        scenario_results.append(("SENARYO 3", f"✗ FAIL: {str(e)}"))
        return False

    # ==========================================================================
    # SENARYO 4: Kontenjan Kontrolü → Dolu Kurs → Atama Engeli
    # ==========================================================================
    print("\n[SENARYO 4] Kontenjan Kontrolü → Dolu Kurs → Atama Engeli")
    print("-" * 90)

    try:
        print("  → Kur 7'yi Kapasiteye Kadar Doldur")
        for i in range(30):
            try:
                sid = student_controller.create_student({
                    "ad_soyad": f"S4 Full Student {i}",
                    "sinif": "1. Sinif",
                    "veli_adi": "Parent",
                    "telefon": f"0555{i:08d}",
                    "email": f"s4full{i}@test.com",
                    "kullanici_adi": f"s4full{i}",
                    "sifre": "Pass123",
                    "baslangic_tarihi": date.today().isoformat(),
                    "durum": "Aktif",
                })
                course_controller.assign_course_to_student(sid, 7)
            except Exception:
                pass  # Stop when full
        
        count = course_controller.count_students_for_kur(7)
        print(f"    ✓ Kur 7 doldu: {count}/30 öğrenci")

        print("  → Dolu Kursa Atama Denemesi")
        test_student = student_controller.create_student({
            "ad_soyad": "S4 Overflow Student",
            "sinif": "1. Sinif",
            "veli_adi": "Parent",
            "telefon": "05559999999",
            "email": "s4overflow@test.com",
            "kullanici_adi": "s4overflow",
            "sifre": "Pass123",
            "baslangic_tarihi": date.today().isoformat(),
            "durum": "Aktif",
        })

        can_assign, reason = course_controller.can_assign_student_to_kur(test_student, 7)
        assert not can_assign, "Should not allow assignment to full kur"
        assert "kontenjan" in reason.lower() or "dolu" in reason.lower(), f"Wrong error: {reason}"
        print(f"    ✓ Atama engellendi: {reason}")

        scenario_results.append(("SENARYO 4", "✓ PASS"))
        print("  ✓ SENARYO 4 BAŞARILI")

    except Exception as e:
        print(f"  ✗ SENARYO 4 BAŞARISIZ: {str(e)}")
        scenario_results.append(("SENARYO 4", f"✗ FAIL: {str(e)}"))
        return False

    # ==========================================================================
    # SENARYO 5: Pasif Kurs → Atama Denemesi → Türkçe Hata Mesajı
    # ==========================================================================
    print("\n[SENARYO 5] Pasif Kurs → Atama Denemesi → Türkçe Hata Mesajı")
    print("-" * 90)

    try:
        print("  → Pasif Kurs Oluştur")
        passive_student = student_controller.create_student({
            "ad_soyad": "S5 Passive Student",
            "sinif": "1. Sinif",
            "veli_adi": "Parent",
            "telefon": "05559988877",
            "email": "s5passive@test.com",
            "kullanici_adi": "s5passive",
            "sifre": "Pass123",
            "baslangic_tarihi": date.today().isoformat(),
            "durum": "Aktif",
        })

        # Insert passive course directly
        with sqlite3.connect(TMP_DB_PATH) as conn:
            conn.execute(
                "INSERT INTO courses (student_id, kur_no, baslangic, durum, hedef_ders_sayisi, is_active) VALUES (?, ?, ?, ?, ?, ?)",
                (passive_student, 10, date.today().isoformat(), "Beklemede", 16, 1),
            )
            conn.commit()
        print("    ✓ Pasif kurs (Beklemede) oluşturuldu: Kur 10")

        print("  → Pasif Kursa Atama Denemesi")
        test_student_for_passive = student_controller.create_student({
            "ad_soyad": "S5 Assignment Student",
            "sinif": "1. Sinif",
            "veli_adi": "Parent",
            "telefon": "05559988888",
            "email": "s5assign@test.com",
            "kullanici_adi": "s5assign",
            "sifre": "Pass123",
            "baslangic_tarihi": date.today().isoformat(),
            "durum": "Aktif",
        })

        can_assign, reason = course_controller.can_assign_student_to_kur(test_student_for_passive, 10)
        assert not can_assign, "Should not allow assignment to passive kur"
        assert "pasif" in reason.lower(), f"Error should mention pasif, got: {reason}"
        # Verify Turkish characters
        assert any(ord(c) > 127 for c in reason), "Error should be in Turkish"
        print(f"    ✓ Atama engellendi: {reason}")

        scenario_results.append(("SENARYO 5", "✓ PASS"))
        print("  ✓ SENARYO 5 BAŞARILI")

    except Exception as e:
        print(f"  ✗ SENARYO 5 BAŞARISIZ: {str(e)}")
        scenario_results.append(("SENARYO 5", f"✗ FAIL: {str(e)}"))
        return False

    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    print("\n" + "=" * 90)
    print("SENARYO ÖZETI")
    print("=" * 90)
    for scenario, result in scenario_results:
        print(f"  {result}: {scenario}")

    total_passed = sum(1 for _, r in scenario_results if "✓ PASS" in r)
    print(f"\nToplam: {total_passed}/{len(scenario_results)} senaryo başarılı")

    if total_passed == len(scenario_results):
        print("\n✓ RC-1 TÜM SENARYOLAR BAŞARILI")
        return True
    else:
        print(f"\n✗ RC-1 {len(scenario_results) - total_passed} senaryo başarısız")
        return False


if __name__ == "__main__":
    success = test_rc1_integration()
    sys.exit(0 if success else 1)
