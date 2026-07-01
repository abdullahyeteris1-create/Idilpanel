# Sprint 03 Plani (Revize)

## Hedef Yol Haritasi

Sprint 03:
- Database
- Repository
- Service
- Controller

Sprint 04:
- Epic 4.0A: Lesson Module Specification
- Phase 1: Lesson Module
- Phase 2: Measurement Module
- Phase 3: Report Module

Sprint 05:
- Dashboard
- Real UI Binding
- CRUD Screens
- Analytics
- Release Candidate

---

## Sprint 03 Kapsami

### 1) Database
- SQLite temel altyapi
- Baglanti ve transaction temeli
- Temel tablo ve iliski zemini

### 2) Repository
- BaseRepository + entity repository yapisi
- SQL erisim soyutlamasi
- Hazir CRUD altyapisi

### 3) Service
- BaseService + domain service yapisi
- Foundation ve Business Rules disiplini
- Validation ve temel is kurallari

### 4) Controller
- Service ile UI arasinda orkestrasyon katmani
- UI'yi is kurallarindan ayirma

---

## Sprint 04 Kapsami

### Epic 4.0A) Lesson Module Specification
- Feature Spec hazirlanir
- Sequence Diagram hazirlanir
- Acceptance Criteria hazirlanir
- Test Plan hazirlanir
- Bu dort belge onaylanmadan implementasyon baslamaz

### Phase 1) Lesson Module

#### Epic 4.1A) Lesson Repository
- Lesson repository akislarinin stabil calismasi dogrulanir
- Create/get/list/update/delete tabanli veri erisimi hazirlanir

#### Epic 4.1B) Lesson Service
- Lesson service akisi repository ile baglanir
- Lesson create/update/delete is kurali cagrilari stabil hale getirilir

#### Epic 4.1C) Lesson Controller
- Lesson controller service ile baglanir
- UI istegini service katmanina tasiyan bridge metotlari netlestirilir

#### Epic 4.1D) Lesson UI Binding
- Lesson UI ekrani controller uzerinden gercek CRUD akisini kullanir
- Lesson olusturma/guncelleme/silme akisi UI tarafinda calisir

#### Epic 4.1E) Lesson Event Integration
- Lesson olusturma sonrasi gerekli event tetikleme altyapisi aktif edilir
- Measurement hesaplama ve report uretimi kendi modullerinde kalir
- Modul bagimliligi gevsek bagli (loose coupling) prensibiyle korunur

#### Epic 4.1F) Lesson Module Review
- Lesson modulu icin E2E test sonuclari degerlendirilir
- Teknik borc notlari cikartilir ve Lesson Module "Closed" karari verilir

### Phase 2) Measurement Module

#### Epic 4.2A) Measurement Repository
- Measurement repository akislarinin stabil calismasi dogrulanir
- Create/get/list/update/delete tabanli veri erisimi hazirlanir

#### Epic 4.2B) Measurement Service
- Measurement service akisi repository ile baglanir
- WPM, anlama ve gelisim hesaplamalarina temel olacak service akisi stabilize edilir

#### Epic 4.2C) Measurement Controller
- Measurement controller service ile baglanir
- UI istegini service katmanina tasiyan bridge metotlari netlestirilir

#### Epic 4.2D) Measurement UI
- Measurement UI ekrani controller uzerinden gercek akisla baglanir
- Olcum verisinin olusturma/goruntuleme akisi UI tarafinda calisir

#### Epic 4.2E) Measurement Report Integration
- Measurement ciktilari Report modulu icin entegrasyon noktalarina baglanir
- Olcumden rapora veri aktarim zinciri dogrulanir

#### Epic 4.2F) Measurement Module Review
- Measurement modulu icin E2E test sonuclari degerlendirilir
- Teknik borc notlari cikartilir ve Measurement Module "Closed" karari verilir

### Phase 3) Report Module

