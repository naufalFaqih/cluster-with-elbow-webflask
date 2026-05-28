# Sistem Pemetaan Ketimpangan Digital Jawa Barat

Aplikasi web berbasis Flask untuk memetakan ketimpangan digital antar kabupaten/kota di Provinsi Jawa Barat menggunakan algoritma **K-Means Clustering**, evaluasi **Elbow Method** dan **Silhouette Score**, serta visualisasi **peta tematik** dengan Leaflet.js.

## Fitur Utama

- Autentikasi login/logout (role: `admin`, `user`)
- Dashboard ringkasan analisis
- CRUD data wilayah dan data ketimpangan digital
- Upload dataset Excel/CSV
- Preprocessing dan normalisasi MinMaxScaler
- Penentuan jumlah cluster optimal (Elbow Method + Silhouette Score)
- Proses K-Means clustering dengan pelabelan **berdasarkan centroid** (Tinggi / Sedang / Rendah)
- Tabel hasil clustering + export Excel/CSV
- Peta tematik kabupaten/kota Jawa Barat (Leaflet.js + GeoJSON)

## Tech Stack

- **Backend**: Python 3.10+, Flask, mysql-connector-python, pandas, numpy, scikit-learn, openpyxl
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript, Chart.js, Leaflet.js
- **Database**: MySQL 8.x (atau SQLite untuk pengembangan lokal)

## Struktur Folder

```
pemetaan-digital-jabar/
├── app.py                  # entry point
├── config.py               # konfigurasi
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py         # Flask factory
│   ├── db.py               # helper koneksi DB (mysql / sqlite fallback)
│   ├── models/             # 4 model (user, wilayah, data_ketimpangan, hasil_clustering)
│   ├── routes/             # 6 blueprint
│   ├── services/           # preprocessing, normalization, kmeans, evaluation, export
│   ├── templates/          # Jinja2 templates
│   └── static/             # css, js, geojson
├── database/
│   ├── schema.sql          # MySQL schema
│   ├── schema_sqlite.sql   # SQLite schema (fallback)
│   └── seed.sql            # akun default + 27 kab/kota + data 2023
├── uploads/                # file upload sementara (di-ignore git)
└── docs/
    ├── PRD.md
    ├── workflow-github.md
    ├── database-design.md
    └── testing-plan.md
```

## Setup

### 1. Clone & buat virtual environment

```bash
git clone <repo-url> pemetaan-digital-jabar
cd pemetaan-digital-jabar
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Setup environment

```bash
cp .env.example .env       # Linux/macOS
copy .env.example .env     # Windows
```

Edit `.env` sesuai konfigurasi MySQL Anda. Untuk pengembangan cepat tanpa MySQL, set `DB_DRIVER=sqlite`.

### 3. Setup database

#### MySQL

```bash
mysql -u root -p
CREATE DATABASE pemetaan_digital_jabar;
exit
mysql -u root -p pemetaan_digital_jabar < database/schema.sql
mysql -u root -p pemetaan_digital_jabar < database/seed.sql
```

#### SQLite (fallback dev)

Jalankan helper init (akan otomatis saat `DB_DRIVER=sqlite`):

```bash
python -c "from app import create_app; from app.db import init_sqlite; create_app(); init_sqlite()"
```

### 4. Jalankan aplikasi

```bash
python app.py
```

Buka `http://localhost:5000`.

### Akun default

| Role  | Username | Password    |
|-------|----------|-------------|
| admin | admin    | admin123    |
| user  | user     | user123     |

## Variabel Indikator (Data 2023)

1. `internet`           — Persentase rumah tangga dengan akses internet
2. `laptop`             — Persentase penduduk yang memiliki komputer/laptop
3. `smartphone`         — Persentase penduduk yang memiliki smartphone
4. `literasi_digital`   — Indeks literasi digital

## Algoritma

- **Normalisasi**: `MinMaxScaler` (rentang 0–1).
- **Elbow Method**: SSE (inertia) untuk `k = 1..10`.
- **Silhouette Score**: untuk `k = 2..10`.
- **K-Means**: `random_state=42`, `n_init=10`.
- **Pelabelan**: rata-rata centroid → Tinggi / Sedang / Rendah (bukan berdasarkan nomor cluster).

## Lisensi

Untuk keperluan akademik (skripsi).
