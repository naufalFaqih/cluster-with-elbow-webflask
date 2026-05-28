"""Map (peta tematik) routes — Leaflet + GeoJSON Jawa Barat.

PRD #25 (basic map), #26 (color by cluster), #27 (popup detail).
"""
from __future__ import annotations

from flask import Blueprint, jsonify, render_template

from app.models import hasil_clustering_model
from app.routes.decorators import login_required

bp = Blueprint("map", __name__, url_prefix="/peta")


KATEGORI_COLORS = {
    "Tinggi": "#16a34a",   # green
    "Sedang": "#eab308",   # yellow
    "Rendah": "#dc2626",   # red
}


@bp.route("/")
@login_required
def peta():
    return render_template("map/peta.html", warna=KATEGORI_COLORS)


@bp.route("/api/hasil")
@login_required
def api_hasil():
    """Return hasil clustering ready to be matched with GeoJSON."""
    items = hasil_clustering_model.all_hasil()
    payload = []
    for it in items:
        payload.append(
            {
                "wilayah_id": it["wilayah_id"],
                "nama_wilayah": (it.get("nama_wilayah") or "").upper(),
                "tahun": it.get("tahun"),
                "internet": it.get("internet"),
                "laptop": it.get("laptop"),
                "smartphone": it.get("smartphone"),
                "literasi_digital": it.get("literasi_digital"),
                "internet_norm": it.get("internet_norm"),
                "laptop_norm": it.get("laptop_norm"),
                "smartphone_norm": it.get("smartphone_norm"),
                "literasi_digital_norm": it.get("literasi_digital_norm"),
                "cluster": it.get("cluster"),
                "kategori": it.get("kategori"),
            }
        )
    return jsonify({"items": payload, "warna": KATEGORI_COLORS})