#### Epic 4.3A) Report Repository
- Report repository akislarinin stabil calismasi dogrulanir
- Create/get/list/update/delete tabanli veri erisimi hazirlanir

#### Epic 4.3B) Report Service
- Report service akisi repository ile baglanir
- Ogrenci ve veli raporu uretim akislarinin service temel akisi stabil hale getirilir

#### Epic 4.3C) Report Controller
- Report controller service ile baglanir
- UI istegini service katmanina tasiyan bridge metotlari netlestirilir

#### Epic 4.3D) Report Dashboard Integration
- Report ciktilari dashboard veri katmanina baglanir
- Dashboard tarafinda rapor ozet verisi akisi dogrulanir

#### Epic 4.3E) Report PDF Export
- Report ciktilarinin PDF export akisina baglanmasi tamamlanir
- PDF uretim zincirinin rapor verisiyle tutarliligi dogrulanir

#### Epic 4.3F) Report Module Review
- Report modulu icin E2E test sonuclari degerlendirilir
- Teknik borc notlari cikartilir ve Report Module "Closed" karari verilir

---

## Sprint 05 Kapsami

### 1) Dashboard
- Canli veri ozetlerinin dashboard katmanina baglanmasi

### 2) Real UI Binding
- UI ekranlarinin service/controller akislarina tam baglanmasi

### 3) CRUD Screens
- Domain ekranlari icin olusturma, listeleme, guncelleme ve silme akislarinin UI katmaninda tamamlanmasi

### 4) Analytics
- Dashboard ve raporlama katmaninda karar destek metriklerinin genisletilmesi

### 5) Release Candidate
- Sprint ciktilarinin stabilize edilmesi, son dogrulamalarin tamamlanmasi ve yayin adayinin hazirlanmasi

---

## Sprint Exit Criteria

### Sprint 03 Exit Criteria
- ✅ Database tamamlandi
- ✅ Repository tamamlandi
- ✅ Service tamamlandi
- ✅ Controller tamamlandi
- ✅ Tum katmanlar test edildi
- ✅ Git temiz
- ✅ Sprint Review tamamlandi

### Sprint 04 Exit Criteria
- ✅ Lesson Module create/update/delete akisları calisiyor
- ✅ Measurement Module WPM, anlama yuzdesi ve gelisim metriklerini uretiyor
- ✅ Report Module ogrenci ve veli raporu uretiyor
- ✅ Dashboard veri ihtiyaci icin rapor ciktilari hazir
- ✅ Sprint 04 E2E testleri gecti

### Sprint 05 Exit Criteria
- ✅ Dashboard gercek verilerle calisiyor
- ✅ CRUD ekranlari aktif
- ✅ Real UI Binding tamamlandi
- ✅ Analytics calisiyor
- ✅ Release Candidate olusturuldu

---

## Release Freeze (Sprint 05 Sonu)

Release Candidate olusturulduktan sonra yeni ozellik eklenmez.

Yalnizca su degisikliklere izin verilir:
- Bug fix
- Performans iyilestirmesi
- UI polish
- Dokumantasyon

---

## Test ve Kapanis Standardi

Her epic sonunda zorunlu sira:
1. py_compile
2. Import Test
3. Runtime Test

Kurallar:
- Runtime temiz degilse epic tamamlanmis sayilmaz.
- Epic kapsam disina cikilmaz.
- Kod ve plan commitleri ayri tutulur.

---

## Feature Epic Gelistirme Standardi

Artik gelistirme donemi katman odakli degil, ozellik odakli yurur.

Zorunlu epic yasam dongusu:
1. Capability Definition
2. Feature Epic
3. Workflow Review
4. Feature Spec
5. Acceptance Criteria
6. Test Plan
7. Definition of Ready (DoR)
8. Implementation
9. Code Review
10. Refactor (gerekirse)
11. End-to-End Test
12. Definition of Done (DoD)
13. Module Review
14. Closed

