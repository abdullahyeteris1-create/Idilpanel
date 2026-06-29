# IDIL HIZLI OKUMA - UI Interaction Specification

## 1. Belgenin Amaci

Bu dokumanin amaci:

- Tum ekranlarda tutarli kullanici etkilesimi saglamak
- Kullanici deneyimini standartlastirmak
- Gelistiriciler icin referans dokuman olusturmak
- Flet gelistirme surecinde ortak davranis kurallarini belirlemek

Bu belge, urun davranisinin teknik uygulamaya dogru ve tekrar edilebilir bicimde aktarilmasi icin ana referans olarak kullanilir.

---

## 2. Genel Etkilesim Ilkeleri

Temel ilkeler:

- Az tiklama
- Tek bakista bilgi
- Hizli veri girisi
- Tutarli davranis
- Geri alinabilir islemler
- Gereksiz onay pencerelerinden kacinma

Uygulama kurallari:

- Birincil eylem her ekranda tek ve belirgin olmalidir.
- Kritik bilgi alanlari ekranin ilk gorunen bolgesinde sunulmalidir.
- Bir eylemin sonucu her zaman gorunur geri bildirimle desteklenmelidir.
- Hata durumlari kullaniciya cozum odakli mesajlarla iletilmelidir.

---

## 3. Mouse Etkilesimleri

| Etkilesim | Kullanim Amaci | Beklenen Davranis |
|---|---|---|
| Tek Tiklama | Secim, acma, eylem tetikleme | Aninda secim veya eylem |
| Cift Tiklama | Hizli detay acma (sinirli alanlarda) | Detay paneli veya kayit acilisi |
| Sag Tiklama | Baglamsal menu (ileri seviye) | Islem menusu acilir |
| Hover | Bilgi onizleme, odak belirtme | Hafif gorunur vurgu, tooltip opsiyonu |
| Mouse Wheel | Liste/icerik kaydirma | Kaydirma performansi akici olmali |
| Drag and Drop (gelecek surum) | Ders tasima, siralama | Cakisma kontrolu ile birakma |

Not:

- Cift tiklama, yanlis eylem riskini arttirdigi alanlarda kullanilmamalidir.
- Sag tiklama olmadan da ayni eyleme erisilebilmelidir.

---

## 4. Klavye Kisayollari

| Kisayol | Islev | Davranis |
|---|---|---|
| Ctrl + S | Kaydet | Acik formu veya aktif kaydi kaydeder |
| Ctrl + F | Ara | Ekran ici arama alanina odaklanir |
| Ctrl + N | Yeni Kayit | Yeni kayit olusturma akisini baslatir |
| Ctrl + P | PDF / Yazdir | Yazdirma veya PDF onizleme akisini acar |
| ESC | Kapat | Modal, dialog veya sag paneli kapatir |
| ENTER | Onayla | Secili eylemi onaylar |
| TAB | Sonraki Alan | Formda bir sonraki alana gecer |
| Shift + TAB | Onceki Alan | Formda bir onceki alana gecer |
| F5 | Yenile | Aktif ekran verisini yeniler |

Gelecekte eklenebilecek kisayollar:

- Ctrl + D: Gunu ac
- Ctrl + Shift + F: Gelismis filtre
- Alt + 1..9: Hizli moduller arasi gecis

---

## 5. Form Kurallari

Kapsanan alan tipleri:

- TextField
- Dropdown
- Time Picker
- Date Picker
- Search Box
- Text Area

### 5.1 Ortak Form Davranisi

- Placeholder kullanimi: Beklenen veri formati kisa ornekle gosterilir.
- Zorunlu alan isareti: Etiket yaninda acik bicimde belirtilir.
- Hata mesajlari: Alan altinda net ve duzeltme odakli gosterilir.
- Dogrulama kurallari: Alan bazli ve kaydetme oncesi toplu kontrol uygulanir.
- Klavye kullanimi: Tum alanlar TAB sirasina uygun gezinilebilir olmalidir.

### 5.2 Alan Bazli Kurallar

