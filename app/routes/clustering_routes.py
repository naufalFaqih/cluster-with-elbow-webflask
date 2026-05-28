"""Clustering routes — normalisasi (PRD #16), elbow (PRD #17)."""
from __future__ import annotations

from flask import (
    Blueprint,
    flash,
    render_template,
    request,
)

from app.models import data_ketimpangan_model
from app.routes.decorators import login_required
from app.services import (
    evaluation_service,
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
    error: str | None = None

    run_now = request.method == "POST" or request.args.get("run") == "1"

    if run_now and rows:
        try:
            df = preprocessing_service.to_feature_matrix(rows)
            matrix, _ = normalization_service.normalize(df)
            result = evaluation_service.run_evaluasi(matrix, k_min=1, k_max=10)
            elbow_data = result.elbow
            flash("Analisis Elbow Method berhasil dijalankan.", "success")
        except preprocessing_service.PreprocessingError as exc:
            error = str(exc)
            flash(error, "danger")
        except Exception as exc:  # noqa: BLE001
            error = f"Gagal menjalankan evaluasi: {exc}"
            flash(error, "danger")

    return render_template(
        "clustering/elbow.html",
        elbow_data=elbow_data,
        error=error,
    )
