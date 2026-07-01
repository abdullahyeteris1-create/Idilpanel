# IDİL HIZLI OKUMA
# Design System
# 13 - Layout

## Amaç

Bu doküman uygulamanın genel yerleşim (Layout) standartlarını tanımlar.

Dashboard, Öğrenciler, Haftalık Program,
Ders Kayıtları, Ölçümler,
Raporlar ve Ayarlar ekranları
yalnızca bu yerleşim sistemini kullanacaktır.

Hiçbir ekran kendi layout yapısını oluşturamaz.

---

# Genel Sayfa Yapısı

+-----------------------------------------------------------------------+

Sidebar

↓

Topbar

↓

Content Area

↓

Page Footer (Opsiyonel)

+-----------------------------------------------------------------------+

---

# Uygulama Yerleşimi

+----------------+-------------------------------------------------------+

Sidebar

260 px

+

Content Area

Expand

+----------------+-------------------------------------------------------+

---

# Sidebar

Genişlik

260 px

Daraltılmış

72 px

Sabit

Evet

---

# Topbar

Yükseklik

72 px

Sabit

Evet

---

# Content Area

Padding

24 px

Maksimum Genişlik

1600 px

Yatay Ortala

Evet

Scroll

Dikey

Yatay Scroll

Sadece gerektiğinde

---

# Grid Sistemi

12 Column Grid

Desktop

12 kolon

Tablet

8 kolon

Mobil

4 kolon

Grid Gap

24 px

---

# Sayfa Boşlukları

Üst

24 px

Alt

24 px

Sol

24 px

Sağ

24 px

---

# Kartlar Arası Boşluk

24 px

---

# Form Alanları

Inputlar arası

16 px

Form grupları arası

24 px

---

# Dashboard Yerleşimi

1. Satır

4 adet Statistic Card

(3-3-3-3)

↓

2. Satır

Grafik

(8)

+

Yaklaşan Dersler

(4)

↓

3. Satır

Son Ölçümler

(6)

+

Bugünkü Dersler

(6)

---

# Öğrenciler Yerleşimi

+--------------------------+--------------------------------------+

Form Card

35%

+

Liste Card

65%

+--------------------------+--------------------------------------+

Form sabit genişlik

420 px

Liste

Expand

---

# Haftalık Program

Tam genişlik

7 Gün

↓

Her gün eşit genişlik

↓

Yatay Scroll yalnızca küçük ekranlarda

---

# Ders Kayıtları

+----------------------+--------------------------------------+

Filtre Paneli

30%

+

Ders Listesi

70%

+----------------------+--------------------------------------+

---

# Ölçümler

Üst

Filtreler

↓

Alt

Grafik

+

Liste

---

# Raporlar

Sol

Filtre

30%

↓

Sağ

Rapor Önizleme

70%

---

# Ayarlar

Kategori Menüsü

25%

↓

İçerik

75%

---

# Dialoglar

Maksimum Genişlik

640 px

Padding

24 px

Radius

16 px

---

# Responsive

Desktop

>= 1440 px

Sidebar açık

İki kolon

---

Laptop

1366–1439 px

Sidebar açık

İki kolon

Form daraltılabilir

---

Tablet

768–1365 px

Sidebar daraltılabilir

Tek kolon

Kartlar alt alta

---

Mobil

< 768 px

Hamburger Menü

Tek kolon

Kartlar tam genişlik

---

# Minimum Çözünürlük

Desteklenen Minimum

1366 × 768

Bu çözünürlükte

- Sidebar kullanılabilir olmalı
- Topbar bozulmamalı
- Haftalık Program erişilebilir olmalı
- Öğrenci ekranı kaymadan kullanılabilmeli

---

# Maksimum İçerik Genişliği

1600 px

Daha büyük ekranlarda

İçerik ortalanmalıdır.

---

# Scroll Kuralları

Sayfa

Dikey Scroll

Sidebar

Scroll yok

Topbar

Scroll yok

Tablolar

Gerekirse kendi içinde

Haftalık Program

Sadece küçük ekranlarda yatay scroll

---

# Kullanıcı Deneyimi Kuralları

Sayfa açıldığında

İlk görünen alan her zaman sayfa başlığı olmalıdır.

Kullanıcı hiçbir zaman
yatay scroll yapmak zorunda bırakılmamalıdır.

Yatay scroll yalnızca
Haftalık Program
ve çok geniş tablolar için kullanılabilir.

---

# KURAL

Bütün ekranlar bu layout sistemine göre oluşturulacaktır.

Yeni sayfa tasarlanırken
önce bu doküman referans alınacaktır.

Layout standardı dışına çıkılmaz.
