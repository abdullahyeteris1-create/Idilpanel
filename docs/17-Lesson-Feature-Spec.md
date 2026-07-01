# Epic 4.0A - Lesson Module Feature Spec

Date: 2026-06-29
Status: Draft for approval

## 1) Feature Objective

Lesson Module, ogrencinin gercek ders yasam dongusunu yonetir:
- ders olusturma
- ders guncelleme
- ders silme

Bu modulin cikisi, Measurement ve Report modulleri icin guvenilir kaynak veri uretmektir.

## 2) Scope

In Scope:
- Lesson kaydi olusturma
- Lesson kaydi guncelleme
- Lesson kaydi silme
- UI -> Controller -> Service -> Repository -> SQLite zinciriyle gercek veri akisi

Out of Scope:
- Yeni mimari degisikligi (Architecture Freeze)
- Yeni tablo tasarimi
- Yeni business domain genisletmesi
- Measurement hesap kurallarini degistirme
- Report format degistirme

## 3) Actors

- Admin / Ogretmen: ders kaydini olusturur, duzeltir, siler.

## 4) Data Model Expectations

Lesson kaydi asgari olarak su alanlari tasir:
- course_id
- lesson_no
- tarih
- metin (opsiyonel)
- durum
- ogretmen_notu (opsiyonel)

Not: Kesin alanlar mevcut schema ve mevcut repository/service kontratlarina gore kullanilir.

## 5) User Flow

1. Kullanici ogrenci/course baglaminda ders olustur ekranina gelir.
2. Zorunlu alanlari girer ve kaydeder.
3. Sistem lesson kaydini SQLite'a yazar.
4. Kullanici kaydi listede gorur.
5. Kullanici lesson kaydini gunceller.
6. Sistem guncel kaydi yazar ve listede gosterir.
7. Kullanici lesson kaydini siler.
8. Sistem kaydi kaldirir ve listeyi yeniler.

## 6) Non-Functional Requirements

- Runtime sirasinda traceback olusmamali.
- CRUD islemleri hatada anlamli mesaj donmeli.
- UI mevcut tasarim dilini korumali.

## 7) Constraints

- Database/Repository/Service/Controller yapisal refactor yok.
- Sadece feature ihtiyaci kadar uygulama kodu degisir.
- Sprint standardi: py_compile -> Import Test -> Runtime Test zorunlu.

## 8) Deliverables

- Lesson Module UI entegrasyonu (mevcut mimariye uygun)
- E2E CRUD dogrulamasi
- Module Review girdisi olacak teknik bulgular
