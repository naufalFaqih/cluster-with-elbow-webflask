# GeoJSON Jawa Barat

File **`Kabupaten-Kota (Provinsi Jawa Barat).geojson`** di folder ini berisi
batas resmi 27 kabupaten/kota Provinsi Jawa Barat. Setiap feature memiliki
properti `WADMKK` / `nama_kabkota` / `NAME_2` yang dipakai untuk match dengan
`wilayah.nama_wilayah` di database.

Logika pemilihan property name di `peta.html` dan `dashboard/index.html`
mendukung beberapa fallback (`nama_kabkota`, `WADMKK`, `NAME_2`, `name`).
