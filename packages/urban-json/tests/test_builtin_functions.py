"""Fonctions intégrées pures supplémentaires (chaînes + maths).

Portées des ``CustomServices`` .NET. Conventions reprises :
    * chaînes : ``None`` -> ``None``, chaîne -> résultat, autre -> ``False`` ;
    * maths : valeur non numérique (ou ``None``) -> ``None``.

Quirks .NET conservés (fidélité) : ``floor``/``round``/``min``/``max`` renvoient
un flottant ; ``round`` est un arrondi bancaire (demi vers pair) ; ``min``/``max``
sont binaires (deux nombres, pas un agrégat de tableau).
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source if source is not None else {})["r"]


STRING_CASES = [
    pytest.param('{ "r": upper($.s) }', {"s": "abc"}, "ABC", id="upper"),
    pytest.param('{ "r": lower($.s) }', {"s": "AbC"}, "abc", id="lower"),
    pytest.param('{ "r": trim($.s) }', {"s": "  x  "}, "x", id="trim-espaces"),
    pytest.param('{ "r": trim($.s, "xy") }', {"s": "xyhelloyx"}, "hello", id="trim-chars"),
    pytest.param('{ "r": split($.s, ",") }', {"s": "a,b,c"}, ["a", "b", "c"], id="split"),
    pytest.param('{ "r": startswith($.s, "ab") }', {"s": "abc"}, True, id="startswith"),
    pytest.param('{ "r": endswith($.s, "bc") }', {"s": "abc"}, True, id="endswith"),
    pytest.param('{ "r": stringcontains($.s, "b") }', {"s": "abc"}, True, id="stringcontains"),
]

MATH_CASES = [
    pytest.param('{ "r": abs($.n) }', {"n": -5}, 5, id="abs-int"),
    pytest.param('{ "r": abs($.n) }', {"n": -2.5}, 2.5, id="abs-float"),
    pytest.param('{ "r": floor($.n) }', {"n": 2.7}, 2.0, id="floor"),
    pytest.param('{ "r": round($.n) }', {"n": 2.5}, 2.0, id="round-banquier-pair"),
    pytest.param('{ "r": round($.n) }', {"n": 3.5}, 4.0, id="round-banquier-impair"),
    pytest.param('{ "r": min($.a, $.b) }', {"a": 3, "b": 5}, 3.0, id="min"),
    pytest.param('{ "r": max($.a, $.b) }', {"a": 3, "b": 5}, 5.0, id="max"),
]


@pytest.mark.parametrize("template, source, expected", STRING_CASES + MATH_CASES)
def test_pure_functions(template: str, source, expected) -> None:
    result = run(template, source)
    assert result == expected
    assert type(result) is type(expected)  # fidélité de type (ex. float pour floor)


def test_string_function_conventions() -> None:
    assert run('{ "r": upper($.x) }', {}) is None  # null -> null
    assert run('{ "r": upper($.n) }', {"n": 5}) is False  # non-chaîne -> False


def test_math_function_conventions() -> None:
    assert run('{ "r": abs($.s) }', {"s": "x"}) is None  # non-nombre -> null
    assert run('{ "r": abs($.x) }', {}) is None  # null -> null
