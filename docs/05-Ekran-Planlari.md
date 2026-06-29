# Haftalik Program Ekrani - Figma Uretim Plani

## 1. Dokuman Amaci

Bu dokuman, Haftalik Program ekraninin Figma ortaminda dogrudan uretilebilmesi icin teknik tasarim planini tanimlar.

Kapsam:

- Frame yapisi
- Auto Layout kurallari
- Komponent envanteri
- Variant sistemi
- Etkilesim (prototype) akislari
- Responsive davranis

Bu plan, tasarimci ve gelistirici ekip icin ortak referans olarak kullanilir.

---

## 2. Figma Sayfa Yapisi

Figma dosyasi icin onerilen sayfa duzeni:

| Sayfa | Icerik |
|---|---|
| 00-Cover | Proje adi, versiyon, tarih |
| 01-Foundations | Renk, tipografi, spacing tokenlari |
| 02-Components | Tum UI komponentleri ve variantlari |
| 03-Weekly-Schedule | Haftalik Program ekranlari |
| 04-Prototype | Akislar ve gecisler |
| 05-Handoff | Notlar, olcu, export kurallari |

---

## 3. Ana Frame Spesifikasyonu

### 3.1 Base Frame

| Ozellik | Deger |
|---|---|
| Frame Adi | WeeklySchedule/Desktop |
| Boyut | 1440 x 1024 |
| Arka Plan | #F8FAFC |
| Grid | 12 kolon, 24 px margin, 16 px gutter |
| Ana Padding | 24 px |

### 3.2 Ana Bolumler

| Bolum | Boyut/Oran | Not |
|---|---|---|
| Sidebar | 248 px sabit | Sol navigasyon |
| Header | 80 px sabit | Ust aksiyon alani |
| Main Grid | Esnek | 7 gun x 9 satir |
| Right Panel | 360 px | Secili ders detay paneli |
| Bottom Summary | 72 px | Program ozeti |

---

## 4. Auto Layout Kurallari

### 4.1 Root Layout

- Yatay Auto Layout
- Cocuklar: Sidebar + ContentArea
- Sidebar: Fixed width
- ContentArea: Fill container

### 4.2 ContentArea

- Dikey Auto Layout
- Cocuklar: Header, WeekGridArea, BottomSummary
- Header: Hug content (80 px)
- WeekGridArea: Fill container
- BottomSummary: Fixed (72 px)

### 4.3 WeekGridArea

- Yatay Auto Layout
- Cocuklar: 7 DayColumn + (opsiyonel) RightPanel
- DayColumn: Fill container (esit dagilim)
- Kolonlar arasi bosluk: 12 px

### 4.4 DayColumn

- Dikey Auto Layout
- Cocuklar: DayHeader + 9 adet LessonSlot
- DayHeader: 52 px
- LessonSlot: 84 px
- Satirlar arasi bosluk: 10 px

---

## 5. Komponent Envanteri

## 5.1 Navigasyon Komponentleri

| Komponent | Aciklama |
|---|---|
| Logo/Brand | Sol ustte marka alani |
| Sidebar/Item | Ikon + metin menusu |
| Header/WeekPicker | Hafta secici ve ileri-geri kontrolleri |
| Header/ActionButton | Yazdir, Excel, Yeni Ders |

## 5.2 Program Komponentleri

| Komponent | Aciklama |
|---|---|
| Calendar/DayHeader | Gun adi + tarih |
| Calendar/TimeField | Time Picker tabanli saat girisi |
| Calendar/LessonSlot | Dolu veya bos slot kutusu |
| Card/Lesson | Ogrenci ders karti |
| Card/EmptySlot | Buyuk + ikonlu bos saat kutusu |

## 5.3 Detay Panel Komponentleri

| Komponent | Aciklama |
|---|---|
| Panel/RightDetail | Sag panel kapsayici |
| Panel/Section | Baslik + icerik bloklari |
| Metric/Progress | Ilerleme gostergesi (6/16) |
| Action/QuickAction | Dersi Baslat, Ogrenci Karti, Duzenle, Sil |

## 5.4 Alt Ozet Komponentleri

| Komponent | Aciklama |
|---|---|
| Summary/Bar | Alt sabit ozet container |
| Summary/Item | Toplam Ders, Bos Saat, Toplam Sure |

---

## 6. Variant Sistemi

### 6.1 Sidebar/Item

Property set:

- state: Default, Hover, Active
- icon: Dashboard, Weekly, Students, Lessons, Reports, PDF, Settings

### 6.2 Header/ActionButton

Property set:

