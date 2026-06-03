# Implementasi K-Means Clustering

Dokumen ini menjelaskan alur kerja preprocessing, normalisasi, evaluasi, dan
K-Means clustering pada sistem. Struktur ini dapat digunakan langsung sebagai
dasar **Bab IV — Hasil dan Pembahasan** skripsi.

---

## 1. Alur Pipeline

```
Database → Preprocessing → Normalisasi → Evaluasi (Elbow + Silhouette)
        → K-Means → Pelabelan Centroid → Simpan Hasil → Visualisasi
```

| Tahap         | Modul                                                     |
|---------------|-----------------------------------------------------------|
| Preprocessing | `app/services/preprocessing_service.py`                   |
| Normalisasi   | `app/services/normalization_service.py`                   |
| Evaluasi      | `app/services/evaluation_service.py`                      |
| K-Means       | `app/services/kmeans_service.py`                          |
| Persistensi   | `app/models/hasil_clustering_model.py`                    |
| Export        | `app/services/export_service.py`                          |

---

## 2. Preprocessing (`preprocessing_service.py`)

### 2.1 Pembersihan Kolom

Untuk dataset upload, kolom dirapikan menjadi snake_case dan diberi alias:

| Sumber                       | Hasil                |
|------------------------------|----------------------|
| `Lokasi kabupaten/Kota`      | `wilayah`            |
| `Literasi Digital`           | `literasi_digital`   |
| `Komputer/Laptop`            | `laptop`             |
| `Handphone`, `Hp`            | `smartphone`         |

### 2.2 Validasi

- Kolom wajib: `wilayah`, `tahun`, `internet`, `laptop`, `smartphone`,
  `literasi_digital`.
- Kolom indikator dikonversi ke numerik (`pd.to_numeric`).
- Baris dengan nilai kosong pada kolom indikator atau `wilayah/tahun`
  dianggap **invalid** → `PreprocessingError` dengan pesan eksplisit.
- Wilayah/tahun ganda dianggap duplikat → ditolak.

### 2.3 Penyiapan untuk K-Means

`to_feature_matrix(rows)` menerima list-of-dict dari DB dan mengembalikan
DataFrame siap dinormalisasi. Memvalidasi kembali bahwa tidak ada NaN
pada kolom indikator.

---

## 3. Normalisasi (`normalization_service.py`)

Menggunakan `sklearn.preprocessing.MinMaxScaler` pada 4 indikator:

```python
scaler = MinMaxScaler()
matrix = scaler.fit_transform(df[INDIKATOR].to_numpy(dtype=float))
```

- Output `matrix` adalah `numpy.ndarray` shape `(n_samples, 4)` dengan
  rentang `[0, 1]` per kolom.
- Pembulatan **tidak** dilakukan pada nilai yang dipakai untuk K-Means.
  Pembulatan hanya dilakukan saat ditampilkan di tabel preview.

---

## 4. Evaluasi (`evaluation_service.py`)

### 4.1 Elbow Method (SSE / Inertia)

```python
for k in range(1, 11):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(matrix)
    elbow.append({"k": k, "sse": model.inertia_})
```

Grafik `SSE` vs `k` ditampilkan dengan Chart.js. Titik "siku" (elbow)
menunjukkan jumlah cluster yang optimal.

Sistem mendeteksi siku secara otomatis dengan metode jarak maksimum:

1. Normalisasi titik `(k, SSE)` ke rentang 0..1.
2. Tarik garis dari titik evaluasi pertama ke titik evaluasi terakhir.
3. Pilih titik interior dengan jarak terbesar terhadap garis tersebut sebagai
   `rekomendasi_elbow`.

### 4.2 Silhouette Score

```python
for k in range(2, 11):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(matrix)
    score = silhouette_score(matrix, labels)
    silhouette.append({"k": k, "score": score})

rekomendasi_k = max(silhouette, key=lambda r: r["score"])["k"]
```

