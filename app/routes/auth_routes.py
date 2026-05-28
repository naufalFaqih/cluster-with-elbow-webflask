"""Auth routes — login & logout (PRD #7, #8)."""
from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models import user_model

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("auth.login"))

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
                return redirect(url_for("auth.login"))

    return render_template("auth/login.html", error=error)


@bp.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for("auth.login"))
