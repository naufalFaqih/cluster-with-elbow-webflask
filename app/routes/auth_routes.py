"""Auth routes — login & logout (PRD #7, #8)."""
from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models import user_model

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard.index"))

    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            error = "Username dan password wajib diisi."
        else:
            user = user_model.find_by_username(username)
            if user is None or not user_model.verify_password(user["password"], password):
                error = "Username atau password salah."
            else:
                session.clear()
                session["user_id"] = user["id"]
                session["user_nama"] = user["nama"]
                session["user_username"] = user["username"]
                session["user_role"] = user["role"]
                flash(f"Selamat datang, {user['nama']}!", "success")
                return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html", error=error)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("dashboard.index"))

    error = None
    form_data = {"nama": "", "username": ""}

    if request.method == "POST":
        nama = (request.form.get("nama") or "").strip()
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        confirm_password = request.form.get("confirm_password") or ""
        form_data = {"nama": nama, "username": username}

        if not nama or not username or not password or not confirm_password:
            error = "Nama, username, password, dan konfirmasi password wajib diisi."
        elif password != confirm_password:
            error = "Konfirmasi password tidak sesuai."
        elif user_model.username_exists(username):
            error = "Username sudah digunakan."
        else:
            user_model.create(nama, username, password, role="user")
            flash("Registrasi berhasil. Silakan login.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", error=error, form_data=form_data)


@bp.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for("auth.login"))
