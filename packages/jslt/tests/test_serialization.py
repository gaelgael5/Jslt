"""Sérialisation AST → source (round-trip), analogue du ``ToString`` du .NET.

Propriété vérifiée : pour un template ``t`` et une source ``src``,

    parse(t).to_source()  est ré-analysable, et
    parse(parse(t).to_source()).transform(src) == parse(t).transform(src)

Autrement dit, la re-sérialisation préserve le **comportement** (pas forcément
la mise en forme au caractère près).
"""

from __future__ import annotations

import pytest

from jslt import JsltTemplate

# (template, source) — couvre les grandes constructions du langage.
ROUND_TRIP_CASES = [
    pytest.param('{ "n": "x" }', {}, id="constante-string"),
    pytest.param('{ "i": 6, "d": 6.7, "b": true, "z": null }', {}, id="constantes"),
    pytest.param('{ "name": $.n }', {"n": "a"}, id="jsonpath-simple"),
    pytest.param('{ "deep": $..n }', {"a": {"n": 1}, "n": 2}, id="descente-recursive"),
    pytest.param('{ "idx": $.list[0] }', {"list": [10, 20]}, id="indice"),
    pytest.param('{ "wild": $.* }', {"a": 1, "b": 2}, id="wildcard"),
    pytest.param('{ "slice": $.list[1:3] }', {"list": [1, 2, 3, 4]}, id="slice"),
    pytest.param('{ "sum": $.a + $.b }', {"a": 1, "b": 2}, id="operateur-binaire"),
    pytest.param('{ "neg": !$.flag }', {"flag": True}, id="negation"),
    pytest.param('{ "co": $.a ?? $.b }', {"b": 9}, id="coalesce"),
    pytest.param('{ "prices": sum($.n) }', {"n": [1, 2, 3]}, id="fonction"),
    pytest.param('{ "up": upper($.s) }', {"s": "hi"}, id="fonction-texte"),
    pytest.param(
        '[ { "$source": $.items, "k": $.n } ]',
        {"items": [{"n": 1}, {"n": 2}]},
        id="boucle",
    ),
    pytest.param(
        '[ { "$source": $.items, "$where": $.ok, "k": $.n } ]',
        {"items": [{"n": 1, "ok": True}, {"n": 2, "ok": False}]},
        id="boucle-where",
    ),
    pytest.param('{ "v:": 1, "a": v: }', {}, id="variable-decl-ref"),
    pytest.param('{ "b:": $.obj, "bb": b:$.x }', {"obj": {"x": 7}}, id="variable-projection"),
    pytest.param(
        '{ "w": when($.a) { "x": 1, "default": 0 } }',
        {"a": "x"},
        id="when-switch",
    ),
    pytest.param('{ "f": $.items[?(@.n > 1)] }', {"items": [{"n": 1}, {"n": 2}]}, id="filtre"),
    pytest.param(
        '{ "f": $.items[?(@.n == 1 | @.n == 3)] }',
        {"items": [{"n": 1}, {"n": 2}, {"n": 3}]},
        id="filtre-ou",
    ),
    pytest.param('{ "casted": $.n #integer }', {"n": "42"}, id="cast"),
]


@pytest.mark.parametrize("template, source", ROUND_TRIP_CASES)
def test_to_source_is_reparseable(template: str, source) -> None:
    serialized = JsltTemplate.parse(template).to_source()
    # Doit se ré-analyser sans erreur.
    assert JsltTemplate.parse(serialized) is not None


@pytest.mark.parametrize("template, source", ROUND_TRIP_CASES)
def test_round_trip_preserves_behaviour(template: str, source) -> None:
    original = JsltTemplate.parse(template)
    reparsed = JsltTemplate.parse(original.to_source())
    assert reparsed.transform(source) == original.transform(source)


def test_to_source_is_idempotent() -> None:
    # Re-sérialiser la sortie redonne exactement la même chaîne.
    template = '{ "sum": $.a + $.b, "name": upper($.n) }'
    once = JsltTemplate.parse(template).to_source()
    twice = JsltTemplate.parse(once).to_source()
    assert once == twice
