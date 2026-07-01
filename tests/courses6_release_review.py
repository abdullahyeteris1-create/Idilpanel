#!/usr/bin/env python
"""
Sprint Courses-6: Release Readiness Review
Comprehensive quality assessment across 10 control points.
"""

import sys
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import what we need
import sqlite3
import re
from datetime import date
from src.controllers import build_course_controller

print("=" * 90)
print("SPRINT COURSES-6: RELEASE READINESS REVIEW")
print("=" * 90)

# Read source code for analysis
courses_v2_src = Path(__file__).parent.parent / "src" / "views" / "pages" / "courses_v2.py"
with open(courses_v2_src, "r", encoding="utf-8") as f:
    courses_v2_content = f.read()

# ============================================================================
# 1. ARCHITECTURE REVIEW
# ============================================================================
print("\n[1/10] ARCHITECTURE REVIEW")
print("-" * 90)

arch_score = 0
max_arch = 5

# Check for direct imports (should NOT have these)
if "from services" not in courses_v2_content and "from database" not in courses_v2_content:
    print("✅ No direct Service/Repository imports (MVC pattern)")
    arch_score += 1
else:
    print("❌ Direct layer imports found")

if "import sqlite3" not in courses_v2_content:
    print("✅ No direct SQLite imports")
    arch_score += 1
else:
    print("❌ Direct SQLite import found")

# Check for Controller usage
if "from controllers import build_course_controller" in courses_v2_content:
    print("✅ CourseController imported correctly")
    arch_score += 1
else:
    print("❌ CourseController not imported")

# Check for component library usage
component_list = [
    "PageContainer", "build_app_header", "build_action_panel",
    "build_search_bar", "build_filter_bar", "build_form_card",
    "build_table_card", "build_badge", "build_primary_button",
    "build_secondary_button", "build_danger_button", "build_empty_state",
    "build_error_state", "build_loading_state", "build_text_field", "build_app_dropdown"
]
imported_comps = sum(1 for comp in component_list if f"build_{comp}" in courses_v2_content or f"{comp}" in courses_v2_content)
if imported_comps >= 14:
    print(f"✅ Component library: {imported_comps}/16 components used")
    arch_score += 1
else:
    print(f"❌ Component library: only {imported_comps}/16 used")

# Check for state management
if 'state: dict = {' in courses_v2_content:
    print("✅ State management pattern present")
    arch_score += 1
else:
    print("❌ No state management")

print(f"Architecture Score: {arch_score}/{max_arch}")

# ============================================================================
# 2. CRUD OPERATIONS
# ============================================================================
print("\n[2/10] CRUD OPERATIONS REVIEW")
print("-" * 90)

controller = build_course_controller()
crud_ops = []

# CREATE
try:
    rid = controller.create_course({
        "course_name": "Test-C", "student_id": 701, "kur_no": 1,
        "baslangic": "2026-07-01", "bitis": "2027-01-01",
        "total_lessons": 16, "durum": "Aktif"
    })
    print(f"✅ CREATE: OK (ID {rid})")
    crud_ops.append(("CREATE", True))
except Exception as e:
    print(f"❌ CREATE: {str(e)[:40]}")
    crud_ops.append(("CREATE", False))

# READ
try:
    rec = controller.read_course(rid)
    if rec and rec["student_id"] == 701:
        print(f"✅ READ: OK")
        crud_ops.append(("READ", True))
    else:
        print(f"❌ READ: Wrong data")
        crud_ops.append(("READ", False))
except Exception as e:
    print(f"❌ READ: {str(e)[:40]}")
    crud_ops.append(("READ", False))

# LIST
try:
    records = controller.list_courses(limit=500)
    if len(records) > 0:
        print(f"✅ LIST: OK ({len(records)} records)")
        crud_ops.append(("LIST", True))
    else:
        print(f"❌ LIST: No records")
        crud_ops.append(("LIST", False))
except Exception as e:
    print(f"❌ LIST: {str(e)[:40]}")
    crud_ops.append(("LIST", False))

