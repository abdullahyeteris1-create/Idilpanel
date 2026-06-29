# 1. Belgenin Amaci

Bu belgenin amaci, Sprint 03 ve sonraki gelistirmelerde veri akisini tek bir resmi referans altinda standartlastirmaktir.

Ana hedefler:
- Veri akisinin standartlastirilmasi
- Katmanlar arasi sorumluluklarin netlestirilmesi
- Business Logic'in sadece dogru katmanda calistirilmasinin tanimlanmasi
- SQLite tabanli kalici veri mimarisi icin temel cercevenin kurulmasi

---

# 2. Genel Mimari

Sistem katmanli bir yapi ile tasarlanir:

UI
↓
Controller
↓
Service
↓
Repository
↓
SQLite Database

Katman sorumluluklari:
- UI: Kullaniciya gorunum sunar, veri gosterir, kullanici girdisini toplar.
- Controller: UI olaylarini yakalar, uygun Service cagrisini tetikler, sonuc geri donusunu UI'a iletir.
- Service: Is kurallarini (Business Logic) uygular, dogrulama/hesaplama/karar mekanizmasini yonetir.
- Repository: Veritabanina erisim soyutlamasi saglar, SQL/kalicilik islemlerini ust katmandan ayirir.
- SQLite Database: Kalici veri kaynagidir; tablolar, iliskiler, indeksler ve veri butunlugu burada korunur.

---

# 3. Temel Veri Akisi

Akis:

Student
↓
Course
↓
Schedule
↓
Lesson
↓
Measurement
↓
Report

## Student
- Gorevi: Ogrencinin kimlik ve temel profil bilgisini temsil etmek.
- Sorumlulugu: Ogrenciye ait tum egitsel surecin baglandigi ana kayit olmaktir.
- Sonraki adima aktarilan veri: student_id, ad/soyad, sinif, aktiflik durumu.

## Course
- Gorevi: Ogrenciye tanimli egitim paketini/kur planini tutmak.
- Sorumlulugu: Hedef kazanimi, sure, kur seviyesi ve ders kapsam bilgisini yonetmek.
- Sonraki adima aktarilan veri: course_id, student_id, kur_no, toplam_ders_sayisi, baslangic/bitis bilgileri.

## Schedule
- Gorevi: Derslerin haftalik zaman planini temsil etmek.
- Sorumlulugu: Hangi gun/saat slotunda hangi dersin planlanacagini belirtmek.
- Sonraki adima aktarilan veri: schedule_id, course_id, gun, saat, slot_tipi, planlama_durumu.

## Lesson
- Gorevi: Gerceklesen veya planlanan tekil ders kaydini temsil etmek.
- Sorumlulugu: Dersin tarihi, icerigi, sureci ve durumunu izlemek.
- Sonraki adima aktarilan veri: lesson_id, course_id, schedule_id, tarih, durum, konu_ozeti.

## Measurement
- Gorevi: Lesson ciktilarini olcmek ve performans metriklerini kaydetmek.
- Sorumlulugu: Dogruluk, hiz, kavrama, tamamlama gibi olcumleri standart formatta tutmak.
- Sonraki adima aktarilan veri: measurement_id, lesson_id, metrik_degerleri, notlar, olcum_zamani.

## Report
- Gorevi: Course/Lesson/Measurement verisini raporlanabilir bir gorunume donusturmek.
- Sorumlulugu: Donemsel ilerleme, durum ozetleri ve karar destek ciktisi uretmek.
- Sonraki adima aktarilan veri: report_id, course_id, kapsanan_lessonlar, ozet_metrikler, oneri/yorum.

---

# 4. Entity Iliskileri

- Student -> bircok Course
  - Tur: bire-cok (1-N)
  - Aciklama: Bir ogrenci farkli donemlerde birden fazla course kaydina sahip olabilir.

- Course -> bircok Schedule
  - Tur: bire-cok (1-N)
  - Aciklama: Her course birden fazla gun/saat plani uretebilir.

- Course -> bircok Lesson
  - Tur: bire-cok (1-N)
  - Aciklama: Bir course kapsaminda birden fazla ders islenir.

- Lesson -> bir Measurement
  - Tur: bire-bir (1-1) (ilk mimari hedefi)
  - Aciklama: Her lesson icin tek olcum seti tutulur.

- Course -> bircok Report
  - Tur: bire-cok (1-N)
  - Aciklama: Ayni course icin farkli donemlerde veya formatlarda birden fazla rapor uretilebilir.

- Report -> bircok Lesson
  - Tur: cok-cok (N-N) (join tablo ile)
  - Aciklama: Bir rapor birden fazla dersi kapsar; bir ders farkli raporlarda yer alabilir.

---

# 5. Katman Bazli Veri Akisi

UI
↓
Controller
↓
Service
↓
Repository
↓
SQLite

