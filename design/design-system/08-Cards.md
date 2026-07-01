# IDİL HIZLI OKUMA
# Design System
# 08 - Cards

## Amaç

Bu doküman uygulamada kullanılacak tüm kart (Card) bileşenlerini tanımlar.

Kartlar uygulamanın temel yapı taşıdır.

Dashboard, Öğrenciler, Haftalık Program, Ders Kayıtları, Ölçümler,
Raporlar ve Ayarlar ekranları yalnızca bu kart tiplerini kullanacaktır.

Yeni kart tipi oluşturulmaz.

---

# Genel Kart Standardı

Arka Plan

Surface (#FFFFFF)

Radius

16 px

Padding

24 px

Shadow

Medium

Border

1 px Border Color

Hover

Çok hafif gölge artışı

İç Boşluk

24 px

Kartlar Arası Boşluk

24 px

---

# CARD TYPE 1

## Form Card

Amaç

Veri giriş ekranları

Örnek

Öğrenci Bilgileri

Kurs Bilgileri

Ders Bilgileri

İçerik

Başlık

↓

Form Alanları

↓

Butonlar

Yapı

+---------------------------------------+

👤 Başlık

-----------------------------------------

Ad Soyad

Sınıf

Telefon

...

-----------------------------------------

[ Temizle ] [ Kaydet ]

+---------------------------------------+

---

# CARD TYPE 2

## List Card

Amaç

Kayıt listeleri

Örnek

Öğrenci Listesi

Kurs Listesi

Ders Listesi

İçerik

Başlık

↓

Arama

↓

Filtreler

↓

Liste

Yapı

+---------------------------------------+

📋 Öğrenci Listesi

🔍 Ara

○ Tümü

○ Aktif

○ Pasif

○ Tamamlandı

-----------------------------------------

👤 Abdullah Yeter

5-A • 2. Kur

Aktif

-----------------------------------------

👤 Ayşe Demir

6-B • 1. Kur

Tamamlandı

+---------------------------------------+

---

# CARD TYPE 3

## Statistic Card

Amaç

Dashboard istatistikleri

Örnek

Toplam Öğrenci

Bugünkü Ders

Tamamlanan Ders

Aktif Kurs

Yapı

+---------------------------+

👥

125

Toplam Öğrenci

+---------------------------+

---

# CARD TYPE 4

## Chart Card

Amaç

Grafikler

Örnek

Okuma Hızı

Anlama

Başarı

Gelir

Yapı

+--------------------------------+

📈

Grafik

+--------------------------------+

---

# CARD TYPE 5

## Calendar Card

Amaç

Haftalık Program

Yapı

+--------------------------------+

📅

Haftalık Takvim

+--------------------------------+

---

# CARD TYPE 6

## Report Card

Amaç

Rapor Görüntüleme

Örnek

Veli Raporu

Gelişim Raporu

PDF Önizleme

Yapı

+--------------------------------+

📄

Rapor

+--------------------------------+

---

# CARD TYPE 7

## Information Card

Amaç

Bilgilendirme

Uyarılar

Sistem Mesajları

Örnek

Yedekleme başarılı

Bugün 8 ders var

Lisans süresi doluyor

---

# CARD TYPE 8

## Empty State Card

Amaç

Liste boş olduğunda gösterilir.

İçerik

İkon

↓

Başlık

↓

Açıklama

↓

Ana Buton

Örnek

Henüz öğrenci eklenmemiş.

[ Yeni Öğrenci Ekle ]

---

# Kart Başlıkları

Kart başlıkları

H3

22 px

Medium

Kart açıklamaları

Body

16 px

---

# Kart Butonları

Kart içinde en fazla

2

Primary Button bulunabilir.

Diğer işlemler Secondary Button kullanmalıdır.

---

# Kart İçi Form

Inputlar

16 px

boşluk ile dizilir.

---

# Responsive

Desktop

İki kolon

Tablet

Tek kolon

Mobil

Tek kolon

---

# KURAL

Kartlar uygulamanın temel yapı taşıdır.

Hiçbir sayfa kart kullanmadan oluşturulmaz.

Bütün ekranlar yalnızca bu dokümanda tanımlanan kart tiplerini kullanacaktır.
