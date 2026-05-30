"""User model — authentication and role management."""
from __future__ import annotations

from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db


def find_by_username(username: str) -> Optional[dict]:
    return get_db().fetchone(
        "SELECT id, nama, username, password, role FROM users WHERE username = %s",
        (username,),
    )


def username_exists(username: str) -> bool:
    row = get_db().fetchone(
        "SELECT id FROM users WHERE username = %s",
        (username,),
    )
    return row is not None


def find_by_id(user_id: int) -> Optional[dict]:
    return get_db().fetchone(
        "SELECT id, nama, username, role FROM users WHERE id = %s",
        (user_id,),
    )


def all_users() -> list[dict]:
    return get_db().fetchall(
        "SELECT id, nama, username, role, created_at FROM users ORDER BY id"
    )


def create(nama: str, username: str, password: str, role: str = "user") -> int:
    if role not in ("admin", "user"):
        raise ValueError("role must be 'admin' or 'user'")
    return get_db().execute(
        "INSERT INTO users (nama, username, password, role) VALUES (%s, %s, %s, %s)",
        (nama, username, generate_password_hash(password, method="pbkdf2:sha256"), role),
    )


def verify_password(stored_hash: str, candidate: str) -> bool:
    return check_password_hash(stored_hash, candidate)
