-- IDIL HIZLI OKUMA
-- Official SQLite schema (v1)
-- Rules applied:
-- - CREATE TABLE, PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, DEFAULT, INDEX
-- - No trigger, no view, no seed/insert data, no migration scripts

-- 1) students
-- Holds student identity and contact information.
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_soyad TEXT NOT NULL,
    sinif TEXT,
    veli_adi TEXT,
    telefon TEXT,
    eposta TEXT,
    baslangic_tarihi TEXT NOT NULL,
    durum TEXT NOT NULL DEFAULT 'Aktif'
        CHECK (durum IN ('Aktif', 'Beklemede')),
    notlar TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    deleted_at TEXT DEFAULT NULL,
    UNIQUE (eposta, is_active)
);

-- 2) courses
-- Represents course cycles of a student (one student can have many courses).
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    kur_no INTEGER NOT NULL,
    baslangic TEXT NOT NULL,
    bitis TEXT,
    durum TEXT NOT NULL DEFAULT 'Aktif'
        CHECK (durum IN ('Aktif', 'Beklemede', 'Tamamlandi', 'Iptal')),
    hedef_ders_sayisi INTEGER NOT NULL DEFAULT 16
        CHECK (hedef_ders_sayisi = 16),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    deleted_at TEXT DEFAULT NULL,
    UNIQUE (student_id, kur_no, is_active),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- 3) schedules
-- Planned lessons in weekly calendar (planning model, not actual execution).
CREATE TABLE schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER,
    plan_tarihi TEXT NOT NULL,
    baslangic_saati TEXT NOT NULL,
    bitis_saati TEXT NOT NULL,
    durum TEXT NOT NULL DEFAULT 'Planlandi'
        CHECK (durum IN ('Planlandi', 'Tamamlandi', 'Gelmedi', 'Iptal', 'Telafi Bekliyor', 'Yarim Kaldi')),
    aciklama TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    deleted_at TEXT DEFAULT NULL,
    UNIQUE (plan_tarihi, baslangic_saati, bitis_saati, is_active),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    CHECK (bitis_saati > baslangic_saati)
);

-- 4) lessons
-- Actual lesson records (execution model, separate from schedules).
CREATE TABLE lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER,
    course_id INTEGER NOT NULL,
    lesson_no INTEGER NOT NULL
        CHECK (lesson_no BETWEEN 1 AND 16),
    tarih TEXT NOT NULL,
    metin TEXT,
    durum TEXT NOT NULL DEFAULT 'Planlandi'
        CHECK (durum IN ('Planlandi', 'Tamamlandi', 'Gelmedi', 'Iptal', 'Telafi Bekliyor', 'Yarim Kaldi')),
    ogretmen_notu TEXT,
    baslangic_gercek TEXT,
    bitis_gercek TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    deleted_at TEXT DEFAULT NULL,
    UNIQUE (course_id, lesson_no, is_active),
    FOREIGN KEY (schedule_id) REFERENCES schedules(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- 5) measurements
-- Performance metrics of a lesson. Kept separate for normalization.
CREATE TABLE measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER NOT NULL,
    kelime_sayisi INTEGER NOT NULL
        CHECK (kelime_sayisi >= 0),
    sure REAL NOT NULL
        CHECK (sure > 0),
    okuma_hizi REAL NOT NULL
        CHECK (okuma_hizi >= 0),
    anlama REAL NOT NULL
        CHECK (anlama >= 0 AND anlama <= 100),
    odak INTEGER NOT NULL
        CHECK (odak BETWEEN 1 AND 10),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    deleted_at TEXT DEFAULT NULL,
    UNIQUE (lesson_id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

-- 6) reports
-- Stores generated report/PDF history.
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER,
    rapor_tipi TEXT NOT NULL
        CHECK (rapor_tipi IN ('Haftalik', 'Kur Sonu', 'Ozel')),
    baslangic_tarih TEXT,
    bitis_tarih TEXT,
    dosya_yolu TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    deleted_at TEXT DEFAULT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- 7) report_items
-- Bridge table for many-to-many relation between reports and lessons.
CREATE TABLE report_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    lesson_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    deleted_at TEXT DEFAULT NULL,
    UNIQUE (report_id, lesson_id, is_active),
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

-- 8) settings
-- Application-level key/value settings.
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ayar_anahtari TEXT NOT NULL,
    ayar_degeri TEXT NOT NULL,
    kategori TEXT,
    aciklama TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    deleted_at TEXT DEFAULT NULL,
    UNIQUE (ayar_anahtari, is_active)
);

-- Indexes
CREATE INDEX idx_students_ad_soyad ON students(ad_soyad);
CREATE INDEX idx_students_durum ON students(durum);

CREATE INDEX idx_courses_student_kur_no ON courses(student_id, kur_no);
CREATE INDEX idx_courses_durum ON courses(durum);

CREATE INDEX idx_schedules_plan_tarih_saat ON schedules(plan_tarihi, baslangic_saati);
CREATE INDEX idx_schedules_durum ON schedules(durum);

CREATE INDEX idx_lessons_tarih ON lessons(tarih);
CREATE INDEX idx_lessons_course_lesson_no ON lessons(course_id, lesson_no);
CREATE INDEX idx_lessons_durum ON lessons(durum);

CREATE INDEX idx_measurements_lesson_id ON measurements(lesson_id);

CREATE INDEX idx_reports_student_created_at ON reports(student_id, created_at);
CREATE INDEX idx_reports_rapor_tipi ON reports(rapor_tipi);

CREATE INDEX idx_report_items_report_id ON report_items(report_id);
CREATE INDEX idx_report_items_lesson_id ON report_items(lesson_id);

CREATE INDEX idx_settings_anahtar ON settings(ayar_anahtari);
