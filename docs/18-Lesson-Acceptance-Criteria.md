# Epic 4.0A - Lesson Module Acceptance Criteria

Date: 2026-06-29
Status: Draft for approval

## Functional Criteria

1. Create Lesson
- Given gecerli lesson verisi
- When kullanici olustur islemi yapar
- Then sistem yeni lesson kaydi olusturur ve ID doner

2. Get/List Lesson
- Given mevcut lesson kayitlari
- When kullanici getir/listele islemi yapar
- Then sistem dogru kaydi/kayitlari doner

3. Update Lesson
- Given mevcut lesson kaydi
- When kullanici gecerli degisikliklerle guncelleme yapar
- Then lesson kaydi guncellenir ve sonuc true/updated olarak doner

4. Delete Lesson
- Given mevcut lesson kaydi
- When kullanici silme islemi yapar
- Then kayit silinir ve sonuc true/deleted olarak doner

## Architecture Criteria

1. UI sadece LessonController ile konusur.
2. LessonController sadece LessonService ile konusur.
3. LessonService, lesson akisi icin LessonRepository ve gerekli oldugunda StudentRepository/CourseRepository ile konusur.
4. Repository katmani sadece SQLite ile konusur.
5. Katman atlama olmaz (UI -> Controller -> Service -> Repository -> SQLite).

## Validation and Stability Criteria

1. py_compile sonucu temiz.
2. Import Test sonucu temiz.
3. Runtime Test sonucu temiz.
4. E2E lesson CRUD zinciri create/get/list/update/delete olarak pass.

## Completion Criteria

- Tum functional kriterler PASS.
- Tum architecture kriterleri PASS.
- Tum validation kriterleri PASS.
- Module Review icin teknik borc notlari cikarilmis.
