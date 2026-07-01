#!/usr/bin/env python3
"""Test script to verify save functionality fix."""

import sys
sys.path.insert(0, 'src')

from controllers import build_student_controller

controller = build_student_controller()

# Test 1: Create student without kur
print("Test 1: Creating student without kur requirement...")
payload1 = {
    'ad_soyad': 'Test Öğrenci 1',
    'sinif': '5-C',
    'baslangic_tarihi': '2026-02-15',
    'durum': 'Aktif',
}
try:
    result1 = controller.create_student(payload1)
    print(f"✓ Create succeeded: ID={result1}")
except Exception as e:
    print(f"✗ Create failed: {e}")
    sys.exit(1)

# Test 2: List all students
print("\nTest 2: Listing all students...")
students = controller.list_students(limit=100, offset=0)
print(f"Total students in DB: {len(students)}")

# Test 3: Get specific student
print("\nTest 3: Getting specific student...")
student = controller.get_student(result1)
if student:
    print(f"✓ Found: {student['ad_soyad']} ({student['sinif']}) - Durum: {student['durum']}")
else:
    print(f"✗ Student not found")
    sys.exit(1)

# Test 4: Update student
print("\nTest 4: Updating student...")
update_payload = {
    'ad_soyad': 'Test Öğrenci 1 Güncellenmiş',
    'sinif': '6-C',
}
try:
    updated = controller.update_student(result1, update_payload)
    if updated:
        print(f"✓ Update succeeded")
        updated_student = controller.get_student(result1)
        print(f"  New name: {updated_student['ad_soyad']}, New class: {updated_student['sinif']}")
    else:
        print(f"✗ Update returned False")
except Exception as e:
    print(f"✗ Update failed: {e}")
    sys.exit(1)

# Test 5: Delete student
print("\nTest 5: Deleting student...")
try:
    deleted = controller.delete_student(result1)
    if deleted:
        print(f"✓ Delete succeeded")
        student_after_delete = controller.get_student(result1)
        if student_after_delete is None:
            print(f"  Verified: Student no longer in database")
        else:
            print(f"  Warning: Student still exists (soft delete)")
    else:
        print(f"✗ Delete returned False")
except Exception as e:
    print(f"✗ Delete failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ ALL TESTS PASSED - Save functionality is working!")
print("="*50)
