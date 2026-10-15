"""Phase 2a — JSONPath simple contre le document source.

Couverture : racine ``$``, sélecteur de nom (``.name`` / ``['name']`` /
``["name"]``), sélecteur d'indice (``[0]``, négatifs), et sémantique de
résultat portée de ``RuntimeContext.GetContentByJPath`` :
    * 0 correspondance -> ``None``
    * 1 correspondance -> la valeur
    * N correspondances -> la liste des valeurs

On teste à deux niveaux : le moteur JSONPath isolé, et la transformation
complète via l'API.
"""

from __future__ import annotations

import pytest

from jslt import JsltTemplate
from jslt.jsonpath import IndexSelector, JsonPath, NameSelector, PathScope, PathSegment

SOURCE = {
    "n": "Alice",
    "nested": {"a": {"b": 42}},
    "items": [{"n": 1}, {"n": 2}, {"n": 3}],
    "list": [10, 20, 30],
}


# --- moteur JSONPath isolé -------------------------------------------------
def test_engine_name_selector() -> None:
    path = JsonPath(PathScope.GLOBAL, [PathSegment([NameSelector("n")])])
    assert path.select_values(SOURCE) == ["Alice"]


def test_engine_index_selector_negative() -> None:
    path = JsonPath(
        PathScope.GLOBAL,
        [PathSegment([NameSelector("list")]), PathSegment([IndexSelector(-1)])],
    )
    assert path.select_values(SOURCE) == [30]


def test_engine_missing_returns_empty() -> None:
    path = JsonPath(PathScope.GLOBAL, [PathSegment([NameSelector("nope")])])
    assert path.select_values(SOURCE) == []


def test_engine_is_singular() -> None:
    path = JsonPath(PathScope.GLOBAL, [PathSegment([NameSelector("n")])])
    assert path.is_singular is True


# --- via la transformation -------------------------------------------------
TRANSFORM_CASES = [
    pytest.param('{ "name": $.n }', {"name": "Alice"}, id="nom-simple"),
    pytest.param('{ "deep": $.nested.a.b }', {"deep": 42}, id="nom-chaine"),
    pytest.param('{ "first": $.list[0] }', {"first": 10}, id="indice-0"),
    pytest.param('{ "last": $.list[-1] }', {"last": 30}, id="indice-negatif"),
    pytest.param('{ "k": $["n"] }', {"k": "Alice"}, id="crochet-double-quote"),
    pytest.param("{ \"k\": $['n'] }", {"k": "Alice"}, id="crochet-simple-quote"),
    pytest.param('{ "missing": $.nope }', {"missing": None}, id="absent-donne-null"),
    pytest.param('{ "whole": $ }', {"whole": SOURCE}, id="racine"),
]


@pytest.mark.parametrize("template, expected", TRANSFORM_CASES)
def test_transform_jsonpath(template: str, expected) -> None:
    assert JsltTemplate.parse(template).transform(SOURCE) == expected


def test_missing_path_is_null_not_omitted() -> None:
    # Conformité .NET : un chemin sans correspondance produit la valeur null,
    # la propriété n'est pas omise.
    result = JsltTemplate.parse('{ "a": $.absent }').transform(SOURCE)
    assert result == {"a": None}
    assert "a" in result
