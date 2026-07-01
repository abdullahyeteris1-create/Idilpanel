# 07 - TableCard

## Amaç

TableCard, listeleme ve kayit yonetimi senaryolarinda tabloyu kart semantiği icinde sunan bilesendir. Baslik, arama, filtre, tablo ve sayfalama bolumlerini bir araya getirerek islevsel ve tutarli bir veri gorunumu saglar.

## Kullanım Alanları

- Ogrenci listeleri
- Kurs ve ders kayit tablolari
- Olcum ve rapor kayit gorunumleri
- Yonetim panellerinde veri tarama ve filtreleme

## Kullanıldığı Ekranlar

- Ogrenciler ekrani liste alani
- Ders Kayitlari listeleme bolumu
- Olcum ve rapor odakli tablolasma gerektiren sayfalar

## Kullanılmaması Gereken Yerler

- Kisa KPI ozet kartlari
- Form veri giris odakli paneller
- Tamamen gorsel chart odakli bolumler
- Tek satirli bilgi kutulari

## Görsel Yapı

TableCard bes bolumden olusur:

1. Baslik
2. Arama
3. Filtre
4. Tablo
5. Sayfalama

09 Tables standardina uygun olarak satir, baslik ve ayirici cizgi davranisi korunur.

## Alt Componentler

- Card Container
- Header Row
- Search Bar
- Filter Bar
- Data Table
- Pagination Bar
- Empty State, veri yoksa

## Parametreler (API)

Mevcut temel tablo API:

- Fonksiyon: build_app_table
- columns: kolon basliklari
- rows: satir verileri
- heading_row_height: baslik satiri yuksekligi
- data_row_min_height: satir min yukseklik
- data_row_max_height: satir max yukseklik

TableCard compositional kullaniminda arama, filtre ve sayfalama kontrolleri dis kapsayici tarafindan saglanir.

## Responsive Davranış

- Desktop: Tum kolonlar ve kontrol cubuklari gorunur
- Tablet: Kolon araliklari optimize edilir, gerekirse ikincil bilgiler kisaltilir
- Mobil: Tablo yatay kaydirma veya kartlasma deseni ile okunabilirlik korunur
- Arama ve filtre kontrolleri dar alanda alt satira kirilabilir

## Renk Kuralları

- Kart zemini: surface
- Kart kenari ve tablo cizgileri: border
- Baslik satiri zemini: primary alpha ton
- Baslik metinleri: text_secondary
- Veri hucre metinleri: text_primary
- Hover satiri: hafif background vurgusu

## İkon Kuralları

- Arama ve filtre ikonlarinda sadece Material Icons kullanilir
- Sayfalama yon ikonlari semantik ve tutarli olmalidir
- Ikon boyutlari kontrollere uygun olmalidir

## Boyutlar

- Baslik satiri yuksekligi: 44 px
- Veri satiri min yukseklik: 44 px
- Veri satiri max yukseklik: 52 px
- Kart radius: card standardi
- Tablo kolon spacing: token bazli 16

## Padding

- Kart ic padding: 16 px
- Header ve kontrol satiri ic bosluklari token bazli olmalidir
- Sayfalama satiri yeterli tiklanabilir alan saglamalidir

## Spacing

- Header ile arama arasi md spacing
- Arama ile filtre arasi sm veya md spacing
- Filtre ile tablo arasi md spacing
- Tablo ile sayfalama arasi md spacing

## State'ler

- Default: Baslik, kontrol satiri, tablo ve sayfalama normal gorunumdedir
- Hover: Satir veya kontrol elemanlarinda hover geri bildirimi uygulanir
- Focus: Arama ve filtre inputlarinda focus belirgindir
- Disabled: Filtre veya sayfalama elemanlari gerektiginde disabled olabilir
- Error: Veri yukleme veya filtreleme hatalarinda tablo ustu veya empty-state seviyesinde hata mesaji gosterilebilir

## Örnek Kullanım

Temel tablo kullanim ornegi:

build_app_table(
	columns=["Tarih", "Ogrenci", "Hiz", "Anlama"],
	rows=data_rows,
	heading_row_height=44,
	data_row_min_height=44,
	data_row_max_height=52
)

TableCard yapi olarak bu tablo etrafinda arama, filtre ve sayfalama bolumleri ile compose edilir.

## Kabul Kriterleri

1. TableCard yapisi bes bolumu eksiksiz icerir: baslik, arama, filtre, tablo, sayfalama.
2. 09 Tables standardina uygun satir yuksekligi ve baslik yapisi korunur.
3. Arama ve filtre kontrolleri tabloyla anlamsal olarak bagli calisir.
4. Responsive kirilimlarda tablo okunabilirligi korunur.
5. Empty state ve hata durumlari dokumanda net tanimlanir.

## Definition of Done

- Tum zorunlu basliklar eksiksiz doldurulmustur.
- TableCard ek kurallari ve 09 Tables uyumu belgeye yansitilmistir.
- API tanimi mevcut build_app_table fonksiyonu ile tutarlidir.
- State, spacing, padding ve responsive kurallari acikca belirtilmistir.
