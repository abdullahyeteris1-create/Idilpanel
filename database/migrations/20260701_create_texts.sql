-- Sprint TX-1 - Metin Kutuphanesi

CREATE TABLE IF NOT EXISTS texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    course_level INTEGER NOT NULL
        CHECK (course_level >= 1),
    category TEXT,
    word_count INTEGER
        CHECK (word_count IS NULL OR word_count >= 0),
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_texts_title ON texts(title);
CREATE INDEX IF NOT EXISTS idx_texts_course_level ON texts(course_level);
CREATE INDEX IF NOT EXISTS idx_texts_is_active ON texts(is_active);
