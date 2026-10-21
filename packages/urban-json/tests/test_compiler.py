"""Chemin compilé (``JsltTemplate.build``) — équivalence et comportement.

Le chemin compilé doit produire **exactement** le même résultat que
l'interpréteur d'AST. On le vérifie sur un jeu de cas ciblés (un par type de
nœud) **et** sur tous les exemples du guide.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from urban_json import FunctionRegistry, JsltTemplate

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

def _find_docs() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "docs"
        if (candidate / "guide.md").is_file():
            return candidate
    raise FileNotFoundError("dossier docs/ introuvable")


_BLOCK_RE = re.compile(r"```(\w+)[^\n]*\n(.*?)```", re.DOTALL)


def _guide_triples() -> list:
    cases = []
    for guide in sorted(_find_docs().glob("guide*.md")):
        blocks = _BLOCK_RE.findall(guide.read_text(encoding="utf-8"))
        for i in range(len(blocks) - 2):
            (l0, tpl), (l1, src), (l2, out) = blocks[i], blocks[i + 1], blocks[i + 2]
            if l0 == "jslt" and l1 == "json" and l2 == "json":
                cases.append(
                    pytest.param(tpl.strip(), src.strip(), out.strip(),
                                 id=f"{guide.name}-{i}")
                )
    return cases


GUIDE_CASES = _guide_triples()


def test_guide_cases_found() -> None:
    assert len(GUIDE_CASES) >= 20


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
