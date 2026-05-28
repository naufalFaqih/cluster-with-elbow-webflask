# PRD — Sistem Pemetaan Ketimpangan Digital Jawa Barat

> Salinan PRD/Project Requirement Document untuk arsip `docs/`. Sumber asli berada
> pada dokumen "Sistem Pemetaan Ketimpangan Digital Jawa Barat.pdf".

## 1. Informasi Project

- **Nama**: Sistem Pemetaan Ketimpangan Digital di Jawa Barat Menggunakan K-Means Clustering
- **Tujuan**: Aplikasi web Flask untuk mengelola data indikator ketimpangan
  digital kabupaten/kota di Jawa Barat, melakukan clustering K-Means,
  evaluasi Elbow Method + Silhouette Score, serta visualisasi peta tematik.
- **Target Pengguna**: Admin (kelola data, hasil, visualisasi) & User
  (login, pilih variabel, jalankan clustering, lihat hasil + peta).

## 2. Fitur Utama

1. Autentikasi login/logout (role: `admin`, `user`)
2. Dashboard ringkasan (4 stat card, Elbow chart, donut, peta)
3. CRUD wilayah & CRUD data ketimpangan digital
4. Upload dataset Excel/CSV
5. Preprocessing data + Normalisasi MinMaxScaler
6. Penentuan k optimal: Elbow Method + Silhouette Score
7. K-Means Clustering (`random_state=42`, `n_init=10`)
8. Pelabelan cluster Tinggi / Sedang / Rendah berdasarkan **rata-rata centroid**
9. Penyimpanan hasil clustering ke DB (replace lama → tidak duplikat)
10. Tabel hasil + filter kategori
11. Peta tematik (Leaflet.js + GeoJSON) dengan popup detail
12. Export hasil clustering ke Excel & CSV
13. Black box testing untuk fitur kunci

## 3. Tech Stack

| Layer    | Pilihan                                                                  |
|----------|--------------------------------------------------------------------------|
| Backend  | Python 3.10+, Flask, mysql-connector-python, pandas, numpy, scikit-learn, openpyxl |
| Frontend | HTML, CSS, Bootstrap-style custom CSS, JavaScript, Chart.js, Leaflet.js  |
| Database | MySQL 8.x (atau SQLite untuk pengembangan lokal)                         |
| Tools    | Visual Studio Code, Git, GitHub                                          |

## 4. Variabel Indikator (Data 2023)

| Variabel            | Deskripsi                                                |
|---------------------|----------------------------------------------------------|
| `internet`          | Persentase rumah tangga dengan akses internet            |
| `laptop`            | Persentase penduduk yang memiliki komputer/laptop        |
| `smartphone`        | Persentase penduduk yang memiliki smartphone             |
| `literasi_digital`  | Indeks literasi digital                                  |

Wilayah penelitian: 27 kabupaten/kota Provinsi Jawa Barat.

## 5. Database Schema

5 tabel inti — lihat `docs/database-design.md`.

## 6. Algoritma

- **Normalisasi**: `MinMaxScaler` (rentang 0–1).
- **Elbow Method**: SSE (`KMeans.inertia_`) untuk `k = 1..10`.
- **Silhouette Score**: `sklearn.metrics.silhouette_score` untuk `k = 2..10`.
  Rekomendasi `k` = nilai dengan score tertinggi.
- **K-Means**: `random_state=42`, `n_init=10`.
- **Pelabelan**: rata-rata centroid → urut descending → `Tinggi` / `Sedang` / `Rendah`.

## 7. Output

- Aplikasi web Flask siap dijalankan.
- Login admin (`admin`/`admin123`) dan user (`user`/`user123`).
- Dataset 27 kab/kota tahun 2023 sudah ter-seed.
- Hasil clustering tampil di tabel + peta tematik.
- Export Excel/CSV.
- Dokumentasi `docs/` lengkap untuk Bab IV skripsi.

## 8. Risiko & Mitigasi (ringkas)

| Risiko                              | Mitigasi                                                |
|-------------------------------------|---------------------------------------------------------|
| Nama wilayah ≠ GeoJSON              | Mapping huruf kapital + alias `KAB./KOTA`               |
| Label cluster salah                 | Berdasarkan rata-rata centroid, bukan nomor cluster     |
| Dataset tidak lengkap               | `PreprocessingError` dengan pesan eksplisit             |
| Hasil cluster bervariasi tiap run   | `random_state=42`, `n_init=10`                          |
| Elbow subjektif                     | Silhouette Score sebagai pendamping evaluasi            |
