#!/usr/bin/env python3
"""Test course loading directly."""

import sys
sys.path.insert(0, 'src')

from controllers import build_course_controller

print("Testing course controller...")
print("-" * 70)

try:
    controller = build_course_controller()
    print(f"✓ Controller created: {type(controller).__name__}")
    
    print("\nCalling list_courses(limit=1000, offset=0)...")
    courses = list(controller.list_courses(limit=1000, offset=0))
    print(f"✓ Got {len(courses)} courses")
    
    if courses:
        print("\nFirst course:")
        print(f"  {courses[0]}")
    
    print("\n✓ TEST PASSED - Courses load successfully")

except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}")
    print(f"  Message: {e}")
    
    import traceback
    print("\nFull traceback:")
    print(traceback.format_exc())
    
    print("\n✗ TEST FAILED")
    sys.exit(1)
