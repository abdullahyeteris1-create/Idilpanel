# IDİL HIZLI OKUMA
# Design System
# 11 - Topbar

## Amaç

Bu doküman uygulamanın üst navigasyon (Topbar) standardını tanımlar.

Topbar;

- kullanıcının bulunduğu sayfayı gösterir,
- hızlı işlemleri sunar,
- bildirimleri gösterir,
- kullanıcı bilgilerini içerir.

Tüm ekranlarda aynı Topbar kullanılacaktır.

---

# Genel Yapı

Konum

Sayfanın üst kısmı

Yükseklik

72 px

Arka Plan

Surface (#FFFFFF)

Alt Border

1 px Border Color

Padding

24 px

Shadow

None

---

# Yerleşim

+---------------------------------------------------------------+

Sol Alan

↓

Sayfa Başlığı

↓

Breadcrumb

---------------------------------------------------------------

Sağ Alan

↓

Arama

↓

Bildirim

↓

Kullanıcı Profili

↓

Hızlı İşlemler

+---------------------------------------------------------------+

---

# Sol Bölüm

## Sayfa Başlığı

H2

28 px

SemiBold

Örnek

Dashboard

Öğrenciler

Haftalık Program

Ders Kayıtları

---

## Breadcrumb

Boyut

14 px

Renk

Text Secondary

Örnek

Ana Sayfa

>

Öğrenciler

---

# Sağ Bölüm

Sıralama

🔍 Arama

↓

🔔 Bildirimler

↓

➕ Hızlı İşlem

↓

👤 Kullanıcı

---

# Arama Kutusu

Genişlik

320 px

Yükseklik

48 px

Radius

Full

İkon

Sol tarafta

Placeholder

"Öğrenci, kurs veya ders ara..."

---

# Bildirim Butonu

Boyut

48 x 48

Radius

Full

İkon

Bell

Yeni bildirim varsa

Kırmızı rozet

Örnek

🔔 3

---

# Hızlı İşlem Butonu

Primary Button

Metin

+ Yeni

Tıklandığında

Hızlı Menü açılır

Örnek

Yeni Öğrenci

Yeni Ders

Yeni Kurs

Yeni Ölçüm

---

# Kullanıcı Profili

Avatar

40 px

↓

Ad Soyad

↓

Rol

Örnek

👤

Abdullah Yeter

Yönetici

---

# Kullanıcı Menüsü

Tıklandığında

Profil

Şifre Değiştir

Yedek Al

Çıkış Yap

---

# Sayfa Bazlı İşlemler

Dashboard

↓

Bugün

Yenile

Öğrenciler

↓

Yeni Öğrenci

Dışa Aktar

Haftalık Program

↓

Bugün

Bu Hafta

Sonraki Hafta

Ders Kayıtları

↓

Yeni Ders

Filtrele

Ölçümler

↓

Yeni Ölçüm

Grafikler

Raporlar

↓

PDF Oluştur

Excel Aktar

---

# Responsive

Desktop

Tüm bileşenler görünür

Tablet

Arama küçülür

Mobil

Arama gizlenir

Hamburger Menü kullanılır

---

# Animasyon

Dropdown

150 ms

Hover

150 ms

---

# Kullanıcı Deneyimi Kuralları

Her sayfanın başlığı Topbar'da görünmelidir.

Kullanıcı bulunduğu ekranı tek bakışta anlamalıdır.

Arama kutusu tüm modüllerde aynı görünmelidir.

Bildirimler standart ikon ile gösterilmelidir.

Profil alanı her zaman sağ üst köşede bulunmalıdır.

---

# KURAL

Topbar uygulamanın ortak bileşenidir.

Hiçbir ekran kendi Topbar tasarımını oluşturamaz.

Tüm ekranlar yalnızca bu standart Topbar'ı kullanacaktır.
