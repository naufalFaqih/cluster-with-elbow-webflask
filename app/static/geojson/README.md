# GeoJSON Jawa Barat

File **`Kabupaten-Kota (Provinsi Jawa Barat).geojson`** di folder ini berisi
batas resmi kabupaten/kota Provinsi Jawa Barat (format GADM).

## Struktur Properti

Tiap feature memiliki:

| Property  | Contoh                  | Catatan                                      |
|-----------|-------------------------|----------------------------------------------|
| `NAME_2`  | `Bogor`, `Kota Bandung` | Nama wilayah; sebagian Kota sudah ber-prefix |
| `TYPE_2`  | `Kabupaten`, `Kota`     | Dipakai untuk membentuk nama kanonik         |
| `VARNAME_2` | -                     | Variant name                                 |
| `NL_NAME_2` | -                     | Native language name                         |

Logika di `peta.html` membentuk nama kanonik `KABUPATEN X` / `KOTA X` dari
`TYPE_2 + NAME_2` agar match dengan `wilayah.nama_wilayah` di database.

## Catatan Coverage

Total feature: **27** — tetapi 1 di antaranya bukan administratif:

- ✅ 26 features (Kabupaten/Kota) → match dengan 26 wilayah di DB.
- ⚠️ 1 feature `Waduk Cirata` (`TYPE_2 = Water Body`) → otomatis di-skip
  saat rendering (dianggap perairan).
- ❌ **`KABUPATEN PANGANDARAN` tidak ada di GeoJSON ini** — Pangandaran
  dimekarkan dari Ciamis pada tahun 2012, sehingga GeoJSON yang lebih lama
  tidak memuatnya. Wilayah ini tetap muncul di tabel hasil clustering namun
  **tidak akan tergambar di peta**.

Untuk memperbaiki, ganti file dengan GeoJSON yang lebih baru (mis. dari portal
OneMap Indonesia atau Bappeda Jabar). Pastikan property `NAME_2` + `TYPE_2`
tetap digunakan, atau update logika `pickName()` di `peta.html`.