- type: Primary, Secondary, Ghost, Danger
- size: M, L
- icon: None, Left, Right
- state: Default, Hover, Pressed, Disabled

### 6.3 Calendar/LessonSlot

Property set:

- kind: Empty, Filled
- state: Default, Hover, Selected
- status: Planlandi, Yapildi, Iptal, TelafiBekliyor, TelafiYapildi, Tamamlandi

### 6.4 Card/Lesson

Property set:

- avatar: On, Off
- status: Planlandi, Yapildi, Iptal, TelafiBekliyor, TelafiYapildi, Tamamlandi
- selected: True, False

### 6.5 Panel/RightDetail

Property set:

- mode: Closed, Open
- lessonState: Planned, Completed, Makeup, Cancelled

---

## 7. Tasarim Tokenlari (Design System Uyumlu)

## 7.1 Renkler

| Token | HEX |
|---|---|
| color.primary | #1E3A8A |
| color.secondary | #14B8A6 |
| color.success | #22C55E |
| color.warning | #F59E0B |
| color.danger | #EF4444 |
| color.purple | #8B5CF6 |
| color.background | #F8FAFC |
| color.surface | #FFFFFF |

## 7.2 Radius ve Shadow

| Token | Deger |
|---|---|
| radius.card | 16 px |
| radius.input | 12 px |
| shadow.soft | 0 2 8 0 rgba(15, 23, 42, 0.06) |

## 7.3 Spacing

4, 8, 16, 24, 32, 48, 64 px

---

## 8. Haftalik Grid Kurallari

- Ekranda her zaman 7 gun kolon olarak gorunur.
- Her gun altinda her zaman 9 satir bulunur.
- Saatler sabit degildir, Time Picker ile kullanici tarafindan duzenlenir.
- Saat alani dropdown degil, dogrudan time picker davranisindadir.
- Dolu slotlar tek tip kart boyutu ile gosterilir.
- Bos slotlar buyuk + ikonu ile aksiyona davet eder.

---

## 9. Sag Panel Icerik Haritasi

Panel bolum sirasi:

1. Ogrenci Bilgileri
2. Ders Bilgileri
3. Kur Bilgisi
4. Ilerleme
5. Son Olcumler
6. Hizli Islemler

Hizli islemler butonlari:

- Dersi Baslat (Primary)
- Ogrenci Karti (Secondary)
- Duzenle (Ghost)
- Sil (Danger)

---

## 10. Prototip Akislari

### Akis-01: Bos Slottan Ders Ekle

1. Bos slot uzerine tikla
2. Sag panel acilir (Open)
3. Time picker ve ogrenci secimi yapilir
4. Kaydet ile kart Filled state'e gecer

### Akis-02: Ders Secimi ve Inceleme

1. Dolu ders kartina tikla
2. Kart Selected state olur
3. Sag panel ders detaylari ile acilir

### Akis-03: Durum Guncelleme

1. Sag panelde durum degistirilir
2. Kart status rengi guncellenir
3. Alt ozet metrikleri yeniden hesaplanir

---

## 11. Responsive Kurallar

| Kirma Noktasi | Davranis |
|---|---|
| Desktop >=1200 | 7 kolon sabit, sag panel yanda |
| Tablet 768-1199 | Grid yatay kaydirma, panel overlay |
| Mobil <=767 | Gun bazli tek kolon, panel full-screen sheet |

---

## 12. Handoff Kontrol Listesi

Tasarim tesliminden once kontrol edilmelidir:

- Tum komponentler adlandirilmis mi?
- Tum variant property'leri tanimli mi?
- Auto Layout kurallari bozulmadan resize oluyor mu?
- Renk ve tipografi tokenlari design system ile birebir mi?
- 7 gun x 9 satir kurali her breakpoint'te korunuyor mu?
- Time picker alani dropdown olarak tasarlanmadi mi?
- Sag panel acik/kapali prototip gecisleri tanimli mi?

---

## 13. Dosya Isimlendirme Standardi

Onerilen frame isimleri:

- WeeklySchedule/Desktop/Default
- WeeklySchedule/Desktop/WithSelection
- WeeklySchedule/Desktop/RightPanelOpen
- WeeklySchedule/Tablet/Default
- WeeklySchedule/Mobile/DayView

Komponent isimleri:

- Sidebar/Item
- Header/WeekPicker
- Calendar/DayColumn
- Calendar/LessonSlot
- Card/Lesson
- Panel/RightDetail
- Summary/Item

Bu isimlendirme, gelistirme handoff surecinde netlik ve hiz saglar.
