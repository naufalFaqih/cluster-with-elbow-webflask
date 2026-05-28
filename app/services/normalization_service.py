"""Normalisasi MinMaxScaler (PRD #16)."""
from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

INDIKATOR = ["internet", "laptop", "smartphone", "literasi_digital"]


def normalize(df: pd.DataFrame, indikator: Sequence[str] = INDIKATOR) -> tuple[np.ndarray, MinMaxScaler]:
    """Return matrix ter-normalisasi (0..1) tanpa pembulatan."""
    scaler = MinMaxScaler()
    matrix = scaler.fit_transform(df[list(indikator)].to_numpy(dtype=float))
    return matrix, scaler


def attach_normalized_columns(
    df: pd.DataFrame, matrix: np.ndarray, indikator: Sequence[str] = INDIKATOR
) -> pd.DataFrame:
    """Pasang kolom *_norm pada DataFrame original (untuk display)."""
    out = df.copy()
    for i, col in enumerate(indikator):
        out[f"{col}_norm"] = matrix[:, i]
    return out
