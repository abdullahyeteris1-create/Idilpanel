-- MVP v0.9 - Ders kayitlari odaklanma yuzdesi
-- Eski kayitlar NULL kalir; yeni kayitlarda opsiyonel olarak doldurulur.

ALTER TABLE lessons ADD COLUMN focus_percent REAL;
