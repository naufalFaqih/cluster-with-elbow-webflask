"""Clustering routes — normalisasi, elbow, K-Means proses (PRD #16, #17, #18, #21, #22, #23)."""
from __future__ import annotations

import math
from typing import Any

from flask import (
    Blueprint,
    Response,
    flash,
    jsonify,
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
    export_service,
    kmeans_service,
    normalization_service,
    preprocessing_service,
)

bp = Blueprint("clustering", __name__, url_prefix="/clustering")


def _safe_number(value: Any):
    """Convert NaN/inf -> None for JSON-friendly responses."""
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return f


def _persist_evaluasi(result: evaluation_service.EvaluasiResult) -> None:
    hasil_clustering_model.truncate_evaluasi()
    hasil_clustering_model.insert_evaluasi(
        evaluation_service.merge_for_storage(result)
    )


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
    rekomendasi_elbow: int | None = None
    rekomendasi_silhouette: int | None = None
    rekomendasi_final: int | None = None
    error: str | None = None

    run_now = request.method == "POST" or request.args.get("run") == "1"

    if run_now and rows:
        try:
            df = preprocessing_service.to_feature_matrix(rows)
            matrix, _ = normalization_service.normalize(df)
            result = evaluation_service.run_evaluasi(matrix, k_min=1, k_max=10)
            elbow_data = result.elbow
            silhouette_data = result.silhouette
            rekomendasi_elbow = result.rekomendasi_elbow
            rekomendasi_silhouette = result.rekomendasi_silhouette
            rekomendasi_final = result.rekomendasi_final

            # Persist evaluasi (replace previous)
            _persist_evaluasi(result)

            flash(
                f"Analisis selesai. Rekomendasi k final = {rekomendasi_final}." if rekomendasi_final
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
        rekomendasi_elbow=rekomendasi_elbow,
        rekomendasi_silhouette=rekomendasi_silhouette,
        rekomendasi_final=rekomendasi_final,
        error=error,
    )


@bp.route("/proses", methods=["POST"])
@login_required
def proses():
    """Jalankan K-Means dan SIMPAN hasil ke DB (PRD #21)."""
    raw_n_clusters = (request.form.get("n_clusters") or "").strip().lower()
    use_auto_k = raw_n_clusters in ("", "auto")
    manual_n_clusters: int | None = None
    if not use_auto_k:
        try:
            manual_n_clusters = int(raw_n_clusters)
        except ValueError:
            use_auto_k = True

    rows = data_ketimpangan_model.all_data()
    if not rows:
        flash("Belum ada data ketimpangan untuk diproses.", "warning")
        return redirect(url_for("dashboard.index"))

    try:
        df = preprocessing_service.to_feature_matrix(rows)
        matrix, _ = normalization_service.normalize(df)
        max_clusters = max(1, min(10, len(matrix)))

        if use_auto_k:
            if len(matrix) >= 2:
                evaluasi = evaluation_service.run_evaluasi(matrix, k_min=1, k_max=10)
                _persist_evaluasi(evaluasi)
                n_clusters = evaluasi.rekomendasi_final or min(3, max_clusters)
            else:
                n_clusters = 1
        else:
            n_clusters = manual_n_clusters or 3

        n_clusters = max(1, min(n_clusters, max_clusters))
        result = kmeans_service.run_kmeans(matrix, n_clusters=n_clusters)
        hasil_rows = kmeans_service.build_hasil_rows(df, matrix, result)

        # Replace previous hasil — PRD #21
        hasil_clustering_model.truncate()
        hasil_clustering_model.insert_many(hasil_rows)

        flash(
            f"Clustering K-Means (k={n_clusters}) berhasil"
            f"{' berdasarkan rekomendasi Elbow' if use_auto_k else ''}. "
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


# ---------------------------------------------------------------------------
# JSON endpoints (for dashboard widgets)
# ---------------------------------------------------------------------------
@bp.route("/api/distribusi")
@login_required
def api_distribusi():
    return jsonify({"distribusi": hasil_clustering_model.distribusi()})


@bp.route("/api/elbow")
@login_required
def api_elbow():
    """Compute Elbow + Silhouette on-the-fly for dashboard widget."""
    rows = data_ketimpangan_model.all_data()
    if not rows:
        return jsonify({
            "elbow": [],
            "silhouette": [],
            "rekomendasi": None,
            "rekomendasi_elbow": None,
            "rekomendasi_silhouette": None,
            "rekomendasi_final": None,
        })
    try:
        df = preprocessing_service.to_feature_matrix(rows)
        matrix, _ = normalization_service.normalize(df)
        result = evaluation_service.run_evaluasi(matrix, k_min=1, k_max=7)
        return jsonify(
            {
                "elbow": [
                    {"k": r["k"], "sse": _safe_number(r["sse"])} for r in result.elbow
                ],
                "silhouette": [
                    {"k": r["k"], "score": _safe_number(r["score"])}
                    for r in result.silhouette
                ],
                "rekomendasi": result.rekomendasi_final,
                "rekomendasi_elbow": result.rekomendasi_elbow,
                "rekomendasi_silhouette": result.rekomendasi_silhouette,
                "rekomendasi_final": result.rekomendasi_final,
            }
        )
    except Exception as exc:  # noqa: BLE001
        return jsonify({
            "error": str(exc),
            "elbow": [],
            "silhouette": [],
            "rekomendasi": None,
            "rekomendasi_elbow": None,
            "rekomendasi_silhouette": None,
            "rekomendasi_final": None,
        }), 400


# ---------------------------------------------------------------------------
# Export hasil clustering (PRD #23)
# ---------------------------------------------------------------------------
@bp.route("/export/<fmt>")
@login_required
def export(fmt: str):
    fmt = (fmt or "").lower()
    rows = hasil_clustering_model.all_hasil()
    if not rows:
        flash("Belum ada hasil clustering untuk di-export.", "warning")
        return redirect(url_for("clustering.hasil"))

    if fmt in ("excel", "xlsx"):
        data = export_service.to_excel_bytes(rows)
        return Response(
            data,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=hasil_clustering.xlsx"
            },
        )
    if fmt == "csv":
        data = export_service.to_csv_bytes(rows)
        return Response(
            data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=hasil_clustering.csv"},
        )

    flash("Format export tidak dikenali. Gunakan 'excel' atau 'csv'.", "danger")
    return redirect(url_for("clustering.hasil"))
