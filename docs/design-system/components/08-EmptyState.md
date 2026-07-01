# 08 - EmptyState

## Amaç

EmptyState, veri veya sonuc bulunmayan durumlarda kullaniciya ne oldugunu aciklayan ve bir sonraki adimi gosteren bilgilendirici bilesendir.

## Kullanım Alanları

- Liste, tablo veya kart alaninda veri yoksa
- Ilk kullanim senaryolari
- Filtre sonucu bos donen ekranlar
- Silme/islem sonrasi bos kalan alanlar

## Kullanıldığı Ekranlar

- Dashboard ders/olcum kartlari bos durumlari
- Ogrenci, ders, olcum ve rapor liste ekranlari
- Arama/filtre sonuc alanlari

## Kullanılmaması Gereken Yerler

- Hata sayfalari, error state ayridir
- Yukleme devam ederken, loading state kullanilir
- Gercek veri varken yalanci bos durum gosterimi

## Görsel Yapı

Bos durum yapisi su alt ogeleri opsiyonel olarak destekler:

1. Ikon
2. Baslik
3. Aciklama
4. Primary Action, opsiyonel
5. Secondary Action, opsiyonel

## Alt Componentler

- EmptyState Container
- Icon Wrapper
- Title Text
- Description Text
- Actions Row
- Primary Button, opsiyonel
- Secondary Button, opsiyonel

## API

Onerilen API:

- build_empty_state
- title: baslik metni
- description: aciklama metni
- icon: Material icon
- primary_action_label: opsiyonel
- primary_action_on_click: opsiyonel
- secondary_action_label: opsiyonel
- secondary_action_on_click: opsiyonel

## Responsive Davranış

- Desktop: ikon ve metin ortali, aksiyonlar yatay
- Tablet: ayni hiyerarsi, aksiyonlarda wrap olabilir
- Mobil: aksiyonlar tek kolon veya alt alta

## State'ler

- Default: ikon, metin ve opsiyonel aksiyonlar gorunur
- Hover: butonlar kendi hover durumlarini gosterir
- Focus: aksiyon butonlarinda odak gorunur olmalidir
- Disabled: ilgili aksiyonlar disabled olarak gosterilebilir

## Boyutlar

- Ikon: 24-40 px araligi
- Baslik: h3 veya body-strong seviyesinde
- Aciklama: body/caption seviyesinde
- Aksiyon alaninda butonlar standart button yuksekligini korur

## Padding

- Container ic padding: card/panel standardina uygun
- Ikon-metin-aksiyon bloklari arasinda dikey bosluk korunur

## Spacing

- Ikon ile baslik arasi: sm/md
- Baslik ile aciklama arasi: xs/sm
- Aciklama ile aksiyonlar arasi: md
- Aksiyon butonlari arasi: sm

## Renk Kuralları

- Zemin: surface veya baglamin arka plan tonu
- Baslik: text_primary
- Aciklama: text_secondary
- Ikon: passive veya primary ton
- Primary/Secondary aksiyonlar button standardina uyar

## İkon Kuralları

- Sadece Material Icons kullanilir
- Ikon semantigi bos durumu aciklamalidir
- Ikon tek ve odakli olmalidir, coklu ikon kullanilmaz

## Accessibility

- Baslik-aciklama metin kontrasti okunabilir olmalidir
- Aksiyonlar klavye ile ulasilabilir olmalidir
- Empty state metni ekrani okuyucu tarafindan anlamli okunmalidir

## Örnek Kullanım

build_empty_state(
	title="Kayit bulunamadi",
	description="Filtre kriterlerine uygun sonuc yok.",
	icon="INBOX_OUTLINED",
	primary_action_label="Filtreyi Temizle",
	primary_action_on_click=on_reset,
	secondary_action_label="Yeni Kayit",
	secondary_action_on_click=on_create
)

## Kabul Kriterleri

1. Ikon, baslik, aciklama, primary action ve secondary action alanlari opsiyonel olarak desteklenir.
2. Bos durum ile hata/yukleme durumlari birbirine karistirilmaz.
3. Responsive kirilimlarda metin ve aksiyonlar okunabilir kalir.
4. Design token kurallarina uyulur.

## Definition of Done

- 18 baslik eksiksiz dokumante edilmistir.
- EmptyState ek kuralindaki tum opsiyonel alanlar tanimlanmistir.
- API, state ve accessibility beklentileri netlestirilmistir.