- Silhouette tidak terdefinisi untuk `k = 1`.
- Sistem menampilkan `rekomendasi_silhouette` = nilai dengan score tertinggi
  sebagai pembanding kualitas cluster.
- Hasil disimpan ke tabel `evaluasi_clustering` (`jumlah_cluster`, `sse`,
  `silhouette_score`).

### 4.3 Rekomendasi k Final

Proses clustering default menggunakan auto-k:

```python
rekomendasi_final = rekomendasi_elbow or rekomendasi_silhouette or 3
```

Elbow menjadi rekomendasi utama. Silhouette dipakai sebagai fallback jika
Elbow tidak bisa dihitung, misalnya karena titik evaluasi terlalu sedikit.
Nilai fallback `3` tetap dibatasi oleh jumlah data yang tersedia.

---

## 5. K-Means (`kmeans_service.py`)

```python
model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
labels = model.fit_predict(matrix)
centroids = model.cluster_centers_
```

Parameter:

- `random_state=42` — agar hasil reproducible.
- `n_init=10` — KMeans mencoba 10 inisialisasi acak; centroid terbaik dipakai.
- `n_clusters` default berasal dari `rekomendasi_final`, bukan hard-code `3`.
  Override manual tetap dapat dikirim melalui form jika dibutuhkan.

---

## 6. Pelabelan Centroid (`label_clusters_by_centroid`)

> **Pelabelan TIDAK boleh berdasarkan nomor cluster acak dari sklearn.**
> Pelabelan dilakukan berdasarkan **rata-rata nilai centroid** per cluster
> (4 indikator → 1 nilai skalar).

```python
means = centroids.mean(axis=1)        # shape (n_clusters,)
order = np.argsort(-means)            # descending → cluster 'paling tinggi' dulu
mapping = {
    order[0]: "Tinggi",
    order[1]: "Sedang",
    order[2]: "Rendah",
}
```

Untuk `k = 2` → label `Tinggi` & `Rendah`. Untuk `k > 3`, urutan centroid
tetap dikelompokkan ke tiga kategori: bagian atas `Tinggi`, bagian tengah
`Sedang`, dan bagian bawah `Rendah`.

**Konsekuensi**: meskipun di run berikutnya sklearn mengembalikan nomor
cluster yang berbeda, **kategori** (Tinggi/Sedang/Rendah) tetap konsisten
karena ditentukan oleh nilai centroid, bukan urutan label.

---

## 7. Persistensi Hasil

Tabel `hasil_clustering`:

| Kolom                       | Asal                                          |
|-----------------------------|-----------------------------------------------|
| `data_ketimpangan_id`       | FK ke `data_ketimpangan.id`                   |
| `cluster`                   | label numerik dari sklearn                    |
| `kategori`                  | hasil `label_clusters_by_centroid`            |
| `internet_norm` dst.        | nilai matrix ter-normalisasi                  |

Strategi **replace**:

```python
hasil_clustering_model.truncate()
hasil_clustering_model.insert_many(rows)
```

Dengan begitu, menjalankan ulang clustering tidak meninggalkan duplikasi.

---

## 8. Visualisasi & Export

- **Tabel hasil** (`/clustering/hasil`) — daftar wilayah + kategori + filter.
- **Peta tematik** (`/peta`) — Leaflet + GeoJSON; warna polygon mengikuti
  kategori (`Tinggi=hijau`, `Sedang=kuning`, `Rendah=merah`). Popup
  menampilkan tahun, cluster, kategori, dan 4 indikator (asli + normalisasi).
- **Export** (`/clustering/export/excel|csv`) — file berisi nama wilayah,
  tahun, indikator asli, indikator ternormalisasi, cluster, kategori.

---

## 9. Reproduktibilitas

Konfigurasi yang menjamin hasil konsisten:

```text
random_state = 42
n_init       = 10
indikator    = [internet, laptop, smartphone, literasi_digital]
tahun_data   = 2023
```

Selama dataset & parameter di atas tidak berubah, hasil clustering & label
kategori akan sama persis di setiap run.
