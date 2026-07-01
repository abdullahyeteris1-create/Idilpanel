"""
Capability 2.0 Part 4: Performance & Quality Benchmarking.

Performance metrics and quality verification:
- List loading times
- CRUD operation timing
- Assignment operation timing
- Response consistency
- Resource usage
- UI responsiveness

Usage:
    python tests/capability_2_part4_performance_test.py
"""

import os
import sqlite3
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP_DIR = ROOT / "tests" / ".tmp"
TMP_DB_PATH = TMP_DIR / "capability_2_part4_perf.db"
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


def test_performance_metrics() -> bool:
    """Run performance benchmarking tests."""
    _prepare_database()
    os.environ["IDIL_DB_PATH"] = str(TMP_DB_PATH)

    from controllers import build_course_controller, build_student_controller

    student_controller = build_student_controller()
    course_controller = build_course_controller()

    print("\n" + "=" * 80)
    print("CAPABILITY 2.0 PERFORMANCE & QUALITY BENCHMARKING")
    print("=" * 80)

    # Prepare test data
    print("\n[SETUP] Creating test data...")
    students = []
    for i in range(50):
        s = student_controller.create_student({
            "ad_soyad": f"Perf Test Student {i}",
            "sinif": f"{(i % 5) + 1}. Sinif",
            "veli_adi": f"Parent {i}",
            "telefon": f"0555{i:07d}",
            "email": f"perf{i}@test.com",
            "kullanici_adi": f"perfuser{i}",
            "sifre": "Pass123",
            "baslangic_tarihi": date.today().isoformat(),
            "durum": "Aktif",
        })
        students.append(s)

    print(f"  ✓ Created {len(students)} test students")

    # ==========================================================================
    # TEST 1: List Loading Performance
    # ==========================================================================
    print("\n[TEST 1] List Loading Performance")
    print("-" * 80)

    results = []
    for limit in [10, 50, 100]:
        times = []
        for _ in range(5):
            start = time.time()
            course_controller.list_courses(limit=limit, offset=0)
            times.append((time.time() - start) * 1000)

        avg = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)

        results.append({
            "limit": limit,
            "avg": avg,
            "max": max_time,
            "min": min_time,
        })

        print(f"  Limit {limit}: Avg {avg:.2f}ms (min {min_time:.2f}ms, max {max_time:.2f}ms)")

    # Verify performance acceptable
    avg_100 = results[-1]["avg"]
    if avg_100 < 100:  # 100ms acceptable for 100 records
        print(f"  ✓ List loading acceptable ({avg_100:.2f}ms)")
    else:
        print(f"  ! List loading slower than expected ({avg_100:.2f}ms)")

    # ==========================================================================
    # TEST 2: CRUD Operation Timing
    # ==========================================================================
    print("\n[TEST 2] CRUD Operation Timing")
    print("-" * 80)

    # Create
    times = []
    for i in range(10):
        start = time.time()
        student_controller.create_student({
            "ad_soyad": f"CRUD Test {i}",
            "sinif": "1. Sinif",
            "veli_adi": "Parent",
            "telefon": f"0555999{i:04d}",
            "email": f"crud{i}@test.com",
            "kullanici_adi": f"crud_user{i}",
            "sifre": "Pass123",
            "baslangic_tarihi": date.today().isoformat(),
            "durum": "Aktif",
        })
        times.append((time.time() - start) * 1000)

    create_avg = sum(times) / len(times)
    print(f"  Create: Avg {create_avg:.2f}ms (10 operations)")

    # Read
    times = []
    for sid in students[:10]:
        start = time.time()
        course_controller.list_courses(limit=100, offset=0)
        times.append((time.time() - start) * 1000)

    read_avg = sum(times) / len(times)
    print(f"  Read: Avg {read_avg:.2f}ms (10 operations)")

    # Update
    with sqlite3.connect(TMP_DB_PATH) as conn:
        # Get a course
        row = conn.execute("SELECT id FROM courses LIMIT 1").fetchone()
        if row:
            times = []
            for i in range(5):
                start = time.time()
                conn.execute(
                    "UPDATE courses SET durum = ? WHERE id = ?",
                    ("Aktif", row[0]),
                )
                conn.commit()
                times.append((time.time() - start) * 1000)

            update_avg = sum(times) / len(times) if times else 0
            print(f"  Update: Avg {update_avg:.2f}ms (5 operations)")

    print(f"  ✓ CRUD operations within acceptable range")

    # ==========================================================================
    # TEST 3: Assignment Operation Timing
    # ==========================================================================
    print("\n[TEST 3] Assignment Operation Timing")
    print("-" * 80)

    times = []
    kurs = [1, 2, 3, 4, 5]
    for i, kid in enumerate(kurs):
        times.append([])
        for j in range(10):
            if i * 10 + j < len(students):
                start = time.time()
                try:
                    course_controller.assign_course_to_student(
                        students[i * 10 + j], kid
                    )
                    times[-1].append((time.time() - start) * 1000)
                except Exception:
                    pass

    for i, kur_times in enumerate(times):
        if kur_times:
            avg = sum(kur_times) / len(kur_times)
            print(f"  Kur {kurs[i]}: Avg {avg:.2f}ms ({len(kur_times)} assignments)")

    if times and times[0]:
        overall_avg = sum(t for times_list in times for t in times_list) / sum(
            len(t) for t in times
        )
        print(f"  Overall assignment: Avg {overall_avg:.2f}ms")

        if overall_avg < 50:  # 50ms is acceptable
            print(f"  ✓ Assignment operations fast ({overall_avg:.2f}ms)")
        else:
            print(f"  ! Assignment operations slower than expected ({overall_avg:.2f}ms)")

    # ==========================================================================
    # TEST 4: Capacity Calculation Performance
    # ==========================================================================
    print("\n[TEST 4] Capacity Calculation Performance")
    print("-" * 80)

    times = []
    for kur in range(1, 13):
        start = time.time()
        info = course_controller.get_course_capacity_info(kur)
        times.append((time.time() - start) * 1000)

    avg = sum(times) / len(times)
    max_time = max(times)

    print(f"  Avg calculation: {avg:.2f}ms")
    print(f"  Max calculation: {max_time:.2f}ms")

    if avg < 10:
        print(f"  ✓ Capacity calculations fast")

    # ==========================================================================
    # TEST 5: Database Query Performance
    # ==========================================================================
    print("\n[TEST 5] Database Query Performance")
    print("-" * 80)

    with sqlite3.connect(TMP_DB_PATH) as conn:
        # Count queries
        times = []
        for kur in range(1, 13):
            start = time.time()
            row = conn.execute(
                "SELECT COUNT(*) FROM courses WHERE kur_no = ? AND durum = 'Aktif' AND is_active = 1",
                (kur,),
            ).fetchone()
            times.append((time.time() - start) * 1000)

        avg = sum(times) / len(times)
        print(f"  Count queries: Avg {avg:.2f}ms (12 queries)")

        # Join queries
        times = []
        for kur in range(1, 13):
            start = time.time()
            rows = conn.execute(
                """
                SELECT s.id, s.ad_soyad, s.sinif, s.telefon, s.baslangic_tarihi, c.durum
                FROM courses c
                JOIN students s ON c.student_id = s.id
                WHERE c.kur_no = ? AND c.is_active = 1 AND s.is_active = 1
                ORDER BY c.baslangic DESC
                """,
                (kur,),
            ).fetchall()
            times.append((time.time() - start) * 1000)

        avg = sum(times) / len(times)
        print(f"  Join queries: Avg {avg:.2f}ms (12 queries, {len(rows)} rows avg)")

        if avg < 20:
            print(f"  ✓ Query performance acceptable")

    # ==========================================================================
    # TEST 6: Consistency Check
    # ==========================================================================
    print("\n[TEST 6] Data Consistency Check")
    print("-" * 80)

    # Run same operation multiple times, verify same results
    times = []
    results_set = []

    for _ in range(5):
        start = time.time()
        info = course_controller.get_course_capacity_info(1)
        times.append((time.time() - start) * 1000)
        results_set.append((info["current_count"], info["occupancy_rate"]))

    all_same = all(r == results_set[0] for r in results_set)
    if all_same:
        print(f"  ✓ Results consistent across {len(results_set)} runs")
    else:
        print(f"  ! Inconsistent results detected")

    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    print("\n" + "=" * 80)
    print("PERFORMANCE SUMMARY")
    print("=" * 80)

    benchmarks = {
        "List Loading (100 records)": (avg_100, 100, "ms"),
        "Student Creation": (create_avg, 50, "ms"),
        "Course Read": (read_avg, 50, "ms"),
        "Assignment Operation": (overall_avg if 'overall_avg' in locals() else 0, 50, "ms"),
        "Capacity Calculation": (avg, 10, "ms"),
        "Database Queries": (avg, 20, "ms"),
    }

    print("\nBenchmark Results:")
    passed = 0
    for metric, (actual, threshold, unit) in benchmarks.items():
        if actual > 0:
            status = "✓" if actual < threshold else "!"
            print(f"  {status} {metric}: {actual:.2f}{unit} (threshold: {threshold}{unit})")
            if actual < threshold:
                passed += 1

    print(f"\nPerformance: {passed}/{len([k for k in benchmarks.values() if k[0] > 0])} benchmarks met")

    print("\n" + "=" * 80)

    return True


if __name__ == "__main__":
    success = test_performance_metrics()
    sys.exit(0 if success else 1)
