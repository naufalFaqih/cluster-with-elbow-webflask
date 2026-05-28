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
    """Jumlah anggota per kategori (Tinggi/Sedang/Rendah)."""
    return get_db().fetchall(
        """
        SELECT cluster, kategori, COUNT(*) AS jumlah
        FROM hasil_clustering
        GROUP BY cluster, kategori
        ORDER BY cluster
        """
    )


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
