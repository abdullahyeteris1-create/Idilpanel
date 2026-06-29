# Sprint 01 - UI Foundation

## Sprint Amaci

IDIL HIZLI OKUMA Yonetim Sistemi icin temel kullanici arayuzu altyapisini olusturmak.

Bu sprintte is kurallari gelistirilmeyecektir. Tum ekranlarin kullanacagi ortak UI temeli, layout yapisi ve yonlendirme altyapisi hazirlanacaktir.

---

## Sprint Kapsami

- Ortak tema sistemi (renk, tipografi, spacing, radius, shadow)
- Ortak bilesen kutuphanesi (button, card, form alanlari, dialog vb.)
- Ana uygulama layout yapisi (sidebar, topbar, content)
- Sayfalar arasi gecis (routing/navigation)
- Bos sayfa iskeletlerinin hazirlanmasi

---

## Epic 1 - Project Foundation

### Gorevler

1. Flet proje yapisini kontrol et.
2. `src` klasor yapisini dogrula (`app`, `components`, `theme`, `views`, `utils`, `controllers`, `models`, `services`).
3. Ortak ayar dosyalari icin temel iskeleti olustur.
4. Tema altyapisinin baglanacagi ana uygulama giris noktasini netlestir.

### Cikis Kriteri

- Proje klasor yapisi sprint mimarisine uygun ve tutarli olmalidir.

---

## Epic 2 - Theme System

### Hedef Dosyalar

- `colors.py`
- `typography.py`
- `spacing.py`
- `radius.py`
- `shadows.py`
- `theme.py`

### Gorevler

5. Tema dosya iskeletlerini olustur.
6. Renk tokenlarini merkezi hale getir.
7. Tipografi sabitlerini tanimla.
8. Spacing, radius ve shadow tokenlarini tanimla.
9. `theme.py` icinde tum tokenlari birlestiren tema yapisini hazirla.

### Cikis Kriteri

- Tum ekranlarda tekrar kullanilabilecek tekil ve merkezi tema sistemi hazir olmalidir.

---

## Epic 3 - UI Components

### Ortak Bilesenler

- Primary Button
- Secondary Button
- Card
- Badge
- TextField
- SearchBox
- Dropdown
- Dialog
- Snackbar

### Gorevler

10. Bilesen klasor yapisini ve dosya organizasyonunu olustur.
11. Buton bilesenlerini (Primary/Secondary) ortak API ile hazirla.
12. Card ve Badge bilesenlerini olustur.
13. Form bilesenlerini olustur (`TextField`, `SearchBox`, `Dropdown`).
14. Geri bildirim bilesenlerini olustur (`Dialog`, `Snackbar`).

### Cikis Kriteri

- Veri baglantisi olmadan calisan, tekrar kullanilabilir ortak bilesen seti hazir olmalidir.

---

## Epic 4 - Layout

### Hedef Yapilar

- Sidebar
- Topbar
- Content Area
- Responsive Layout
- Navigation

### Gorevler

15. Ana sayfa iskeletini (sidebar + topbar + content) olustur.
16. Sidebar menusu ve aktif sayfa gosterimini bagla.
17. Topbar yapisini olustur ve ortak aksiyon alanini hazirla.
18. Content alani icin sayfa kapsayici layout yapisini standardize et.
19. Desktop-oncelikli responsive davranisi ekle.

### Cikis Kriteri

- Uygulamanin tum sayfalari ortak layout sistemi uzerinden calisabilmelidir.

---

## Epic 5 - Routing

### Olusturulacak Sayfalar (Bos Iskelet)

- Dashboard
- Haftalik Program
- Ogrenciler
- Ders Kayitlari
- Gelisim Raporlari
- PDF
- Ayarlar

### Gorevler

20. Routing altyapisini olustur.
21. Bos sayfa dosyalarini olustur.
22. Sidebar menusu ile routing baglantisini tamamla.
23. Sayfalar arasi gecisleri test et.

### Cikis Kriteri

- Tum hedef sayfalar arasinda kesintisiz gecis yapilabilmelidir.

---

## Sprint Sonunda Beklenen Ciktilar

- Calisan Flet uygulamasi
- Sol Sidebar
- Topbar
- Sayfalar arasinda gecis
- Ortak Theme
- Ortak Component yapisi
- Responsive ana iskelet

---

## Sprint Disi (Bu Sprintte Yapilmayacak)

- Veritabani baglantisi
- CRUD islemleri
- Haftalik Program ekraninin detayli is kurallari
- Grafikler
- PDF uretimi

---

## Sprint Tamamlanma Tanimi (Definition of Done)

1. Uygulama calisir durumda acilmalidir.
2. Sidebar ve topbar tum sayfalarda tutarli gorunmelidir.
3. Hedef sayfalar arasi gecis sorunsuz calismalidir.
4. Ortak tema ve bilesenler merkezi yapidan kullanilmalidir.
5. Kod organizasyonu `src` mimarisiyle uyumlu olmalidir.

---

## Sprint Riskleri

- Flet surum uyumsuzlugu
- Responsive davranislarin beklenenden farkli calismasi
- Component mimarisinin erken degismesi
- Tema sisteminin ileride genisletilmesi gerekmesi

---

## Acceptance Criteria

- Uygulama hata vermeden aciliyor.
- Sidebar tum sayfalarda ayni.
- Theme tek merkezden yonetiliyor.
- Button component tum sayfalarda ayni.
- Responsive yapi 1440 px ve 1024 px ekranlarda test edildi.
- Kod PEP8 uyumlu.

---

## Sprint Sonu Demo

Sprint sonunda gosterilecek canli demo kapsamı:

- Uygulama aciliyor.
- Sidebar calisiyor.
- Topbar calisiyor.
- Sayfalar arasinda gecis var.
- Theme aktif.
- Component sistemi hazir.
