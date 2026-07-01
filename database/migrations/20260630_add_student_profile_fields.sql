-- Epic 2 - Database update for student profile fields
-- Adds missing fields requested by product scope.

ALTER TABLE students ADD COLUMN email TEXT;
ALTER TABLE students ADD COLUMN kullanici_adi TEXT;
ALTER TABLE students ADD COLUMN sifre TEXT;
ALTER TABLE students ADD COLUMN bitis_tarihi TEXT;

-- Backfill: keep existing data reachable through the new email column.
UPDATE students
SET email = eposta
WHERE (email IS NULL OR email = '')
  AND (eposta IS NOT NULL AND eposta <> '');
