#!/usr/bin/env python3
"""Test page building - check for initialization exceptions."""

import sys
sys.path.insert(0, 'src')

print("="*70)
print("PAGE BUILD INITIALIZATION TEST")
print("="*70)
print()

print("Step 1: Import students_v2 module...")
try:
    from views.pages.students_v2 import build_students_v2_page
    print("✓ Import successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)

print()
print("Step 2: Build students_v2_page()...")
try:
    page = build_students_v2_page()
    print("✓ Page built successfully")
    print(f"✓ Page type: {type(page)}")
except Exception as e:
    print(f"✗ Page build failed!")
    print()
    print("="*70)
    print("EXCEPTION DURING PAGE BUILD:")
    print("="*70)
    
    exc_type = type(e).__name__
    exc_msg = str(e)
    
    import traceback
    tb_lines = traceback.format_exc().split('\n')
    
    print()
    for line in tb_lines:
        print(line)
    
    print()
    print("="*70)
    print(f"Exception Type: {exc_type}")
    print(f"Exception Msg:  {exc_msg}")
    print("="*70)
