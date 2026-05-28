"""Data ketimpangan digital model (4 indikator + tahun + wilayah)."""
from __future__ import annotations

from typing import Optional

from app.db import get_db


_BASE_SELECT = """
SELECT  d.id,
        d.wilayah_id,
        w.nama_wilayah,
        w.provinsi,
        d.tahun,
        d.internet,
        d.laptop,
        d.smartphone,
        d.literasi_digital
FROM    data_ketimpangan d
JOIN    wilayah w ON w.id = d.wilayah_id
"""


def all_data(tahun: Optional[int] = None) -> list[dict]:
    if tahun is None:
        return get_db().fetchall(_BASE_SELECT + " ORDER BY w.id")
    return get_db().fetchall(
        _BASE_SELECT + " WHERE d.tahun = %s ORDER BY w.id", (tahun,)
    )


def find_by_id(data_id: int) -> Optional[dict]:
    return get_db().fetchone(_BASE_SELECT + " WHERE d.id = %s", (data_id,))


def find_by_wilayah_tahun(wilayah_id: int, tahun: int) -> Optional[dict]:
    return get_db().fetchone(
        _BASE_SELECT + " WHERE d.wilayah_id = %s AND d.tahun = %s",
        (wilayah_id, tahun),
    )


def _validate(internet: float, laptop: float, smartphone: float, literasi: float) -> None:
    for label, value in (
        ("internet", internet),
        ("laptop", laptop),
        ("smartphone", smartphone),
        ("literasi_digital", literasi),
    ):
        if value is None:
            raise ValueError(f"{label} wajib diisi")
        try:
            float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{label} harus angka") from exc


def create(
    wilayah_id: int,
    tahun: int,
    internet: float,
    laptop: float,
    smartphone: float,
    literasi_digital: float,
) -> int:
    _validate(internet, laptop, smartphone, literasi_digital)
    return get_db().execute(
        """
        INSERT INTO data_ketimpangan
            (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (wilayah_id, tahun, float(internet), float(laptop), float(smartphone), float(literasi_digital)),
    )


def update(
    data_id: int,
    wilayah_id: int,
    tahun: int,
    internet: float,
    laptop: float,
    smartphone: float,
    literasi_digital: float,
) -> None:
    _validate(internet, laptop, smartphone, literasi_digital)
    get_db().execute(
        """
        UPDATE data_ketimpangan
        SET wilayah_id = %s,
            tahun = %s,
            internet = %s,
            laptop = %s,
            smartphone = %s,
            literasi_digital = %s
        WHERE id = %s
        """,
        (wilayah_id, tahun, float(internet), float(laptop), float(smartphone), float(literasi_digital), data_id),
    )


def upsert_by_wilayah(
    wilayah_id: int,
    tahun: int,
    internet: float,
    laptop: float,
    smartphone: float,
    literasi_digital: float,
) -> int:
    """Insert atau update berdasarkan (wilayah_id, tahun)."""
    existing = find_by_wilayah_tahun(wilayah_id, tahun)
    if existing:
        update(
            existing["id"],
            wilayah_id,
            tahun,
            internet,
            laptop,
            smartphone,
            literasi_digital,
        )
        return existing["id"]
    return create(wilayah_id, tahun, internet, laptop, smartphone, literasi_digital)


def delete(data_id: int) -> None:
    get_db().execute("DELETE FROM data_ketimpangan WHERE id = %s", (data_id,))


def count(tahun: Optional[int] = None) -> int:
    if tahun is None:
        row = get_db().fetchone("SELECT COUNT(*) AS jumlah FROM data_ketimpangan")
    else:
        row = get_db().fetchone(
            "SELECT COUNT(*) AS jumlah FROM data_ketimpangan WHERE tahun = %s", (tahun,)
        )
    return int(row["jumlah"]) if row else 0