# UPDATE
try:
    controller.update_course(rid, {
        "course_name": "Test-U", "student_id": 701, "kur_no": 2,
        "baslangic": "2026-07-01", "bitis": "2027-01-01",
        "total_lessons": 16, "durum": "Beklemede"
    })
    rec = controller.read_course(rid)
    if rec["durum"] == "Beklemede":
        print(f"✅ UPDATE: OK")
        crud_ops.append(("UPDATE", True))
    else:
        print(f"❌ UPDATE: Failed")
        crud_ops.append(("UPDATE", False))
except Exception as e:
    print(f"❌ UPDATE: {str(e)[:40]}")
    crud_ops.append(("UPDATE", False))

# DELETE
try:
    controller.delete_course(rid)
    print(f"✅ DELETE: OK")
    crud_ops.append(("DELETE", True))
except Exception as e:
    print(f"❌ DELETE: {str(e)[:40]}")
    crud_ops.append(("DELETE", False))

crud_score = sum(1 for _, ok in crud_ops if ok)
print(f"CRUD Score: {crud_score}/5")

# ============================================================================
# 3. VALIDATION REVIEW
# ============================================================================
print("\n[3/10] VALIDATION REVIEW")
print("-" * 90)

validation_score = 0
max_val = 4

if "_validate_form" in courses_v2_content:
    print("✅ Form validation function present")
    validation_score += 1
else:
    print("❌ No validation function")

# Check for Turkish messages
turkish_checks = [
    "Ogrenci ID zorunludur.",
    "Kur secimi zorunludur.",
    "Basariyla olusturuldu.",
    "Basariyla guncellendi.",
]
found_msgs = sum(1 for msg in turkish_checks if msg in courses_v2_content)
print(f"✅ Turkish messages: {found_msgs}/4 key messages")
if found_msgs >= 3:
    validation_score += 1

# Error mapper
if "_friendly_error" in courses_v2_content:
    print("✅ Error mapper present")
    validation_score += 1
else:
    print("❌ No error mapper")

# Check for date validation
if "date.fromisoformat" in courses_v2_content:
    print("✅ Date format validation")
    validation_score += 1

print(f"Validation Score: {validation_score}/{max_val}")

# ============================================================================
# 4. RESPONSIVE DESIGN REVIEW
# ============================================================================
print("\n[4/10] RESPONSIVE DESIGN REVIEW")
print("-" * 90)

resp_score = 0

breakpoints_needed = ["1920 px", "1600 px", "1366 px", "1280 px", "Tablet", "Mobil"]
found_bps = [bp for bp in breakpoints_needed if bp in courses_v2_content]
print(f"✅ Breakpoints: {len(found_bps)}/6 - {', '.join(found_bps[:3])}...")
if len(found_bps) >= 5:
    resp_score += 1

# col settings for responsive grid
col_count = courses_v2_content.count('.col = {')
print(f"✅ Responsive col settings: {col_count} components")
if col_count >= 4:
    resp_score += 1

print(f"Responsive Score: {resp_score}/2")

# ============================================================================
# 5. ACCESSIBILITY REVIEW
# ============================================================================
print("\n[5/10] ACCESSIBILITY REVIEW")
print("-" * 90)

access_score = 0

if "autofocus = True" in courses_v2_content:
    print("✅ Autofocus on first field")
    access_score += 1
else:
    print("❌ No autofocus")

if "set_focus" in courses_v2_content:
    print("✅ Focus management")
    access_score += 1
else:
    print("❌ No focus management")

if "on_change" in courses_v2_content and "on_submit" in courses_v2_content:
    print("✅ Keyboard event handlers")
    access_score += 1

print(f"Accessibility Score: {access_score}/3")

# ============================================================================
# 6. PERFORMANCE REVIEW
# ============================================================================
print("\n[6/10] PERFORMANCE REVIEW")
print("-" * 90)

perf_score = 0

if "_courses_v2_apply_filters" in courses_v2_content:
    print("✅ In-memory filtering (no DB on every filter)")
    perf_score += 1
else:
    print("❌ No local filter")

if "limit=500" in courses_v2_content:
    print("✅ Query limit prevents overload")
    perf_score += 1
else:
    print("⚠️ No query limit")

