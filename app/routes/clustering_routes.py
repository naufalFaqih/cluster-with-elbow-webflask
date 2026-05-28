"""Clustering routes — normalisasi, elbow, K-Means proses (PRD #16, #17, #18, #21)."""
from __future__ import annotations

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.models import (
    data_ketimpangan_model,
    hasil_clustering_model,
)
from app.routes.decorators import login_required
from app.services import (
    evaluation_service,
    kmeans_service,
    normalization_service,
    preprocessing_service,
)

bp = Blueprint("clustering", __name__, url_prefix="/clustering")


@bp.route("/normalisasi")
@login_required
def normalisasi():
    rows = data_ketimpangan_model.all_data()
    preview: list[dict] = []
    if rows:
        try:
            df = preprocessing_service.to_feature_matrix(rows)
            matrix, _ = normalization_service.normalize(df)
            df_norm = normalization_service.attach_normalized_columns(df, matrix)
            preview = df_norm.to_dict(orient="records")
        except preprocessing_service.PreprocessingError as exc:
            flash(str(exc), "warning")
    return render_template("clustering/normalisasi.html", items=preview)


@bp.route("/elbow", methods=["GET", "POST"])
@login_required
def elbow():
    rows = data_ketimpangan_model.all_data()
    elbow_data: list[dict] = []
    silhouette_data: list[dict] = []
    rekomendasi: int | None = None
    error: str | None = None

    run_now = request.method == "POST" or request.args.get("run") == "1"

    if run_now and rows:
        try:
            df = preprocessing_service.to_feature_matrix(rows)
            matrix, _ = normalization_service.normalize(df)
            result = evaluation_service.run_evaluasi(matrix, k_min=1, k_max=10)
            elbow_data = result.elbow
            silhouette_data = result.silhouette
            rekomendasi = result.rekomendasi_silhouette

            # Persist evaluasi (replace previous)
            hasil_clustering_model.truncate_evaluasi()
            hasil_clustering_model.insert_evaluasi(
                evaluation_service.merge_for_storage(result)
            )

            flash(
                f"Analisis selesai. Rekomendasi k = {rekomendasi}." if rekomendasi
                else "Analisis Elbow selesai.",
                "success",
            )
        except preprocessing_service.PreprocessingError as exc:
            error = str(exc)
            flash(error, "danger")
        except Exception as exc:  # noqa: BLE001
            error = f"Gagal menjalankan evaluasi: {exc}"
            flash(error, "danger")

    return render_template(
        "clustering/elbow.html",
        elbow_data=elbow_data,
        silhouette_data=silhouette_data,
        rekomendasi=rekomendasi,
        error=error,
    )


@bp.route("/proses", methods=["POST"])
@login_required
def proses():
    """Jalankan K-Means dan SIMPAN hasil ke DB (PRD #21)."""
    try:
        n_clusters = int(request.form.get("n_clusters", 3))
    except ValueError:
        n_clusters = 3
    n_clusters = max(1, min(n_clusters, 10))

    rows = data_ketimpangan_model.all_data()
    if not rows:
        flash("Belum ada data ketimpangan untuk diproses.", "warning")
        return redirect(url_for("dashboard.index"))

    try:
        df = preprocessing_service.to_feature_matrix(rows)
        matrix, _ = normalization_service.normalize(df)
        result = kmeans_service.run_kmeans(matrix, n_clusters=n_clusters)
        hasil_rows = kmeans_service.build_hasil_rows(df, matrix, result)

        # Replace previous hasil — PRD #21
        hasil_clustering_model.truncate()
        hasil_clustering_model.insert_many(hasil_rows)

        flash(
            f"Clustering K-Means (k={n_clusters}) berhasil. "
            "Label kategori dipetakan dari centroid (Tinggi/Sedang/Rendah).",
            "success",
        )
    except preprocessing_service.PreprocessingError as exc:
        flash(str(exc), "danger")
    except Exception as exc:  # noqa: BLE001
        flash(f"Gagal menjalankan clustering: {exc}", "danger")

    next_url = request.form.get("next") or url_for("dashboard.index")
    return redirect(next_url)


@bp.route("/hasil")
@login_required
def hasil():
    items = hasil_clustering_model.all_hasil()
    distribusi = hasil_clustering_model.distribusi()
    return render_template(
        "clustering/hasil.html",
        items=items,
        distribusi=distribusi,
    )
