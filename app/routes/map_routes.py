"""Map (peta tematik) routes — Leaflet + GeoJSON Jawa Barat.

PRD #25 (basic map), #26 (color by cluster), #27 (popup detail), #39 (stats).
"""
from __future__ import annotations

from flask import Blueprint, current_app, jsonify, render_template

from app.models import hasil_clustering_model
from app.routes.decorators import login_required

bp = Blueprint("map", __name__, url_prefix="/peta")


KATEGORI_COLORS = {
    "Tinggi": "#16a34a",   # green — akses tinggi, ketimpangan rendah
    "Sedang": "#eab308",   # yellow
    "Rendah": "#dc2626",   # red — akses rendah, ketimpangan tinggi
}
KATEGORI_COLORS = {
    "Rendah": "#16a34a",   # green - ketimpangan rendah
    "Tinggi": "#dc2626",   # red - ketimpangan tinggi
}


def _skor_ketimpangan(item: dict) -> float | None:
    """Skor 0..1 — semakin tinggi, semakin tinggi ketimpangan digital."""
    fields = ("internet", "laptop", "smartphone", "literasi_digital")
    try:
        values = [float(item[f]) for f in fields if item.get(f) is not None]
    except (TypeError, ValueError):
        return None
    if len(values) != len(fields):
        return None
    return round(1.0 - sum(values) / len(values), 4)


@bp.route("/")
@login_required
def peta():
    return render_template("map/peta.html", warna=KATEGORI_COLORS)


@bp.route("/api/hasil")
@login_required
def api_hasil():
    """Hasil clustering siap di-match ke GeoJSON.

    Setiap item juga memuat `skor_ketimpangan` agar popup bisa langsung
    menampilkan tanpa perhitungan client-side.
    """
    items = hasil_clustering_model.all_hasil()
    payload = []
    indikator = current_app.config.get("INDIKATOR", [
        "internet", "laptop", "smartphone", "literasi_digital",
    ])
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
                "skor_ketimpangan": _skor_ketimpangan(it),
                "jumlah_variabel": len(indikator),
            }
        )
    return jsonify({"items": payload, "warna": KATEGORI_COLORS})


@bp.route("/api/stats")
@login_required
def api_stats():
    """Statistik cluster untuk panel kanan & tabel ringkasan."""
    stats = hasil_clustering_model.cluster_stats()
    total = sum(s["jumlah"] for s in stats)
    return jsonify({
        "stats": stats,
        "total": total,
        "warna": KATEGORI_COLORS,
    })
