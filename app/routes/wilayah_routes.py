"""Wilayah CRUD routes (PRD #12). Admin-only mutations."""
from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import wilayah_model
from app.routes.decorators import admin_required, login_required

bp = Blueprint("wilayah", __name__, url_prefix="/wilayah")


@bp.route("/")
@login_required
def index():
    items = wilayah_model.all_wilayah()
    return render_template("wilayah/index.html", items=items)


@bp.route("/create", methods=["POST"])
@admin_required
def create():
    nama = (request.form.get("nama_wilayah") or "").strip()
    provinsi = (request.form.get("provinsi") or "Jawa Barat").strip() or "Jawa Barat"
    if not nama:
        flash("Nama wilayah wajib diisi.", "danger")
    else:
        try:
            wilayah_model.create(nama, provinsi)
            flash(f"Wilayah '{nama}' berhasil ditambahkan.", "success")
        except Exception as exc:  # noqa: BLE001
            flash(f"Gagal menambah wilayah: {exc}", "danger")
    return redirect(url_for("wilayah.index"))


@bp.route("/<int:wilayah_id>/update", methods=["POST"])
@admin_required
def update(wilayah_id: int):
    nama = (request.form.get("nama_wilayah") or "").strip()
    provinsi = (request.form.get("provinsi") or "Jawa Barat").strip() or "Jawa Barat"
    if not nama:
        flash("Nama wilayah wajib diisi.", "danger")
    else:
        try:
            wilayah_model.update(wilayah_id, nama, provinsi)
            flash("Wilayah berhasil diperbarui.", "success")
        except Exception as exc:  # noqa: BLE001
            flash(f"Gagal memperbarui wilayah: {exc}", "danger")
    return redirect(url_for("wilayah.index"))


@bp.route("/<int:wilayah_id>/delete", methods=["POST"])
@admin_required
def delete(wilayah_id: int):
    try:
        wilayah_model.delete(wilayah_id)
        flash("Wilayah berhasil dihapus.", "success")
    except Exception as exc:  # noqa: BLE001
        flash(f"Gagal menghapus wilayah: {exc}", "danger")
    return redirect(url_for("wilayah.index"))
