"""Evaluation service — Elbow Method (PRD #17).

Catatan: Silhouette Score ditambahkan pada issue #18.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.cluster import KMeans


@dataclass
class EvaluasiResult:
    elbow: list[dict]      # [{k, sse}]
    silhouette: list[dict] = None  # diisi pada issue #18
    rekomendasi_silhouette: int | None = None


def run_evaluasi(
    matrix: np.ndarray,
    k_min: int = 1,
    k_max: int = 10,
    random_state: int = 42,
    n_init: int = 10,
) -> EvaluasiResult:
    """Hitung SSE/Inertia untuk k = k_min..k_max."""
    n_samples = len(matrix)
    if n_samples < 2:
        raise ValueError("Minimal butuh 2 data untuk evaluasi clustering.")

    k_max = min(k_max, max(2, n_samples - 1))

    elbow: list[dict] = []
    for k in range(k_min, k_max + 1):
        model = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
        model.fit(matrix)
        elbow.append({"k": k, "sse": float(model.inertia_)})

    return EvaluasiResult(elbow=elbow, silhouette=[], rekomendasi_silhouette=None)


def merge_for_storage(result: EvaluasiResult) -> list[dict]:
    """Gabungkan ke baris siap insert ke evaluasi_clustering."""
    sse_by_k = {r["k"]: r["sse"] for r in result.elbow}
    sil_by_k = {r["k"]: r["score"] for r in (result.silhouette or [])}
    all_k = sorted(set(sse_by_k) | set(sil_by_k))
    return [
        {
            "jumlah_cluster": k,
            "sse": sse_by_k.get(k),
            "silhouette_score": sil_by_k.get(k),
        }
        for k in all_k
    ]
