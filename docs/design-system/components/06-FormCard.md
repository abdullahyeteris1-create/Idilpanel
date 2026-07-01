# 06 - FormCard

## Amaç

FormCard, veri giris ve guncelleme senaryolarinda form alanlarini duzenli bir kart hiyerarsisi icinde sunan bilesendir. Bilesen, icerik yogun formlari okunur ve bolumlenmis hale getirir.

## Kullanım Alanları

- Ogrenci kayit ve guncelleme formlari
- Ders veya olcum veri giris bloklari
- Ayar ve profil duzenleme formlari
- Cok alanli CRUD operasyon ekranlari

## Kullanıldığı Ekranlar

- Ogrenciler ekrani
- Ders Kayitlari ekranindaki giris bolumleri
- Form tabanli panel sayfalari

## Kullanılmaması Gereken Yerler

- Salt okunur ozet kartlari
- Performans KPI kartlari
- Tablo agirlikli liste ekranlari
- Cok kisa tek alanli hizli aksiyonlar

## Görsel Yapı

FormCard dort bolumden olusur:

1. Baslik
2. Aciklama, opsiyonel
3. Form Alanlari
4. Alt Buton Alani

Bu yapi Ogrenciler ekranindaki form organizasyonunu referans alir.

## Alt Componentler

- Card Container
- Header Title
- Optional Subtitle
- Field Grid veya Field Stack
- Action Footer
- Primary ve Secondary Butonlar

## Parametreler (API)

Mevcut yapi ile FormCard genelde build_app_card veya AppCard uzerinden compose edilir.

- Fonksiyon: build_app_card
- title: form kart basligi
- subtitle: aciklama metni, opsiyonel
- content: form alanlari kapsayicisi
- action: ust satir aksiyon alani, opsiyonel

Form footer aksiyonlari ayri buton bilesenleri ile saglanir.

## Responsive Davranış

- Desktop: Alanlar cok kolonlu duzenlenebilir
- Tablet: Ikili kolon veya tek kolon uyarlamasi
- Mobil: Tek kolon field akisi
- Footer butonlari dar alanda alt alta veya tam genislik gorunebilir

## Renk Kuralları

- Kart zemini: surface
- Kart kenari: border
- Baslik: text_primary
- Aciklama: text_secondary
- Field label ve helper metinleri: tipografi standardina uygun tokenlar
- Hata metni: danger tonu

## İkon Kuralları

- FormCard genelinde ikon zorunlu degildir
- Kullanilan ikonlar Material Icons olmalidir
- Prefix veya suffix ikonlari input semantigine uygun secilmelidir
- Ikon rengi text_secondary veya baglama uygun semantik renk olmalidir

## Boyutlar

- Kart radius: Design System card veya panel standardi
- Input yuksekligi: ilgili input bilesen standardina gore
- Buton yuksekligi: 48 px, button standardi
- Baslik ve aciklama boyutlari typografi tokenlariyla uyumlu

## Padding

- Kart genel padding: buyuk form kartlarinda 24 px seviyesinde kullanilir
- Alan gruplari arasinda tutarli ic bosluk korunur
- Footer bolumunde butonlari ayiran token bazli bosluk uygulanir

## Spacing

- Baslik ve aciklama arasi: kucuk dikey bosluk
- Alanlar arasi: md veya lg spacing tokenlari
- Footer butonlari arasi: sm veya md spacing tokenlari
- Field label ile input arasi sabit alan boslugu

## State'ler

- Default: Tanimli form alanlari ve aksiyonlar normal gorunumde
- Hover: Buton ve interactive field alanlarinda hover geri bildirimi
- Focus: Input odak durumlari belirgin sekilde gorunur
- Disabled: Form alanlari veya butonlar disabled durumda pasiflestirilir
- Error: Validasyon hatalarinda field seviyesinde hata rengi ve mesaj gosterilir

## Örnek Kullanım

Asagidaki kullanim FormCard compositional yapiyi gosterir:

build_app_card(
	title="Ogrenci Bilgileri",
	subtitle="Temel kayit bilgilerini girin",
	content=form_fields_container,
	action=top_right_action
)

Alt buton alani icin PrimaryButton ve SecondaryButton birlikte kullanilir.

## Kabul Kriterleri

1. FormCard dort zorunlu bolumu destekler: baslik, opsiyonel aciklama, form alanlari, alt buton alani.
2. Ogrenciler ekrani referans alinmis yapi ile tutarlilik saglanir.
3. Field ve buton bilesenleri mevcut Design System tokenlari ile uyumludur.
4. Mobilde tek kolon form akisi bozulmadan devam eder.
5. Hata ve disabled state davranislari acikca tanimlanmistir.

## Definition of Done

- Tum zorunlu basliklar eksiksiz dokumante edilmistir.
- FormCard ek kurallari belgeye eksiksiz yansitilmistir.
- API tanimi mevcut bilesen adlariyla uyumludur.
- State, responsive ve token kurallari netlestirilmistir.
