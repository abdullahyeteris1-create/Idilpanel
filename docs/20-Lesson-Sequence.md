# Epic 4.0A - Lesson Module Sequence

Date: 2026-06-29
Status: Draft for approval

## Purpose

Bu belge, Lesson Module ozelliginin adim adim islem sirasini tanimlar.
Kodlama oncesi ekipte ortak akisi netlestirmek icin kullanilir.

## End-to-End Sequence

1. Kullanici lesson ekranina girer.
2. Kullanici course baglamini secer.
3. Kullanici lesson olusturma formunu doldurur.
4. UI, LessonController.create_lesson() cagrisi yapar.
5. Controller, LessonService.create_lesson() cagrisi yapar.
6. Service, LessonRepository.create() cagrisi yapar.
7. Repository, SQLite'a kayit yazar.
8. Basarili sonuc UI'ya doner ve liste yenilenir.

## Full Lifecycle Sequence (Reference)

Bu referans akis, Lesson olusturma sonrasi olcum ve rapor guncellemesini tek zincirde gosterir:

1. User
2. Weekly Program
3. LessonController.create_lesson()
4. LessonService.create_lesson()
5. LessonRepository.create()
6. SQLite
7. MeasurementService.calculate()
8. ReportService.refresh()
9. Dashboard.update()

## Update Sequence

1. Kullanici mevcut lesson kaydini secer.
2. Kullanici alanlari gunceller.
3. UI, LessonController.update_lesson() cagrisi yapar.
4. Controller, LessonService.update_lesson() cagrisi yapar.
5. Service, LessonRepository.update() cagrisi yapar.
6. Repository, SQLite kaydini gunceller.
7. Sonuc UI'ya doner ve liste yenilenir.

## Delete Sequence

1. Kullanici mevcut lesson kaydini secer.
2. UI, LessonController.delete_lesson() cagrisi yapar.
3. Controller, LessonService.delete_lesson() cagrisi yapar.
4. Service, LessonRepository.delete() cagrisi yapar.
5. Repository, SQLite kaydini siler.
6. Sonuc UI'ya doner ve liste yenilenir.

## Layer Contract

- UI sadece Controller ile konusur.
- Controller sadece Service ile konusur.
- Service sadece Repository ile konusur.
- Repository sadece Database ile konusur.

## Failure Handling

- Her adimda hata olursa zincir bir ust katmana hata olarak doner.
- UI, hatayi kullaniciya anlamli mesaj olarak gosterir.
- Traceback olusturan durumlar bug olarak kaydedilir.

## Approval Gate

Lesson implementasyonu baslamadan once bu sequence belgesi Feature Spec,
Acceptance Criteria ve Test Plan ile birlikte onaylanir.
