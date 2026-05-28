"""Data ketimpangan CRUD + upload routes (PRD #13, #14)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.utils import secure_filename

from app.models import data_ketimpangan_model, wilayah_model
from app.routes.decorators import admin_required, login_required
from app.services import preprocessing_service

bp = Blueprint("data", __name__, url_prefix="/data")


def _allowed(filename: str) -> bool:
    ext = (filename.rsplit(".", 1)[-1] or "").lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


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


@bp.route("/upload", methods=["GET", "POST"])
@admin_required
def upload():
    if request.method == "POST":
        f = request.files.get("file")
        if not f or f.filename == "":
            flash("Pilih file Excel/CSV terlebih dahulu.", "danger")
            return redirect(url_for("data.upload"))
        if not _allowed(f.filename):
            flash("Format file tidak didukung. Gunakan .xlsx, .xls, atau .csv.", "danger")
            return redirect(url_for("data.upload"))

        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        upload_folder.mkdir(parents=True, exist_ok=True)
        save_path = upload_folder / secure_filename(f.filename)
        f.save(save_path)

        try:
            if save_path.suffix.lower() == ".csv":
                df = pd.read_csv(save_path)
            else:
                df = pd.read_excel(save_path)

            df = preprocessing_service.clean_uploaded_dataframe(
                df, default_tahun=current_app.config["DEFAULT_TAHUN"]
            )

            inserted, updated = 0, 0
            for _, row in df.iterrows():
                wilayah = wilayah_model.find_by_nama(row["wilayah"])
                if not wilayah:
                    new_id = wilayah_model.create(row["wilayah"])
                    wilayah = {"id": new_id}

                existing = data_ketimpangan_model.find_by_wilayah_tahun(
                    wilayah["id"], int(row["tahun"])
                )
                if existing:
                    data_ketimpangan_model.update(
                        existing["id"],
                        wilayah["id"],
                        int(row["tahun"]),
                        row["internet"],
                        row["laptop"],
                        row["smartphone"],
                        row["literasi_digital"],
                    )
                    updated += 1
                else:
                    data_ketimpangan_model.create(
                        wilayah["id"],
                        int(row["tahun"]),
                        row["internet"],
                        row["laptop"],
                        row["smartphone"],
                        row["literasi_digital"],
                    )
                    inserted += 1

            flash(
                f"Upload berhasil. {inserted} data baru, {updated} data diperbarui.",
                "success",
            )
        except preprocessing_service.PreprocessingError as exc:
            flash(f"Validasi dataset gagal: {exc}", "danger")
        except Exception as exc:  # noqa: BLE001
            flash(f"Gagal memproses file: {exc}", "danger")
        finally:
            try:
                save_path.unlink(missing_ok=True)
            except Exception:  # noqa: BLE001
                pass

        return redirect(url_for("data.index"))

    return render_template("data/upload.html")
