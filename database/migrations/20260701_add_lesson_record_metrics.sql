-- Sprint LR-2 - Kur bazli ders kaydi alanlari
-- Hizi kullanici manuel girer; anlama/algi opsiyoneldir.

ALTER TABLE lessons ADD COLUMN okuma_hizi REAL;
ALTER TABLE lessons ADD COLUMN anlama_algi REAL;
ALTER TABLE lessons ADD COLUMN gun_no INTEGER NOT NULL DEFAULT 1;
