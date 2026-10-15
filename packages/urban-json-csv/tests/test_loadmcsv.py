"""Tests de ``loadmcsv`` (CSV multi-enregistrements hiérarchique).

Couvre : #DEF/colonnes, hiérarchie par règles, enfants homonymes -> tableau,
métadonnées (#clé + _metadatas), fichier plat (sans règle), découverte entry
point, usage en template.
"""

from __future__ import annotations

from pathlib import Path

from urban_json import JsltTemplate

from urban_json_csv import execute_loadmcsv

CATALOG = (
    "#SOURCE;demo\n"
    "#DEF;CATALOG;id;name\n"
    "#DEF;BOOK;code;title\n"
    "CATALOG;1;Librairie\n"
    "BOOK;a;Alpha\n"
    "BOOK;b;Beta\n"
    "#END\n"
)


def _write(tmp_path: Path, name: str, content: str) -> str:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return str(path)


def _strip_meta(obj):
    """Retire récursivement les _metadatas (chemin non déterministe) pour comparer."""
    if isinstance(obj, dict):
        return {k: _strip_meta(v) for k, v in obj.items() if k != "_metadatas"}
    if isinstance(obj, list):
        return [_strip_meta(v) for v in obj]
    return obj


def test_hierarchy_and_columns(tmp_path: Path) -> None:
    path = _write(tmp_path, "catalog.mcsv", CATALOG)
    result = execute_loadmcsv(None, path, "CATALOG:BOOK")
    assert _strip_meta(result) == {
        "BOOK": [
            {"code": "a", "title": "Alpha"},
            {"code": "b", "title": "Beta"},
        ],
        "id": "1",
        "name": "Librairie",
    }


def test_metadatas_present(tmp_path: Path) -> None:
    path = _write(tmp_path, "catalog.mcsv", CATALOG)
    result = execute_loadmcsv(None, path, "CATALOG:BOOK")
    meta = result["_metadatas"]
    assert meta["SOURCE"] == "demo"              # métadonnée #SOURCE
    assert meta["_filename"].endswith("catalog.mcsv")
    assert meta["_encodingFile"] == "utf-8"


def test_single_child_is_still_array(tmp_path: Path) -> None:
    content = (
        "#DEF;CATALOG;id\n#DEF;BOOK;code\nCATALOG;1\nBOOK;a\n#END\n"
    )
    path = _write(tmp_path, "one.mcsv", content)
    result = execute_loadmcsv(None, path, "CATALOG:BOOK")
    assert result["BOOK"] == [{"code": "a"}]     # toujours un tableau


def test_trailing_separator_tolerated(tmp_path: Path) -> None:
    # Le .NET suppose un ';' final ; le portage tolère les deux formes.
    content = "#DEF;R;a;b\nR;1;2;\n#END\n"
    path = _write(tmp_path, "t.mcsv", content)
    assert _strip_meta(execute_loadmcsv(None, path, "")) == {"a": "1", "b": "2"}


def test_flat_without_rule_nests_under_first(tmp_path: Path) -> None:
    # Sans règle, tout s'imbrique sous le premier bloc (fidèle au .NET).
    content = "#DEF;A;x\n#DEF;B;y\nA;1\nB;2\n#END\n"
    path = _write(tmp_path, "flat.mcsv", content)
    result = execute_loadmcsv(None, path, "")
    assert _strip_meta(result) == {"x": "1", "B": [{"y": "2"}]}


def test_discovered_via_entry_point() -> None:
    from urban_json import default_registry, load_plugins

    load_plugins(default_registry)
    assert "loadmcsv" in default_registry


def test_in_template(tmp_path: Path) -> None:
    path = _write(tmp_path, "catalog.mcsv", CATALOG)
    template = (
        f'[ {{ "$source": selectmany(loadmcsv("{path}", "CATALOG:BOOK"), $.BOOK.*),'
        '     "t": $.title } ]'
    )
    assert JsltTemplate.parse(template).transform({}) == [{"t": "Alpha"}, {"t": "Beta"}]
