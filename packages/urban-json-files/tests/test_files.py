"""loadjson, iteratejsonfile, concatpath — port de Services.cs / Services.paths.cs."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from urban_json import FunctionRegistry, JsltError, JsltTemplate

from urban_json_files import register


@pytest.fixture(scope="module")
def registry() -> FunctionRegistry:
    reg = FunctionRegistry()
    register(reg)
    return reg


def run(registry, expression: str, source=None):
    return JsltTemplate.parse(f'{{ "r": {expression} }}').transform(source or {}, functions=registry)["r"]


def _write(tmp_path: Path, name: str, data, raw: str | None = None) -> str:
    path = tmp_path / name
    path.write_text(raw if raw is not None else json.dumps(data), encoding="utf-8")
    return str(path)


def test_loadjson(registry, tmp_path) -> None:
    path = _write(tmp_path, "a.json", {"k": [1, 2], "s": "é"})
    assert run(registry, "loadjson($.p)", {"p": path}) == {"k": [1, 2], "s": "é"}


def test_loadjson_bom(registry, tmp_path) -> None:
    path = _write(tmp_path, "bom.json", None, raw="﻿[1]")
    assert run(registry, "loadjson($.p)", {"p": path}) == [1]


def test_loadjson_fichier_absent_donne_null(registry, tmp_path) -> None:
    assert run(registry, "loadjson($.p)", {"p": str(tmp_path / "absent.json")}) is None


def test_loadjson_json_invalide(registry, tmp_path) -> None:
    path = _write(tmp_path, "bad.json", None, raw="{oops")
    with pytest.raises(JsltError, match="JSON invalide"):
        run(registry, "loadjson($.p)", {"p": path})


def test_loadjson_chemin_manquant(registry) -> None:
    with pytest.raises(JsltError, match="loadjson"):
        run(registry, "loadjson($.p)", {"p": None})


def test_iteratejsonfile(registry, tmp_path) -> None:
    path = _write(tmp_path, "big.json", {"root": {"a": {"id": 1}, "b": {"id": 2}}})
    assert run(registry, 'iteratejsonfile($.p, "$.root.*")', {"p": path}) == [{"id": 1}, {"id": 2}]


def test_iteratejsonfile_chemin_compile(registry, tmp_path) -> None:
    path = _write(tmp_path, "big.json", {"items": [{"id": 1}, {"id": 2}]})
    assert run(registry, "iteratejsonfile($.p, $.items[*].id)", {"p": path}) == [1, 2]


def test_iteratejsonfile_dans_une_boucle(registry, tmp_path) -> None:
    # Usage du test .NET : la fonction alimente une projection par élément.
    path = _write(tmp_path, "big.json", {"root": [{"n": "a"}, {"n": "b"}]})
    template = JsltTemplate.parse('{ "r": [ { "$": iteratejsonfile($.p, "$.root[*]"), "nom": $.n } ] }')
    assert template.transform({"p": path}, functions=registry)["r"] == [{"nom": "a"}, {"nom": "b"}]


@pytest.mark.parametrize("expression", ['iteratejsonfile($.p, "$.x")', "iteratejsonfile(null, null)"])
def test_iteratejsonfile_erreurs(registry, tmp_path, expression) -> None:
    with pytest.raises(JsltError, match="iteratejsonfile"):
        run(registry, expression, {"p": str(tmp_path / "absent.json")})


def test_concatpath(registry) -> None:
    assert run(registry, 'concatpath(["data", "2026", "file.json"])') == os.path.join("data", "2026", "file.json")


def test_concatpath_ignore_null_et_convertit(registry) -> None:
    assert run(registry, 'concatpath(["a", null, 3])') == os.path.join("a", "3")


def test_concatpath_segment_absolu_repart_de_la_racine(registry) -> None:
    root = os.path.abspath(os.sep)
    out = run(registry, "concatpath($.p)", {"p": ["a", os.path.join(root, "etc"), "x"]})
    assert out == os.path.join(root, "etc", "x")


@pytest.mark.parametrize("value", [None, "abc", []])
def test_concatpath_entrees_vides(registry, value) -> None:
    assert run(registry, "concatpath($.p)", {"p": value}) in (None, "")


def test_catalogue_documente(registry) -> None:
    names = {e["name"]: e for e in registry.catalog()}
    assert set(names) == {"loadjson", "iteratejsonfile", "concatpath"}
    assert all(len(e["description"]) >= 15 for e in names.values())


def test_decouverte_par_entry_point() -> None:
    from urban_json import default_registry, load_plugins

    load_plugins()
    assert "loadjson" in default_registry