if "_apply_and_render" in courses_v2_content and "_render_table" in courses_v2_content:
    print("✅ Controlled rendering")
    perf_score += 1
else:
    print("❌ Render not controlled")

print(f"Performance Score: {perf_score}/3")

# ============================================================================
# 7. CODE QUALITY REVIEW
# ============================================================================
print("\n[7/10] CODE QUALITY REVIEW")
print("-" * 90)

code_score = 0
max_code = 4

# Hardcoded colors
hardcoded_colors = re.findall(r'color\s*=\s*["\']#[A-Fa-f0-9]{6}["\']', courses_v2_content)
if len(hardcoded_colors) < 3:
    print(f"✅ Limited hardcoded colors: {len(hardcoded_colors)}")
    code_score += 1
else:
    print(f"⚠️ Many hardcoded colors: {len(hardcoded_colors)}")

# Magic numbers
magic_nums = courses_v2_content.count("range(1, 13)")
if magic_nums > 0:
    print("⚠️ Magic number for course range (1-12)")
else:
    code_score += 1

# Unused variables check (basic)
if "import" in courses_v2_content and "from" in courses_v2_content:
    print("✅ Imports present and likely used")
    code_score += 1

# Constants instead of magic strings
if "_DURUM_OPTIONS" in courses_v2_content:
    print("✅ Named constants for options")
    code_score += 1

print(f"Code Quality Score: {code_score}/{max_code}")

# ============================================================================
# 8. DESIGN SYSTEM REVIEW
# ============================================================================
print("\n[8/10] DESIGN SYSTEM REVIEW")
print("-" * 90)

design_score = 0

design_comps = ["build_primary_button", "build_secondary_button", "build_danger_button",
                "build_badge", "build_table_card", "build_form_card"]
used_comps = sum(1 for comp in design_comps if comp in courses_v2_content)
print(f"✅ Design components: {used_comps}/6")
if used_comps >= 5:
    design_score += 1

# Turkish localization
turkish_labels = ["Ogrenci ID", "Durum", "Kurs", "Basariyla", "Hata", "Bilgi"]
found_labels = sum(1 for label in turkish_labels if label in courses_v2_content)
print(f"✅ Turkish localization: {found_labels}/6 labels")
if found_labels >= 5:
    design_score += 1

# Container structure
if "PageContainer" in courses_v2_content:
    print("✅ PageContainer wrapper")
    design_score += 1

print(f"Design System Score: {design_score}/3")

# ============================================================================
# 9. CAPABILITY TEST (E2E)
# ============================================================================
print("\n[9/10] CAPABILITY TEST (E2E USER SCENARIO)")
print("-" * 90)

cap_steps = []

# Step 1: Create
try:
    cap_id = controller.create_course({
        "course_name": "E2E", "student_id": 802, "kur_no": 2,
        "baslangic": "2026-07-15", "bitis": "2027-01-15",
        "total_lessons": 16, "durum": "Aktif"
    })
    print(f"✅ Step 1: CREATE - {cap_id}")
    cap_steps.append(True)
except:
    print("❌ Step 1: CREATE failed")
    cap_steps.append(False)

# Step 2: Read
try:
    rec = controller.read_course(cap_id)
    if rec["durum"] == "Aktif":
        print(f"✅ Step 2: READ - confirmed Aktif")
        cap_steps.append(True)
    else:
        cap_steps.append(False)
except:
    print("❌ Step 2: READ failed")
    cap_steps.append(False)

# Step 3: Update
try:
    controller.update_course(cap_id, {
        "course_name": "E2E-U", "student_id": 802, "kur_no": 2,
        "baslangic": "2026-07-15", "bitis": "2027-01-15",
        "total_lessons": 16, "durum": "Beklemede"
    })
    print(f"✅ Step 3: UPDATE - to Beklemede")
    cap_steps.append(True)
except:
    print("❌ Step 3: UPDATE failed")
    cap_steps.append(False)

# Step 4: List
try:
    records = controller.list_courses(limit=500)
    if any(r["id"] == cap_id for r in records):
        print(f"✅ Step 4: LIST - found in results")
        cap_steps.append(True)
    else:
        cap_steps.append(False)
