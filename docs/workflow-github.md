# GitHub Workflow

Dokumen ini menjelaskan aturan kerja Git/GitHub yang **wajib** diikuti untuk
project ini. Sumber acuan: PRD §6.

## 1. Branch Utama

| Branch       | Peran                                            |
|--------------|--------------------------------------------------|
| `main`       | Production / stabil                              |
| `develop`    | Integrasi development                            |
| `feature/*`  | Fitur baru                                       |
| `bugfix/*`   | Perbaikan bug                                    |
| `hotfix/*`   | Perbaikan cepat dari `main`                      |
| `docs/*`     | Dokumentasi                                      |
| `refactor/*` | Refactor kode tanpa mengubah fitur               |
| `test/*`     | Pengujian                                        |

## 2. Aturan Branch

- **Wajib** mulai dari issue terlebih dahulu.
- **Setiap issue → satu branch**.
- Branch dibuat dari `develop`, **bukan** dari `main`.
- Format penamaan: `<tipe>/<nomor-issue>-<nama-fitur>`.

```
feature/1-setup-repository
feature/2-setup-flask-project
feature/14-upload-dataset
docs/32-readme-project
test/28-blackbox-login
```

## 3. Format Commit (Conventional Commits)

| Prefix      | Untuk                                            |
|-------------|--------------------------------------------------|
| `feat:`     | Fitur baru                                       |
| `fix:`      | Perbaikan bug                                    |
| `docs:`     | Dokumentasi                                      |
| `style:`    | Formatting (tidak ubah logic)                    |
| `refactor:` | Refactor (tidak ubah fitur)                      |
| `test:`     | Tambah / perbaiki test                           |
| `chore:`    | Konfigurasi / dependency / setup                 |

Pesan commit harus singkat dan diakhiri dengan referensi issue:

```
feat: implement login (#7)

- add user_model with pbkdf2 password hashing
- add /auth/login route + login.html template

Closes #7
```

## 4. Pull Request Workflow

```
1. Create issue
2. Create branch FROM develop
3. Implement feature/fix
4. Commit changes (conventional commits)
5. Push branch
6. Open Pull Request → develop
7. Review checklist
8. Merge to develop (--no-ff agar history terlihat)
```

Setelah seluruh fitur stabil, baru `develop` di-merge ke `main`.

## 5. Aturan untuk Eksekusi (AI Agent / Developer)

1. Jangan mengerjakan banyak fitur dalam satu branch.
2. Setiap fitur harus dimulai dari issue.
3. Setiap branch harus dibuat dari `develop`.
4. Setelah selesai, buat Pull Request ke `develop`.
5. **Jangan langsung commit ke `main`**.
6. Jangan menyimpan `.env`, dataset rahasia, cache, atau virtualenv ke repo
   (sudah dikonfigurasi di `.gitignore`).
7. Jangan mengubah struktur project tanpa alasan jelas.
8. Bug → buat issue baru, jangan campur perbaikan dengan fitur lain.
9. Ada perubahan logic K-Means → update `docs/kmeans-implementation` (#34).
10. Ada perubahan database → update `database/schema.sql` & `database/seed.sql`.

## 6. Template Issue

```markdown
## Deskripsi
Jelaskan fitur/bug/dokumentasi yang akan dikerjakan.

## Tujuan
Jelaskan tujuan pengerjaan issue ini.

## Task
- [ ] Task 1
- [ ] Task 2

## Acceptance Criteria
- [ ] Kriteria selesai 1
- [ ] Kriteria selesai 2

## Catatan
Tambahkan catatan teknis jika diperlukan.
```

## 7. Template Pull Request

```markdown
## Ringkasan
Jelaskan perubahan yang dibuat.

## Related Issue
Closes #N

## Perubahan
- Perubahan 1
- Perubahan 2

## Cara Pengujian
1. Jalankan aplikasi.
2. Buka halaman terkait.
3. Cek hasil sesuai acceptance criteria.

## Checklist
- [ ] Kode berjalan tanpa error.
- [ ] Tidak ada file rahasia yang ikut ter-commit.
- [ ] Sudah mengikuti struktur project.
- [ ] Sudah diuji secara manual.
- [ ] Dokumentasi diperbarui jika diperlukan.
```

## 8. Definition of Done

- Kode diimplementasikan & berjalan tanpa error.
- Acceptance criteria terpenuhi.
- Sudah diuji manual.
- Tidak ada file rahasia ter-commit.
- Dokumentasi diperbarui jika diperlukan.
- PR dibuat & di-merge ke `develop`.

## 9. Riwayat Branch Project (per issue)

Branch yang sudah di-merge ke `develop`:

| Issue | Branch                                        | Tipe       |
|-------|-----------------------------------------------|------------|
| #1    | `feature/1-setup-repository`                  | feature    |
| #2    | `feature/2-setup-flask-project`               | feature    |
| #3    | `feature/3-setup-environment-config`          | feature    |
| #4    | `feature/4-create-database-schema`            | feature    |
| #5    | `feature/5-create-database-seeder`            | feature    |
| #6    | `feature/6-database-connection`               | feature    |
| #7    | `feature/7-login`                             | feature    |
| #8    | `feature/8-logout`                            | feature    |
| #9    | `feature/9-role-based-access`                 | feature    |
| #10   | `feature/10-main-layout`                      | feature    |
| #11   | `feature/11-dashboard`                        | feature    |
| #12   | `feature/12-crud-wilayah`                     | feature    |
| #13   | `feature/13-crud-data-ketimpangan`            | feature    |
| #14   | `feature/14-upload-dataset`                   | feature    |
| #15   | `feature/15-preprocessing-data`               | feature    |
| #16   | `feature/16-minmax-normalization`             | feature    |
| #17   | `feature/17-elbow-method`                     | feature    |
| #18   | `feature/18-silhouette-score`                 | feature    |
| #19   | `feature/19-kmeans-service`                   | feature    |
| #20   | `feature/20-cluster-labeling-centroid`        | feature    |
| #21   | `feature/21-save-clustering-result`           | feature    |
| #22   | `feature/22-clustering-result-page`           | feature    |
| #23   | `feature/23-export-clustering-result`         | feature    |
| #24   | `feature/24-add-jabar-geojson`                | feature    |
| #25   | `feature/25-leaflet-map`                      | feature    |
| #26   | `feature/26-map-cluster-coloring`             | feature    |
| #27   | `feature/27-map-popup-detail`                 | feature    |
| #35   | `refactor/35-dashboard-full-integration`      | refactor   |
| #32   | `docs/32-readme-project`                      | docs       |
| #33   | `docs/33-github-workflow`                     | docs       |
| #34   | `docs/34-kmeans-implementation`               | docs       |

Cek riwayat dengan:

```bash
git log --oneline --graph --all
```
