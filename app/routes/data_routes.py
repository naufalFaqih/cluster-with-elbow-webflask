"""Data ketimpangan CRUD routes (PRD #13)."""
from __future__ import annotations

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.models import data_ketimpangan_model, wilayah_model
from app.routes.decorators import admin_required, login_required

bp = Blueprint("data", __name__, url_prefix="/data")


@bp.route("/")
@login_required
def index():
    items = data_ketimpangan_model.all_data()
    wilayah = wilayah_model.all_wilayah()
    default_tahun = current_app.config.get("DEFAULT_TAHUN", 2023)
    return render_template(
        "data/index.html",
        items=items,
        wilayah=wilayah,
        default_tahun=default_tahun,
    )


@bp.route("/create", methods=["POST"])
@admin_required
def create():
    try:
        wilayah_id = int(request.form["wilayah_id"])
        tahun = int(request.form["tahun"])
        data_ketimpangan_model.upsert_by_wilayah(
            wilayah_id,
            tahun,
            request.form.get("internet"),
            request.form.get("laptop"),
            request.form.get("smartphone"),
            request.form.get("literasi_digital"),
        )
        flash("Data ketimpangan berhasil disimpan.", "success")
    except (ValueError, KeyError) as exc:
        flash(f"Input tidak valid: {exc}", "danger")
    except Exception as exc:  # noqa: BLE001
        flash(f"Gagal menyimpan data: {exc}", "danger")
    return redirect(url_for("data.index"))


@bp.route("/<int:data_id>/update", methods=["POST"])
@admin_required
def update(data_id: int):
    try:
        wilayah_id = int(request.form["wilayah_id"])
        tahun = int(request.form["tahun"])
        data_ketimpangan_model.update(
            data_id,
            wilayah_id,
            tahun,
            request.form.get("internet"),
            request.form.get("laptop"),
            request.form.get("smartphone"),
            request.form.get("literasi_digital"),
        )
        flash("Data berhasil diperbarui.", "success")
    except (ValueError, KeyError) as exc:
        flash(f"Input tidak valid: {exc}", "danger")
    except Exception as exc:  # noqa: BLE001
        flash(f"Gagal memperbarui data: {exc}", "danger")
    return redirect(url_for("data.index"))


@bp.route("/<int:data_id>/delete", methods=["POST"])
@admin_required
def delete(data_id: int):
    try:
        data_ketimpangan_model.delete(data_id)
        flash("Data berhasil dihapus.", "success")
    except Exception as exc:  # noqa: BLE001
        flash(f"Gagal menghapus data: {exc}", "danger")
    return redirect(url_for("data.index"))
