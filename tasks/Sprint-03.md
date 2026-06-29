# Sprint 03 Plani

## Sprint Amaci
Sprint 03 amaci, uygulamanin veri katmanini adim adim kurmak ve UI tarafinda olusturulan yapilari kalici veri akisi ile guvenli sekilde entegre etmektir.

Ana hedefler:
- SQLite tabanli temel veri altyapisini olusturmak
- Katmanli mimariye uygun Repository ve Service katmanlarini hayata gecirmek
- Student, Weekly Program, Lesson, Measurement ve Dashboard akislarini canli veri ile beslemek
- Sprint 02'de belirlenen mimari ve test disiplinini koruyarak ilerlemek

---

## Epic Listesi
1. Epic 3.1 - SQLite Foundation
2. Epic 3.2 - Repository Layer
3. Epic 3.3 - Service Layer
4. Epic 3.4 - Student CRUD
5. Epic 3.5 - Weekly Program Integration
6. Epic 3.6 - Lesson Records
7. Epic 3.7 - Measurements
8. Epic 3.8 - Dashboard Live Data

---

## Epic Kapsamlari

### Epic 3.1 - SQLite Foundation
Kapsam:
- Veritabani baglanti stratejisini belirlemek
- Temel tablo yapilarini mimari dokuman ile hizalamak
- Migration ve baslatma akisinin teknik cercevesini netlestirmek

### Epic 3.2 - Repository Layer
Kapsam:
- Entity bazli repository sorumluluklarini tanimlamak
- Veri erisim metodlarini standartlastirmak
- SQL sorgularini uygulama katmanlarindan izole etmek

### Epic 3.3 - Service Layer
Kapsam:
- Business Logic kurallarini Service katmanina tasimak
- Is kurallarini merkezi hale getirmek
- Controller/UI tarafinin yalnizca orkestrasyon ve gorunum sorumlulugunda kalmasini saglamak

### Epic 3.4 - Student CRUD
Kapsam:
- Student olusturma, listeleme, guncelleme ve silme akislarini katmanli mimariya uygun sekilde tamamlamak
- Veri dogrulama kurallarini Service katmaninda toplamak

### Epic 3.5 - Weekly Program Integration
Kapsam:
- Weekly Program ekranindaki statik yapiyi veri kaynagi ile baglamak
- Slot, ders plani ve secili kart akislarini canli veriye gecirmek

### Epic 3.6 - Lesson Records
Kapsam:
- Lesson kayitlarinin olusturma ve listeleme akislarini devreye almak
- Course, Schedule ve Lesson iliskilerini veri katmaninda dogru sekilde baglamak

### Epic 3.7 - Measurements
Kapsam:
- Lesson bazli olcum verilerinin kayit ve okuma akislarini eklemek
- Olcum metriklerinin raporlamaya uygun formatta tutulmasini saglamak

### Epic 3.8 - Dashboard Live Data
Kapsam:
- Dashboard metriklerini canli veri kaynagindan beslemek
- Student, Course, Lesson ve Measurement tablolarindan gelen veriyi ozet KPI'lara donusturmek

---

## Yapilacaklar
- Katmanli mimariya uygun veri akislarini epikler bazinda adim adim uygulamak
- Her epic sonunda dogrulama testlerini eksiksiz kosmak
- Mimari dokumanlara uygun entity iliskilerini korumak
- Kod degisikliklerini kucuk, izlenebilir ve testli commit'ler halinde ilerletmek
- UI katmanini business logic'ten ayri tutmak

## Yapilmayacaklar
- UI icinde business logic yazilmayacak
- Controller disina daginik is kurali yerlestirilmeyecek
- Plansiz refactor ile sprint kapsam disina cikilmayacak
- Testsiz epic kapatilmayacak
- Sprint disi ozellik eklenmeyecek

---

## Definition of Done
Bir epic'in tamamlanmis sayilmasi icin asagidaki kosullarin tamami saglanmalidir:
- Epic kapsamindaki tum maddeler uygulanmis olmali
- Mimari katman sinirlari korunmus olmali
- py_compile temiz olmali
- Import Test temiz olmali
- Runtime Test temiz olmali
- Uygulama traceback olmadan acilmali
- Degisiklikler dokumante edilmis olmali

---

## Test Standartlari
Her epic sonunda asagidaki sira zorunludur:
1. py_compile
2. Import Test
3. Runtime Test

Test politikasi:
- Runtime temiz degilse epic tamamlanmis sayilmaz
- Sorun varsa bir sonraki epic'e gecilmez
- Test sonuclari kisa teknik rapor ile kayda alinır

---

## Git Calisma Disiplini
- Her epic icin odakli ve anlamli commit mesajlari kullanilir
- Commit oncesi dogrulama testleri calistirilir
- Gereksiz dosya ve gecici artefaktlar commit edilmez
- Sprint milestone etiketleri yalnizca stabil noktada olusturulur
- Calisma alani (working tree) temiz olmadan release/milestone islemi yapilmaz

---

## Sprint 03 Cikis Kriteri
Sprint 03 sonunda beklenen durum:
- Veri katmani (SQLite + Repository + Service) calisir halde
- Student CRUD tamamlanmis
- Weekly Program, Lesson, Measurement ve Dashboard canli veriyle entegre
- Test zinciri tum epiklerde temiz
