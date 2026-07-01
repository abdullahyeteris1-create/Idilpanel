# 03 - ActionPanel

## Amaç

ActionPanel, sik kullanilan islemleri tek bir kart icinde toplu ve hizli erisimle sunan reusable aksiyon bilesenidir. Sabit ekran bagimliligi olmadan, disaridan verilen action listesi ile calisir.

## Kullanım Alanları

- Dashboard hizli islem bolumu
- Ogrenci ekrani hizli aksiyonlari
- Ders/olcum/rapor ekranlarinda sik aksiyonlar
- Yonetim paneli operasyon kisayollari

## Kullanıldığı Ekranlar

- Dashboard
- Ogrenciler
- Haftalik Program
- Ders Kayitlari
- Olcumler
- Gelisim Raporlari

## Kullanılmaması Gereken Yerler

- Uzun metin aciklamasi gereken bloklar
- Form odakli veri giris alanlari
- Tablo veya kayit listesi sunumu
- Kritik/yikici islemlerde onaysiz tek tik akislari

## Görsel Yapı

Panel yapisi su sirayi izler:

1. Baslik satiri (ikon + baslik)
2. Alt aciklama
3. Action grid (button kartlari)

Her action karti:

- Sol: ikon kapsayici
- Orta: baslik + alt aciklama
- Tum satir tiklanabilir alan

## Alt Componentler

- Panel Container
- Header Row
- Subtitle Text
- Responsive Action Grid
- Action Button Item
- Icon Capsule
- Title/Subtitle Text Block

## Parametreler (API)

Ana bilesen parametreleri:

- `title`: Panel basligi
- `subtitle`: Panel aciklama metni
- `actions`: Action listesi

Action item parametreleri:

- `key`: Benzersiz kimlik
- `title`: Action basligi
- `subtitle`: Action alt metni
- `icon`: Material icon kimligi
- `on_click`: Callback

## Responsive Davranış

- Desktop: 2 kolon (2x2 grid)
- Tablet: 2 kolon
- Mobil: 1 kolon
- Button yuksekligi tum kirilimlarda sabit kalir

## Renk Kuralları

- Panel zemini: `surface`
- Panel kenari: `border`
- Action zemini: `surface`
- Action hover shadow: `card` -> `hover`
- Icon kapsayici zemini: `primary` alpha
- Baslik metni: `text_primary`
- Alt metin: `text_secondary`

## İkon Kuralları

- Sadece Material Icons kullanilir
- Ikon kapsayici: dairesel form
- Ikon rengi: `primary`
- Ikon kapsayici boyutu: `32px`
- Her action icin tek ikon kullanilir

## Boyutlar

- Action button yuksekligi: `72px`
- Action button radius: `12px`
- Panel radius: `16px`
- Baslik metni: `22px`
- Subtitle metni: `16px`
- Action baslik: `16px`
- Action alt metin: `14px`

## Padding

- Panel padding: `24px`
- Action item padding: `12/8`
- Icon ve metin blogu arasi yatay bosluk: `12px`

## Spacing

- Header ve subtitle arasi: panel column akisi
- Subtitle ve grid arasi: panel column akisi
- Grid item araliklari: `12px`
- Action baslik-alt metin arasi: `2px`

## Örnek Kullanım

```python
from components.action_panel import build_action_panel

panel = build_action_panel(
	title="Hizli Islemler",
	subtitle="Sik kullanilan islemler",
	actions=[
		{
			"key": "new-student",
			"title": "Yeni Ogrenci",
			"subtitle": "Kayit olustur",
			"icon": "PERSON_ADD",
			"on_click": None,
		},
	],
)
```

## Kabul Kriterleri

1. Panel sabit aksiyonlar yerine disaridan verilen `actions` listesi ile calisir.
2. Action item boyut, radius ve padding degerleri standartla uyumludur.
3. Responsive grid desktop/tablet 2 kolon, mobil 1 kolon davranisini korur.
4. Hover shadow gecisi tum action itemlarda tutarlidir.
5. Icon ve tipografi hiyerarsisi Design System ile uyumludur.
6. Tekrar kullanima uygun ekran-bagimsiz API sunulur.

## Definition of Done

- Tum zorunlu dokumantasyon basliklari eksiksiz doldurulmustur.
- API parametreleri panel ve action item seviyesinde netlestirilmistir.
- Responsive, renk, ikon ve olcu kurallari acikca tanimlanmistir.
- Bilesenin reusable oldugu ve sabit dashboard bagimliligi olmadigi belgelenmistir.
