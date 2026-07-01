#!/usr/bin/env python3
"""
Direct test: Simulate _payload() and controller.create_student()
to capture real exception without UI.
"""

import sys
sys.path.insert(0, 'src')

import flet as ft
from datetime import datetime
from components import build_text_field, build_app_datepicker, build_app_dropdown

print("="*70)
print("DIRECT CONTROLLER TEST - CAPTURING REAL EXCEPTION")
print("="*70)
print()

# Create mock form fields (exactly like in students_v2.py)
name_field = ft.TextField(value="Test Öğrenci Form")
class_field = ft.TextField(value="3-B")
parent_field = ft.TextField(value="")
phone_field = ft.TextField(value="")
email_field = ft.TextField(value="test@example.com")
username_field = ft.TextField(value="")
password_field = ft.TextField(value="", password=True)
start_date = build_app_datepicker("Baslangic Tarihi", required=True)
start_date.value = "2026-05-01"
end_date = build_app_datepicker("Bitis Tarihi")
end_date.value = ""
kur_dropdown = build_app_dropdown("Kur", options=[str(i) for i in range(1, 17)])
kur_dropdown.value = None  # No kur selected
status_dropdown = build_app_dropdown("Durum", options=["Aktif", "Beklemede"], value="Aktif")
notes_field = ft.TextField(value="Test not", multiline=True)

def _get_date_value(date_picker):
    """Extract date value from app datepicker."""
    val = date_picker.value if hasattr(date_picker, 'value') else None
    return str(val or "").strip()

def _set_date_value(date_picker, val):
    """Set date value to app datepicker."""
    if hasattr(date_picker, 'value'):
        date_picker.value = val

def _payload():
    """Build payload exactly as in students_v2.py."""
    return {
        "ad_soyad": str(name_field.value or "").strip(),
        "sinif": str(class_field.value or "").strip(),
        "veli_adi": str(parent_field.value or "").strip(),
        "telefon": str(phone_field.value or "").strip(),
        "email": str(email_field.value or "").strip(),
        "kullanici_adi": str(username_field.value or "").strip(),
        "sifre": str(password_field.value or "").strip(),
        "baslangic_tarihi": _get_date_value(start_date),
        "bitis_tarihi": _get_date_value(end_date),
        "durum": str(status_dropdown.value or "Aktif").strip(),
        "notlar": str(notes_field.value or "").strip(),
    }

# Test 1: Check payload
print("Step 1: Generate payload from mock form fields")
print("-"*70)
payload = _payload()
print("Payload generated:")
for key, value in payload.items():
    if value:
        print(f"  {key}: '{value}'")
    else:
        print(f"  {key}: (empty)")
print()

# Test 2: Try to create student
print("Step 2: Call controller.create_student(payload)")
print("-"*70)

try:
    from controllers import build_student_controller
    controller = build_student_controller()
    print(f"✓ Controller instantiated")
    print(f"✓ Calling controller.create_student(payload)...")
    
    result = controller.create_student(payload)
    print(f"✓ Student created successfully: ID={result}")
    
except Exception as exc:
    # Get full exception info
    import traceback
    exc_type = type(exc).__name__
    exc_file = traceback.extract_tb(exc.__traceback__)[-1].filename
    exc_line = traceback.extract_tb(exc.__traceback__)[-1].lineno
    exc_func = traceback.extract_tb(exc.__traceback__)[-1].name
    exc_message = str(exc)
    full_traceback = traceback.format_exc()
    
    print()
    print("="*70)
    print("✗ REAL EXCEPTION CAPTURED")
    print("="*70)
    print()
    print(f"Exception Type:  {exc_type}")
    print(f"Exception File:  {exc_file}")
    print(f"Exception Line:  {exc_line}")
    print(f"Exception Func:  {exc_func}")
    print(f"Exception Msg:   {exc_message}")
    print()
    print("-"*70)
    print("FULL TRACEBACK:")
    print("-"*70)
    print(full_traceback)
    print("="*70)
    
    # Save to file
    with open('debug_exception.log', 'w', encoding='utf-8') as f:
        f.write(f"Exception Type: {exc_type}\n")
        f.write(f"Exception File: {exc_file}\n")
        f.write(f"Exception Line: {exc_line}\n")
        f.write(f"Exception Func: {exc_func}\n")
        f.write(f"Exception Msg:  {exc_message}\n\n")
        f.write("FULL TRACEBACK:\n")
        f.write(full_traceback)
    
    print("\n(Exception details saved to debug_exception.log)")
