-- ============================================================
-- Schema SQLite (fallback dev) — Pemetaan Ketimpangan Digital Jawa Barat
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wilayah (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_wilayah TEXT NOT NULL,
    provinsi TEXT DEFAULT 'Jawa Barat',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_ketimpangan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wilayah_id INTEGER NOT NULL,
    tahun INTEGER NOT NULL,
    internet REAL NOT NULL,
    laptop REAL NOT NULL,
    smartphone REAL NOT NULL,
    literasi_digital REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wilayah_id) REFERENCES wilayah(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS hasil_clustering (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_ketimpangan_id INTEGER NOT NULL,
    cluster INTEGER NOT NULL,
    kategori TEXT NOT NULL,
    internet_norm REAL,
    laptop_norm REAL,
    smartphone_norm REAL,
    literasi_digital_norm REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (data_ketimpangan_id) REFERENCES data_ketimpangan(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS evaluasi_clustering (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jumlah_cluster INTEGER NOT NULL,
    sse REAL,
    silhouette_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
