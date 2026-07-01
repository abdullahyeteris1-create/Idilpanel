# 05 - Topbar

## Amaç

Topbar, sayfa seviyesinde baglamsal bilgi ve hizli aksiyonlari sunan ust navigasyon bilesenidir. Sayfa basligi, breadcrumb, global arama, bildirim, hizli islem ve profil erisimini tek satirda toplar.

## Kullanım Alanları

- Dashboard ve tum ana sayfa ust alanlari
- Sayfa baglami ve hiyerarsi gosterimi
- Uygulama genel arama girisi
- Bildirim ve profil islemleri

## Kullanıldığı Ekranlar

- Dashboard
- Ogrenciler
- Haftalik Program
- Ders Kayitlari
- Olcumler
- Kurslar
- Gelisim Raporlari
- Ayarlar

## Kullanılmaması Gereken Yerler

- Tam ekran modal ve odakli form akislari
- Login veya onboarding gibi sade ekranlar
- Ust bar gerektirmeyen tek aksiyon sayfalari

## Görsel Yapı

Topbar su bolumlerden olusur:

1. Sol blok
- Sayfa Basligi
- Breadcrumb

2. Sag blok
- Global Search
- Notifications
- Quick Action
- User Profile

## Alt Componentler

- Page Title Text
- Breadcrumb Text
- Search Container
- Notification Button ve Badge
- Quick Action PopupMenu
- User Profile PopupMenu

## Parametreler (API)

Mevcut API:

- Fonksiyon: build_topbar_component
- route: aktif rota
- notification_count: bildirim adedi
- user_name: profil gorunen ad
- user_role: profil rol metni

Not: Baslik ve breadcrumb route bilgisinden uretilir.

## Responsive Davranış

- Desktop: Tum bolumler gorunur
- Laptop: Tum bolumler korunur, yatay bosluk optimize edilir
- Tablet: Search ve menu grubu sikistirilabilir
- Mobil: Topbar minimal moda gecirilerek tek satir odakli kullanim tercih edilir

## Renk Kuralları

- Topbar zemin: surface
- Alt border: border
- Ana baslik: text_primary
- Breadcrumb ve yardimci metin: text_secondary
- Quick Action zemin: primary
- Quick Action metin: surface
- Notification badge: danger

## İkon Kuralları

- Sadece Material Icons kullanilir
- Search ikonu: SEARCH
- Notification ikonu: NOTIFICATIONS
- Profile avatar ikonu: ACCOUNT_CIRCLE
- Ikon boyutlari 18 ile 22 araliginda, baglam bazli tutarli olmalidir

## Boyutlar

- Topbar yuksekligi: 72 px
- Search alani: 320 x 48 px
- Notification buton: 48 x 48 px
- Quick Action yuksekligi: 48 px
- Profile alan yuksekligi: 48 px

## Padding

- Topbar genel padding: 24 12 24 12
- Search ic padding: 12 0 12 0
- Quick Action ic padding: 16 0 16 0

## Spacing

- Sol baslik ve breadcrumb arasi: 2 px
- Sag blok item arasi: 12 px
- Search ikon ve metin arasi: 8 px
- Profile ic satir arasi: 8 px

## State'ler

- Default: Tum alanlar standart renk ve shadow degerleri ile gorunur
- Hover: Interactive elemanlarda overlay veya border geri bildirimi gorunur
- Focus: Search ve menu tetikleyicilerinde odak halkasi veya belirgin odak durumu bulunur
- Disabled: Topbar genelinde standart olarak kullanilmaz, gerekiyorsa ilgili alt bilesen bazinda uygulanir
- Error: Topbar seviyesinde hata state yoktur, hata mesajlari sayfa iceriginde ele alinmalidir

## Örnek Kullanım

Asagidaki kullanim Topbar bileseninin mevcut API ile olusturulmasini gosterir:

build_topbar_component(
	route="/dashboard",
	notification_count=3,
	user_name="Abdullah Yeter",
	user_role="Yonetici"
)

## Kabul Kriterleri

1. Topbar icinde sayfa basligi, breadcrumb, global search, notifications, quick action ve user profile bolumleri vardir.
2. Baslik ve breadcrumb route bilgisinden tutarli uretilir.
3. Boyut, padding, spacing ve renk kurallari Design System ile uyumludur.
4. Interactive elemanlar odaklanabilir ve tiklanabilir alana sahiptir.
5. Responsive kirilimlarda ust barin okunabilirligi korunur.

## Definition of Done

- Tum zorunlu basliklar eksiksiz doldurulmustur.
- API parametreleri mevcut implementasyon ile uyumludur.
- Topbar ek kurallarindaki tum bolumler belgelenmistir.
- Dokuman tasarim tokenlari ve kullanim sinirlari acikca tanimlar.
