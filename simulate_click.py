#!/usr/bin/env python3
"""
Simulate save button click directly - test _handle_create logic.
"""

import sys
sys.path.insert(0, 'src')

import flet as ft
from components import build_text_field, build_app_datepicker, build_app_dropdown

print("="*70)
print("SIMULATING SAVE BUTTON CLICK - FULL FLOW TEST")
print("="*70)
print()

# Import students_v2 internals
from views.pages.students_v2 import build_students_v2_page

# We need to simulate the form fields and state
# Let's build a mock event that simulates save button click

print("Step 1: Build page...")
try:
    page = build_students_v2_page()
    print("✓ Page built")
except Exception as e:
    print(f"✗ Page build failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("Step 2: Simulate form input and save click...")
print("(This will test the _handle_create flow without UI)")
print()

# Create a mock page event
class MockPage:
    def __init__(self):
        self.overlay = []
    
    def update(self):
        pass
    
    def open(self, dialog):
        pass
    
    def close(self, dialog):
        pass

class MockEvent:
    def __init__(self):
        self.page = MockPage()

# Now we need to import and call _handle_create
# But _handle_create is defined inside build_students_v2_page()
# So we need to extract it...

print("Note: _handle_create is defined inside build_students_v2_page()")
print("Cannot directly call it from outside.")
print()
print("Checking for debug log files after page build...")

import os
import glob

debug_files = glob.glob('debug*.log')
if debug_files:
    print(f"✓ Found {len(debug_files)} debug files:")
    for f in debug_files:
        print(f"\n  File: {f}")
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"  Content ({len(content)} bytes):")
        print("-"*70)
        print(content)
        print("-"*70)
else:
    print("(No debug files created yet - page built without errors)")
    print("(Build succeeded, no exceptions during initialization)")
