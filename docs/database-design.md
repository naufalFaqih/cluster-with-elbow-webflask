# Database Design

Sistem menggunakan 5 tabel inti. File schema utama: `database/schema.sql`
(MySQL) dan `database/schema_sqlite.sql` (SQLite fallback). Seed default:
`database/seed.sql`.

---

## 1. Tabel `users`

Akun login dengan dua role.

| Kolom        | Tipe              | Keterangan                                |
|--------------|-------------------|-------------------------------------------|
| `id`         | INT, PK, AI       |                                           |
| `nama`       | VARCHAR(100)      | nama tampilan                             |
| `username`   | VARCHAR(100), UQ  | unique, dipakai login                     |
| `password`   | VARCHAR(255)      | hash `pbkdf2:sha256` (Werkzeug)           |
| `role`       | ENUM              | `admin` / `user`                          |
| `created_at` | TIMESTAMP         |                                           |
| `updated_at` | TIMESTAMP         |                                           |

---

## 2. Tabel `wilayah`

27 kabupaten/kota Provinsi Jawa Barat.

| Kolom          | Tipe          | Keterangan                                    |
|----------------|---------------|-----------------------------------------------|
| `id`           | INT, PK, AI   |                                               |
| `nama_wilayah` | VARCHAR(100)  | huruf kapital (`KABUPATEN BOGOR`, `KOTA …`)   |
| `provinsi`     | VARCHAR(100)  | default `Jawa Barat`                          |
| timestamps     | TIMESTAMP × 2 |                                               |

---

## 3. Tabel `data_ketimpangan`

Indikator ketimpangan digital per wilayah / tahun.

| Kolom               | Tipe          | Keterangan                                  |
|---------------------|---------------|---------------------------------------------|
| `id`                | INT, PK, AI   |                                             |
| `wilayah_id`        | INT, FK       | `wilayah(id)` — `ON DELETE CASCADE`         |
| `tahun`             | INT           | default project: 2023                       |
| `internet`          | FLOAT         | rasio rumah tangga akses internet           |
| `laptop`            | FLOAT         | rasio kepemilikan komputer/laptop           |
| `smartphone`        | FLOAT         | rasio kepemilikan smartphone                |
| `literasi_digital`  | FLOAT         | indeks literasi digital                     |
| timestamps          | TIMESTAMP × 2 |                                             |

Constraint logis: `(wilayah_id, tahun)` unik (di-enforce di service layer
melalui `find_by_wilayah_tahun` + `upsert`).

---

## 4. Tabel `hasil_clustering`

Hasil K-Means per data ketimpangan.

| Kolom                    | Tipe          | Keterangan                            |
|--------------------------|---------------|---------------------------------------|
| `id`                     | INT, PK, AI   |                                       |
| `data_ketimpangan_id`    | INT, FK       | CASCADE delete                        |
| `cluster`                | INT           | label sklearn (`0..k-1`)              |
| `kategori`               | VARCHAR(50)   | `Tinggi` / `Sedang` / `Rendah`        |
| `internet_norm` dst.     | FLOAT         | hasil MinMaxScaler                    |
| `created_at`             | TIMESTAMP     |                                       |

Strategi update: **replace all** sebelum insert untuk menghindari duplikasi.

---

## 5. Tabel `evaluasi_clustering`

Hasil Elbow Method + Silhouette Score.

| Kolom                | Tipe         | Keterangan                  |
|----------------------|--------------|-----------------------------|
| `id`                 | INT, PK, AI  |                             |
| `jumlah_cluster`     | INT          | nilai `k`                   |
| `sse`                | FLOAT, NULL  | inertia (Elbow)             |
| `silhouette_score`   | FLOAT, NULL  | hanya untuk `k >= 2`        |
| `created_at`         | TIMESTAMP    |                             |

---

## 6. ER Diagram (ringkas)

```
users (id, username, role)               — independen

wilayah (id, nama_wilayah, provinsi)
   │ 1
   │   N
data_ketimpangan (wilayah_id, tahun, indikator…)
   │ 1
   │   N
hasil_clustering (data_ketimpangan_id, cluster, kategori, *_norm)

evaluasi_clustering (jumlah_cluster, sse, silhouette_score)
                                  — independen
```

---

## 7. Index & Performansi

Untuk dataset 27 wilayah, query cepat tanpa index tambahan. Jika dataset
diperluas (multi-tahun, multi-provinsi), index berikut direkomendasikan:

```sql
CREATE INDEX idx_data_wilayah_tahun ON data_ketimpangan(wilayah_id, tahun);
CREATE INDEX idx_hasil_data         ON hasil_clustering(data_ketimpangan_id);
```

---

## 8. Default Account & Seed

Setelah `seed.sql` dijalankan:

| Role  | Username | Password    |
|-------|----------|-------------|
| admin | admin    | admin123    |
| user  | user     | user123     |

Plus 27 wilayah Jawa Barat + data 2023 dari `dataset pemetaan diigital.csv.xlsx`.
