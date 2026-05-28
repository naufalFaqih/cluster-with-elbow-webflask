"""Preprocessing service (PRD #15).

Tugas:
* Load data dari DB / DataFrame upload.
* Cek missing value.
* Pastikan tipe data numerik.
* Tolak data yang tidak lengkap.
* Rapikan nama kolom.
"""
from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS = ["wilayah", "tahun", "internet", "laptop", "smartphone", "literasi_digital"]
INDIKATOR = ["internet", "laptop", "smartphone", "literasi_digital"]


class PreprocessingError(ValueError):
    """Diraise saat data tidak valid."""


def normalize_column_name(name: str) -> str:
    """Sanitise column name to snake_case."""
    s = (name or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    aliases = {
        "lokasi_kabupaten_kota": "wilayah",
        "kabupaten_kota": "wilayah",
        "nama_wilayah": "wilayah",
        "literasi": "literasi_digital",
        "literasi_digital": "literasi_digital",
        "komputer": "laptop",
        "komputer_laptop": "laptop",
        "hp": "smartphone",
        "handphone": "smartphone",
    }
    return aliases.get(s, s)


def clean_uploaded_dataframe(df: pd.DataFrame, default_tahun: int = 2023) -> pd.DataFrame:
    """Bersihkan DataFrame dari upload Excel/CSV."""
    if df is None or df.empty:
        raise PreprocessingError("Dataset kosong.")

    # Drop full-empty rows
    df = df.dropna(how="all").copy()

    # Rename columns
    df.columns = [normalize_column_name(c) for c in df.columns]

    # Drop helper / unnamed columns
    df = df.loc[:, [c for c in df.columns if c and not c.startswith("unnamed")]]

    # Tahun default kalau kolom tidak ada
    if "tahun" not in df.columns:
        df["tahun"] = default_tahun

    # Cek kolom wajib
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise PreprocessingError(
            f"Kolom wajib tidak lengkap. Tambahkan: {', '.join(missing)}"
        )

    # Bersihkan provinsi kalau ada
    if "provinsi" in df.columns:
        df["provinsi"] = df["provinsi"].astype(str).str.strip()

    df["wilayah"] = df["wilayah"].astype(str).str.strip().str.upper()

    # Konversi numerik
    for col in INDIKATOR:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce").astype("Int64")

    # Validasi missing value pada indikator (PRD #15)
    invalid = df[df[INDIKATOR + ["wilayah", "tahun"]].isnull().any(axis=1)]
    if not invalid.empty:
        rows = ", ".join(invalid["wilayah"].fillna("(unknown)").astype(str).tolist())
        raise PreprocessingError(
            f"Terdapat {len(invalid)} baris dengan nilai kosong pada: {rows}. "
            "Lengkapi atau hapus baris tersebut sebelum upload."
        )

    # Cek wilayah duplikat untuk tahun yang sama
    dup = df.groupby(["wilayah", "tahun"]).size()
    dup = dup[dup > 1]
    if not dup.empty:
        raise PreprocessingError(
            f"Terdapat data duplikat untuk wilayah/tahun: {list(dup.index)}"
        )

    return df.reset_index(drop=True)


def to_feature_matrix(rows: Iterable[dict], indikator: list[str] = INDIKATOR) -> pd.DataFrame:
    """Konversi list-of-dict → DataFrame yang siap untuk K-Means."""
    df = pd.DataFrame(list(rows))
    if df.empty:
        raise PreprocessingError("Tidak ada data untuk diproses.")
    missing = [c for c in indikator if c not in df.columns]
    if missing:
        raise PreprocessingError(f"Kolom indikator hilang: {', '.join(missing)}")
    for col in indikator:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if df[indikator].isnull().any().any():
        raise PreprocessingError("Terdapat missing value pada kolom indikator.")
    return df
