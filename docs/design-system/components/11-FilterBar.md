# 11 - FilterBar

## Amaç

FilterBar, kayitlari coklu kriterlerle daraltmak ve filtre durumunu gorunur sekilde yonetmek icin kullanilan kontrol cubugudur.

## Kullanım Alanları

- Liste ve tablo ekranlarinda ileri filtreleme
- Rapor ve olcum kayit gorunumleri
- Dashboard alt modullerde kapsam daraltma

## Kullanıldığı Ekranlar

- Ogrenciler, ders, olcum ve rapor liste alanlari
- TableCard ust kontrol bolumleri

## Kullanılmaması Gereken Yerler

- Tek kriterli basit arama durumlari, SearchBar yeterlidir
- Kapsami dar olmayan tek adimli akislarda gereksiz karmasa olusturur

## Görsel Yapı

FilterBar su yapilari destekler:

1. FilterChip
2. Dropdown
3. Date Filter
4. Reset Filter

## Alt Componentler

- Filter Container
- Chip Group
- Dropdown Control
- Date Picker Control
- Reset Action Button

## API

Onerilen API:

- build_filter_bar
- chips: FilterChip listesi
- dropdown_filters: secim listeleri
- date_filter: tarih aralik/tek tarih kontrolu
- on_change: filtre degisim callback
- on_reset: tum filtreleri sifirlama callback

## Responsive Davranış

- Desktop: tum kontroller yatay satirda
- Tablet: kontroller iki satira kirilabilir
- Mobil: kontroller alt alta akarak okunur kalir

## State'ler

- Default: secili olmayan filtreler normal gorunumde
- Hover: chip ve kontrollerde hafif vurgu
- Focus: input/dropdown/date alanlarinda odak belirgindir
- Disabled: filtre kontrolleri pasiflestirilebilir

## Boyutlar

- Chip yuksekligi: compact badge/button standardina yakin
- Dropdown ve date filter yuksekligi: input standardi
- Reset buton yuksekligi: button standardi

## Padding

- FilterBar container ic padding: panel veya card standardina uyumlu
- Chip ve kontrol ic paddingleri bilesen standardinda kalir

## Spacing

- Chipler arasi: xs/sm
- Kontroller arasi: sm/md
- FilterBar ile tablo arasi: md

## Renk Kuralları

- Arka plan: surface
- Border/cizgi: border
- Secili chip: primary alpha ton
- Metin: text_primary/text_secondary
- Reset aksiyonu: secondary veya neutral button tonu

## İkon Kuralları

- Sadece Material Icons
- Date filter ve reset ikonlari semantik secilmelidir
- Ikonlar metin okunurlugunu engellememelidir

## Accessibility

- Tum filtre kontrolleri klavye ile ulasilabilir olmalidir
- Secili filtre durumu metin veya aria etiketi ile anlasilir olmalidir
- Renk tek basina anlam tasimamali, secim metniyle desteklenmelidir

## Örnek Kullanım

build_filter_bar(
	chips=chip_items,
	dropdown_filters=dropdown_items,
	date_filter=date_range,
	on_change=on_filter_change,
	on_reset=on_filter_reset
)

## Kabul Kriterleri

1. FilterChip, Dropdown, Date Filter ve Reset Filter yapilari desteklenir.
2. Secili filtre durumu gorunur ve temizlenebilir olur.
3. Responsive kirilimlarda kontrol kalabaligi okunabilir sekilde dagitilir.
4. Design token ve tablolarla ortak spacing kurallari korunur.

## Definition of Done

- 18 baslik eksiksiz doldurulmustur.
- FilterBar ek kurallari dokumanda acikca tanimlanmistir.
- API, state ve accessibility beklentileri netlestirilmistir.
