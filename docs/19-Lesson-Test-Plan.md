# Epic 4.0A - Lesson Module Test Plan

Date: 2026-06-29
Status: Draft for approval

## 1) Test Strategy

Kapsam:
- Feature-level test (Lesson CRUD)
- Katmanlar arasi entegrasyon testi
- Runtime smoke testi

Yontem:
- Otomatik script tabanli E2E CRUD dogrulamasi
- Manuel UI smoke kontrolu

## 2) Test Environments

- Local workspace
- Python virtual environment (.venv)
- SQLite database: database/idilpanel.db

## 3) Test Scenarios

### Scenario A - Create
- Valid payload ile create
- Beklenen: yeni lesson ID donmeli

### Scenario B - Get/List
- Create sonrasi get by id
- Listede kaydin gorunmesi
- Beklenen: kayit tutarli donmeli

### Scenario C - Update
- Mevcut kaydi guncelle
- Beklenen: update sonucu true ve guncel veri okunabilir

### Scenario D - Delete
- Kaydi sil
- Beklenen: delete sonucu true ve kayit listede gorunmez

### Scenario E - Validation Path
- Eksik/hatali zorunlu alanla create/update dene
- Beklenen: anlamli hata mesaji

### Scenario F - Layer Integrity
- UI -> Controller -> Service -> Repository -> SQLite zinciri disina cikilmadigini kontrol et

## 4) Mandatory Validation Order

1. py_compile
2. Import Test
3. Runtime Test
4. Lesson CRUD E2E script

## 5) Exit Decision

PASS kosulu:
- Tum zorunlu validasyonlar temiz
- CRUD E2E senaryolari pass
- Kritik hata yok

FAIL kosulu:
- Runtime traceback
- CRUD zincirinde herhangi bir adimda hata
- Katman ihlali tespiti
