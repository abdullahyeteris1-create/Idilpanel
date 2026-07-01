#!/usr/bin/env python3
"""Test course controller to find list_courses error."""

import sys
sys.path.insert(0, 'src')

print("="*70)
print("COURSE CONTROLLER TEST")
print("="*70)
print()

print("Step 1: Build course_controller...")
try:
    from controllers import build_course_controller
    course_controller = build_course_controller()
    print("✓ Course controller instantiated")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print()
print("Step 2: Call course_controller.list_courses()...")
try:
    courses = course_controller.list_courses(limit=1000, offset=0)
    print(f"✓ list_courses() returned: {type(courses)}")
    
    courses_list = list(courses)
    print(f"✓ Converted to list: {len(courses_list)} courses")
    
except Exception as e:
    print(f"✗ list_courses() FAILED!")
    print()
    print("="*70)
    print("EXCEPTION:")
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
