"""Create GitHub issues for the project per PRD section 7.

Issues #1-#34 mirror the PRD task list. #35 covers dashboard refactor.
#36 is the login redirect bugfix discovered during smoke test.

Run from project root:
    python scripts/create_issues.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = "naufalFaqih/cluster-with-elbow-webflask"

# (number, title, kind, branch, body)
# kind in {feature, docs, refactor, bugfix, test}
ISSUES = [
    (1,  "Setup Repository GitHub",                 "feature",  "feature/1-setup-repository",                  "Inisialisasi repository: .gitignore, README, struktur folder awal, branch main + develop."),
    (2,  "Setup Flask Project",                     "feature",  "feature/2-setup-flask-project",               "Buat Flask app factory, app.py, config.py, struktur app/{routes,models,services,templates,static}."),
    (3,  "Setup Configuration dan Environment",     "feature",  "feature/3-setup-environment-config",          "Buat .env.example, dotenv loading di config.py, konfigurasi DB + secret key + uploads."),
    (4,  "Membuat Schema Database",                 "feature",  "feature/4-create-database-schema",            "5 tabel: users, wilayah, data_ketimpangan, hasil_clustering, evaluasi_clustering. MySQL + SQLite fallback."),
    (5,  "Membuat Seeder Data Awal",                "feature",  "feature/5-create-database-seeder",            "Akun admin/user default, 27 kab/kota Jawa Barat, data ketimpangan 2023."),
    (6,  "Membuat Koneksi Database",                "feature",  "feature/6-database-connection",               "Helper DBHelper di app/db.py, support MySQL + SQLite, normalize %s placeholder, init SQLite otomatis."),
    (7,  "Implementasi Login",                      "feature",  "feature/7-login",                             "User model dengan pbkdf2 hash, /auth/login route, login.html template dengan branded card."),
    (8,  "Implementasi Logout",                     "feature",  "feature/8-logout",                            "Route /auth/logout, clear session, redirect ke login dengan flash."),
    (9,  "Implementasi Role Admin dan User",        "feature",  "feature/9-role-based-access",                 "Decorator login_required + admin_required di app/routes/decorators.py."),
    (10, "Membuat Layout Utama",                    "feature",  "feature/10-main-layout",                      "base.html dengan sidebar biru + topbar + content area. Sidebar nav berdasarkan role."),
    (11, "Membuat Dashboard",                       "feature",  "feature/11-dashboard",                        "Dashboard route + template dengan 4 stat card (jumlah wilayah, variabel, metode, status)."),
    (12, "CRUD Data Wilayah",                       "feature",  "feature/12-crud-wilayah",                     "wilayah_model + wilayah_routes + template untuk admin tambah/edit/hapus wilayah."),
    (13, "CRUD Data Ketimpangan Digital",           "feature",  "feature/13-crud-data-ketimpangan",            "data_ketimpangan_model + data_routes + template dengan validasi numerik 4 indikator."),
    (14, "Upload Dataset Excel/CSV",                "feature",  "feature/14-upload-dataset",                   "Halaman upload, terima .xlsx/.xls/.csv, validasi kolom wajib, simpan ke DB."),
    (15, "Implementasi Preprocessing Data",         "feature",  "feature/15-preprocessing-data",               "preprocessing_service: clean_uploaded_dataframe + to_feature_matrix, alias kolom, cek missing/duplikat."),
    (16, "Implementasi Normalisasi MinMaxScaler",   "feature",  "feature/16-minmax-normalization",             "normalization_service pakai sklearn MinMaxScaler. Tabel preview hasil normalisasi."),
    (17, "Implementasi Elbow Method",               "feature",  "feature/17-elbow-method",                     "evaluation_service hitung SSE k=1..10, tampilkan grafik Elbow + tabel."),
    (18, "Implementasi Silhouette Score",           "feature",  "feature/18-silhouette-score",                 "Hitung silhouette k=2..10, tampilkan rekomendasi k tertinggi."),
    (19, "Implementasi K-Means Service",            "feature",  "feature/19-kmeans-service",                   "kmeans_service.run_kmeans dengan random_state=42, n_init=10."),
    (20, "Pelabelan Cluster Berdasarkan Centroid",  "feature",  "feature/20-cluster-labeling-centroid",        "label_clusters_by_centroid: rata-rata centroid -> Tinggi/Sedang/Rendah, konsisten antar run."),
    (21, "Simpan Hasil Clustering ke Database",     "feature",  "feature/21-save-clustering-result",           "hasil_clustering_model truncate + insert_many. Replace strategy untuk mencegah duplikat."),
    (22, "Halaman Hasil Clustering",                "feature",  "feature/22-clustering-result-page",           "Tabel hasil + filter kategori + summary card per kategori."),
    (23, "Export Hasil Clustering",                 "feature",  "feature/23-export-clustering-result",         "Export Excel (.xlsx) dan CSV via export_service. Topbar action di hasil page."),
    (24, "Menambahkan GeoJSON Jawa Barat",          "feature",  "feature/24-add-jabar-geojson",                "GeoJSON 27 kab/kota di app/static/geojson, properti nama_kabkota."),
    (25, "Implementasi Peta Leaflet",               "feature",  "feature/25-leaflet-map",                      "map_routes + peta.html dengan Leaflet + OSM tiles. View Jawa Barat."),
    (26, "Pewarnaan Peta Berdasarkan Cluster",      "feature",  "feature/26-map-cluster-coloring",             "Match wilayah dengan KAB/KOTA alias. Hijau (Tinggi), Kuning (Sedang), Merah (Rendah)."),
    (27, "Popup Detail Wilayah pada Peta",          "feature",  "feature/27-map-popup-detail",                 "Popup tabel: nama, tahun, cluster, kategori, indikator asli + normalisasi."),
    (28, "Black Box Testing Fitur Login",           "test",     None,                                          "Test cases L01-L08: login valid/invalid, akses tanpa login, logout. Lihat docs/testing-plan.md."),
    (29, "Black Box Testing Kelola Data",           "test",     None,                                          "Test cases W01-W05, D01-D04, U01-U06: CRUD wilayah, CRUD data ketimpangan, upload Excel/CSV."),
    (30, "Pengujian Proses Clustering",             "test",     None,                                          "Test cases C01-C09: normalisasi, Elbow, Silhouette, K-Means, label centroid, re-run consistency."),
    (31, "Pengujian Peta Tematik",                  "test",     None,                                          "Test cases M01-M07: peta tampil, polygon, pewarnaan, popup, legend, refresh cluster."),
    (32, "Menulis README Project",                  "docs",     "docs/32-readme-project",                      "README dengan setup instructions, tech stack, struktur folder, akun default, algoritma. Plus docs/PRD.md."),
    (33, "Dokumentasi Workflow GitHub",             "docs",     "docs/33-github-workflow",                     "docs/workflow-github.md: branch types, conventional commits, PR workflow, definition of done, audit trail."),
    (34, "Dokumentasi Implementasi K-Means",        "docs",     "docs/34-kmeans-implementation",               "docs/kmeans-implementation.md untuk Bab IV skripsi. Plus docs/database-design.md dan testing-plan.md."),
    (35, "Refactor Dashboard Full Integration",     "refactor", "refactor/35-dashboard-full-integration",      "Refactor dashboard route + template untuk match mockup penuh: Elbow chart + donut + Leaflet map. Tambah API endpoint /clustering/api/elbow + /clustering/api/distribusi."),
    (36, "Bugfix: Login Redirect Loop",             "bugfix",   "bugfix/36-login-redirect-target",             "Setelah login berhasil, redirect ke /auth/login (loop). Fix: redirect ke dashboard.index. Ditemukan via smoke test."),
]


KIND_LABELS = {
    "feature":  ["enhancement"],
    "docs":     ["documentation"],
    "refactor": ["enhancement"],
    "bugfix":   ["bug"],
    "test":     ["enhancement"],
}


def issue_body(num: int, title: str, kind: str, branch: str | None, summary: str) -> str:
    completed = branch is not None
    parts = [
        "## Deskripsi",
        summary,
        "",
        "## Tujuan",
        f"Menyelesaikan task PRD §7 issue #{num}: {title}.",
        "",
        "## Acceptance Criteria",
    ]
    if kind == "feature":
        parts += [
            "- [x] Implementasi sesuai PRD",
            "- [x] Tidak menimbulkan error pada `python app.py`",
            "- [x] Code mengikuti struktur project",
            "- [x] Manual testing OK",
        ]
    elif kind == "docs":
        parts += [
            "- [x] Dokumen tersedia di `docs/`",
            "- [x] Konten sesuai PRD",
            "- [x] Cukup detail untuk dijadikan referensi Bab IV",
        ]
    elif kind == "refactor":
        parts += [
            "- [x] Tidak mengubah business logic",
            "- [x] UI/UX match mockup dashboard",
            "- [x] Smoke test masih lulus",
        ]
    elif kind == "bugfix":
        parts += [
            "- [x] Bug ter-reproduce dan terverifikasi",
            "- [x] Fix sesuai akar masalah",
            "- [x] Smoke test lulus setelah fix",
        ]
    elif kind == "test":
        parts += [
            "- [ ] Eksekusi semua test case di `docs/testing-plan.md`",
            "- [ ] Bug yang ditemukan dibuat issue baru",
            "- [ ] Hasil test diisi tanggal + status",
        ]

    parts += ["", "## Branch", f"`{branch}`" if branch else "_Tidak ada branch — task pengujian manual._"]

    if completed:
        parts += [
            "",
            "## Status",
            f"✅ Selesai dan ter-merge ke `develop` -> `main` via branch `{branch}`.",
        ]
    else:
        parts += [
            "",
            "## Status",
            "📋 Open — eksekusi pengujian manual sesuai `docs/testing-plan.md`.",
        ]

    return "\n".join(parts)


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        sys.stderr.write(f"FAILED: {' '.join(cmd)}\n{result.stderr}\n")
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def label_exists(name: str) -> bool:
    out = run(["gh", "label", "list", "--repo", REPO, "--json", "name"])
    return f'"{name}"' in out


def ensure_label(name: str, color: str, description: str) -> None:
    if not label_exists(name):
        run(["gh", "label", "create", name, "--repo", REPO,
             "--color", color, "--description", description])


def main() -> None:
    # Default labels usually exist (bug, enhancement, documentation).
    # Add custom ones we use:
    ensure_label("feature",  "0e8a16", "Fitur baru")
    ensure_label("refactor", "fbca04", "Refactor (no behaviour change)")
    ensure_label("test",     "5319e7", "Black box / manual testing")

    print(f"Creating {len(ISSUES)} issues on {REPO}\n")

    for (num, title, kind, branch, summary) in ISSUES:
        body = issue_body(num, title, kind, branch, summary)

        labels = []
        if kind == "feature":  labels = ["enhancement", "feature"]
        elif kind == "docs":   labels = ["documentation"]
        elif kind == "refactor": labels = ["refactor"]
        elif kind == "bugfix": labels = ["bug"]
        elif kind == "test":   labels = ["test"]

        cmd = ["gh", "issue", "create",
               "--repo", REPO,
               "--title", title,
               "--body", body]
        for lbl in labels:
            cmd += ["--label", lbl]

        url = run(cmd)
        print(f"  #{num:2d}  {title:42s}  {url}")

        # Auto-close completed issues
        if branch is not None:
            issue_num = url.rstrip("/").rsplit("/", 1)[-1]
            run(["gh", "issue", "close", issue_num,
                 "--repo", REPO,
                 "--comment", f"Diselesaikan via branch `{branch}` dan ter-merge ke `develop` -> `main` (release v1.0)."])
            print(f"        -> closed (resolved by {branch})")

    print("\nDone.")


if __name__ == "__main__":
    main()
