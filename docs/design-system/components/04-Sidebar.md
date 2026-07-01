# 04 - Sidebar

## Amaç

Sidebar, uygulamanin ana navigasyonunu tek bir dikey panel uzerinden sunan ve aktif rota bilgisini gorsel olarak vurgulayan temel yerlesim bilesenidir.

## Kullanım Alanları

- Uygulama geneli ana navigasyon
- Dashboard tabanli yonetim ekranlari
- Sol panel gerektiren sabit layout yapilari
- Rota bazli sayfa gecisleri

## Kullanıldığı Ekranlar

- Dashboard layout
- Ogrenciler
- Haftalik Program
- Ders Kayitlari
- Olcumler
- Gelisim Raporlari
- Ayarlar

## Kullanılmaması Gereken Yerler

- Mobilde dar alanda sabit acik panel gerekmeyen sayfalar
- Tek ekranlik, navigasyonsuz modal akislar
- Wizard adim akislari (ust stepper tercih edilir)
- Kisa sureli tek aksiyon sayfalari

## Görsel Yapı

Sidebar asagidaki bolumlerden olusur:

1. Logo/urun kimlik alani
2. Menu listesi (rota itemlari)
3. Footer (kullanici ozeti ve cikis alani)

Menu item yapisi:

- Ikon
- Label
- Aktif durumda farkli zemin ve metin rengi

## Alt Componentler

- Sidebar Container
- Brand Block
- Navigation Menu
- Navigation Item
- User Footer Block
- Logout Action Row

## Parametreler (API)

- `active_route`: Aktif rota bilgisi
- `on_navigate`: Rota degistirme callback'i
- `user_name`: Footer kullanici adi
- `user_role`: Footer rol bilgisi
- `items`: Ozel menu item listesi (opsiyonel)

Item yapisi:

- `route`
- `icon`
- `label`

## Responsive Davranış

- Desktop: Sabit sol panel gorunumu
- Laptop: Ayni yapi korunur
- Tablet ve altinda: layout seviyesinde gizleme/alternatif navigasyon uygulanabilir
- Mobil: tek kolon akis tercih edilir, sidebar genelde kapali/acilir desenle kullanilir

## Renk Kuralları

- Sidebar zemin: `primary`
- Aktif item zemin: `surface`
- Aktif item metin/ikon: `primary`
- Pasif item metin/ikon: `surface` alpha
- Ayirici cizgi: `surface` alpha

## İkon Kuralları

- Sadece Material Icons kullanilir
- Menu ikon boyutu: `24px`
- Footer avatar ikon boyutu: tasarim standardina uygun
- Ikon rengi aktif/pasif state'e gore degisir

## Boyutlar

- Sidebar genisligi: `260px`
- Menu item yuksekligi: `48px`
- Menu item radius: `10px`
- Ana baslik: `18px`
- Menu label: `16px`
- Footer metin: `12-14px`

## Padding

- Sidebar genel padding: `24px`
- Menu item yatay padding: `12px`
- Footer blok ici spacing: Design System standardina uygun sabit degerler

## Spacing

- Brand-menu-footer bloklari arasi: `24px`
- Menu itemlar arasi: `8px`
- Ikon-label arasi: `12px`
- Footer satirlari arasi: `8px`

## Örnek Kullanım

```python
from components.sidebar import build_sidebar_component

sidebar = build_sidebar_component(
	active_route="/dashboard",
	on_navigate=lambda route: None,
	user_name="Abdullah Yeter",
	user_role="Yonetici",
)
```

## Kabul Kriterleri

1. Aktif rota itemi gorsel olarak acik sekilde vurgulanir.
2. Tum menu itemlari standart boyut, radius ve spacing degerlerini korur.
3. Sidebar genisligi sabit ve layout ile uyumludur.
4. Rota gecisleri yalnizca `on_navigate` callback'i ile yonetilir.
5. Brand, menu ve footer hiyerarsisi tum ekranlarda bozulmaz.
6. Design token disina cikilmadan renk ve tipografi uygulanir.

## Definition of Done

- Sidebar dokumani tum zorunlu basliklarla tamamlanmistir.
- API parametreleri ve item yapisi netlestirilmistir.
- Responsive kullanim sinirlari acikca belirtilmistir.
- Renk, ikon, boyut, padding ve spacing kurallari standardize edilmistir.
