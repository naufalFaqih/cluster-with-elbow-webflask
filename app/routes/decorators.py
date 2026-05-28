"""Auth decorators (PRD #9 — role-based access)."""
from __future__ import annotations

from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapper


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("auth.login"))
        if session.get("user_role") != "admin":
            flash("Halaman ini hanya dapat diakses oleh admin.", "danger")
            return redirect(url_for("dashboard.index"))
        return view(*args, **kwargs)

    return wrapper
