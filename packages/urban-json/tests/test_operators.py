"""Phase 3b — opérateurs.

Comparaison, arithmétique, logiques, bit-à-bit, coalesce, négation, avec
précédence standard (associativité gauche). Le type de l'opérande gauche pilote
la coercion (``+`` sur chaîne = concaténation), conforme à
``RuntimeContext.EvaluateBinaryOperator``.

Écarts volontaires documentés : ``^`` = XOR entier (et non puissance) ; ``||``
corrige le copier-coller fautif .NET (OU et non ET).
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate

SRC = {"prop1": {"SubPprop1": 2}, "prop2": 3, "a": 10, "b": 4, "flag": True, "no": False}

# Cas portés des tests binaires de CompileUnitTest1 (oracle).
DOTNET_CASES = [
    pytest.param('{ "p": $.prop1.SubPprop1 + $.prop2 }', {"p": 5}, id="add"),
    pytest.param('{ "p": $.prop1.SubPprop1 - $.prop2 }', {"p": -1}, id="subtract"),
    pytest.param('{ "p": $.prop1.SubPprop1 * $.prop2 }', {"p": 6}, id="multiply"),
]

OPERATOR_CASES = [
    pytest.param('{ "r": $.a / $.b }', {"r": 2}, id="divide-entiere-tronquee"),
    pytest.param('{ "r": $.a % $.b }', {"r": 2}, id="modulo"),
    pytest.param('{ "s": "x" + $.prop2 }', {"s": "x3"}, id="concat-string"),
    pytest.param('{ "r": $.a > $.b }', {"r": True}, id="greater"),
    pytest.param('{ "r": $.a == 10 }', {"r": True}, id="equal"),
    pytest.param('{ "r": $.a != 10 }', {"r": False}, id="not-equal"),
    pytest.param('{ "r": $.flag && $.no }', {"r": False}, id="and-booleen"),
    pytest.param('{ "r": $.flag || $.no }', {"r": True}, id="or-booleen"),
    pytest.param('{ "r": !$.no }', {"r": True}, id="negation"),
    pytest.param('{ "r": $.missing ?? 42 }', {"r": 42}, id="coalesce-null"),
    pytest.param('{ "r": $.a ?? 42 }', {"r": 10}, id="coalesce-present"),
    pytest.param('{ "r": 5 ^ 3 }', {"r": 6}, id="xor"),
    pytest.param('{ "r": 6 & 3 }', {"r": 2}, id="bitwise-and"),
    pytest.param('{ "r": 4 | 1 }', {"r": 5}, id="bitwise-or"),
]

PRECEDENCE_CASES = [
    pytest.param('{ "r": 2 + 3 * 4 }', {"r": 14}, id="mult-avant-add"),
    pytest.param('{ "r": 2 * 3 + 4 }', {"r": 10}, id="mult-puis-add"),
    pytest.param('{ "r": 10 - 2 - 3 }', {"r": 5}, id="assoc-gauche"),
    # `??` lie plus fort que comparaisons et logique, moins que l'arithmétique.
    pytest.param('{ "r": $.missing ?? "x" == "x" }', {"r": True}, id="coalesce-avant-egalite"),
    pytest.param('{ "r": $.a ?? 0 == 10 }', {"r": True}, id="coalesce-present-avant-egalite"),
    pytest.param('{ "r": $.missing ?? 3 > 2 }', {"r": True}, id="coalesce-avant-comparaison"),
    pytest.param('{ "r": $.missing ?? true && $.flag }', {"r": True}, id="coalesce-avant-et"),
    pytest.param('{ "r": $.missing ?? 1 + 2 }', {"r": 3}, id="coalesce-apres-addition"),
    pytest.param('{ "r": $.a ?? 1 + 2 }', {"r": 10}, id="coalesce-present-apres-addition"),
]

# Les parenthèses regroupent une opération complète, pas un seul opérande.
PARENTHESES_CASES = [
    pytest.param('{ "r": (2 + 3) * 4 }', {"r": 20}, id="parentheses-add-avant-mult"),
    pytest.param('{ "r": 10 - (2 - 3) }', {"r": 11}, id="parentheses-assoc-droite"),
    pytest.param('{ "r": (($.missing ?? "x")) == "x" }', {"r": True}, id="parentheses-coalesce"),
    pytest.param('{ "r": ($.a ?? 0) == 10 }', {"r": True}, id="parentheses-coalesce-present"),
    pytest.param('{ "r": !($.a == 10) }', {"r": False}, id="parentheses-negation"),
    pytest.param('{ "r": (2 + 3) #string }', {"r": "5"}, id="parentheses-cast"),
]


@pytest.mark.parametrize(
    "template, expected",
    DOTNET_CASES + OPERATOR_CASES + PRECEDENCE_CASES + PARENTHESES_CASES,
)
def test_operators(template: str, expected) -> None:
    assert JsltTemplate.parse(template).transform(SRC) == expected


# Le chaînage `->` est couvert en Phase 4a (voir tests/test_functions.py).
