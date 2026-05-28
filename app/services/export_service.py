"""Export hasil clustering ke Excel/CSV (PRD #23)."""
from __future__ import annotations

import io
from typing import Iterable

import pandas as pd


COLUMNS_ORDER = [
    "wilayah_id",
    "nama_wilayah",
    "provinsi",
    "tahun",
    "internet",
    "laptop",
    "smartphone",
    "literasi_digital",
    "internet_norm",
    "laptop_norm",
    "smartphone_norm",
    "literasi_digital_norm",
    "cluster",
    "kategori",
]


def _frame(rows: Iterable[dict]) -> pd.DataFrame:
    df = pd.DataFrame(list(rows))
    if df.empty:
        df = pd.DataFrame(columns=COLUMNS_ORDER)
    available = [c for c in COLUMNS_ORDER if c in df.columns]
    extra = [c for c in df.columns if c not in available]
    return df[available + extra]


def to_excel_bytes(rows: Iterable[dict]) -> bytes:
    df = _frame(rows)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="hasil_clustering")
    buffer.seek(0)
    return buffer.read()


def to_csv_bytes(rows: Iterable[dict]) -> bytes:
    df = _frame(rows)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8-sig")
