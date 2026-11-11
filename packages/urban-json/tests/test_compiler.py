"""Chemin compilé (``JsltTemplate.build``) — équivalence et comportement.

Le chemin compilé doit produire **exactement** le même résultat que
l'interpréteur d'AST. On le vérifie sur un jeu de cas ciblés (un par type de
nœud) **et** sur tous les exemples du guide.
"""

from __future__ import annotations

import json

import pytest

from _docs import DOCS, NO_DOCS, doc_triples
from urban_json import FunctionRegistry, JsltTemplate

# Sans `docs/`, ces tests n'ont pas de matière : on le dit au lieu de les faire
# échouer (cf. `_docs.find_docs`).
pytestmark = pytest.mark.skipif(DOCS is None, reason=NO_DOCS)


# --- cas ciblés : un par construction --------------------------------------

EQUIV_CASES = [
    pytest.param('{ "v": "Paris" }', {}, id="constante"),
    pytest.param('{ "n": $.user.name }', {"user": {"name": "A"}}, id="jpath"),
    pytest.param('{ "ids": $..id }', {"a": {"id": 1}, "b": {"id": 2}}, id="descente"),
    pytest.param('{ "u:": $.user, "n": u:$.name }', {"user": {"name": "B"}}, id="variable"),
    pytest.param('{ "s": $.a + $.b }', {"a": 1, "b": 2}, id="operateur-binaire"),
    pytest.param('{ "v": $.x ?? "def" }', {}, id="coalesce"),
    pytest.param('{ "n": !$.b }', {"b": True}, id="operateur-unaire"),
    pytest.param('{ "t": sum($.n) }', {"n": [1, 2, 3]}, id="fonction"),
    # Arguments paresseux (`lazy_args`) : la fonction évalue elle-même
    # l'expression, une fois par élément pour `sort`, jamais pour le repli
    # inutile de `trydefault`. Les deux chemins doivent le faire pareil.
    pytest.param('{ "t": sort($.items, $.k) }', {"items": [{"k": 2}, {"k": 1}]}, id="lazy-sort"),
    pytest.param('{ "t": sort($.n, foldtext($), true) }', {"n": ["b", "A"]}, id="lazy-sort-calcule"),
    pytest.param('{ "t": trydefault($.a / $.b, "ko") }', {"a": 1, "b": 0}, id="lazy-trydefault"),
    pytest.param('{ "t": trydefault($.a, sum($.bad)) }', {"a": 1, "bad": ["x"]}, id="lazy-non-evalue"),
    pytest.param('{ "i": $.s #integer }', {"s": "42"}, id="cast"),
    pytest.param(
        '{ "r": when($.x) { "a": 1, "default": 0 } }', {"x": "a"}, id="when-match"
    ),
    pytest.param(
        '{ "r": when($.x) { "a": 1, "default": 0 } }', {"x": "z"}, id="when-default"
    ),
    pytest.param(
        '[ { "$source": $.u, "n": $.name } ]',
        {"u": [{"name": "A"}, {"name": "B"}]},
        id="boucle",
    ),
    pytest.param(
        '[ { "$source": $.items, "$where": $.ok, "n": $.n } ]',
        {"items": [{"ok": True, "n": 1}, {"ok": False, "n": 2}]},
        id="boucle-where",
    ),
    pytest.param(
        '[ { "$source": $.groups, "g": $.key,'
        '    "rows": [ { "$source": $.items, "v": $.v } ] } ]',
        {"groups": [{"key": "g1", "items": [{"v": 1}, {"v": 2}]}]},
        id="boucle-imbriquee",
    ),
    pytest.param('{ "g": $.items[?(@.n > 1)] }', {"items": [{"n": 1}, {"n": 2}]}, id="filtre"),
    pytest.param('{ "src": { "$source": $.a, "x": $.v } }', {"a": {"v": 9}}, id="objet-source"),
]


@pytest.mark.parametrize("template, source", EQUIV_CASES)
def test_compiled_matches_interpreter(template: str, source) -> None:
    interpreted = JsltTemplate.parse(template).transform(source)
    compiled = JsltTemplate.parse(template).build().transform(source)
    assert compiled == interpreted


# --- équivalence sur tous les exemples du guide ----------------------------
# Les exemples sont extraits par `_docs.py`, partagé avec `test_guide_examples.py` :
# un document thématique ajouté entre donc dans les deux suites à la fois.

GUIDE_CASES = doc_triples()


def test_guide_cases_found() -> None:
    assert len(GUIDE_CASES) >= 100


@pytest.mark.parametrize("template, source, expected", GUIDE_CASES)
def test_compiled_guide_examples(template: str, source: str, expected: str) -> None:
    doc = json.loads(source)
    want = json.loads(expected)
    compiled = JsltTemplate.parse(template).build().transform(doc)
    assert compiled == want
    # et strictement identique à l'interpréteur
    assert compiled == JsltTemplate.parse(template).transform(doc)


# --- comportement de build() ----------------------------------------------

def test_build_is_idempotent_and_returns_self() -> None:
    tpl = JsltTemplate.parse('{ "v": $.x }')
    first = tpl.build()
    assert first is tpl
    compiled_program = tpl._compiled
    tpl.build()  # 2e appel : ne recompile pas
    assert tpl._compiled is compiled_program


def test_transform_without_build_uses_interpreter() -> None:
    tpl = JsltTemplate.parse('{ "v": $.x }')
    assert tpl._compiled is None
    assert tpl.transform({"x": 1}) == {"v": 1}
    assert tpl._compiled is None


def test_compiled_honours_custom_registry() -> None:
    registry = FunctionRegistry()
    registry.register("double", lambda ctx, x=None: x * 2)

    tpl = JsltTemplate.parse('{ "r": double($.n) }').build()
    assert tpl.transform({"n": 21}, functions=registry) == {"r": 42}
