"""Turkish localization strings for user-facing UI text."""

from __future__ import annotations

TEXT = {
    "page_title": "Öğrenciler",
    "student_dropdown": "Kayıtlı Öğrenci",
    "name": "Ad Soyad",
    "class": "Sınıf",
    "kur": "Kur",
    "start_date": "Başlangıç Tarihi",
    "parent_name": "Veli Adı",
    "username": "Kullanıcı Adı",
    "password": "Şifre",
    "notes": "Notlar",
    "records": "Kayıtlar",
    "ready": "Hazır",
    "list_refresh": "Liste güncellendi.",
    "list_unavailable": "Liste alınamadı. Lütfen önce veri tabanını hazırlayın.",
    "select_record": "Lütfen kayıtlı öğrenci seçin.",
    "record_not_found": "Kayıt bulunamadı.",
    "created": "Kayıt başarıyla oluşturuldu.",
    "updated": "Kayıt başarıyla güncellendi.",
    "deleted": "Kayıt silindi.",
    "get_success": "Kayıt getirildi.",
    "unknown_error": "Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.",
    "save": "Kaydet",
    "get": "Getir",
    "list": "Listele",
    "update": "Güncelle",
    "delete": "Sil",
    "pick_date": "Tarih Seç",
    "date_required": "Bu alan zorunludur.",
    "name_required": "Bu alan zorunludur.",
    "class_required": "Bu alan zorunludur.",
    "kur_required": "Bu alan zorunludur.",
    "date_invalid": "Tarih bilgisi geçersiz.",
    "error_prefix": "İşlem sırasında bir hata oluştu.",
}

ERROR_MAP = {
    "student data must be a mapping": "Kayıt verisi geçersiz.",
    "student name cannot be empty": "Bu alan zorunludur.",
    "student first name cannot be empty": "Bu alan zorunludur.",
    "student last name cannot be empty": "Bu alan zorunludur.",
    "student class information cannot be empty": "Bu alan zorunludur.",
    "student start date cannot be empty": "Bu alan zorunludur.",
    "student start date must be a valid date": "Tarih bilgisi geçersiz.",
    "student end date must be a valid date": "Tarih bilgisi geçersiz.",
    "student end date cannot be before start date": "Bitiş tarihi başlangıç tarihinden önce olamaz.",
    "student email must be valid": "E-posta adresi geçersiz.",
    "student status must be Aktif or Beklemede": "Durum bilgisi geçersiz.",
    "lesson data must be a mapping": "Kayıt verisi geçersiz.",
    "lesson_date is required": "Bu alan zorunludur.",
    "lesson_date must be YYYY-MM-DD": "Tarih bilgisi geçersiz.",
    "student not found": "Kayıt bulunamadı.",
    "selected course does not belong to selected student": "Seçilen kurs bu öğrenciye ait değil.",
    "lesson_no must be between 1 and 16": "Ders numarası geçersiz.",
    "word_count must be positive": "Kelime sayısı geçersiz.",
    "duration must be positive": "Süre bilgisi geçersiz.",
    "comprehension must be between 0 and 100": "Anlama yüzdesi 0 ile 100 arasında olmalıdır.",
    "invalid literal for int()": "Lütfen geçerli bir kayıt seçin.",
    "FOREIGN KEY constraint failed": "İlişkili kayıt bulunamadı.",
}


def tr_text(key: str) -> str:
    return TEXT.get(key, key)


def tr_error_message(exc: Exception) -> str:
    message = str(exc)
    for source, target in ERROR_MAP.items():
        if source in message:
            return target
    return TEXT["unknown_error"]
