# Testing Plan — Black Box

Dokumen pengujian black-box untuk fitur-fitur kunci sistem. Format kompatibel
dengan PRD #28–#31. Eksekusi pengujian mengikuti urutan menu pada sidebar.

Notasi:

- ✅ = sesuai
- ❌ = tidak sesuai (buatkan issue bug)

---

## 1. Login (PRD #28)

| TC   | Skenario                              | Input                                  | Output Diharapkan                    | Hasil |
|------|---------------------------------------|----------------------------------------|--------------------------------------|-------|
| L01  | Login admin valid                     | `admin` / `admin123`                   | Redirect ke dashboard                |       |
| L02  | Login user valid                      | `user` / `user123`                     | Redirect ke dashboard                |       |
| L03  | Username salah                        | `xxx` / `admin123`                     | Flash "Username atau password salah" |       |
| L04  | Password salah                        | `admin` / `xxx`                        | Flash "Username atau password salah" |       |
| L05  | Field kosong                          | `""` / `""`                            | Flash "Username dan password wajib"  |       |
| L06  | Akses dashboard tanpa login           | GET `/dashboard/`                      | Redirect ke `/auth/login`            |       |
| L07  | Logout                                | klik menu Logout                       | Redirect ke `/auth/login` + flash    |       |
| L08  | Akses dashboard setelah logout        | GET `/dashboard/`                      | Redirect ke `/auth/login`            |       |

### 1.1 Register

| TC   | Skenario                              | Input                                  | Output Diharapkan                    | Hasil |
|------|---------------------------------------|----------------------------------------|--------------------------------------|-------|
| R01  | Register valid                        | nama, username baru, password sama     | Redirect ke login + flash sukses     |       |
| R02  | Username duplikat                     | username yang sudah terdaftar          | Flash "Username sudah digunakan"     |       |
| R03  | Password tidak sama                   | password dan konfirmasi berbeda        | Flash "Konfirmasi password tidak sesuai" |   |
| R04  | Field kosong                          | form kosong                            | Flash field wajib diisi              |       |
| R05  | Login akun baru                       | username/password hasil register       | Redirect ke dashboard                |       |
| R06  | Akses register saat sudah login       | GET `/auth/register`                   | Redirect ke dashboard                |       |

---

## 2. Kelola Data (PRD #29)

### 2.1 CRUD Wilayah

| TC   | Skenario                       | Input                                | Output Diharapkan                       | Hasil |
|------|--------------------------------|--------------------------------------|-----------------------------------------|-------|
| W01  | Tambah wilayah valid           | `KOTA TEST`                          | Tampil di tabel + flash success         |       |
| W02  | Tambah wilayah kosong          | `""`                                 | Flash "Nama wilayah wajib diisi"        |       |
| W03  | Update nama wilayah            | edit baris → `KOTA TEST 2`           | Tabel terupdate                         |       |
| W04  | Hapus wilayah (admin)          | klik Hapus pada `KOTA TEST 2`        | Konfirmasi → baris hilang               |       |
| W05  | User biasa akses POST create   | POST `/wilayah/create`               | Redirect dashboard + flash danger       |       |

### 2.2 CRUD Data Ketimpangan

| TC   | Skenario                       | Input                                  | Output Diharapkan                     | Hasil |
|------|--------------------------------|----------------------------------------|---------------------------------------|-------|
| D01  | Tambah data lengkap            | wilayah, 2023, 0.95, 0.30, 0.50, 0.97  | Baris baru di tabel                   |       |
| D02  | Tambah duplikat (wilayah/tahun)| sama                                   | Data ter-update (upsert)              |       |
| D03  | Input non-numerik              | `internet=abc`                         | Form HTML5 menolak / flash danger     |       |
| D04  | Hapus data                     | klik Hapus                             | Baris hilang dari tabel               |       |

### 2.3 Upload Dataset

| TC   | Skenario                       | Input                                                       | Output                              | Hasil |
|------|--------------------------------|-------------------------------------------------------------|-------------------------------------|-------|
| U01  | Upload Excel valid             | `dataset pemetaan diigital.csv.xlsx`                        | Flash sukses + data masuk           |       |
| U02  | Upload CSV valid               | file CSV dengan kolom wajib                                 | Flash sukses                        |       |
| U03  | Upload format tidak didukung   | `.txt`                                                      | Flash danger "format tidak didukung"|       |
| U04  | File tanpa kolom `internet`    | Excel tanpa kolom internet                                  | Flash danger "Kolom wajib …"        |       |
| U05  | File berisi NaN                | baris dengan internet kosong                                | Flash danger "missing value"        |       |
| U06  | Upload tanpa file              | submit kosong                                               | Flash danger "pilih file dahulu"    |       |

---

## 3. Proses Clustering (PRD #30)

| TC   | Skenario                                     | Output Diharapkan                                 | Hasil |
|------|----------------------------------------------|---------------------------------------------------|-------|
| C01  | Buka halaman Normalisasi                     | Tabel raw + `*_norm` rentang 0..1                 |       |
| C02  | Jalankan Elbow Method                        | Grafik SSE turun saat k naik (siku terlihat)      |       |
| C03  | Silhouette Score                             | Bar chart k=2..7, skor pada rentang -1..1         |       |
| C04  | Rekomendasi k                                | Banner sukses menampilkan k optimal               |       |
| C05  | Proses Clustering auto-k                     | Flash sukses menyebut k rekomendasi, tabel hasil terisi 27 baris | |
| C06  | Label kategori                               | 3 kategori muncul: Tinggi/Sedang/Rendah           |       |
| C07  | Re-run clustering                            | Tabel hasil tidak duplikat (replaced)             |       |
| C08  | Konsistensi label antar run                  | Kategori sama untuk wilayah yang sama             |       |
| C09  | Hapus semua data → run                       | Flash warning "Belum ada data ketimpangan"        |       |

---

## 4. Peta Tematik (PRD #31)

| TC   | Skenario                                  | Output Diharapkan                              | Hasil |
|------|-------------------------------------------|------------------------------------------------|-------|
| M01  | Buka halaman Peta Cluster                 | Peta Leaflet tampil + tile OSM                 |       |
| M02  | Polygon kab/kota                          | 27 polygon Jawa Barat tampil                   |       |
| M03  | Pewarnaan setelah clustering              | Hijau/Kuning/Merah sesuai kategori             |       |
| M04  | Wilayah tanpa hasil                       | Polygon abu-abu                                |       |
| M05  | Klik polygon                              | Popup tampil dengan nama, cluster, kategori, indikator |   |
| M06  | Legend                                    | 4 entry: Tinggi, Sedang, Rendah, Tanpa Data    |       |
| M07  | Refresh Cluster                           | Warna update sesuai cluster baru               |       |

---

## 5. Export

| TC   | Skenario                | Output                                                |
|------|-------------------------|-------------------------------------------------------|
| E01  | Export Excel            | `hasil_clustering.xlsx` ter-download, dapat dibuka    |
| E02  | Export CSV              | `hasil_clustering.csv` ter-download, encoding UTF-8   |
| E03  | Export tanpa hasil      | Flash warning "Belum ada hasil clustering"            |

---

## 6. Tooling Pengujian

- **Manual** menggunakan browser Chrome / Firefox.
- **Login akun**: gunakan `admin` (akses penuh) dan `user` (read-only).
- Setelah selesai, isi kolom **Hasil** dengan ✅ / ❌ + tanggal pengujian.
- Bug yang ditemukan dicatatkan ke issue baru sesuai PRD §6.4.
