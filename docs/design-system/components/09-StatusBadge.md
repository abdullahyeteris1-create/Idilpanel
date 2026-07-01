# 09 - StatusBadge

## Amaç

StatusBadge, kayit veya islem durumunu kisa ve renk kodlu bir etiketle gosteren mikro bilesendir.

## Kullanım Alanları

- Durum etiketleri (aktif, bekliyor, tamamlandi, iptal)
- Tablo satiri durum kolonlari
- Kart icindeki durum ozetleri
- Filtre chip benzeri semantik isaretlemeler

## Kullanıldığı Ekranlar

- Dashboard ders ve olcum kartlari
- Ogrenci, ders, rapor liste alanlari
- Form yaninda durum gostergesi gereken bolgeler

## Kullanılmaması Gereken Yerler

- Uzun metin aciklamalari
- Buton yerine tiklanabilir ana aksiyon olarak
- Kritik hata mesaji gostermek icin, bunun yerine alert kullanilir

## Görsel Yapı

Badge yapisi:

1. Opsiyonel ikon
2. Durum metni
3. Semantik renkli zemin ve border

## Alt Componentler

- Badge Container
- Optional Icon
- Label Text
- Tone Border

## API

Mevcut API:

- build_badge
- text: badge metni
- variant: tone tipi
- icon: opsiyonel icon

Desteklenecek tipler:

- success
- warning
- danger
- info
- neutral

Not: mevcut implementasyonda info ve neutral tipleri secondary/passive tonlariyla eslenebilir.

## Responsive Davranış

- Desktop/Tablet/Mobil: inline kompakt gorunum korunur
- Dar alanda metin kisaltma veya wrap stratejisi baglama gore uygulanir

## State'ler

- Default: semantik renkli normal gorunum
- Hover: ihtiyaca gore hafif vurgu, zorunlu degil
- Focus: klavye odagi gereken interaktif badge senaryosunda gorunur odak
- Disabled: pasif gorunum, dusuk kontrastli varyant

## Boyutlar

- Yazi boyutu: caption/small araligi
- Ikon boyutu: 16 px
- Radius: button radius standardi
- Yatay/dikey padding: sm/xs tokenlari

## Padding

- Sol/sag: sm
- Ust/alt: xs

## Spacing

- Ikon-metin arasi: xs
- Badge'ler arasi: sm veya md

## Renk Kuralları

- success: yesil ton
- warning: sari/turuncu ton
- danger: kirmizi ton
- info: mavi/ikincil bilgi tonu
- neutral: gri/pasif ton
- Her tonda metin ve border ayni semantik tona bagli olmalidir

## İkon Kuralları

- Sadece Material Icons
- Ikon opsiyoneldir
- Ikon kullanildiginda metin semantigini desteklemelidir

## Accessibility

- Metin kontrasti okunabilir seviyede olmalidir
- Renk tek basina anlam tasimamalidir; metinle desteklenmelidir
- Interaktif badge ise odak ve klavye erisimi zorunludur

## Örnek Kullanım

build_badge(
	text="Tamamlandi",
	variant="success",
	icon="CHECK_CIRCLE"
)

## Kabul Kriterleri

1. success, warning, danger, info, neutral tipleri dokumanda net tanimlanir.
2. Badge ikonlu ve ikonsuz kullanimlari destekler.
3. Boyut, padding, spacing ve radius Design System ile tutarlidir.
4. Renk kurallari semantik ve erisilebilir kontrastla tanimlanmistir.

## Definition of Done

- 18 baslik eksiksiz doldurulmustur.
- StatusBadge tipleri ve API parametreleri netlestirilmistir.
- Accessibility ve semantik renk kurallari belgelenmistir.
