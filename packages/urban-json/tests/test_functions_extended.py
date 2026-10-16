"""Fonctions intégrées étendues : maths, texte, encodage, divers, collections.

Portées des ``CustomServices`` .NET. Les fonctions non déterministes (``uuid``,
``now``) sont testées sur leur forme, pas leur valeur.
"""

from __future__ import annotations

import math

import pytest

from urban_json import JsltTemplate


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source if source is not None else {})["r"]


MATH_CASES = [
    pytest.param('{ "r": sqrt($.n) }', {"n": 9}, 3.0, id="sqrt"),
    pytest.param('{ "r": pow($.a, $.b) }', {"a": 2, "b": 10}, 1024.0, id="pow"),
    pytest.param('{ "r": truncate($.n) }', {"n": 3.9}, 3.0, id="truncate"),
    pytest.param('{ "r": exp($.n) }', {"n": 0}, 1.0, id="exp"),
    pytest.param('{ "r": logarithm10($.n) }', {"n": 1000}, 3.0, id="log10"),
    pytest.param('{ "r": logarithm2($.n) }', {"n": 8}, 3.0, id="log2"),
    pytest.param('{ "r": sin($.n) }', {"n": 0}, 0.0, id="sin"),
    pytest.param('{ "r": cos($.n) }', {"n": 0}, 1.0, id="cos"),
    pytest.param('{ "r": atan2($.a, $.b) }', {"a": 0, "b": 1}, 0.0, id="atan2"),
]

TEXT_CASES = [
    pytest.param('{ "r": indexof($.s, "b") }', {"s": "abc"}, 1, id="indexof"),
    pytest.param('{ "r": indexof($.s, "z") }', {"s": "abc"}, -1, id="indexof-absent"),
    pytest.param('{ "r": lastindexof($.s, "a") }', {"s": "banana"}, 5, id="lastindexof"),
    pytest.param('{ "r": padleft($.s, 5, "0") }', {"s": "7"}, "00007", id="padleft"),
    pytest.param('{ "r": padright($.s, 3, "-") }', {"s": "x"}, "x--", id="padright"),
    pytest.param('{ "r": stringlenght($.s) }', {"s": "hello"}, 5, id="stringlenght"),
    pytest.param('{ "r": stringlenght($.x) }', {}, 0, id="stringlenght-null"),
]

ENCODING_CASES = [
    pytest.param('{ "r": tobase64($.s) }', {"s": "test"}, "dGVzdA==", id="tobase64"),
    pytest.param('{ "r": frombase64($.s) }', {"s": "dGVzdA=="}, "test", id="frombase64"),
    pytest.param(
        '{ "r": sha256($.s) }',
        {"s": "abc"},
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        id="sha256-abc",
    ),
]

MISC_CASES = [
    pytest.param('{ "r": isnull($.x) }', {}, True, id="isnull-true"),
    pytest.param('{ "r": isnull($.a) }', {"a": 1}, False, id="isnull-false"),
    pytest.param('{ "r": isnotnull($.a) }', {"a": 1}, True, id="isnotnull"),
]

COLLECTION_CASES = [
    pytest.param('{ "r": limit($.a, 2) }', {"a": [1, 2, 3, 4]}, [1, 2], id="limit"),
    pytest.param('{ "r": union($.a) }', {"a": [[1, 2], [3], [4]]}, [1, 2, 3, 4], id="union"),
    pytest.param('{ "r": select($.a, $.*.n) }', {"a": [{"n": 1}, {"n": 2}]}, 1, id="select"),
    pytest.param(
        '{ "r": selectmany($.a, $.*.n) }', {"a": [{"n": 1}, {"n": 2}]}, [1, 2], id="selectmany"
    ),
]


@pytest.mark.parametrize(
    "template, source, expected",
    MATH_CASES + TEXT_CASES + ENCODING_CASES + MISC_CASES + COLLECTION_CASES,
)
def test_extended_functions(template: str, source, expected) -> None:
    assert run(template, source) == expected


def test_constants() -> None:
    assert run('{ "r": pi() }') == math.pi
    assert run('{ "r": e() }') == math.e


def test_uuid_shape() -> None:
    value = run('{ "r": uuid() }')
    assert isinstance(value, str)
    assert len(value) == 36 and value.count("-") == 4


def test_now_is_iso_string() -> None:
    value = run('{ "r": now() }')
    assert isinstance(value, str)
    # Analysable comme un datetime ISO.
    from datetime import datetime

    datetime.fromisoformat(value)
