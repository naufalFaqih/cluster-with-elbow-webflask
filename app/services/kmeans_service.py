"""K-Means clustering service (PRD #19, #20).

* random_state=42, n_init=10
* Pelabelan kategori (Tinggi/Sedang/Rendah) berdasarkan rata-rata centroid.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

KATEGORI_LABELS_3 = ["Tinggi", "Sedang", "Rendah"]


@dataclass
class ClusteringResult:
    n_clusters: int
    labels: np.ndarray            # cluster id per data
    centroids: np.ndarray         # centroid (n_clusters, n_features)
    inertia: float
    cluster_kategori: dict[int, str]  # mapping cluster_id → "Tinggi"/"Sedang"/"Rendah"
    kategori_per_row: list[str]   # kategori per data (panjang sama dengan labels)


def run_kmeans(
    matrix: np.ndarray,
    n_clusters: int = 3,
    random_state: int = 42,
    n_init: int = 10,
) -> ClusteringResult:
    """Jalankan K-Means + label kategori berdasarkan centroid (PRD #20)."""
    if matrix is None or len(matrix) == 0:
        raise ValueError("Matrix kosong, tidak dapat clustering.")
    if n_clusters < 1:
        raise ValueError("n_clusters minimal 1.")

    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=n_init,
    )
    labels = model.fit_predict(matrix)
    centroids = model.cluster_centers_

    cluster_kategori = label_clusters_by_centroid(centroids, n_clusters)
    kategori_per_row = [cluster_kategori[int(c)] for c in labels]

    return ClusteringResult(
        n_clusters=n_clusters,
        labels=labels,
        centroids=centroids,
        inertia=float(model.inertia_),
        cluster_kategori=cluster_kategori,
        kategori_per_row=kategori_per_row,
    )


def label_clusters_by_centroid(
    centroids: np.ndarray,
    n_clusters: int,
    label_pool: Sequence[str] = KATEGORI_LABELS_3,
) -> dict[int, str]:
    """Pelabelan cluster berdasarkan rata-rata centroid (PRD #20).

    * Hitung rata-rata centroid per cluster (1 nilai skalar per cluster).
    * Urutkan dari tertinggi → terendah.
    * Mapping ke ``Tinggi``, ``Sedang``, ``Rendah``.
    * Jika jumlah cluster > 3, urutan centroid dibagi ke tiga kategori
      agar peta, statistik, dan export tetap memakai label yang sama.

    Konsisten meskipun nomor cluster scikit-learn berubah.
    """
    means = centroids.mean(axis=1)
    order = np.argsort(-means)  # descending

    if n_clusters == len(label_pool):
        return {int(order[i]): label_pool[i] for i in range(n_clusters)}

    mapping: dict[int, str] = {}
    if n_clusters == 1:
        mapping[int(order[0])] = "Tinggi"
    elif n_clusters == 2:
        mapping[int(order[0])] = "Tinggi"
        mapping[int(order[1])] = "Rendah"
    else:
        groups = np.array_split(order, len(label_pool))
        for label, group in zip(label_pool, groups):
            for idx in group:
                mapping[int(idx)] = label
    return mapping


def build_hasil_rows(
    df: pd.DataFrame,
    matrix_norm: np.ndarray,
    result: ClusteringResult,
    indikator: Sequence[str] = ("internet", "laptop", "smartphone", "literasi_digital"),
) -> list[dict]:
    """Susun list-of-dict siap insert ke tabel hasil_clustering."""
    rows: list[dict] = []
    indikator = list(indikator)
    for i, row in df.reset_index(drop=True).iterrows():
        rows.append(
            {
                "data_ketimpangan_id": int(row["id"]),
                "cluster": int(result.labels[i]),
                "kategori": result.kategori_per_row[i],
                "internet_norm": float(matrix_norm[i][indikator.index("internet")]),
                "laptop_norm": float(matrix_norm[i][indikator.index("laptop")]),
                "smartphone_norm": float(matrix_norm[i][indikator.index("smartphone")]),
                "literasi_digital_norm": float(matrix_norm[i][indikator.index("literasi_digital")]),
            }
        )
    return rows