## UI
- Giris: Kullanici etkileşimi (tiklama, form girdisi, filtre).
- Islem: Girdi toplama, gorunumde durum yansitma.
- Cikis: Controller'a olay/veri iletimi.

## Controller
- Giris: UI olaylari ve ham girdi.
- Islem: Akis yonlendirme, ilgili Service metodunu cagirma.
- Cikis: Service'e normalize edilmis talep; UI'a sonuc modeli.

## Service
- Giris: Controller'dan gelen is talepleri.
- Islem: Business Logic, kural dogrulama, hesaplama, durum gecisleri.
- Cikis: Repository'ye kalicilik talebi veya Controller'a is sonucu DTO'su.

## Repository
- Giris: Service'in veri erisim talepleri.
- Islem: SQL sorgu/calismasi, mapleme, transaction yonetimi.
- Cikis: Service'e domain'e uygun veri modeli.

## SQLite
- Giris: Repository SQL islemleri.
- Islem: Veri yazma/okuma/guncelleme/silme, constraint kontrolu.
- Cikis: Kalici veri ve sorgu sonuc setleri.

---

# 6. Is Kurallarinin Konumu

- UI
  - Yalnizca gorunum, durum gosterimi ve temel kullanici etkileşimi.
- Controller
  - UI ile Service arasinda istek/yanit orkestrasyonu.
- Service
  - Tum Business Logic burada calisir.
- Repository
  - Veri erisimi ve kalicilik soyutlamasi.
- SQLite
  - Kalici veri depolama ve butunluk kurallari.

Kesin kural:
- Is kurallari UI icinde yazilmamalidir.
- UI katmani karar vermez; karar Service katmaninda verilir.

---

# 7. CRUD Akisi

## Create
UI -> Controller -> Service (kural/dogrulama) -> Repository (INSERT) -> SQLite -> Repository -> Service -> Controller -> UI

## Read
UI -> Controller -> Service (filtreleme kurali) -> Repository (SELECT) -> SQLite -> Repository -> Service -> Controller -> UI

## Update
UI -> Controller -> Service (durum gecisi + dogrulama) -> Repository (UPDATE) -> SQLite -> Repository -> Service -> Controller -> UI

## Delete
UI -> Controller -> Service (silme politikalari) -> Repository (DELETE/soft-delete) -> SQLite -> Repository -> Service -> Controller -> UI

Not:
- Transaction gerektiren cok adimli islemlerde transaction siniri Repository katmaninda yonetilir.

---

# 8. Haftalik Program Veri Akisi

Bos slot
↓
Planlanan ders
↓
Lesson
↓
Measurement
↓
Dashboard
↓
Report

Adim aciklamalari:
- Bos slot: Programdaki atanmamis zaman araligini temsil eder.
- Planlanan ders: Slot bir Course baglamiyla eslenir ve plan kaydi olusur.
- Lesson: Planlanan kayit ders gerceklestiginde lesson kaydina donusur.
- Measurement: Ders sonunda olcum metrikleri lesson'a bagli kaydedilir.
- Dashboard: Guncel lesson/measurement verileri ozet KPI'lara donusturulur.
- Report: Dashboard ve ham verilerden donemsel/analitik cikti uretilir.

---

# 9. Dashboard Veri Kaynaklari

Dashboard'in temel veri kaynaklari:
- Students: Toplam/aktif ogrenci sayilari, sinif dagilimi.
- Courses: Kur bazli ilerleme, tamamlanma oranlari.
- Lessons: Planlanan-gerceklesen ders, durum dagilimi.
- Measurements: Performans metrikleri, trend ve risk sinyalleri.
- Schedules (onerilen ek kaynak): Bos/dolu slot oranlari, haftalik yogunluk.

Dashboard, dogrudan UI hesaplamasi yerine Service katmaninda uretilecek ozet veriyi kullanmalidir.

---

# 10. Gelecek Genisletmeler

Mimari, asagidaki genisletmeleri destekleyecek sekilde katmanli ve moduler tasarlanmistir:
- Coklu ogretmen
- Coklu sube
- Online ders
- Gelir takibi
- Odeme sistemi
- Yedekleme
- Senkronizasyon

Genisleme prensibi:
- Yeni senaryolar once domain/entity seviyesinde modellenir.
- Is kurallari Service katmanina eklenir.
- Repository kalicilik uyarlamasi yapar.
- UI yalnizca yeni gorunum/etkileşim ihtiyacini yansitir.

---

# Sonuc

Bu dokuman, Sprint 03 ve sonraki tum gelistirmelerde veri akisinin resmi referansi olarak kullanilacaktir.
Katman sinirlari korunarak ilerlemek; test edilebilirlik, bakim kolayligi ve olceklenebilirlik icin zorunludur.
