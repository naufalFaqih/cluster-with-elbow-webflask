"""Dashboard route (PRD #11)."""
from __future__ import annotations

from flask import Blueprint, render_template

from app.db import get_db
from app.routes.decorators import login_required

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
@login_required
def index():
    db = get_db()
    jumlah_wilayah = db.fetchone("SELECT COUNT(*) AS jumlah FROM wilayah")["jumlah"]
    jumlah_data = db.fetchone("SELECT COUNT(*) AS jumlah FROM data_ketimpangan")["jumlah"]
    jumlah_hasil = db.fetchone("SELECT COUNT(*) AS jumlah FROM hasil_clustering")["jumlah"]

    # 5 Variabel = 4 indikator + tahun (sesuai mockup dashboard)
    jumlah_variabel = 5

    return render_template(
        "dashboard/index.html",
        jumlah_wilayah=jumlah_wilayah,
        jumlah_data=jumlah_data,
        jumlah_hasil=jumlah_hasil,
        jumlah_variabel=jumlah_variabel,
        distribusi=[],
    )
