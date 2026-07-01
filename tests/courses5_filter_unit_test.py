#!/usr/bin/env python
"""
Sprint Courses-5: Filter & Sort Logic Unit Test
Tests ONLY the filter/sort logic without UI dependencies.
"""

print("=" * 70)
print("Sprint Courses-5: Filter & Sort Logic Unit Test")
print("=" * 70)

# Test data: sample courses with fields from schema
test_courses = [
    {"student_id": 101, "kur_no": 1, "baslangic": "2025-01-01", "durum": "Aktif"},
    {"student_id": 102, "kur_no": 2, "baslangic": "2025-01-05", "durum": "Beklemede"},
    {"student_id": 103, "kur_no": 1, "baslangic": "2025-01-10", "durum": "Tamamlandi"},
    {"student_id": 104, "kur_no": 3, "baslangic": "2025-02-01", "durum": "Aktif"},
    {"student_id": 105, "kur_no": 2, "baslangic": "2025-02-05", "durum": "Iptal"},
]

def _courses_v2_apply_filters(
    records: list[dict],
    search_query: str,
    status_filter: str,
    kur_filter: str,
    sort_field: str = "student_id",
    sort_direction: str = "Artan",
) -> list[dict]:
    """Apply search, status/kur filters, and sort to course records."""
    filtered = []
    
    for record in records:
        # Search filter
        if search_query.strip():
            query_lower = search_query.lower().strip()
            if not (
                query_lower in str(record.get("student_id", "")).lower()
                or query_lower in str(record.get("kur_no", "")).lower()
                or query_lower in str(record.get("baslangic", "")).lower()
                or query_lower in record.get("durum", "").lower()
            ):
                continue
        
        # Status filter
        if status_filter != "Tumu" and record.get("durum") != status_filter:
            continue
        
        # Kur filter
        if kur_filter != "Tumu" and str(record.get("kur_no", "")) != kur_filter:
            continue
        
        filtered.append(record)
    
    # Apply sort
    reverse = sort_direction == "Azalan"
    if sort_field == "Kur":
        filtered.sort(key=lambda x: int(x.get("kur_no", 0) or 0), reverse=reverse)
    elif sort_field == "Baslangic":
        filtered.sort(key=lambda x: str(x.get("baslangic", "")), reverse=reverse)
    else:  # "Ogrenci ID" default
        filtered.sort(key=lambda x: int(x.get("student_id", 0) or 0), reverse=reverse)
    
    return filtered


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
print(f"  Result: student_id={result[0]['student_id']}")

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
print(f"  Result: student_id={result[0]['student_id']}, durum={result[0]['durum']}")

# Test 10: No results case
print("\n✓ Test 10: No results (search '999')")
result = _courses_v2_apply_filters(test_courses, "999", "Tumu", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 0, "Should be empty"
print(f"  Result: {len(result)} kayit (empty state)")

# Test 11: Complex filter (Aktif + Kur=1)
print("\n✓ Test 11: Filter Durum='Aktif' + Kur='1'")
result = _courses_v2_apply_filters(test_courses, "", "Aktif", "1", "Ogrenci ID", "Artan")
assert len(result) == 1, f"Expected 1 record, got {len(result)}"
assert result[0]["student_id"] == 101, "Wrong student"
print(f"  Result: student_id={result[0]['student_id']}")

# Test 12: Search + Filter + Sort combined
print("\n✓ Test 12: Search + Filter + Sort combined")
result = _courses_v2_apply_filters(test_courses, "", "Aktif", "Tumu", "Ogrenci ID", "Azalan")
ids = [r["student_id"] for r in result]
assert len(result) == 2, "Should have 2 Aktif records"
assert ids == [104, 101], "Wrong sort order"
print(f"  Result: {len(result)} kayit sorted {ids}")

# Test 13: Search case-insensitive
print("\n✓ Test 13: Search case-insensitive")
result = _courses_v2_apply_filters(test_courses, "AKTIF", "Tumu", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 2, f"Expected 2 records, got {len(result)}"
assert all(r["durum"] == "Aktif" for r in result), "Case-insensitive search failed"
print(f"  Result: {len(result)} kayit with 'AKTIF' search")

# Test 14: Filter Beklemede
print("\n✓ Test 14: Filter Durum='Beklemede'")
result = _courses_v2_apply_filters(test_courses, "", "Beklemede", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 1, f"Expected 1 record, got {len(result)}"
assert result[0]["durum"] == "Beklemede", "Wrong status"
print(f"  Result: {result[0]}")

# Test 15: Filter Iptal
print("\n✓ Test 15: Filter Durum='Iptal'")
result = _courses_v2_apply_filters(test_courses, "", "Iptal", "Tumu", "Ogrenci ID", "Artan")
assert len(result) == 1, f"Expected 1 record, got {len(result)}"
assert result[0]["durum"] == "Iptal", "Wrong status"
print(f"  Result: {result[0]}")

print("\n" + "=" * 70)
print("✅ All 15 tests passed! Filter & sort logic validated.")
print("=" * 70)
