"""Wilayah (kabupaten/kota) model."""
from __future__ import annotations

from typing import Optional

from app.db import get_db


def all_wilayah() -> list[dict]:
    return get_db().fetchall(
        "SELECT id, nama_wilayah, provinsi FROM wilayah ORDER BY id"
    )


def find_by_id(wilayah_id: int) -> Optional[dict]:
    return get_db().fetchone(
        "SELECT id, nama_wilayah, provinsi FROM wilayah WHERE id = %s",
        (wilayah_id,),
    )


def find_by_nama(nama: str) -> Optional[dict]:
    return get_db().fetchone(
        "SELECT id, nama_wilayah, provinsi FROM wilayah WHERE UPPER(nama_wilayah) = UPPER(%s)",
        (nama,),
    )


def create(nama_wilayah: str, provinsi: str = "Jawa Barat") -> int:
    nama = (nama_wilayah or "").strip()
    if not nama:
        raise ValueError("nama_wilayah wajib diisi")
    return get_db().execute(
        "INSERT INTO wilayah (nama_wilayah, provinsi) VALUES (%s, %s)",
        (nama, provinsi or "Jawa Barat"),
    )


def update(wilayah_id: int, nama_wilayah: str, provinsi: str = "Jawa Barat") -> None:
    nama = (nama_wilayah or "").strip()
    if not nama:
        raise ValueError("nama_wilayah wajib diisi")
    get_db().execute(
        "UPDATE wilayah SET nama_wilayah = %s, provinsi = %s WHERE id = %s",
        (nama, provinsi or "Jawa Barat", wilayah_id),
    )


def delete(wilayah_id: int) -> None:
    get_db().execute("DELETE FROM wilayah WHERE id = %s", (wilayah_id,))


def count() -> int:
    row = get_db().fetchone("SELECT COUNT(*) AS jumlah FROM wilayah")
    return int(row["jumlah"]) if row else 0
