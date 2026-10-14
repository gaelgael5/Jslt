"""Phase 4a — fonctions intégrées et chaînage.

Infrastructure de fonctions (registre par nom) et premières fonctions du cœur
(``sum``, ``concat``), plus l'opérateur de chaînage ``->`` qui injecte l'opérande
gauche comme premier argument de la fonction.
"""

from __future__ import annotations

import pytest

from jslt import JsltError, JsltTemplate

FUNCTION_CASES = [
    pytest.param('{ "s": sum($.prices) }', {"prices": [1, 2, 3]}, {"s": 6}, id="sum-entiers"),
    pytest.param('{ "s": sum($.prices) }', {"prices": [1.5, 2.5]}, {"s": 4.0}, id="sum-flottants"),
    pytest.param('{ "s": sum($.e) }', {"e": []}, {"s": 0}, id="sum-vide"),
    pytest.param('{ "c": concat($.w) }', {"w": ["a", "b", "c"]}, {"c": "abc"}, id="concat"),
    pytest.param(
        '{ "c": concat($.w, "-") }', {"w": ["a", "b", "c"]}, {"c": "a-b-c"}, id="concat-sep"
    ),
]

CHAIN_CASES = [
    pytest.param('{ "s": $.prices -> sum() }', {"prices": [10, 20]}, {"s": 30}, id="chain-sum"),
    pytest.param('{ "c": $.w -> concat("|") }', {"w": ["x", "y"]}, {"c": "x|y"}, id="chain-concat"),
]


@pytest.mark.parametrize("template, source, expected", FUNCTION_CASES + CHAIN_CASES)
def test_functions(template: str, source, expected) -> None:
    assert JsltTemplate.parse(template).transform(source) == expected


def test_unknown_function_raises() -> None:
    with pytest.raises(JsltError):
        JsltTemplate.parse('{ "x": nope($.a) }').transform({"a": 1})


def test_chain_equivalent_to_direct_call() -> None:
    source = {"prices": [1, 2, 3, 4]}
    direct = JsltTemplate.parse('{ "s": sum($.prices) }').transform(source)
    chained = JsltTemplate.parse('{ "s": $.prices -> sum() }').transform(source)
    assert direct == chained == {"s": 10}


def test_custom_function_via_registry() -> None:
    # Le registre est extensible : on peut enregistrer une fonction et l'utiliser.
    from jslt.functions import FunctionRegistry
    from jslt.runtime import RuntimeContext, Sources
    from jslt.runtime.evaluator import JsltEvaluationVisitor

    registry = FunctionRegistry()
    registry.register("double", lambda ctx, x: x * 2)

    template = JsltTemplate.parse('{ "d": double($.n) }')
    context = RuntimeContext(Sources({"n": 21}), functions=registry)
    assert template.ast.accept(JsltEvaluationVisitor(context)) == {"d": 42}
