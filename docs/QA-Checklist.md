# QA Checklist - Theme and Components Review

## Kapsam

Bu inceleme su katmanlari kapsar:

- src/theme
- src/components
- referans: docs/09-Design-System.md

Degerlendirme yalnizca analiz amaclidir. Kod degistirilmemistir.

## Kontrol Maddeleri ve Sonuc

| Kontrol Maddesi | Durum | Sonuc Ozeti |
|---|---|---|
| Design System uyumu | Kismi Uyum | Genel semantik yapi dogru; bazi API kararlarinda tutarlilik riski var. |
| Hard-coded renk var mi | Kismi Uyum | Component katmaninda sabit HEX yok; ancak badge alpha degeri sabit string ile veriliyor. |
| Hard-coded font var mi | Kismi Uyum | Font family token uzerinden geliyor; bazi componentlerde FontWeight dogrudan sabit. |
| Hard-coded spacing var mi | Uyumlu | Spacing degerleri componentlerde token uzerinden aliniyor. |
| Theme token kullanimi dogru mu | Uyumlu | Tum componentler THEME_TOKENS ile renk/spacing/radius/typography okuyor. |
| Component API tutarliligi | Kismi Uyum | build_ adlandirmasi tutarli; callback tipleri ve varsayilan davranislar dosyalar arasi farkli. |
| Isimlendirme standardi | Uyumlu | Dosya ve fonksiyon isimleri snake_case ve tutarli. |
| Tekrar eden kod var mi | Iyilestirme Gerekli | Font weight map/donusum fonksiyonu birden fazla dosyada tekrar ediyor. |
| Iyilestirme onerileri var mi | Var | Ortak typography yardimcisi, dialog varyant semantigi, token modele gecis onerilir. |

## Bulgular

### 1. Hard-coded alpha degeri (Dusuk)
- Dosya: src/components/badge.py
- Kanit: _with_alpha fonksiyonunda alpha varsayilani "1F".
- Etki: Renk semantigi token tabanli olsa da saydamlik degeri merkezi token disinda kaliyor.

### 2. Hard-coded FontWeight kullanimi (Orta)
- Dosyalar:
  - src/components/button.py
  - src/components/card.py
  - src/components/badge.py
- Kanit: ft.FontWeight.W_600 / ft.FontWeight.W_400 dogrudan kullaniliyor.
- Etki: Tipografi agirliklari THEME_TOKENS tipografi alanindan okunmadigi icin tema esnekligi azalir.

### 3. Tekrar eden WEIGHT_MAP ve _font_weight (Orta)
- Dosyalar:
  - src/components/text_field.py
  - src/components/dropdown.py
  - src/components/search_box.py
  - src/components/dialog.py
  - src/components/snackbar.py
- Kanit: Ayni WEIGHT_MAP + _font_weight deseni tekrar ediyor.
- Etki: Bakim maliyeti artar; bir degisiklikte birden fazla dosya guncellemek gerekir.

### 4. Dialog onay eylemi varsayilaninin danger olmasi (Orta)
- Dosya: src/components/dialog.py
- Kanit: confirm action sabit olarak "danger" varyantina bagli.
- Etki: Design System kuralinda danger geri alinamaz islemler icin; tum dialoglar icin varsayilan olmasi semantik olarak riskli.

### 5. API tipleme tutarliligi (Dusuk)
- Dosyalar: component katmani geneli
- Kanit: Bazi fonksiyonlarda callback Callable tipli, bazilarinda on_change/on_submit tipleri serbest birakilmis.
- Etki: Gelistirici deneyimi ve IDE yardimi dosyalar arasi farklilik gosterebilir.

### 6. Search hint metninin sabit metin olmasi (Dusuk)
- Dosya: src/components/search_box.py
- Kanit: hint_text varsayilani "Ara...".
- Etki: Tema token ihlali degil; ancak locale veya proje bazli metin yonetimi icin merkezilesmeye uygun degil.

## Guclu Yonler

- Theme katmani renk, tipografi, spacing, radius, shadow tokenlarini merkezi bir noktada tutuyor.
- Component katmaninda THEME_TOKENS kullanimi yaygin ve tutarli.
- Renk paleti, spacing ve radius degerleri Design System ile uyumlu.
- Form alanlarinda normal/focus/error/disabled durumlari buyuk oranda dogru ele alinmis.

## Iyilestirme Onerileri

1. Ortak bir typography util olusturup _font_weight tekrarini tek dosyaya tasiyin.
2. Button/Card/Badge icindeki sabit FontWeight kullanimlarini typography tokenlari ile hizalayin.
3. Badge alpha degerini theme token yapisina ekleyin (ornegin colors.semantic_alpha.badge).
4. Dialog icin confirm varyantini parametreye acin ve varsayilani primary/secondary semantigine cekin.
5. Component callback tiplerini tek standarda baglayin (Callable[[ft.ControlEvent], None] | None).
6. UI metin varsayilanlarini ileride merkezi i18n veya constants katmanina tasimayi planlayin.
