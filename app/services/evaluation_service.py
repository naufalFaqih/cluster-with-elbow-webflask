"""Evaluation service — Elbow Method + Silhouette Score (PRD #17, #18)."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


@dataclass
class EvaluasiResult:
    elbow: list[dict] = field(default_factory=list)
    silhouette: list[dict] = field(default_factory=list)
    rekomendasi_elbow: int | None = None
    rekomendasi_silhouette: int | None = None
    rekomendasi_final: int | None = None


def _clamp_k(k: int, k_min: int, k_max: int) -> int:
    return max(k_min, min(int(k), k_max))


def _recommend_elbow(elbow: list[dict]) -> int | None:
    """Pilih k tujuan dari penurunan SSE absolut terbesar."""
    if len(elbow) < 2:
        return None

    sse_values = np.array([float(row["sse"]) for row in elbow], dtype=float)
    drops = sse_values[:-1] - sse_values[1:]
    if len(drops) == 0 or float(drops.max()) <= 0:
        return None

    best_drop_idx = int(np.argmax(drops))
    return int(elbow[best_drop_idx + 1]["k"])


def run_evaluasi(
    matrix: np.ndarray,
    k_min: int = 1,
    k_max: int = 10,
    random_state: int = 42,
    n_init: int = 10,
) -> EvaluasiResult:
    """Hitung SSE (k=1..k_max) dan Silhouette (k=2..k_max).

    Note: Silhouette tidak terdefinisi untuk k=1.
    """
    n_samples = len(matrix)
    if n_samples < 2:
        raise ValueError("Minimal butuh 2 data untuk evaluasi clustering.")

    k_max = min(k_max, max(2, n_samples - 1))

    elbow: list[dict] = []
    silhouette: list[dict] = []

    for k in range(k_min, k_max + 1):
        model = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
        labels = model.fit_predict(matrix)
        elbow.append({"k": k, "sse": float(model.inertia_)})

        if k >= 2 and k < n_samples and len(set(labels)) > 1:
            score = float(silhouette_score(matrix, labels))
            silhouette.append({"k": k, "score": score})

    rekomendasi_elbow = _recommend_elbow(elbow)
    rekomendasi_silhouette = None
    if silhouette:
        best = max(silhouette, key=lambda r: r["score"])
        rekomendasi_silhouette = best["k"]

    fallback_k = _clamp_k(3, k_min, k_max)
    rekomendasi_final = (
        rekomendasi_elbow
        or rekomendasi_silhouette
        or fallback_k
    )

    return EvaluasiResult(
        elbow=elbow,
        silhouette=silhouette,
        rekomendasi_elbow=rekomendasi_elbow,
        rekomendasi_silhouette=rekomendasi_silhouette,
        rekomendasi_final=rekomendasi_final,
    )


def merge_for_storage(result: EvaluasiResult) -> list[dict]:
    """Gabungkan elbow + silhouette ke baris-baris evaluasi_clustering."""
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
