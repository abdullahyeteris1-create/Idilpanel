# 10 - SearchBar

## Amaç

SearchBar, kullanicinin kayitlari hizli sekilde bulmasi icin metin tabanli arama girisini standart bir UI bileseni olarak sunar.

## Kullanım Alanları

- Tablo/liste ustu arama
- Dashboard global arama
- Form icinde secim/filtreleme aramalari
- Kayit ve rapor ekranlarinda hizli bulma

## Kullanıldığı Ekranlar

- Topbar global search alani
- Ogrenciler liste arama alani
- Ders/olcum/rapor liste ekranlari

## Kullanılmaması Gereken Yerler

- Sayisal filtreleme veya aralik girisi gereken alanlar
- Cok satirli metin giris senaryolari
- Gizli/sifre alanlari

## Görsel Yapı

SearchBar yapisi:

1. Sol ikon
2. Placeholder veya girilen metin
3. Opsiyonel clear button

Girdi alani tek satirli ve odak davranisina sahip olmalidir.

## Alt Componentler

- Text Input Field
- Prefix Search Icon
- Clear Button, opsiyonel
- Hint/Placeholder Text

## API

Mevcut API ve parametreler:

- build_search_box
- placeholder veya hint_text
- icon veya prefix_icon
- clear button, opsiyonel
- onChange veya on_change

Ek desteklenen parametreler:

- value
- on_submit
- disabled

## Responsive Davranış

- Desktop: standart genislikte gorunur
- Tablet: genislik optimize edilir
- Mobil: tam genislik veya ust uste kontrol yerlesimi
- Placeholder metni dar alanda anlamli kalacak uzunlukta olmalidir

## State'ler

- Default: normal border ve metin gorunumu
- Hover: alan veya border vurgu durumuna gecebilir
- Focus: focused border color belirgin olmalidir
- Disabled: metin, ikon ve arka plan pasif gorunume gecer

## Boyutlar

- Yukseklik: input standardina uyumlu
- Border radius: input radius standardi
- Prefix ikon boyutu: 20 px
- Metin boyutu: body

## Padding

- Icerik padding: md/sm tokenlari
- Sol-sag ic bosluklari metin okunurlugunu koruyacak sekilde sabittir

## Spacing

- Ikon ve metin arasi: xs/sm
- SearchBar ile bagli filtre kontrolleri arasi: sm/md

## Renk Kuralları

- Zemin: surface
- Border: border_neutral
- Focus border: primary
- Metin: text_primary
- Placeholder: text_secondary
- Ikon: text_secondary

## İkon Kuralları

- Material search ikonu kullanilir
- Ikon semantigi net olmalidir
- Clear button ikonu gerektiginde tek ve belirgin olmalidir

## Accessibility

- Placeholder metni kontrasti okunabilir olmalidir
- Input klavye ile odaklanabilir olmalidir
- Ekran okuyucu icin alan anlami acik etiketle verilmelidir

## Örnek Kullanım

build_search_box(
	hint_text="Ara...",
	value="",
	on_change=on_change,
	on_submit=on_submit,
	disabled=False
)

## Kabul Kriterleri

1. placeholder, icon, clear button, onChange parametreleri dokumanda tanimlanir.
2. SearchBar state davranislari default/hover/focus/disabled seviyesinde aciklanir.
3. Input tokenlari, renk ve tipografi kurallariyla uyumlu tanimlanir.
4. Responsive kirilimlarda arama alani kullanilabilir kalir.

## Definition of Done

- 18 baslik eksiksiz doldurulmustur.
- SearchBar icin zorunlu parametreler belgelenmistir.
- API isimleri mevcut component adlariyla tutarlidir.
