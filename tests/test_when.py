"""Phase 4c — when / switch.

``when(expr) { "cas1": …, "default": … }`` compare l'expression (``==``) au nom
de chaque cas et produit le bloc du premier cas correspondant ; sinon le bloc
``default`` ; sinon ``null``. ``switch`` est un alias de ``when``.
"""

from __future__ import annotations

import pytest

from jslt import JsltTemplate

WHEN_CASES = [
    pytest.param('{ "r": when($.x) { "a": 1, "b": 2 } }', {"x": "a"}, {"r": 1}, id="premier-cas"),
    pytest.param('{ "r": when($.x) { "a": 1, "b": 2 } }', {"x": "b"}, {"r": 2}, id="second-cas"),
    pytest.param(
        '{ "r": when($.x) { "a": 1, "default": 99 } }', {"x": "zzz"}, {"r": 99}, id="default"
    ),
    pytest.param('{ "r": when($.x) { "a": 1 } }', {"x": "zzz"}, {"r": None}, id="aucun-cas-null"),
    pytest.param(
        '{ "r": when($.x) { "a": { "toto": 1 }, "default": null } }',
        {"x": "a"},
        {"r": {"toto": 1}},
        id="bloc-objet",
    ),
    pytest.param(
        '{ "r": switch($.x) { "a": 1, "default": 0 } }', {"x": "a"}, {"r": 1}, id="alias-switch"
    ),
    pytest.param(
        '{ "v:": "b", "r": when(v:) { "a": 1, "b": 2 } }', {}, {"r": 2}, id="when-sur-variable"
    ),
]


@pytest.mark.parametrize("template, source, expected", WHEN_CASES)
def test_when(template: str, source, expected) -> None:
    assert JsltTemplate.parse(template).transform(source) == expected
