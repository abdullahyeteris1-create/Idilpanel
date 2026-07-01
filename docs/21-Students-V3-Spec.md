"""
EPIC S-1: Students V3 - Professional Student Management Screen

GOAL
Professional student management screen with:
- Left panel: Student form (scrollable fields + fixed buttons)
- Right panel: Card-based student list (searchable, filterable)
- Top bar: Search + Status filters + New Student button
- Context menu: Actions on student

LAYOUT (based on Dashboard v2 pattern)
┌─────────────────────────────────────────────────────────────┐
│ TOP BAR: Search | Filters (Tümü/Aktif/Pasif/Tamamlanan) | New Student
├──────────────────────┬──────────────────────────────────────┤
│                      │                                      │
│  LEFT PANEL          │      RIGHT PANEL                     │
│  Student Form        │      Student List (Cards)            │
│  (%35-40)            │      (%60-65)                        │
│                      │                                      │
│  ┌────────────────┐  │  ┌──────┬──────┬──────┐             │
│  │ Öğrenci Seç ▼  │  │  │Card1 │Card2 │Card3 │ ...         │
│  ├────────────────┤  │  └──────┴──────┴──────┘             │
│  │ Ad Soyad       │  │                                      │
│  │ Sınıf          │  │  ┌──────┬──────┬──────┐             │
│  │ Veli Adı       │  │  │Card4 │Card5 │Card6 │ ...         │
│  │ Kullanıcı Adı  │  │  └──────┴──────┴──────┘             │
│  │ Şifre          │  │                                      │
│  │ Telefon        │  │ (Scrollable list)                    │
│  │ E-posta        │  │                                      │
│  │ Başlangıç      │  │                                      │
│  │ Bitiş          │  │                                      │
│  │ Kur            │  │                                      │
│  │ Notlar         │  │                                      │
│  │ Durum          │  │                                      │
│  │ (Scrollable)   │  │                                      │
│  ├────────────────┤  │                                      │
│  │ [Temizle]      │  │                                      │
│  │ [Kaydet]       │  │                                      │
│  │ [Getir]        │  │                                      │
│  │ [Güncelle]     │  │                                      │
│  │ [Sil]          │  │                                      │
│  │ (Fixed)        │  │                                      │
│  └────────────────┘  │                                      │
│                      │                                      │
└──────────────────────┴──────────────────────────────────────┘

CARD STRUCTURE
┌──────────────────┐
│ Ad Soyad          │
│ Sınıf: 3-B        │
│ Kur: Kur 1        │
│ Tel: 0555123456   │
│ [Aktif]          │ ← Badge with color
└──────────────────┘

SEARCH & FILTERS
- Search: Ad, Telefon, Kullanıcı Adı, Veli (real-time filtering)
- Status: Tümü | Aktif | Pasif | Tamamlanan

INTERACTIONS
- Click card: Select + fill form
- Double-click: Open detail view (future enhancement)
- Right-click: Context menu (Getir, Düzenle, Pasif Yap, Tamamlandı Yap, Sil)
- New: Add new student

USER FLOW
1. User clicks "Yeni Öğrenci" → Form clears, ready for input
2. User fills form → Clicks "Kaydet"
3. Student saved → List auto-refreshes → New student selected + highlighted
4. User searches → Cards filtered in real-time
5. User clicks filter → List updated

DESIGN SYSTEM ALIGNMENT
- Use existing components: build_card, build_badge, build_text_field, etc.
- No new components created
- Dashboard card pattern reused
- Turkish localization
- Responsive layout (form %, not fixed width)

TECH STACK
- Layer chain: students_v3.py → StudentController → StudentService → StudentRepository
- Flet 0.85.3
- AppLayout integration
- Responsive design (expand=True/False)

FILES
- src/views/pages/students_v3.py (new page)
- src/views/pages/students_v2.py (keep as reference, archived)
- Update: src/views/router.py (add /students-v3 route)
- Update: src/views/layout.py (add v3 link if needed)

TESTING
1. CRUD: Create, Read, Update, Delete
2. Search: Filter by multiple fields
3. Status filter: Tümü, Aktif, Pasif, Tamamlanan
4. List refresh: Auto-update on save
5. Selection: Form fills on click
6. Responsive: 1920px, 1366px, 768px, 375px
7. Empty state: No students message

SPRINT COMPLETION
- Commit: all changes to students_v3.py
- Report: List rendering logic + filter logic
- NO: keep students_v2.py for reference
"""
