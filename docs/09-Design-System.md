# İDİL HIZLI OKUMA Yönetim Sistemi - UI Design System

## Belgenin Amacı

Bu doküman yalnızca bir tasarım rehberi değildir. Aşağıdaki ekranların tamamında ortak bir tasarım dili oluşturmak amacıyla hazırlanmıştır:

- Dashboard
- Haftalık Program
- Öğrenci Yönetimi
- Öğrenci Kartı
- Ders Ekranı
- Gelişim Raporu
- PDF Önizleme

Bu belge; ürün tutarlılığı, geliştirici-hızlı teslim uyumu ve kullanıcı deneyiminde standartlaşma için ana referanstır.

---

## 1. Tasarım Felsefesi

Tasarım yaklaşımı aşağıdaki ilkelere dayanır:

- Modern
- Minimal
- Profesyonel
- Öğretmen odaklı
- Hızlı kullanım
- Az tıklama
- Bilgiye tek bakışta ulaşma
- Masaüstü öncelikli
- Mobil uyumlu

Tasarım kararlarında öncelik sırası:

1. Anlaşılabilirlik
2. Hız
3. Tutarlılık
4. Görsel kalite

---

## 2. Renk Paleti

| Kullanım | Renk | HEX |
|---|---|---|
| Primary | Lacivert | #1E3A8A |
| Secondary | Turkuaz | #14B8A6 |
| Success | Yeşil | #22C55E |
| Warning | Turuncu | #F59E0B |
| Danger | Kırmızı | #EF4444 |
| Purple | Mor | #8B5CF6 |
| Background | Açık Gri | #F8FAFC |
| Surface | Beyaz | #FFFFFF |

Renk kullanım kuralları:

- Primary: Ana eylemler, aktif durumlar, vurgu başlıkları.
- Secondary: İkincil vurgu, bilgi kartı etiketleri.
- Success/Warning/Danger: Durum mesajları ve geri bildirimler.
- Background ve Surface: Okunabilir kontrast ve katman ayrımı.

---

## 3. Tipografi

Ana yazı tipi: Poppins

| Stil | Amaç | Önerilen Ağırlık | Boyut Aralığı |
|---|---|---|---|
| Sayfa Başlığı | Sayfa ana başlığı | 700 | 28-36 px |
| Kart Başlığı | Kart üst başlığı | 600 | 18-22 px |
| Alt Başlık | Bölüm başlıkları | 600 | 16-20 px |
| Normal Yazı | Gövde metni | 400 | 14-16 px |
| Küçük Yazı | Yardımcı metinler | 400 | 12-13 px |
| Buton Yazısı | Eylem metni | 600 | 14-16 px |

Tipografi kuralları:

- Satır uzunluğu okunabilirlik için mümkünse 60-90 karakter aralığında tutulur.
- Başlık ve gövde arasında net görsel hiyerarşi korunur.
- Sayısal değer ve metriklerde tabular hizalama tercih edilir.

---

## 4. Boşluk Sistemi (Spacing)

Standart boşluk birimleri:

- 4 px
- 8 px
- 16 px
- 24 px
- 32 px
- 48 px
- 64 px

Önerilen kullanım:

| Boşluk | Kullanım Alanı |
|---|---|
| 4 px | İkon-metni mikro ayrımlar |
| 8 px | Form içi küçük ayrımlar |
| 16 px | Kart içi standart padding |
| 24 px | Bölüm içi blok ayrımı |
| 32 px | Büyük kart ve panel boşlukları |
| 48 px | Sayfa içi ana bölüm ayrımları |
| 64 px | Üst seviye sayfa blok ayrımları |

---

## 5. Kart Tasarımları

Desteklenen kart türleri:

- Bilgi Kartı
- Öğrenci Kartı
- Ders Kartı
- Grafik Kartı

Kart standartları:

| Özellik | Standart |
|---|---|
| Köşe Yuvarlaklığı | 12 px |
| Gölge | Yumuşak, düşük yoğunluklu katman gölgesi |
| İç Boşluk | 16-24 px |
| Başlık Düzeni | Başlık, alt bilgi ve eylem alanı ayrık düzen |

Kart davranış kuralları:

- Kart başlıkları kısa ve eylem odaklı olmalıdır.
- Kritik metrikler kart üst bölgesinde görünmelidir.
- Kart içinde birincil eylem tek olmalıdır.

---

## 6. Buton Sistemi

Desteklenen buton türleri:

- Primary Button
- Secondary Button
- Success Button
- Warning Button
- Danger Button

| Buton Türü | Amaç | Örnek Kullanım |
|---|---|---|
| Primary | Ana eylem | Kaydet, Oluştur |
| Secondary | Yardımcı eylem | Düzenle, Filtrele |
| Success | Pozitif sonuç | Onayla, Tamamla |
| Warning | Dikkat gerektiren işlem | Ertele, Askıya al |
| Danger | Geri alınamaz işlem | Sil, İptal Et |

Buton ilkeleri:

