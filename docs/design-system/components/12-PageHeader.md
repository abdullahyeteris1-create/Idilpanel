# 12 - PageHeader

## Amaç

PageHeader, sayfanin baglamini ve birincil aksiyonlarini ust bolumde tutarli sekilde sunan baslik bilesenidir.

## Kullanım Alanları

- Sayfa basligi ve alt aciklama gosterimi
- Breadcrumb ile hiyerarsi sunumu
- Sayfa seviyesinde birincil/ikincil aksiyon butonlari
- Liste ve form ekranlarinda baslik standardizasyonu

## Kullanıldığı Ekranlar

- Dashboard disindaki icerik sayfalari
- Ogrenciler, ders, olcum, rapor ve ayarlar ekranlari
- Form ve tablo tabanli sayfalar

## Kullanılmaması Gereken Yerler

- Modal diyalog ic basliklari
- Cok kucuk widget kartlari
- Baslik gerektirmeyen tek amacli micro paneller

## Görsel Yapı

PageHeader su alanlari destekler:

1. Title
2. Subtitle
3. Breadcrumb
4. Primary Action
5. Secondary Action

Alanlar baglama gore opsiyonel hale getirilebilir.

## Alt Componentler

- Header Container
- Title Text
- Subtitle Text
- Breadcrumb Row
- Actions Group
- Primary Button
- Secondary Button

## API

Mevcut API adlariyla uyumlu kullanim:

- build_app_header
- title: zorunlu
- subtitle: opsiyonel
- leading: opsiyonel, breadcrumb veya ikon alani
- actions: opsiyonel aksiyon listesi

Not: Breadcrumb, leading veya bagli ust layout bileseni ile saglanabilir.

## Responsive Davranış

- Desktop: baslik/subtitle solda, aksiyonlar sagda
- Tablet: aksiyonlar bir alt satira kayabilir
- Mobil: baslik blogu ve aksiyonlar dikey akisa gecebilir

## State'ler

- Default: baslik ve aksiyonlar standart gorunumde
- Hover: aksiyon butonlari kendi hover durumlarini gosterir
- Focus: aksiyonlar klavye odagini gostermelidir
- Disabled: aksiyon butonlari disabled durumda pasif gorunebilir

## Boyutlar

- Baslik: h1/h2 token seviyesinde
- Subtitle: body token seviyesinde
- Aksiyon butonlari: button standardi yukseklik ve radius
- Header yuksekligi icerige gore esnek olabilir

## Padding

- Header container yatay ve dusey padding token bazli olmalidir
- Baslik blogu ve aksiyon blogu arasinda yeterli bosluk birakilmalidir

## Spacing

- Title ve subtitle arasi: xs/sm
- Sol blog ve sag aksiyonlar arasi: md/lg
- Aksiyon butonlari arasi: sm

## Renk Kuralları

- Baslik: text_primary
- Subtitle ve breadcrumb: text_secondary
- Header zemini baglama gore surface veya sayfa zemini
- Primary/secondary aksiyonlar button tokenlarina uyar

## İkon Kuralları

- Material Icons kullanilir
- Leading alanda ikon varsa baslik semantigini desteklemelidir
- Aksiyon ikonlari buton metniyle anlamsal uyumlu olmalidir

## Accessibility

- Baslik hiyerarsisi semantik olarak dogru seviyede olmalidir
- Breadcrumb ekran okuyucuya anlamli sekilde sunulmalidir
- Aksiyon butonlarinin hit area ve klavye odagi yeterli olmalidir

## Örnek Kullanım

build_app_header(
	title="Ogrenciler",
	subtitle="Kayitlar ve durum ozetleri",
	leading=breadcrumb_control,
	actions=[secondary_button, primary_button]
)

## Kabul Kriterleri

1. Title, subtitle, breadcrumb, primary action ve secondary action alanlari desteklenir.
2. Header, farkli sayfa tiplerinde reusable yapida calisir.
3. Responsive kirilimlarda baslik ve aksiyon okunurlugu korunur.
4. Buton ve tipografi kurallari Design System ile uyumludur.

## Definition of Done

- 18 baslik eksiksiz doldurulmustur.
- PageHeader alanlari ve API parametreleri netlestirilmistir.
- Accessibility, responsive ve state davranislari acikca belgelenmistir.
