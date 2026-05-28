"""Database helper.

Supports two drivers:
  * ``mysql``  — production / PRD spec (mysql-connector-python)
  * ``sqlite`` — local fallback (no MySQL setup required)

The query API is intentionally kept minimal:

    db = get_db()
    rows = db.fetchall("SELECT * FROM users WHERE role = %s", ("admin",))
    db.execute("INSERT INTO users (...) VALUES (...)", (...))

Both drivers accept ``%s`` placeholders — the helper rewrites to ``?`` for
SQLite under the hood.
"""
from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from flask import Flask, current_app, g

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def init_app(app: Flask) -> None:
    """Register teardown + initialise SQLite schema if needed."""
    app.teardown_appcontext(_close_db)

    if app.config["DB_DRIVER"] == "sqlite":
        with app.app_context():
            init_sqlite()


def get_db() -> "DBHelper":
    """Return the per-request DB helper, creating it if necessary."""
    if "db_helper" not in g:
        g.db_helper = DBHelper(current_app.config)
    return g.db_helper


def _close_db(_exc: BaseException | None = None) -> None:
    helper: DBHelper | None = g.pop("db_helper", None)
    if helper is not None:
        helper.close()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
class DBHelper:
    """Thin abstraction over MySQL / SQLite connections."""

    def __init__(self, config: Mapping[str, Any]):
        self.driver = config["DB_DRIVER"]
        self._config = config
        self._conn: Any = None

    # -- connection management -----------------------------------------
    def _connect(self) -> Any:
        if self._conn is not None:
            return self._conn

        if self.driver == "mysql":
            try:
                import mysql.connector  # type: ignore
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "mysql-connector-python is required for DB_DRIVER=mysql. "
                    "Install via `pip install mysql-connector-python`."
                ) from exc

            self._conn = mysql.connector.connect(
                host=self._config["DB_HOST"],
                port=self._config["DB_PORT"],
                user=self._config["DB_USER"],
                password=self._config["DB_PASSWORD"],
                database=self._config["DB_NAME"],
                autocommit=False,
            )
        elif self.driver == "sqlite":
            self._conn = sqlite3.connect(self._config["SQLITE_PATH"])
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON;")
        else:
            raise RuntimeError(f"Unsupported DB_DRIVER: {self.driver!r}")
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            try:
                self._conn.close()
            except Exception:  # pragma: no cover
                logger.exception("Error closing DB connection")
            self._conn = None

    # -- query helpers --------------------------------------------------
    def _normalize(self, sql: str) -> str:
        """Translate %s placeholders to ? for SQLite."""
        if self.driver == "sqlite":
            return sql.replace("%s", "?")
        return sql

    @contextmanager
    def cursor(self):
        conn = self._connect()
        if self.driver == "mysql":
            cur = conn.cursor(dictionary=True)
        else:
            cur = conn.cursor()
        try:
            yield cur
        finally:
            cur.close()

    def fetchall(self, sql: str, params: Sequence[Any] | None = None) -> list[dict]:
        with self.cursor() as cur:
            cur.execute(self._normalize(sql), tuple(params or ()))
            rows = cur.fetchall()
        return [dict(row) for row in rows]

    def fetchone(self, sql: str, params: Sequence[Any] | None = None) -> dict | None:
        with self.cursor() as cur:
            cur.execute(self._normalize(sql), tuple(params or ()))
            row = cur.fetchone()
        return dict(row) if row is not None else None

    def execute(
        self, sql: str, params: Sequence[Any] | None = None, *, commit: bool = True
    ) -> int:
        """Run an INSERT/UPDATE/DELETE. Returns ``lastrowid``."""
        conn = self._connect()
        with self.cursor() as cur:
            cur.execute(self._normalize(sql), tuple(params or ()))
            last_id = cur.lastrowid
        if commit:
            conn.commit()
        return last_id

    def executemany(
        self, sql: str, seq_params: Iterable[Sequence[Any]], *, commit: bool = True
    ) -> None:
        conn = self._connect()
        with self.cursor() as cur:
            cur.executemany(self._normalize(sql), [tuple(p) for p in seq_params])
        if commit:
            conn.commit()

    def commit(self) -> None:
        if self._conn is not None:
            self._conn.commit()


# ---------------------------------------------------------------------------
# SQLite bootstrap
# ---------------------------------------------------------------------------
def init_sqlite() -> None:
    """Create SQLite database from schema + seed if it doesn't already exist."""
    config = current_app.config
    db_path = Path(config["SQLITE_PATH"])
    if db_path.exists():
        logger.info("SQLite DB already exists at %s — skipping init.", db_path)
        return

    base_dir = Path(current_app.root_path).parent
    schema_file = base_dir / "database" / "schema_sqlite.sql"
    seed_file = base_dir / "database" / "seed.sql"

    if not schema_file.exists():
        raise FileNotFoundError(f"Missing schema file: {schema_file}")

    conn = sqlite3.connect(str(db_path))
    conn.executescript(schema_file.read_text(encoding="utf-8"))

    if seed_file.exists():
        conn.executescript(seed_file.read_text(encoding="utf-8"))

    conn.commit()
    conn.close()
    logger.info("SQLite DB initialised at %s", db_path)
