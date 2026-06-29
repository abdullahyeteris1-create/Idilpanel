# İDİL HIZLI OKUMA - Figma Proje Mimarisi

## 1. Doküman Amacı

Bu doküman, İDİL HIZLI OKUMA Yönetim Sistemi için profesyonel seviyede Figma proje yapısını tanımlar.

Kapsam:

- Sayfa (Pages) mimarisi
- Design System içeriği
- Component Set ve Variant planı
- Ekran bazlı Auto Layout stratejisi
- Desktop öncelikli responsive kurallar
- Haftalık Program ekranı için ayrıntılı frame, layer ve bileşen planı

Bu belge yalnızca görsel tasarımı değil, ekipler arası üretim standardını da belirler.

---

## 2. Figma Pages Yapısı

| Sıra | Page Adı | Amaç |
|---|---|---|
| 00 | Cover | Proje kimliği, versiyon, ekip, tarih |
| 01 | Design System | Tokenlar, stil tanımları ve temel kurallar |
| 02 | Components | Tüm yeniden kullanılabilir bileşen setleri |
| 03 | Dashboard | Dashboard ekran akışları ve varyasyonları |
| 04 | Haftalık Program | Ana planlama ekranı (merkez ekran) |
| 05 | Öğrenci Yönetimi | Listeleme, filtreleme, tablo ve durum akışları |
| 06 | Öğrenci Kartı | Profil, kur geçmişi, ders geçmişi |
| 07 | Ders Ekranı | Ders kaydı, ölçüm, not giriş akışları |
| 08 | Gelişim Raporu | Grafikler, performans karşılaştırma, özet |
| 09 | PDF Önizleme | PDF şablonu ve önizleme düzenleri |
| 10 | Prototype | Tıklanabilir akışlar ve etkileşim senaryoları |

Sayfa isimlendirme standardı:

- İki haneli sıra numarası zorunludur.
- Tüm page adları sabit tutulur, sonradan ad değiştirilmez.
- Üretim sırasında yeni deneysel çalışmalar için ayrı bir Sandbox page açılır, ana yapıya karıştırılmaz.

---

## 3. Design System Kapsamı

## 3.1 Color Styles

Tanımlanacak renk stilleri:

- Primary: #1E3A8A
- Secondary: #14B8A6
- Success: #22C55E
- Warning: #F59E0B
- Danger: #EF4444
- Purple: #8B5CF6
- Background: #F8FAFC
- Surface: #FFFFFF
- Text/Primary, Text/Secondary, Border/Subtle, Border/Strong

## 3.2 Text Styles

Font ailesi: Poppins

| Stil Adı | Önerilen Boyut | Ağırlık | Kullanım |
|---|---:|---:|---|
| Display/PageTitle | 32 | 700 | Sayfa başlıkları |
| Heading/H2 | 24 | 700 | Büyük bölüm başlıkları |
| Heading/H3 | 18 | 600 | Kart başlığı ve alt bölüm |
| Body/Regular | 14 | 400 | Standart metin |
| Body/Medium | 14 | 500 | Etiket ve yardımcı bilgi |
| Label/Small | 12 | 500 | Form etiketleri |
| Button/Label | 14 | 600 | Buton metinleri |
| Caption | 11 | 400 | Yardım metni |

## 3.3 Grid System

| Breakpoint | Frame | Grid |
|---|---:|---|
| Desktop | 1440 | 12 kolon, 24 margin, 16 gutter |
| Tablet | 1024 | 8 kolon, 20 margin, 16 gutter |
| Mobile | 390 | 4 kolon, 16 margin, 12 gutter |

## 3.4 Spacing Tokens

4, 8, 12, 16, 24, 32, 48, 64

Token adları:

- space-1: 4
- space-2: 8
- space-3: 12
- space-4: 16
- space-5: 24
- space-6: 32
- space-7: 48
- space-8: 64

## 3.5 Border Radius

- radius-sm: 8
- radius-md: 12
- radius-lg: 16
- radius-xl: 24
- radius-pill: 999

## 3.6 Shadows