| Alan | Kural | Hata Durumu |
|---|---|---|
| TextField | Serbest metin veya formatli veri | Bos/gecersiz format |
| Dropdown | On tanimli secim | Secim yoksa zorunlu uyari |
| Time Picker | Saat secimi ve duzenleme | Saat cakismasi/eksik saat |
| Date Picker | Tarih secimi | Gecersiz tarih araligi |
| Search Box | Anlik filtreleme | Sonuc yok bos durum mesaji |
| Text Area | Uzun not girisi | Karakter siniri uyari mesaji |

---

## 6. Haftalik Program Etkilesimleri

### 6.1 Islem Kurallari

| Islem | Tetikleyici | Sistem Davranisi |
|---|---|---|
| Bos ders kutusuna tiklama | Tek tiklama | Sag panelde yeni ders olusturma formu acilir |
| Dolu ders kartina tiklama | Tek tiklama | Kart secilir, detay paneli acilir |
| Saat duzenleme | Time Picker | Saat guncellenir, cakisma kontrolu yapilir |
| Ders olusturma | Form kaydet | Kart olusur, ozet metrikler guncellenir |
| Ders duzenleme | Secili kart + kaydet | Kart ve detay bilgileri guncellenir |
| Ders silme | Sil aksiyonu + onay | Kayit pasiflenir/silinir, grid guncellenir |
| Sag panel acilmasi | Kart veya bos slot secimi | 200 ms altinda acilis |
| Hafta degistirme | Sol/sag ok veya tarih secici | Takvim haftasi yenilenir |
| Bugune donme | Bugun butonu | Icinde bulunulan haftaya odaklanir |
| Yazdirma | Yazdir butonu | Yazdirma/PDF onizleme akisi acilir |
| Excel aktarimi | Excel butonu | Secili filtre ile dosya uretilir |

Gelecek surum:

- Surukle birak ile ders tasima (cakisma kontrolu zorunlu)

### 6.2 Ornek Senaryo - Bos Slottan Ders Olusturma

1. Ogretmen bos kutuya tiklar.
2. Sag panelde saat ve ogrenci secer.
3. Kaydet tusuna basar.
4. Sistem cakisma kontrolu yapar.
5. Kart takvime yerlestirilir ve durum Planlandi olur.

---

## 7. Ders Karti Kurallari

Durum bazli renk, ikon ve davranis tablosu:

| Durum | Renk | Ikon | Davranis |
|---|---|---|---|
| Planlandi | Primary | Takvim/Saat | Tiklanabilir, duzenlenebilir |
| Devam Ediyor | Secondary | Oynat | Aktif vurgu, canli durum |
| Tamamlandi | Success | Onay | Kilitli ozet, duzenleme sinirli |
| Gelmedi | Warning | Kullanici-X | Telafi adayina otomatik gecis |
| Iptal | Danger | X | Pasif gorunum, neden zorunlu |
| Telafi Bekliyor | Purple | Yenileme | Telafi planlama onceligi |
| Yarim Kaldi | Warning | Duraklat | Devam/telafi karari bekler |

Kart secildiginde:

- Kart kenarligi ve arka plan vurgulanir.
- Sag panel secili karta gore guncellenir.

Hover durumunda:

- Hafif yukselme ve golge artisi uygulanir.
- Hemen gorunen hizli eylem ikonu opsiyonel olarak acilabilir.

---

## 8. Sag Panel Davranisi

Sag panel acilma durumlari:

- Bos ders kutusuna tiklama
- Dolu ders kartina tiklama
- Hedefli "Duzenle" eylemi

Sag panel kapanma durumlari:

- ESC tusu
- Kapat ikonu
- Arka plan tiklamasi (modal degilse)
- Kaydet/iptal sonrasi otomatik kapanis (ekran ayarina bagli)

Kurallar:

- ESC ile kapanma desteklenmelidir.
- Baska karta tiklanirsa panel kapanmaz, icerik yeni secime gore aninda degisir.
- Kaydedilmemis veri varsa cikista "Kaydetmeden Cik" dialogu gosterilir.

---

## 9. Modal ve Dialog Kurallari

