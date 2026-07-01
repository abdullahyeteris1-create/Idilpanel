# IDİL HIZLI OKUMA
# Design System
# 09 - Tables

## Amaç

Bu doküman uygulamadaki tüm liste ve tablo görünümünü standartlaştırır.

Öğrenci Listesi
Kurs Listesi
Ders Listesi
Ölçüm Listesi
Rapor Listesi

yalnızca bu standartları kullanacaktır.

---

# Tasarım Prensibi

Klasik Excel görünümü kullanılmaz.

Tablolar;

• sade
• okunabilir
• kart hissi veren
• satır odaklı
• öğretmen dostu

olmalıdır.

---

# Genel Yapı

Kart

↓

Başlık

↓

Arama

↓

Filtreler

↓

Tablo

↓

Sayfalama

---

# Table Container

Arka Plan

Surface

Radius

16 px

Padding

24 px

Shadow

Medium

---

# Tablo Başlığı

H3

22 px

Medium

Örnek

👨‍🎓 Öğrenci Listesi

📚 Kurs Listesi

📖 Ders Kayıtları

---

# Search

Tablonun üstünde bulunur.

Sol tarafta arama ikonu.

Placeholder örneği

"Öğrenci ara..."

Radius

Full

---

# Filtreler

Aramanın altında bulunur.

Örnek

○ Tümü

○ Aktif

○ Pasif

○ Tamamlandı

Dropdown filtre gerekiyorsa sağ tarafta yer alır.

---

# Kolonlar

Kolon başlıkları

Bold

16 px

Alt çizgi

Border Color

Arka Plan

#F8FAFC

---

# Satırlar

Satır yüksekliği

56 px

Hover

Çok hafif gri

Seçili satır

Primary renk tonunda açık arka plan

---

# Satır İçeriği

İlk kolon

Avatar veya ikon

İkinci kolon

Ana bilgi

Üçüncü kolon

Alt bilgi

Son kolon

Durum etiketi

---

# Durum Etiketleri

🟢 Aktif

Yeşil

🟡 Pasif

Turuncu

🔵 Tamamlandı

Mavi

🔴 Silinmiş

Kırmızı

---

# Satır Aksiyonları

Her satırın sonunda

⋮

(Üç nokta menüsü)

İçerik

Düzenle

Sil

Detay Gör

Rapor Oluştur

Doğrudan çok sayıda ikon kullanılmaz.

---

# Sayfalama

Tablonun altında bulunur.

Göster

10

25

50

100

kayıt

---

# Boş Liste

Liste boşsa

Empty State Card kullanılır.

Örnek

📄

Henüz kayıt bulunmuyor.

[ Yeni Kayıt Oluştur ]

---

# Responsive

Desktop

Tam tablo görünümü

Tablet

Bazı kolonlar gizlenebilir.

Mobil

Kart görünümüne dönüşebilir.

---

# Performans

100+ kayıt olduğunda

Sayfalama kullanılmalıdır.

---

# KURAL

Hiçbir tablo doğrudan DataTable görünümünde bırakılmaz.

Tüm tablolar bu tasarım standardına uymalıdır.

Liste okunabilirliği, veri yoğunluğundan daha önemlidir.