- shadow-soft: 0 2 8 rgba(15,23,42,0.06)
- shadow-mid: 0 6 18 rgba(15,23,42,0.10)
- shadow-focus: 0 0 0 3 rgba(30,58,138,0.18)

## 3.7 Icons

- Boyutlar: 16, 20, 24, 32
- Stil: Outline tabanlı, aynı stroke kalınlığı
- İkon adlandırma: ic/nav-dashboard, ic/action-print, ic/status-success

---

## 4. Components (Component Set Mimarisi)

Aşağıdaki tüm bileşenler Component Set olarak oluşturulur:

- Buttons
- Cards
- Sidebar
- Topbar
- TextField
- Dropdown
- Search Box
- Status Badge
- Student Card
- Lesson Card
- Progress Bar
- Statistic Card
- Chart Card
- Table
- Modal
- Dialog
- Empty State

## 4.1 Variant Property Standardı

Her component set için ortak property yaklaşımı:

- state: default, hover, focus, pressed, disabled
- size: sm, md, lg
- theme: light (dark future-ready)
- icon: none, left, right

## 4.2 Component Bazlı Variant Matrisi

| Component | Zorunlu Variant Property | Not |
|---|---|---|
| Buttons | type, state, size, icon | type: primary/secondary/success/warning/danger/ghost |
| Cards | kind, state | kind: info/student/lesson/chart/stat |
| Sidebar | itemState, collapsed | itemState: default/active/hover |
| Topbar | mode, actionCount | mode: default/withFilters |
| TextField | state, validation, prefixIcon | validation: none/error/success |
| Dropdown | state, selection, searchable | selection: empty/selected |
| Search Box | state, resultState | resultState: idle/result/empty |
| Status Badge | status, tone | status: planned/done/cancel/makeup |
| Student Card | avatar, status, selected | avatar: on/off |
| Lesson Card | status, selected, photo | photo: on/off |
| Progress Bar | progressLevel, showLabel | progressLevel: low/medium/high |
| Statistic Card | trend, emphasis | trend: up/down/neutral |
| Chart Card | chartType, state | chartType: line/bar/pie |
| Table | density, rowState, sortable | density: compact/regular |
| Modal | size, state | size: sm/md/lg |
| Dialog | tone, actionLayout | tone: info/warning/danger |
| Empty State | type, action | type: no-data/no-search/no-filter |

---

## 5. Auto Layout Stratejisi

## 5.1 Genel Kural

- Tüm ana ekran frame'leri Auto Layout ile kurulur.
- Mutlak konumlandırma yalnızca dekoratif öğelerde kullanılır.
- Bileşenler resize olduğunda içerik taşmamalıdır.

## 5.2 Ekran Bazlı Auto Layout Planı

| Ekran | Üst Düzey Düzen | İç Düzen |
|---|---|---|
| Dashboard | Sidebar + Content (yatay) | Header + KPI row + chart row + table |
| Haftalık Program | Sidebar + Content + Right Panel | Header + Week Grid + Summary |
| Öğrenci Yönetimi | Sidebar + Content | Header + Filter row + Table |
| Öğrenci Kartı | Sidebar + Content | Header + Profile + Tabs + Timeline |
| Ders Ekranı | Sidebar + Content | Header + Session form + Metrics |
| Gelişim Raporu | Sidebar + Content | Header + Charts + Comparison cards |
| PDF Önizleme | Sidebar + Content | Header + Preview pane + Export panel |

---

## 6. Responsive Davranış (Desktop Öncelikli)

## 6.1 Breakpoint Davranışları

| Breakpoint | Kural |
|---|---|
| Desktop >= 1200 | Tüm paneller görünür, çok kolon düzen |
| Tablet 768-1199 | Sidebar daralır, ikincil paneller overlay olur |
| Mobile <= 767 | Tek kolon akış, bottom sheet etkileşim |

## 6.2 Responsive İlkeleri

- Öncelik sırası: bilgi erişimi, işlem hızı, dokunmatik ergonomi.
- Mobilde tablo bileşenleri kart görünümüne geçebilir.
- Kritik CTA butonları her kırılımda görünür kalmalıdır.