| Durum | Bilesen | Kural |
|---|---|---|
| Onay pencereleri | Dialog | Kritik aksiyonlarda zorunlu |
| Silme islemleri | Danger Dialog | Cift onay ve acik etiket |
| Kaydetmeden cikis | Warning Dialog | Kaydet, Vazgec, Iptal secenekleri |
| Hata mesajlari | Error Modal/Toast | Hata nedeni + cozum onerisi |
| Basarili islem bildirimi | Success Toast | Kisa sureli olumlu geri bildirim |

Dialog ilkeleri:

- Birincil aksiyon acik ve eylem odakli adla yazilmalidir.
- ESC, tehlikeli silme dialoglarinda varsayilan olarak "iptal" anlamina gelir.

---

## 10. Bildirim Sistemi

| Bildirim Turu | Kullanim | Gosterim Suresi | Davranis |
|---|---|---|---|
| Success Toast | Basarili kayit/islem | 2.5-3 sn | Otomatik kapanir |
| Error Toast | Hata veya kayit basarisiz | 5-7 sn | Otomatik + manuel kapama |
| Warning Toast | Riskli durum/eksik bilgi | 4-5 sn | Eylem onerisi icerebilir |
| Info Toast | Bilgilendirme | 3-4 sn | Pasif bilgilendirme |

Ek kurallar:

- Ayni anda en fazla 3 toast gorunmelidir.
- Kritik hata durumunda toast yerine dialog tercih edilebilir.

---

## 11. Durum Etiketleri (Status Badges)

| Etiket | Onerilen Renk | Ikon Onerisi | Kullanim Notu |
|---|---|---|---|
| Planlandi | Primary | Saat | Varsayilan plan durumu |
| Devam Ediyor | Secondary | Oynat | Canli ders vurgusu |
| Tamamlandi | Success | Check | Tamamlanan kayit |
| Gelmedi | Warning | User-X | Telafi onceligi |
| Iptal | Danger | X | Iptal sebebi ile birlikte |
| Telafi Bekliyor | Purple | Refresh | Takip listesine dusurulur |
| Yarim Kaldi | Warning | Pause | Devam veya telafi bekler |

Kural:

- Etiket renkleri tum modullerde ayni anlami tasimalidir.
- Etiket yalnizca renkle degil, ikon ve metinle de ayirt edilebilir olmalidir.

---

## 12. Performans Kurallari

Hedef sureler:

- Sayfa gecisi < 300 ms
- Sag panel acilisi < 200 ms
- Form kaydi < 2 sn
- PDF olusturma < 5 sn

Izleme ve olcum:

- Kritik akislar icin performans loglari toplanmalidir.
- Esik asimlarinda gelistiriciya tanilanabilir hata kaydi sunulmalidir.

---

## 13. Auto Save Kurallari

- Form alanlari belirli araliklarla otomatik kaydedilebilir (gelecek surum).
- Beklenmeyen kapanmalarda son taslak geri yuklenebilir.
- Otomatik kayit kullaniciya kisa bir bilgi mesajiyla gosterilir.

Ek davranis notlari:

- Otomatik kayit, aktif veri girisi sirasinda akisi bozmadan arka planda calismalidir.
- Son otomatik kayit zamani ilgili formun ust bilgisinde gorunur olmalidir.
- Kayit basarisiz olursa Error Toast ile kullanici bilgilendirilmelidir.

---

## 14. Loading States

Yukleme durumlari, kullaniciya sistemin calistigini net sekilde gostermeli ve belirsizligi azaltmalidir.

| Yukleme Turu | Kullanim Durumu | Davranis |
|---|---|---|
| Skeleton Loading | Liste, kart ve tablo gibi icerik alanlari | Gercek icerik yuklenene kadar yer tutucu bloklar gosterilir |
| Progress Indicator | Adimli is akislari ve form asamalari | Kullaniciya mevcut asama ve kalan adim bilgisi verilir |
| Spinner | Kisa sureli arka plan islemleri | Merkezde veya ilgili bilesen icinde donen yukleme gostergesi |
| Yuzde Gostergesi | Uzun sureli islemler (PDF/Excel/rapor) | Islem ilerlemesi yuzde olarak gorunur |

