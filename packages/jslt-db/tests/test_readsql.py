"""Tests du plugin jslt-db (``connectsql`` / ``readsql``) avec SQLite.

Couvre : descripteur de connexion, lecture + ``$_line``, assainissement des noms
de colonnes, client inconnu, découverte via entry point, usage en template.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest
from jslt import FunctionRegistry, JsltTemplate

from jslt_db import execute_connectsql, execute_readsql, register


def _make_db(tmp_path: Path) -> str:
    path = tmp_path / "app.db"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT, active INTEGER)")
    conn.executemany(
        "INSERT INTO users VALUES (?, ?, ?)",
        [(1, "Alice", 1), (2, "Bob", 0)],
    )
    conn.commit()
    conn.close()
    return str(path)


def test_connectsql_descriptor() -> None:
    cx = execute_connectsql(None, "sqlite", "/tmp/x.db")
    assert cx == {"client": "sqlite", "connection": "/tmp/x.db"}


def test_connectsql_unknown_client() -> None:
    with pytest.raises(ValueError, match="inconnu"):
        execute_connectsql(None, "oracle", "x")


def test_readsql_rows_and_line(tmp_path: Path) -> None:
    cx = execute_connectsql(None, "sqlite", _make_db(tmp_path))
    rows = execute_readsql(None, cx, "SELECT id, name FROM users ORDER BY id")
    assert rows == [
        {"$_line": 1, "id": 1, "name": "Alice"},
        {"$_line": 2, "name": "Bob", "id": 2},
    ]


def test_readsql_column_name_sanitized(tmp_path: Path) -> None:
    cx = execute_connectsql(None, "sqlite", _make_db(tmp_path))
    rows = execute_readsql(None, cx, 'SELECT name AS "Full Name" FROM users WHERE id = 1')
    assert rows == [{"$_line": 1, "Full_Name": "Alice"}]


def test_readsql_requires_descriptor() -> None:
    with pytest.raises(ValueError, match="descripteur"):
        execute_readsql(None, "not-a-descriptor", "SELECT 1")


def test_register_into_custom_registry() -> None:
    reg = FunctionRegistry()
    register(reg)
    assert "connectsql" in reg and "readsql" in reg


def test_discovered_via_entry_point() -> None:
    from jslt import default_registry, load_plugins

    load_plugins(default_registry)
    assert "connectsql" in default_registry and "readsql" in default_registry


def test_in_template(tmp_path: Path) -> None:
    db = _make_db(tmp_path)
    template = (
        "{"
        f'  "cx:": connectsql("sqlite", "{db}"),'
        '  "rows": [ { "$source": readsql(cx:, "SELECT id, name FROM users ORDER BY id"),'
        '             "id": $.id, "n": $.name } ]'
        "}"
    )
    assert JsltTemplate.parse(template).transform({}) == {
        "rows": [{"id": 1, "n": "Alice"}, {"id": 2, "n": "Bob"}]
    }
