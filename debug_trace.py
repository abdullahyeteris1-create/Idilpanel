#!/usr/bin/env python3
"""Trace save button click through all layers to identify exact failure point."""

import sys
sys.path.insert(0, 'src')

def main():
    print("="*70)
    print("SAVE BUTTON CLICK TRACE - Layer-by-Layer Diagnosis")
    print("="*70)
    print()
    
    # Payload that user would submit from form
    form_payload = {
        'ad_soyad': 'Debug Trace Student',
        'sinif': '2-A',
        'baslangic_tarihi': '2026-04-01',
        'durum': 'Aktif',
        # NOTE: No kur field (user didn't select course)
    }
    
    print("Form Input (from UI):")
    for key, value in form_payload.items():
        print(f"  {key}: {value}")
    print()
    
    # Layer 1: UI
    print("-"*70)
    print("LAYER 1: UI (Form Input)")
    print("-"*70)
    print(f"✓ Form displays 12 fields")
    print(f"✓ User fills: {list(form_payload.keys())}")
    print(f"✓ User clicks [Kaydet] button")
    print(f"✓ on_click=_handle_create triggered")
    print()
    
    # Layer 2: Controller
    print("-"*70)
    print("LAYER 2: StudentController")
    print("-"*70)
    
    try:
        from controllers import build_student_controller
        controller = build_student_controller()
        print(f"✓ StudentController instantiated")
        print(f"✓ controller.create_student(payload) called with:")
        print(f"  {form_payload}")
        print()
    except Exception as e:
        print(f"✗ FAILED at controller instantiation: {e}")
        return
    
    # Layer 3: Service
    print("-"*70)
    print("LAYER 3: StudentService.create_student()")
    print("-"*70)
    
    try:
        # Trace through service manually
        from services.student_service import StudentService
        from repositories.student_repository import StudentRepository
        from database.connection_manager import db_manager
        
        service = StudentService(StudentRepository(db_manager))
        print(f"✓ StudentService instantiated")
        print(f"✓ Calling service.validate_student(payload)...")
        
        validated = service.validate_student(form_payload)
        print(f"✓ Validation passed")
        print(f"✓ Calling _to_repository_payload()...")
        
        repo_payload = service._to_repository_payload(validated)
        print(f"✓ Converted to repository payload:")
        for key, value in repo_payload.items():
            print(f"    {key}: {value}")
        print()
        
    except Exception as e:
        print(f"✗ FAILED at service layer: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Layer 4: Repository
    print("-"*70)
    print("LAYER 4: StudentRepository.insert()")
    print("-"*70)
    
    try:
        repo = StudentRepository(db_manager)
        print(f"✓ StudentRepository instantiated")
        print(f"✓ Calling repository.create(repo_payload)...")
        print(f"  Payload fields: {list(repo_payload.keys())}")
        
        student_id = repo.create(repo_payload)
        print(f"✓ INSERT executed successfully")
        print(f"✓ New student ID: {student_id}")
        print()
        
    except Exception as e:
        print(f"✗ FAILED at repository layer!")
        print(f"✗ Error: {e}")
        print()
        
        # Additional diagnostics
        print("-"*70)
        print("LAYER 5: SQLite Database")
        print("-"*70)
        print(f"✗ SQLite INSERT failed with:")
        print(f"   {str(e)}")
        print()
        
        # Check what fields are being sent
        print("Debug Info:")
        print(f"  Repository payload keys: {list(repo_payload.keys())}")
        print(f"  Repository payload: {repo_payload}")
        print()
        
        # Check schema
        print("Database Schema Analysis:")
        import sqlite3
        conn = sqlite3.connect('database/idilpanel.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("PRAGMA table_info(students)")
            columns = cursor.fetchall()
            print("  Students table columns:")
            for col in columns:
                col_name = col['name']
                col_type = col['type']
                col_notnull = col['notnull']
                col_pk = col['pk']
                constraint = "(NOT NULL)" if col_notnull else "(nullable)"
                pk_mark = " [PRIMARY KEY]" if col_pk else ""
                print(f"    - {col_name:20} {col_type:15} {constraint}{pk_mark}")
        finally:
            conn.close()
        
        print()
        print("="*70)
        print("ROOT CAUSE ANALYSIS")
        print("="*70)
        
        if "NOT NULL constraint failed" in str(e):
            constraint_field = str(e).split("students.")[-1].strip() if "students." in str(e) else "unknown"
            print(f"✗ Field '{constraint_field}' is NOT NULL but no value provided")
            print(f"✗ Repository payload missing required field: '{constraint_field}'")
            print(f"✗ Service is not including this field in repository payload")
        
        return
    
    print("="*70)
    print("✓ ALL LAYERS SUCCESSFUL - Student saved to database")
    print("="*70)

if __name__ == "__main__":
    main()
