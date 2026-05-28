"""Dashboard route (PRD #11 + integration with #17, #21, #25-27)."""
from __future__ import annotations

from flask import Blueprint, render_template

from app.models import (
    data_ketimpangan_model,
    hasil_clustering_model,
    wilayah_model,
)
from app.routes.decorators import login_required

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
@login_required
def index():
    jumlah_wilayah = wilayah_model.count()
    jumlah_data = data_ketimpangan_model.count()
    jumlah_hasil = hasil_clustering_model.count()
    distribusi = hasil_clustering_model.distribusi()

    # 5 Variabel = 4 indikator + tahun (sesuai mockup dashboard)
    jumlah_variabel = 5

    return render_template(
        "dashboard/index.html",
        jumlah_wilayah=jumlah_wilayah,
        jumlah_data=jumlah_data,
        jumlah_hasil=jumlah_hasil,
        jumlah_variabel=jumlah_variabel,
        distribusi=distribusi,
    )