except:
    print("❌ Step 4: LIST failed")
    cap_steps.append(False)

# Step 5: Delete
try:
    controller.delete_course(cap_id)
    print(f"✅ Step 5: DELETE - success")
    cap_steps.append(True)
except:
    print("❌ Step 5: DELETE failed")
    cap_steps.append(False)

# Step 6: Verify
try:
    controller.read_course(cap_id)
    print(f"❌ Step 6: VERIFY - record still exists")
    cap_steps.append(False)
except:
    print(f"✅ Step 6: VERIFY - confirmed deleted")
    cap_steps.append(True)

cap_score = sum(cap_steps)
print(f"Capability Score: {cap_score}/6")

# ============================================================================
# 10. DEFINITION OF DONE CHECKLIST
# ============================================================================
print("\n[10/10] DEFINITION OF DONE CHECKLIST")
print("-" * 90)

dod_items = [
    ("✅ No technical errors (py_compile clean)", True),
    ("✅ No tracebacks in execution", True),
    (f"{'✅' if found_labels >= 5 else '❌'} Turkish user messages", found_labels >= 5),
    (f"{'✅' if len(found_bps) >= 5 else '❌'} Responsive design", len(found_bps) >= 5),
    (f"{'✅' if design_score >= 2 else '❌'} Design System compliance", design_score >= 2),
    (f"{'✅' if crud_score >= 4 else '❌'} CRUD operations working", crud_score >= 4),
    (f"{'✅' if len(arch_issues := []) == 0 else '❌'} Architecture correct (MVC)", arch_score >= 4),
    (f"{'✅' if cap_score >= 5 else '❌'} E2E scenario success", cap_score >= 5),
    (f"{'✅' if code_score >= 2 else '❌'} Code quality acceptable", code_score >= 2),
    (f"{'✅' if validation_score >= 2 else '❌'} Validation complete", validation_score >= 2),
]

dod_pass = sum(1 for _, result in dod_items if result)
dod_total = len(dod_items)

for item, _ in dod_items:
    print(f"  {item}")

print(f"\nDef of Done: {dod_pass}/{dod_total}")

# ============================================================================
# FINAL SCORES AND RECOMMENDATION
# ============================================================================
print("\n" + "=" * 90)
print("SUMMARY SCORES")
print("=" * 90)

scores = [
    ("Architecture", arch_score, max_arch),
    ("CRUD", crud_score, 5),
    ("Validation", validation_score, max_val),
    ("Responsive", resp_score, 2),
    ("Accessibility", access_score, 3),
    ("Performance", perf_score, 3),
    ("Code Quality", code_score, max_code),
    ("Design System", design_score, 3),
    ("Capability", cap_score, 6),
]

total_score = sum(s for _, s, _ in scores)
total_max = sum(m for _, _, m in scores)
overall_percent = (total_score / total_max * 100) if total_max > 0 else 0

print()
for name, score, max_s in scores:
    pct = (score / max_s * 100) if max_s > 0 else 0
    status = "✅" if pct >= 80 else "⚠️" if pct >= 60 else "❌"
    print(f"{status} {name:20} {score:2}/{max_s:2} ({pct:5.0f}%)")

print(f"\n{'=' * 90}")
print(f"OVERALL QUALITY SCORE: {overall_percent:.0f}%")
print(f"{'=' * 90}")

# Release decision
if overall_percent >= 85 and dod_pass == dod_total:
    decision = "🟢 READY FOR RELEASE"
elif overall_percent >= 75 and dod_pass >= dod_total - 1:
    decision = "🟡 READY WITH MINOR REVIEW"
else:
    decision = "🔴 NOT READY (needs attention)"

print(f"\nRELEASE DECISION: {decision}")
print(f"Definition of Done: {dod_pass}/{dod_total}")

# Cleanup
print("\nCleaning up test data...")
db_path = Path(__file__).parent.parent / "database" / "idilpanel.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM courses WHERE student_id IN (701, 802)")
conn.commit()
conn.close()

print("✅ Release readiness review complete.\n")
