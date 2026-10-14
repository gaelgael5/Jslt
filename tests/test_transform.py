"""Phase 1 — transformation du cas « défaut ».

Sans opération de transformation, le résultat est exactement ce que décrit le
template (objets, tableaux et constantes matérialisés tels quels).

Une partie des cas est portée depuis la suite .NET
``Black.Beard.Jslt.UnitTests`` (CompileUnitTest1) et sert d'oracle de
conformité : mêmes templates, mêmes résultats attendus.
"""

from __future__ import annotations

import pytest

from jslt import JsltTemplate


# Les templates .NET utilisent des quotes simples remplacées par des doubles ;
# on garde la même convention pour faciliter la comparaison 1:1.
def q(template: str) -> str:
    return template.replace("'", '"')


# Cas portés de CompileUnitTest1 (.NET) — oracle de conformité.
DOTNET_CASES = [
    pytest.param("{ 'propertyName': 'toto' }", {"propertyName": "toto"}, id="property-string"),
    pytest.param("{ 'propertyName': 6 }", {"propertyName": 6}, id="property-integer"),
    pytest.param("{ 'propertyName': 6.7 }", {"propertyName": 6.7}, id="property-decimal"),
]


@pytest.mark.parametrize("template, expected", DOTNET_CASES)
def test_dotnet_conformance(template: str, expected) -> None:
    assert JsltTemplate.parse(q(template)).transform({}) == expected


# Cas supplémentaires du portage (cas « défaut »).
DEFAULT_CASES = [
    pytest.param('{ "flag": true }', {"flag": True}, id="boolean-true"),
    pytest.param('{ "flag": false }', {"flag": False}, id="boolean-false"),
    pytest.param('{ "nothing": null }', {"nothing": None}, id="null"),
    pytest.param('{ "n": "x", "m": "y" }', {"n": "x", "m": "y"}, id="deux-proprietes"),
    pytest.param("{ }", {}, id="objet-vide"),
    pytest.param("[ ]", [], id="tableau-vide"),
    pytest.param("[ 1, 2, 3 ]", [1, 2, 3], id="tableau-entiers"),
    pytest.param(
        '{ "obj": { "a": 1 }, "arr": [ 1, "deux", true, null ] }',
        {"obj": {"a": 1}, "arr": [1, "deux", True, None]},
        id="imbrication",
    ),
    pytest.param('{ "big": 10000000000 }', {"big": 10000000000}, id="entier-large"),
]


@pytest.mark.parametrize("template, expected", DEFAULT_CASES)
def test_default_case(template: str, expected) -> None:
    assert JsltTemplate.parse(template).transform({}) == expected


def test_transform_without_source() -> None:
    # Le cas défaut n'exploite pas la source : transform() sans argument marche.
    assert JsltTemplate.parse('{ "n": "x" }').transform() == {"n": "x"}


def test_integer_is_not_zeroed() -> None:
    # Garde-fou : on ne reproduit pas le bug .NET de VisitJsonValueInteger
    # (qui renvoyait 0 pour tout entier <= Int32.MaxValue).
    assert JsltTemplate.parse('{ "n": 6 }').transform({}) == {"n": 6}
    assert JsltTemplate.parse('{ "n": 42 }').transform({}) == {"n": 42}


def test_duplicate_property_rejected() -> None:
    from jslt import JsltSemanticError

    with pytest.raises(JsltSemanticError):
        JsltTemplate.parse('{ "n": 1, "n": 2 }')
