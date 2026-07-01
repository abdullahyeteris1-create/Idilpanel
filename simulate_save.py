#!/usr/bin/env python3
"""Simulate save button click to capture real runtime exception."""

import sys
import os
sys.path.insert(0, 'src')

# Set up mock Flet page for testing
import flet as ft

# Create minimal Flet app to test
def test_save_exception():
    print("="*70)
    print("SIMULATING SAVE BUTTON CLICK - EXCEPTION CAPTURE")
    print("="*70)
    print()
    
    # Import AFTER setting up path
    from views.pages.students_v2 import build_students_v2_page
    
    # Build the page to trigger any initialization errors
    print("Building students_v2 page...")
    try:
        page = build_students_v2_page()
        print("✓ Page built successfully")
        print()
    except Exception as e:
        print(f"✗ EXCEPTION DURING PAGE BUILD:")
        print()
        import traceback
        print(traceback.format_exc())
        return
    
    # Wait a moment for app to initialize
    print("Checking for debug_exception.log (if save was triggered)...")
    print()
    
    # Check if any debug log was created
    if os.path.exists('debug_exception.log'):
        with open('debug_exception.log', 'r', encoding='utf-8') as f:
            log_content = f.read()
        print("="*70)
        print("CAUGHT EXCEPTION FROM SAVE BUTTON:")
        print("="*70)
        print(log_content)
        print("="*70)
    else:
        print("(No save button clicked yet - app is running)")
        print("(Click [Kaydet] button in the app to capture exception)")

if __name__ == "__main__":
    test_save_exception()
