"""Create GitHub issues #38-#41 for the map-improvement work."""
import subprocess, sys

REPO = "naufalFaqih/cluster-with-elbow-webflask"

ISSUES = [
    (38, "chore: ganti placeholder GeoJSON dengan boundary resmi", "chore",
     "chore/38-replace-placeholder-geojson",
     "Hapus `jabar_kabkota.geojson` (placeholder polygon kotak) dan ganti dengan "
     "GeoJSON resmi GADM Jawa Barat (~7.4 MB). Update peta.html + dashboard agar "
     "mereferensi file baru. Reformat kedua template dengan style Prettier."),
    (39, "feat: cluster statistics API untuk map visualisation", "feature",
     "feature/39-cluster-stats-api",
     "Tambah `hasil_clustering_model.cluster_stats()` yang mengembalikan agregat per kategori: "
     "jumlah, persentase, rata-rata skor ketimpangan (1 - mean indikator), cluster_no terurut "
     "Tinggi → Sedang → Rendah, dan deskripsi human-readable. Endpoint baru `/peta/api/stats`. "
     "Endpoint `/peta/api/hasil` ditambahkan field `skor_ketimpangan` + `jumlah_variabel`."),
    (40, "feat: redesign halaman peta — sidebar layout + ringkasan table", "feature",
     "feature/40-map-redesign-layout",
     "Implementasi mengikuti referensi `peta-visualisasi.jpeg`:\n\n"
     "- Info banner di atas peta\n"
     "- Two-column grid: Leaflet map (kiri) + 3 panel sidebar (kanan)\n"
     "  → Keterangan Cluster, Informasi, Statistik Cluster\n"
     "- Tabel **Ringkasan Hasil Clustering** di bawah peta dengan kolom: "
     "Cluster (badge warna), Kategori, Jumlah Wilayah, Persentase, "
     "Rata-rata Skor Ketimpangan, Keterangan\n"
     "- Permanent label nama wilayah pada setiap polygon (text-shadow)\n"
     "- Popup redesigned: title + Cluster + Skor Ketimpangan + Jumlah Variabel + "
     "link 'Klik untuk detail'\n"
     "- Hover highlight pada polygon\n"
     "- Responsive: panel stack ke bawah peta jika viewport < 1100px\n\n"
     "**Skema warna existing dipertahankan** (Tinggi=hijau, Sedang=kuning, Rendah=merah) "
     "untuk konsistensi dengan dashboard dan halaman hasil."),
    (41, "fix: matching nama wilayah untuk format GADM", "bugfix",
     "bugfix/41-geojson-name-matching",
     "GeoJSON resmi GADM punya struktur:\n"
     "- `NAME_2 = 'Bogor'`, `TYPE_2 = 'Kabupaten'`\n"
     "- `NAME_2 = 'Kota Bogor'`, `TYPE_2 = 'Kota'`\n"
     "- Sebagian Kota tanpa prefix di NAME_2: `Banjar`/`Cimahi`/`Depok`\n\n"
     "Refactor `pickName()` untuk:\n"
     "- Pakai `TYPE_2` membentuk nama kanonik `KABUPATEN X` / `KOTA X`\n"
     "- Strip prefix `KOTA `/`KABUPATEN ` dari NAME_2 jika sudah ada\n"
     "- Skip non-administrative features (`Waduk Cirata` punya TYPE_2='Water Body')\n\n"
     "Hasil verifikasi: **26/26 admin features match** dengan DB. "
     "1 water body otomatis di-skip dengan styling biru subtle. "
     "**Kabupaten Pangandaran tidak ada di GeoJSON ini** (dimekarkan dari Ciamis pada 2012, "
     "GeoJSON lebih lama) — didokumentasikan di `app/static/geojson/README.md`."),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        sys.stderr.write(f"FAILED: {' '.join(cmd)}\n{r.stderr}\n")
        raise SystemExit(r.returncode)
    return r.stdout.strip()


def issue_body(num, title, kind, branch, summary):
    parts = [
        "## Deskripsi", summary, "",
        "## Branch", f"`{branch}`", "",
        "## Status",
        f"✅ Selesai dan ter-merge ke `develop` → `main` via branch `{branch}`.",
    ]
    return "\n".join(parts)


for num, title, kind, branch, summary in ISSUES:
    body = issue_body(num, title, kind, branch, summary)
    label_map = {"feature": "enhancement", "bugfix": "bug", "chore": "enhancement"}
    cmd = [
        "gh", "issue", "create", "--repo", REPO,
        "--title", title,
        "--body", body,
        "--label", label_map.get(kind, "enhancement"),
    ]
    if kind == "feature":
        cmd += ["--label", "feature"]
    url = run(cmd)
    print(f"  #{num}  {title:60s} {url}")

    issue_n = url.rstrip("/").rsplit("/", 1)[-1]
    run(["gh", "issue", "close", issue_n, "--repo", REPO,
         "--comment",
         f"Diselesaikan via `{branch}` dan ter-merge ke develop → main."])
    print(f"        -> closed (resolved by {branch})")

print("\nDone.")
