# 01 - StatisticCard

## Amaç

StatisticCard, dashboard ve ozet ekranlarinda tek bir KPI bilgisini hizli ve okunabilir sekilde gostermek icin kullanilan kart bilesenidir. Bilesen; ikon, baslik, buyuk deger, alt bilgi ve trend bilgisini standart bir hiyerarsi ile sunar.

## Kullanım Alanları

- KPI ozetleri (toplam ogrenci, aktif kurs, bugunku ders vb.)
- Sayfa ustu performans bloklari
- Karar destekli yonetim panelleri
- Filtrelenmis veri ozetleri (donem, sinif, egitmen bazli)

## Görünüm

Kart yapisi asagidaki sabit sirayi takip eder:

1. Ikon alani
2. Baslik
3. Buyuk deger
4. Alt bilgi
5. Trend gostergesi (ok + metin)

Kart, beyaz yuzey uzerinde sinir ve golge ile ayrisir; hover durumunda golge seviyesi artar.

## Parametreler

- `icon`: Material icon kimligi
- `title`: KPI basligi
- `value`: Buyuk sayisal/ozet deger
- `subtitle`: Ek aciklama veya karsilastirma metni
- `trend`: `up`, `down`, `flat` degerlerinden biri

## Boyutlar

- Kart yuksekligi: `120px`
- Kart radius: `16px`
- Yatay/dusey ic bosluk: `24 / 16`
- Ikon kapsayici boyutu: `48px`
- Ikon kapsayici radius: `24px`
- Baslik: `18px`
- Deger: `32px`
- Alt bilgi: `14px`
- Trend metni: `13-14px`

## Responsive Davranış

- Desktop: 4 kart yan yana (4 kolon)
- Tablet: 2x2 kirilim
- Mobil: tek kolon akisi
- Kart ic hiyerarsisi responsive durumdan bagimsiz korunur

## Renk Kuralları

- Kart zemini: `surface`
- Kart kenar cizgisi: `border`
- Ana metinler: `text_primary`
- Ikincil metinler: `text_secondary`
- Ikon arka plan: `primary` %10 alpha
- Trend `up`: `success`
- Trend `down`: `danger`
- Trend `flat`: `passive`
- Hover: shadow medium -> shadow large

## İkon Kuralları

- Sadece Material Icons kullanilmalidir
- Ikon semantigi KPI ile uyumlu olmalidir
- Ikon kapsayici dairesel kalmalidir
- Ikon rengi `primary`, kapsayici arka plan alpha tonlu olmalidir
- Tek kartta tek ikon kullanilir; coklu ikon kullanilmaz

## Kullanıldığı Ekranlar

- Dashboard ana KPI alani
- Ozet rapor bloklari (uygun oldugu yerde)

## Kullanılmaması Gereken Yerler

- Uzun metin veya aciklama agirlikli icerikler
- Detay tablo veya liste sunumu gereken bolgeler
- Cok adimli islem akislari
- Form giris alanlari

## API Örneği

```python
from components.statistic_card import build_statistic_card
import flet as ft

card = build_statistic_card(
	icon=ft.Icons.PERSON,
	title="Toplam Ogrenci",
	value="128",
	subtitle="+12 bu ay",
	trend="up",
)
```

## Kabul Kriterleri

1. Kart yuksekligi, radius, padding ve shadow tokenlari standart degerlerle uyumludur.
2. Ikon-baslik-deger-alt bilgi-trend sirasi korunur.
3. Trend renkleri `up/down/flat` kurallarina tam uyar.
4. Responsive kirilimda desktop/tablet/mobil davranisi bozulmaz.
5. Hardcoded renk yerine design token kullanimi esastir.
6. Dashboard dahil kullanim ekranlarinda tekrar kullanilabilir API ile cagirilir.