Kural seti:

- 300 ms altindaki islemlerde loading gostergesi zorunlu degildir.
- 300 ms ustu islemlerde en az spinner veya skeleton gosterilmelidir.
- 2 saniyeyi asan islemlerde metinsel durum bilgisi ve iptal/arka plana alma secenegi degerlendirilmelidir.
- Uzun islemlerde yuzde bilgisi, "hazirlaniyor", "isleniyor", "tamamlaniyor" gibi durum metinleriyle desteklenmelidir.

---

## 15. Bos Durumlar (Empty States)

Bos durumlar, kullanicinin cikmaza girmesini engelleyen yonlendirici ekran durumlaridir. Her bos durumda kullaniciya:

- Ne oldugu
- Neden oldugu
- Sonraki adimda ne yapacagi

net bicimde gosterilmelidir.

### 15.1 Tasarim Kurallari

- Baslik kisa ve acik olmali: "Henuz ogrenci eklenmemis" gibi.
- Aciklama metni tek cumlede yonlendirici olmali.
- En az bir birincil eylem butonu bulunmali.
- Ikon/ilustrasyon sade olmali, ana aksiyonu golgelememeli.
- Bos durum karti veya paneli, ekranin odak bolgesinde gorunmeli.

### 15.2 Ekran Bazli Bos Durumlar

| Ekran | Bos Durum Mesaji | Birincil Aksiyon |
|---|---|---|
| Ogrenci Yonetimi | Henuz ogrenci eklenmemis. | Yeni Ogrenci Ekle |
| Haftalik Program | Bu haftaya ait planlanmis ders yok. | Ders Planla |
| Ders Ekrani | Secili ders kaydi bulunamadi. | Haftalik Programa Don |
| Gelisim Raporu | Henuz rapor olusturulmamis. | Rapor Olustur |
| PDF Onizleme | Onizlenecek PDF bulunamadi. | Rapor Sec |

### 15.3 Ornek Bos Durum Metinleri

- Henuz ogrenci eklenmemis. [Yeni Ogrenci Ekle]
- Bu haftada henuz ders bulunmuyor. [Ders Planla]
- Henuz rapor yok. [Rapor Olustur]

### 15.4 Davranis Kurallari

- Veri olustugu anda bos durum otomatik kaybolmali ve ilgili liste/kart gorunumu gelmelidir.
- Bos durumdaki buton, kullaniciyi dogrudan ilgili olusturma akisina goturmelidir.
- Arama veya filtre sonucu bos ise genel bos durumdan farkli bir mesaj gosterilmelidir: "Sonuc bulunamadi".
- Hata kaynakli bosluk (yukleme hatasi) ile gercek veri yoklugu ayni mesajla gosterilmemelidir.

---

## 16. Gelecek Ozellikler

Ileride eklenebilecek etkilesimler:

- Drag and Drop
- Toplu secim
- Coklu duzenleme
- Dokunmatik ekran destegi
- Mobil hareketler
- Sesli komut destegi

Yol haritasi notu:

- Gelecek ozellikler, mevcut etkileşim tutarliligini bozmadan asamali olarak devreye alinmalidir.

---

## 17. Yetkilendirme (Future Ready)

Mevcut surum tek kullanici modeliyle calismaktadir. Gelecek surumlerde rol bazli yetkilendirme yapisi asagidaki gibi genisleyebilir:

- Admin
- Ogretmen
- Sekreter

Rol hiyerarsisi:

Admin -> Ogretmen -> Sekreter

> Bu sürüm tek kullanıcı mantığıyla geliştirilmektedir. Ancak tüm etkileşim kuralları çok kullanıcılı yapıya genişletilebilecek şekilde tasarlanacaktır.

---

## Sonuc

Bu dokuman, IDIL HIZLI OKUMA Yonetim Sistemi'nin tum ekranlarinda ortak kullanici deneyimini saglayan ana referans belgedir.

Tasarim, urun ve gelistirme ekipleri; etkilesim kararlarini bu belgeye gore standartlastirir. Boylece hem kullanici memnuniyeti hem de surdurulebilir gelistirme hizi korunur.