Kural:
- Her feature epic, bu sirayi bozmadan tamamlanir.
- Capability Definition tamamlanmadan Workflow Review asamasina gecilmez.
- Workflow Review, Feature Spec, Acceptance Criteria ve Test Plan tamamlanmadan DoR asamasina gecilmez.
- DoR tamamlanmadan implementasyon baslamaz.
- Code Review sonrasi gerekli degilse refactor adimi atlanabilir.
- End-to-End Test, DoD ve Module Review tamamlanmadan epic "Closed" ilan edilmez.

### Definition of Ready (DoR)

Bir feature epic implementasyonuna baslamadan once su sartlarin tamami saglanmis olmalidir:
- Capability Definition hazir
- Workflow Review tamam
- Feature Spec hazir
- Acceptance Criteria hazir
- Test Plan hazir
- Mimari etki analizi tamam
- Kapsam net
- Sprint planina islenmis

DoR kapisi kuralı:
- Yukaridaki maddelerden biri eksikse implementasyon baslamaz.

### Definition of Done (DoD)

Bir epic kapanmadan once su sartlarin tamami saglanmis olmalidir:
- Kod tamamlandi
- Testler gecti
- E2E dogrulandi
- Review tamamlandi
- Git temiz
- Dokumantasyon guncellendi

DoD kapisi kurali:
- Yukaridaki maddelerden biri eksikse epic "Closed" ilan edilmez.

---

## Modul Bazli Calisma ve Kapatma Akisi

Calisma modeli modul bazli ilerler. Her modul kendi icinde tamamen bitirilir ve kapatilir.

Modul tamamlama checklist'i:
- Repository
- Service
- Controller
- UI Integration
- E2E Test

Kapatma kurali:
- Tum checklist maddeleri tamamlanmadan modul "Closed" durumuna alinmaz.
- Bir sonraki modula gecis yalnizca onceki modul "Closed" olduktan sonra yapilir.

Ornek siralama:
- Student Module -> Closed
- Course Module -> Closed
- Sonraki modul -> Closed

---

## Modul Kapanisinda Git Tag Standardi

Her modul Closed oldugunda kucuk bir git tag olusturulur ve remote'a push edilir.

Tag adlandirma ornekleri:
- student-module-complete
- course-module-complete

Release kapanisinda semver release tag'i olusturulur:
- v1.0.0

Ornek komut akisi:
1. git tag student-module-complete
2. git push origin student-module-complete
3. git tag course-module-complete
4. git push origin course-module-complete
5. git tag v1.0.0
6. git push origin v1.0.0

---

## Sprint Kapanisinda Git Standardi

Sprint boyunca plan dosyasi commit disinda tutulur. Sprint sonunda asagidaki sira uygulanir:

1. Sprint Review tamamlanir.
2. tasks/Sprint-03.md son kez guncellenir.
3. Plan dosyasi tek basina commit edilir.
4. Sprint kapanis tag'i olusturulur ve push edilir.

Ornek komut akisi:
1. git add tasks/Sprint-03.md
2. git commit -m "Sprint 03 documentation finalized"
3. git push origin main
4. git tag v0.3.0-core-architecture
5. git push origin v0.3.0-core-architecture

---

## Git Branching Standardi (Release Branch Mantigi)

Milestone bazli tek hat gelisim yerine feature branch akisi kullanilir.

Temel akış:
1. main
2. feature/lesson-module
3. feature/measurement
4. feature/report
5. feature/dashboard

Kurallar:
- Her modül/ozellik kendi feature branch'inde gelistirilir.
- Feature branch tamamlaninca main'e merge edilir.
- Merge oncesi zorunlu dogrulama sirası korunur: py_compile -> Import Test -> Runtime Test.
- Module Review tamamlanmadan ilgili feature branch merge edilmez.

---

## Not

Bu dosya yasayan sprint planidir ve Sprint 03 sonunda tek basina commit edilerek kapanir.
