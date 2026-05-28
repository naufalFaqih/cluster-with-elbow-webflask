"""Clustering routes — normalisasi preview (PRD #16)."""
from __future__ import annotations

from flask import Blueprint, flash, render_template

from app.models import data_ketimpangan_model
from app.routes.decorators import login_required
from app.services import normalization_service, preprocessing_service

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
