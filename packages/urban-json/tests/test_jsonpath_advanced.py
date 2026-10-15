"""Phase 5a — JSONPath avancé : wildcard, descente récursive, slices.

Les sélecteurs sont portés de ``Bb.JPaths`` (WildcardSelector, SliceSelector) et
la descente récursive ``..`` s'appuie sur le segment récursif déjà en place. Les
filtres ``?(...)`` et fonctions de chemin relèvent de la Phase 5b.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate

SRC = {
    "prices": [{"n": 1}, {"n": 2}, {"n": 3}],
    "obj": {"a": 1, "b": 2, "c": 3},
    "list": [10, 20, 30, 40, 50],
    "nested": {"x": {"n": 7}, "y": {"n": 8}, "z": {"m": 9}},
}

ADVANCED_CASES = [
    # wildcard
    pytest.param('{ "r": $.obj.* }', SRC, {"r": [1, 2, 3]}, id="wildcard-objet"),
    pytest.param('{ "r": $.list[*] }', SRC, {"r": [10, 20, 30, 40, 50]}, id="wildcard-tableau"),
    # descente récursive : trouve tous les n (prices + nested)
    pytest.param('{ "r": $..n }', SRC, {"r": [1, 2, 3, 7, 8]}, id="descente-recursive"),
    pytest.param(
        '{ "r": $..n }', {"a": {"n": 1}, "b": {"c": {"n": 2}}}, {"r": [1, 2]}, id="descente-imbriquee"
    ),
    # slices
    pytest.param('{ "r": $.list[1:3] }', SRC, {"r": [20, 30]}, id="slice-binaire"),
    pytest.param('{ "r": $.list[2:] }', SRC, {"r": [30, 40, 50]}, id="slice-gauche"),
    pytest.param('{ "r": $.list[:2] }', SRC, {"r": [10, 20]}, id="slice-droite"),
    pytest.param('{ "r": $.list[-2:] }', SRC, {"r": [40, 50]}, id="slice-negatif"),
]


@pytest.mark.parametrize("template, source, expected", ADVANCED_CASES)
def test_jsonpath_advanced(template: str, source, expected) -> None:
    assert JsltTemplate.parse(template).transform(source) == expected


def test_dotnet_testsum_recursive() -> None:
    # Oracle CompileUnitTest1.TestSum : sum($..n) avec {prices:[{n:1},{n:2},{n:3}]}
    template = '{ "prices": sum($..n) }'
    source = {"prices": [{"n": 1}, {"n": 2}, {"n": 3}]}
    assert JsltTemplate.parse(template).transform(source) == {"prices": 6}
