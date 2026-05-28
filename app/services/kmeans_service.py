"""K-Means clustering service (PRD #19).

* random_state=42, n_init=10
* Pelabelan kategori (Tinggi/Sedang/Rendah) ditambahkan di issue #20.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.cluster import KMeans


@dataclass
class ClusteringResult:
    n_clusters: int
    labels: np.ndarray            # cluster id per data
    centroids: np.ndarray         # centroid (n_clusters, n_features)
    inertia: float


def run_kmeans(
    matrix: np.ndarray,
    n_clusters: int = 3,
    random_state: int = 42,
    n_init: int = 10,
) -> ClusteringResult:
    """Jalankan K-Means dan kembalikan label + centroid mentah."""
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

    return ClusteringResult(
        n_clusters=n_clusters,
        labels=labels,
        centroids=model.cluster_centers_,
        inertia=float(model.inertia_),
    )
