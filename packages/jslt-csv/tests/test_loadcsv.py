"""Tests du plugin jslt-csv (fonction ``loadcsv``).

Couvre : lecture + typage des valeurs, séparateur par défaut ``;``, absence
d'entête, exclusions, assainissement des entêtes, découverte via entry point,
et usage dans un template (boucle ``$source``).
"""

from __future__ import annotations

from pathlib import Path

from jslt import FunctionRegistry, JsltTemplate

from jslt_csv import execute_loadcsv, register


def _write(tmp_path: Path, name: str, content: str) -> str:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return str(path)


def test_loadcsv_basic_typing(tmp_path: Path) -> None:
    csv = "name;age;active\nAlice;30;true\nBob;25;false\n"
    path = _write(tmp_path, "people.csv", csv)
    rows = execute_loadcsv(None, path)
    assert rows == [
        {"name": "Alice", "age": 30, "active": True},
        {"name": "Bob", "age": 25, "active": False},
    ]


def test_loadcsv_decimal_and_leading_zero(tmp_path: Path) -> None:
    csv = "ref;price\nA;1.50\nB;007\n"
    path = _write(tmp_path, "p.csv", csv)
    rows = execute_loadcsv(None, path)
    assert rows[0]["price"] == 1.5
    # "007" ne doit pas devenir un entier (garde-fou .NET) -> reste une chaîne.
    assert rows[1]["price"] == "007"


def test_loadcsv_no_header(tmp_path: Path) -> None:
    path = _write(tmp_path, "nh.csv", "Alice;30\nBob;25\n")
    rows = execute_loadcsv(None, path, has_header=False)
    assert rows == [
        {"Column0": "Alice", "Column1": 30},
        {"Column0": "Bob", "Column1": 25},
    ]


def test_loadcsv_custom_separator(tmp_path: Path) -> None:
    path = _write(tmp_path, "c.csv", "a,b\n1,2\n")
    rows = execute_loadcsv(None, path, separator=",")
    assert rows == [{"a": 1, "b": 2}]


def test_loadcsv_excluded_columns(tmp_path: Path) -> None:
    path = _write(tmp_path, "e.csv", "name;secret\nAlice;x\n")
    rows = execute_loadcsv(None, path, excluded_columns="secret")
    assert rows == [{"name": "Alice"}]


def test_loadcsv_exclude_null_and_empty(tmp_path: Path) -> None:
    path = _write(tmp_path, "n.csv", "a;b\n1;\n")
    rows = execute_loadcsv(None, path, exclude_null_and_empty=True)
    assert rows == [{"a": 1}]  # cellule b vide -> omise


def test_header_sanitized(tmp_path: Path) -> None:
    path = _write(tmp_path, "h.csv", "Prénom Client;Âge\nAlice;30\n")
    rows = execute_loadcsv(None, path)
    assert rows == [{"Prenom_Client": "Alice", "Age": 30}]


def test_register_into_custom_registry(tmp_path: Path) -> None:
    reg = FunctionRegistry()
    register(reg)
    assert "loadcsv" in reg
    assert reg.describe("loadcsv").description


def test_discovered_via_entry_point() -> None:
    # Le plugin est installé : jslt doit le découvrir dans le registre par défaut.
    from jslt import default_registry, load_plugins

    load_plugins(default_registry)
    assert "loadcsv" in default_registry


def test_loadcsv_in_template(tmp_path: Path) -> None:
    path = _write(tmp_path, "t.csv", "name;age\nAlice;30\nBob;25\n")
    template = f'[ {{ "$source": loadcsv("{path}"), "n": $.name, "a": $.age }} ]'
    assert JsltTemplate.parse(template).transform({}) == [
        {"n": "Alice", "a": 30},
        {"n": "Bob", "a": 25},
    ]