- Bir ekranda birincil eylem yalnızca bir adet Primary ile temsil edilir.
- Danger butonları doğrulama adımı olmadan işlem başlatmaz.

---

## 7. Form Alanları

Desteklenen alanlar:

- TextField
- Dropdown
- Date Picker
- Search Box
- Text Area

Form standartları:

- Zorunlu alan göstergesi: Etiket yanında açık ve tutarlı işaret.
- Hata mesajı: Alan altına kısa, düzeltme odaklı metin.
- Placeholder kullanımı: Örnek format veya beklenen giriş türü.
- Etiketler kısa ve eylem odaklı olmalıdır.

| Durum | Görsel Kural |
|---|---|
| Normal | Nötr kenarlık, yüksek okunabilirlik |
| Focus | Primary vurgu kenarlığı |
| Error | Danger renkli kenarlık ve hata metni |
| Disabled | Düşük kontrast, etkileşimsiz görünüm |

---

## 8. Tablo Sistemi

Tablo standartları:

- Satır yüksekliği: 44-52 px
- Başlık satırı: Yarı kalın, sabit arka plan
- Hover efekti: Hafif arka plan vurgusu
- Seçili satır: Primary tonlu belirgin seçim
- Boş tablo görünümü: Açıklayıcı boş durum metni ve eylem önerisi

| Bileşen | Standart |
|---|---|
| Başlık Satırı | Yarı kalın metin, net kolon hizası |
| Veri Satırı | Tutarlı yükseklik, tek satır önceliği |
| Hover | Görsel geri bildirim zorunlu |
| Seçili Satır | Renk + sol vurgu şeridi |
| Boş Durum | İkon, açıklama, yönlendirici buton |

---

## 9. Grafik Sistemi

Desteklenen grafik türleri:

- Çizgi grafiği
- Bar grafiği
- Pasta grafiği

Grafik tasarım kuralları:

- Renkler semantik anlam taşımalıdır.
- Aynı veri kategorisi tüm ekranlarda aynı renkle gösterilmelidir.
- Eksen, etiket ve tooltip sade ve okunaklı olmalıdır.

Önerilen renk eşleşmesi:

| Veri Anlamı | Önerilen Renk |
|---|---|
| Genel performans | Primary |
| Pozitif gelişim | Success |
| Riskli alan | Warning |
| Kritik düşüş | Danger |
| Segment karşılaştırma | Secondary/Purple |

---

## 10. İkon Sistemi

Boyut seti:

- 16
- 20
- 24
- 32

Kullanım kuralları:

| Boyut | Kullanım Alanı |
|---|---|
| 16 | Satır içi yardımcı ikon |
| 20 | Buton içi ikon |
| 24 | Menü ve kart başlığı |
| 32 | Vurgu, boş durum ve özet alanları |

Ek ilkeler:

- İkonlar metinsiz bırakılmamalı, anlamı destekleyen etiketlerle kullanılmalıdır.
- Aynı işlev için farklı ikon kullanılmamalıdır.

---

## 11. Sayfa Yerleşimi

Ana yerleşim bileşenleri:

- Sidebar
- Topbar
- Content
- Kartlar

Yerleşim ilkeleri:

- Sidebar: Ana navigasyon ve modül erişimi.
- Topbar: Sayfa başlığı, hızlı arama, kullanıcı işlemleri.
- Content: Tekil sorumluluk taşıyan modüler bloklar.
- Kartlar: İçeriğin birincil sunum birimi.

Responsive davranış:

- Geniş ekranda çok kolonlu içerik.
- Daralan genişlikte kartlar alt alta akışa geçer.

---

## 12. Responsive Kuralları

| Kırılım | Cihaz | Temel Davranış |
|---|---|---|
| Desktop | 1200 px ve üzeri | Sidebar sabit, çok kolonlu düzen |
| Tablet | 768-1199 px | Sidebar daraltılabilir, 2 kolon önceliği |
| Mobil | 767 px ve altı | Tek kolon, dokunma öncelikli akış |

Responsive ilkeleri:

- Kritik eylemler her kırılımda görünür kalmalıdır.
- Veri yoğun tablolar mobilde kart görünümüne indirgenebilir.
- Dokunmatik hedefler mobilde en az 44 px etkileşim alanı sunmalıdır.

---

## 13. Dark Mode

Dark Mode bu sürümde uygulanmayacaktır.

Gelecek sürüm hazırlık ilkeleri:

- Renkler doğrudan HEX yerine tema token yapısıyla yönetilmelidir.
- Metin ve yüzey kontrastları erişilebilirlik kurallarına göre tanımlanmalıdır.
- Grafik renkleri hem açık hem koyu zeminde ayırt edilebilir olmalıdır.
- Gölge yerine yüzey ton farkları daha güçlü kullanılmalıdır.

---

## Uygulama Notu

Bu tasarım sistemi; Dashboard, Haftalık Program, Öğrenci Yönetimi, Öğrenci Kartı, Ders Ekranı, Gelişim Raporu ve PDF Önizleme ekranlarında tutarlı bir görsel dil sağlamak için zorunlu referans dokümandır.