---

## 7. Haftalık Program (Merkez Ekran) Ayrıntılı Mimari

## 7.1 Frame Yapısı

| Frame | Boyut | Açıklama |
|---|---:|---|
| Weekly/Desktop/Default | 1440x1024 | Sağ panel kapalı durum |
| Weekly/Desktop/Selected | 1440x1024 | Sağ panel açık, ders seçili |
| Weekly/Tablet | 1024x1366 | Grid kaydırmalı yapı |
| Weekly/Mobile/Day | 390x844 | Gün bazlı tek kolon |

## 7.2 Layer (Katman) Düzeni

Katman sırası ve isim standardı:

1. BG/Canvas
2. Layout/Sidebar
3. Layout/Topbar
4. Layout/MainGrid
5. Layout/RightPanel
6. Layout/BottomSummary
7. Overlay/Modal
8. Overlay/Dialog

Day column katmanları:

1. Day/Header
2. Day/Row-01 ... Day/Row-09
3. Day/TimeField-01 ... Day/TimeField-09
4. Day/Slot-01 ... Day/Slot-09

## 7.3 Week Grid Kuralları

- 7 gün sabit kolon: Pazartesi-Pazar.
- Her gün altında tam 9 ders satırı.
- Saat alanı Time Picker ile düzenlenir, dropdown kullanılmaz.
- Satır yüksekliği ve kart ölçüsü tüm günlerde eşit kalır.

Önerilen ölçüler:

- Day header: 52 px
- Lesson row: 84 px
- Row gap: 10 px
- Column gap: 12 px

## 7.4 Component Kullanımı

Haftalık Program ekranında kullanılacak ana componentler:

- Sidebar/Item
- Topbar/WeekPicker
- Button/Primary-Secondary
- Calendar/TimeField
- LessonCard
- EmptyState/SlotPlus
- StatusBadge
- ProgressBar
- Panel/Section
- Summary/StatisticCard

## 7.5 Sağ Panel Planı

Bölüm sırası:

1. Öğrenci Bilgileri
2. Ders Bilgileri
3. Kur Bilgisi
4. İlerleme (6/16)
5. Son Ölçümler
6. Hızlı İşlemler

Hızlı işlemler:

- Dersi Başlat
- Öğrenci Kartı
- Düzenle
- Sil

## 7.6 Responsive Davranış

- Desktop: 7 kolon aynı anda görünür, sağ panel sabit.
- Tablet: Yatay grid kaydırılır, sağ panel overlay açılır.
- Mobile: Tek gün görünür, gün geçişi segmented control ile yapılır.

---

## 8. Prototype Planı

Ana prototip akışları:

1. Boş saatten ders oluşturma
2. Dolu karttan ders detay açma
3. Ders durum güncelleme
4. Hafta değiştirip bugüne dönme
5. Yazdır ve Excel dışa aktarma adımları

Geçiş kuralları:

- Panel açılışı: 180 ms ease-out
- Hover geri bildirimi: 120 ms
- Dialog açılışı: 150 ms scale + fade

---

## 9. Handoff ve Kalite Kontrol

Teslim öncesi kontrol listesi:

- Tüm componentler doğru page altında mı?
- Variant property adları tekil ve tutarlı mı?
- Auto Layout bozulmadan resize testi yapıldı mı?
- Layer isimleri standartta mı?
- Haftalık Programda 7x9 kuralı korunuyor mu?
- Time Picker alanı doğru bileşen olarak mı kullanıldı?
- Renk ve tipografi tokenları Design System ile eşleşiyor mu?

---

## 10. Versiyonlama

Önerilen sürüm etiketi:

- v1.0.0: İlk üretim seti
- v1.1.0: Component genişletmeleri
- v1.2.0: Responsive iyileştirmeler
- v2.0.0: Dark mode uyumlu token yapısı

Bu versiyonlama yaklaşımı, tasarım kararlarının izlenebilirliğini ve ekipler arası netliği sağlar.
