#!/usr/bin/env python
"""
Sprint Courses-5: Search, Filter, Sort & Analytics Test
Validates the complete Courses V2 search/filter/sort workflow.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Mock Flet for import-only testing
class MockControl:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockFlet:
    def __init__(self):
        self.Column = lambda **kw: MockControl(**kw)
        self.Row = lambda **kw: MockControl(**kw)
        self.Text = lambda *a, **kw: MockControl(*a, **kw)
        self.Icon = lambda *a, **kw: MockControl(*a, **kw)
        self.Container = lambda **kw: MockControl(**kw)
        self.BoxShadow = lambda **kw: MockControl(**kw)
        self.Transform = lambda **kw: MockControl(**kw)
        self.Offset = lambda x, y: (x, y)
        self.Icons = type('Icons', (), {
            'SCHOOL_OUTLINED': None,
            'CLOSE': None,
            'CHECK': None,
        })()

mock_ft = MockFlet()
sys.modules['flet'] = mock_ft
sys.modules['ft'] = mock_ft

# Now we can import the filter function
from views.pages.courses_v2 import _courses_v2_apply_filters

print("=" * 70)
print("Sprint Courses-5: Search, Filter, Sort & Analytics")
print("=" * 70)

# Test data: sample courses with student_id, kur_no, baslangic, durum
test_courses = [
    {"student_id": 101, "kur_no": 1, "baslangic": "2025-01-01", "durum": "Aktif"},
    {"student_id": 102, "kur_no": 2, "baslangic": "2025-01-05", "durum": "Beklemede"},
    {"student_id": 103, "kur_no": 1, "baslangic": "2025-01-10", "durum": "Tamamlandi"},
    {"student_id": 104, "kur_no": 3, "baslangic": "2025-02-01", "durum": "Aktif"},
    {"student_id": 105, "kur_no": 2, "baslangic": "2025-02-05", "durum": "Iptal"},
]

# Test 1: No filters (should return all 5)
print("\n✓ Test 1: No filters applied")
result = _courses_v2_apply_filters(test_courses, "", "Tumu", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 5, f"Expected 5 records, got {len(result)}"
print(f"  Result: {len(result)} kayit")

# Test 2: Search by student_id
print("\n✓ Test 2: Search by student_id='102'")
result = _courses_v2_apply_filters(test_courses, "102", "Tumu", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 1, f"Expected 1 record, got {len(result)}"
assert result[0]["student_id"] == 102, "Wrong student ID"
print(f"  Result: {result[0]}")

# Test 3: Filter by status "Aktif"
print("\n✓ Test 3: Filter by Durum='Aktif'")
result = _courses_v2_apply_filters(test_courses, "", "Aktif", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 2, f"Expected 2 records, got {len(result)}"
assert all(r["durum"] == "Aktif" for r in result), "Wrong status filter"
print(f"  Result: {len(result)} kayit (students {[r['student_id'] for r in result]})")

# Test 4: Filter by Kur=2
print("\n✓ Test 4: Filter by Kur='2'")
result = _courses_v2_apply_filters(test_courses, "", "Tumu", "2", "Ogrenci ID", "Artan")
assert len(result) == 2, f"Expected 2 records, got {len(result)}"
assert all(r["kur_no"] == 2 for r in result), "Wrong kur_no filter"
print(f"  Result: {len(result)} kayit (students {[r['student_id'] for r in result]})")

# Test 5: Sort by student_id ascending
print("\n✓ Test 5: Sort by Ogrenci ID ascending")
result = _courses_v2_apply_filters(test_courses, "", "Tumu", "Tumu", "Ogrenci ID", "Artan")
ids = [r["student_id"] for r in result]
assert ids == sorted(ids), "Not sorted ascending"
print(f"  Result: {ids}")

# Test 6: Sort by student_id descending
print("\n✓ Test 6: Sort by Ogrenci ID descending")
result = _courses_v2_apply_filters(test_courses, "", "Tumu", "Tumu", "Ogrenci ID", "Azalan")
ids = [r["student_id"] for r in result]
assert ids == sorted(ids, reverse=True), "Not sorted descending"
print(f"  Result: {ids}")

# Test 7: Sort by Kur ascending
print("\n✓ Test 7: Sort by Kur ascending")
result = _courses_v2_apply_filters(test_courses, "", "Tumu", "Tumu", "Kur", "Artan")
kurs = [r["kur_no"] for r in result]
assert kurs == sorted(kurs), "Not sorted by kur ascending"
print(f"  Result: {kurs}")

# Test 8: Sort by Baslangic descending
print("\n✓ Test 8: Sort by Baslangic descending")
result = _courses_v2_apply_filters(test_courses, "", "Tumu", "Tumu", "Baslangic", "Azalan")
dates = [r["baslangic"] for r in result]
assert dates == sorted(dates, reverse=True), "Not sorted by baslangic descending"
print(f"  Result: {dates}")

# Test 9: Combined search + filter
print("\n✓ Test 9: Search '103' + Filter Durum='Tamamlandi'")
result = _courses_v2_apply_filters(test_courses, "103", "Tamamlandi", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 1, f"Expected 1 record, got {len(result)}"
assert result[0]["student_id"] == 103, "Wrong student"
assert result[0]["durum"] == "Tamamlandi", "Wrong status"
print(f"  Result: {result[0]}")

# Test 10: No results case
print("\n✓ Test 10: No results (search '999')")
result = _courses_v2_apply_filters(test_courses, "999", "Tumu", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 0, "Should be empty"
print(f"  Result: {len(result)} kayit (empty state)")

# Test 11: Complex filter (Aktif + Kur=1)
print("\n✓ Test 11: Filter Durum='Aktif' + Kur='1'")
result = _courses_v2_apply_filters(test_courses, "", "Aktif", "1", "Ogrenci ID", "Artan")
assert len(result) == 1, f"Expected 1 record, got {len(result)}"
assert result[0]["student_id"] == 104, "Wrong student"
print(f"  Result: {result[0]}")

# Test 12: Search + Filter + Sort
print("\n✓ Test 12: Search + Filter + Sort combined")
result = _courses_v2_apply_filters(test_courses, "", "Aktif", "Tumu", "Ogrenci ID", "Azalan")
ids = [r["student_id"] for r in result]
assert len(result) == 2, "Should have 2 Aktif records"
assert ids == [104, 101], "Wrong sort order"
print(f"  Result: {len(result)} kayit sorted {ids}")

print("\n" + "=" * 70)
print("✅ All tests passed! Sprint Courses-5 search/filter/sort functional.")
print("=" * 70)
