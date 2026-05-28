# GeoJSON Jawa Barat

File **`jabar_kabkota.geojson`** di folder ini berisi batas kabupaten/kota Provinsi
Jawa Barat. Setiap feature memiliki properti:

- `nama_kabkota` — nama wilayah dalam huruf kapital, harus cocok dengan `wilayah.nama_wilayah` di database.
- `provinsi` — `JAWA BARAT`.

## Mengganti dengan GeoJSON Resmi

GeoJSON yang ter-bundle adalah **placeholder** (polygon kotak ~10–15 km berbasis
centroid kab/kota) agar peta dapat dirender saat development. Untuk hasil
visualisasi yang akurat:

1. Unduh GeoJSON resmi Jawa Barat (mis. dari portal OneMap Indonesia atau dataset
   Bappeda Jabar).
2. Pastikan ada properti `nama_kabkota` (atau `WADMKK` / `NAME_2`).
3. Replace file `jabar_kabkota.geojson` di folder ini.

Logika pemilihan property name di `dashboard.html` dan `peta.html` mendukung
beberapa fallback (`nama_kabkota`, `WADMKK`, `NAME_2`, `name`).
