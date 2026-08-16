"""Hasil clustering & evaluasi clustering models."""
from __future__ import annotations

from typing import Iterable, Optional

from app.db import get_db


_HASIL_SELECT = """
SELECT  h.id,
        h.data_ketimpangan_id,
        h.cluster,
        h.kategori,
        h.internet_norm,
        h.laptop_norm,
        h.smartphone_norm,
        h.literasi_digital_norm,
        d.tahun,
        d.internet,
        d.laptop,
        d.smartphone,
        d.literasi_digital,
        w.id          AS wilayah_id,
        w.nama_wilayah,
        w.provinsi
FROM    hasil_clustering h
JOIN    data_ketimpangan d ON d.id = h.data_ketimpangan_id
JOIN    wilayah w ON w.id = d.wilayah_id
"""


def all_hasil(tahun: Optional[int] = None) -> list[dict]:
    if tahun is None:
        return get_db().fetchall(_HASIL_SELECT + " ORDER BY w.id")
    return get_db().fetchall(
        _HASIL_SELECT + " WHERE d.tahun = %s ORDER BY w.id", (tahun,)
    )


def truncate(tahun: Optional[int] = None) -> None:
    """Hapus hasil clustering lama (PRD #21 — replace strategy)."""
    db = get_db()
    if tahun is None:
        db.execute("DELETE FROM hasil_clustering")
    else:
        db.execute(
            """
            DELETE FROM hasil_clustering
            WHERE data_ketimpangan_id IN (
                SELECT id FROM data_ketimpangan WHERE tahun = %s
            )
            """,
            (tahun,),
        )


def insert_many(rows: Iterable[dict]) -> None:
    """Bulk insert hasil clustering."""
    payload = []
    for row in rows:
        payload.append(
            (
                row["data_ketimpangan_id"],
                row["cluster"],
                row["kategori"],
                row.get("internet_norm"),
                row.get("laptop_norm"),
                row.get("smartphone_norm"),
                row.get("literasi_digital_norm"),
            )
        )
    if not payload:
        return
    get_db().executemany(
        """
        INSERT INTO hasil_clustering
            (data_ketimpangan_id, cluster, kategori,
             internet_norm, laptop_norm, smartphone_norm, literasi_digital_norm)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        payload,
    )


def count() -> int:
    row = get_db().fetchone("SELECT COUNT(*) AS jumlah FROM hasil_clustering")
    return int(row["jumlah"]) if row else 0


def distribusi() -> list[dict]:
    """Jumlah anggota per kategori ketimpangan (Rendah/Tinggi)."""
    return get_db().fetchall(
        """
        SELECT cluster, kategori, COUNT(*) AS jumlah
        FROM hasil_clustering
        GROUP BY cluster, kategori
        ORDER BY cluster
        """
    )


# ---------------------------------------------------------------------------
# Cluster statistics for map visualisation (PRD #39)
# ---------------------------------------------------------------------------
KATEGORI_ORDER = {"Rendah": 0, "Tinggi": 1}
KATEGORI_DESC = {
    "Tinggi": "Akses digital tinggi — ketimpangan rendah",
    "Sedang": "Akses digital menengah — ketimpangan sedang",
    "Rendah": "Akses digital rendah — ketimpangan tinggi",
}
KATEGORI_DESC = {
    "Rendah": "Ketimpangan digital rendah",
    "Tinggi": "Ketimpangan digital tinggi",
}


def cluster_stats() -> list[dict]:
    """Aggregate per-kategori untuk panel statistik & tabel ringkasan.

    Output per baris:
      cluster_no       — nomor display 1..n urut Tinggi → Sedang → Rendah
      cluster_id       — id cluster mentah dari sklearn
      kategori         — Tinggi / Sedang / Rendah
      jumlah           — jumlah wilayah dalam cluster
      persentase       — % dari total
      rata_skor        — rata-rata "skor ketimpangan" wilayah dalam cluster
                         (skor = 1 - rata-rata 4 indikator; 0 = tanpa ketimpangan)
      keterangan       — deskripsi human-readable
    """
    rows = get_db().fetchall(
        """
        SELECT  h.cluster,
                h.kategori,
                d.internet,
                d.laptop,
                d.smartphone,
                d.literasi_digital
        FROM    hasil_clustering h
        JOIN    data_ketimpangan d ON d.id = h.data_ketimpangan_id
        """
    )
    if not rows:
        return []

    total = len(rows)
    grouped: dict[tuple[int, str], list[float]] = {}
    for r in rows:
        skor = 1.0 - (
            float(r["internet"])
            + float(r["laptop"])
            + float(r["smartphone"])
            + float(r["literasi_digital"])
        ) / 4.0
        key = (int(r["cluster"]), r["kategori"])
        grouped.setdefault(key, []).append(skor)

    result = []
    for (cluster_id, kategori), skors in grouped.items():
        result.append(
            {
                "cluster_id": cluster_id,
                "kategori": kategori,
                "jumlah": len(skors),
                "persentase": round(len(skors) / total * 100, 2),
                "rata_skor": round(sum(skors) / len(skors), 4),
                "keterangan": KATEGORI_DESC.get(kategori, ""),
            }
        )

    # Sort: Rendah → Tinggi, then by cluster_id
    result.sort(key=lambda s: (KATEGORI_ORDER.get(s["kategori"], 99), s["cluster_id"]))
    for i, item in enumerate(result, 0):
        item["cluster_no"] = KATEGORI_ORDER.get(item["kategori"], i)

    return result


def total_count() -> int:
    """Total wilayah yang sudah ter-cluster (alias of count())."""
    return count()


# ---------------------------------------------------------------------------
# Evaluasi (Elbow + Silhouette)
# ---------------------------------------------------------------------------
def truncate_evaluasi() -> None:
    get_db().execute("DELETE FROM evaluasi_clustering")


def insert_evaluasi(rows: Iterable[dict]) -> None:
    payload = [
        (r["jumlah_cluster"], r.get("sse"), r.get("silhouette_score"))
        for r in rows
    ]
    if not payload:
        return
    get_db().executemany(
        """
        INSERT INTO evaluasi_clustering (jumlah_cluster, sse, silhouette_score)
        VALUES (%s, %s, %s)
        """,
        payload,
    )


def all_evaluasi() -> list[dict]:
    return get_db().fetchall(
        """
        SELECT id, jumlah_cluster, sse, silhouette_score, created_at
        FROM evaluasi_clustering
        ORDER BY jumlah_cluster
        """
    )
