# 02 - ChartCard

## Amaç

ChartCard, dashboard ve raporlama ekranlarinda trend ve dagilim bilgisini kart formatinda gostermek icin kullanilan gorsel ozet bilesenidir. Bilesen, baslik-alan-aciklama hiyerarsisi ile veriyi okunur ve karsilastirilabilir hale getirir.

## Kullanım Alanları

- Performans trendi izleme (okuma hizi gelisimi)
- Dagilim ozetleri (anlama orani segmentleri)
- Zaman bazli KPI gorsellestirme
- Dashboard ve rapor ozet bolumleri

## Kullanıldığı Ekranlar

- Dashboard chart alani
- Gelisim raporu ozet bloklari
- Yonetici ozet panelleri

## Kullanılmaması Gereken Yerler

- Uzun tablo verisi gosterimi gereken yerler
- Form girisi veya aksiyon odakli alanlar
- Ham kayit listesi sunumu
- Tek satirli sayisal KPI karti ihtiyaclari (StatisticCard tercih edilir)

## Görsel Yapı

ChartCard asagidaki hiyerarsiyi takip eder:

1. Baslik
2. Alt baslik
3. Grafik alani (bu asamada placeholder)
4. Alt bilgi: son guncelleme + trend + kisa aciklama

Kart, yuzey rengi, border ve shadow ile ayrisir; hover durumunda shadow seviyesi artar.

## Alt Componentler

- Card Container
- Title Block
- Subtitle Text
- Chart Placeholder Area
- Footer Info Block

Not: Bu bilesen icinde gercek chart kutuphanesi entegrasyonu bu sprint kapsaminda degildir.

## Parametreler (API)

- `title`: Kart ana basligi
- `subtitle`: Kart alt basligi
- `updated_at`: Son guncelleme bilgisi
- `trend_text`: Trend metni
- `description`: Kisa aciklama
- `variant`: `line` veya `bar`

## Responsive Davranış

- Desktop: 2 chart kart yan yana
- Tablet: Alt alta tek kolon
- Mobil: Alt alta tek kolon
- Kart ici yapi responsive kirilimlarda bozulmadan korunur

## Renk Kuralları

- Kart zemini: `surface`
- Kart kenari: `border`
- Baslik: `text_primary`
- Alt metinler: `text_secondary`
- Placeholder alan zemini: `background`
- Placeholder ikon: `primary`
- Hover: `shadows.card` -> `shadows.hover`

## İkon Kuralları

- Yalnizca Material Icons kullanilir
- `line` varyanti: `SHOW_CHART`
- `bar` varyanti: `BAR_CHART`
- Ikon rengi semantik olarak `primary` tonundadir
- Ikon sadece placeholder alaninda kullanilir

## Boyutlar

- Kart yuksekligi: `320px`
- Kart radius: `16px`
- Chart placeholder yuksekligi: `150px`
- Placeholder radius: `12px`
- Baslik: `22px`
- Alt baslik: `16px`
- Footer metin: `13px`

## Padding

- Kart ic padding: `24px`
- Placeholder ic hizalama: merkez
- Footer metin blogu ic aralik: `4px`

## Spacing

- Baslik-alt baslik araligi: `14px` yapisi icinde korunur
- Placeholder ustu/alti spacing: kart column akisi ile sabittir
- Footer satirlari arasi spacing: `4px`

## Örnek Kullanım

```python
from components.chart_card import build_chart_card

card = build_chart_card(
	title="Okuma Hizi Gelisimi",
	subtitle="Son 30 gun performans gorunumu",
	updated_at="Bugun 09:45",
	trend_text="Yukari yonlu",
	description="Aylik hedefe yaklasiliyor.",
	variant="line",
)
```

## Kabul Kriterleri

1. Baslik-alt baslik-grafik-alan-alt bilgi hiyerarsisi korunur.
2. Kart boyutlari ve radius Design System ile uyumludur.
3. Placeholder varyantlari (`line`/`bar`) dogru ikonla ayrisir.
4. Hover durumunda shadow gecisi dogru calisir.
5. Responsive kirilimlarda 2 kolon -> 1 kolon davranisi bozulmaz.
6. Hardcoded tasarim degerleri yerine token kullanimi esastir.

## Definition of Done

- Dokumantasyondaki tum zorunlu basliklar doludur.
- API parametreleri acik ve uygulanabilir sekilde tanimlanmistir.
- Responsive, renk, ikon ve boyut kurallari netlestirilmistir.
- ChartCard icin kapsam disi alanlar (gercek chart engine) acikca belirtilmistir.
