"""Phase 4a — fonctions intégrées et chaînage.

Infrastructure de fonctions (registre par nom) et premières fonctions du cœur
(``sum``, ``concat``), plus l'opérateur de chaînage ``->`` qui injecte l'opérande
gauche comme premier argument de la fonction.
"""

from __future__ import annotations

import pytest

from urban_json import JsltError, JsltTemplate

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
    from urban_json.functions import FunctionRegistry
    from urban_json.runtime import RuntimeContext, Sources
    from urban_json.runtime.evaluator import JsltEvaluationVisitor

    registry = FunctionRegistry()
    registry.register("double", lambda ctx, x: x * 2)

    template = JsltTemplate.parse('{ "d": double($.n) }')
    context = RuntimeContext(Sources({"n": 21}), functions=registry)
    assert template.ast.accept(JsltEvaluationVisitor(context)) == {"d": 42}


# --- mise en texte des conteneurs ---------------------------------------------
# Régression : `to_text` rendait `str(valeur)`, donc la représentation **Python**
# d'un tableau ou d'un objet — guillemets simples compris. Elle ressortait dans
# le JSON produit par `concat` et par les clefs de `groupby` / `countby`.


def test_concat_d_un_tableau_imbrique_rend_du_json() -> None:
    template = '{ "r": concat($.l, ",") }'
    source = {"l": [[1, "x"], 2]}
    assert JsltTemplate.parse(template).transform(source) == {"r": '[1,"x"],2'}


def test_concat_d_un_objet_rend_du_json() -> None:
    template = '{ "r": concat($.l) }'
    assert JsltTemplate.parse(template).transform({"l": [{"a": 1}]}) == {"r": '{"a":1}'}


def test_clef_de_groupe_composite_est_du_json() -> None:
    template = '{ "r": groupby($.l, [$.a, $.t]) }'
    source = {"l": [{"a": 1, "t": "x"}]}
    assert JsltTemplate.parse(template).transform(source) == {
        "r": {'[1,"x"]': [{"a": 1, "t": "x"}]}
    }


def test_countby_composite_est_du_json() -> None:
    template = '{ "r": countby($.l, [$.a, $.t]) }'
    source = {"l": [{"a": 1, "t": "x"}]}
    assert JsltTemplate.parse(template).transform(source) == {"r": {'[1,"x"]': 1}}


def test_les_deux_chemins_de_mise_en_texte_concordent() -> None:
    # Le cast `#string` passait déjà par le JSON : les deux doivent dire pareil.
    template = '{ "cast": $.o #string, "texte": concat([$.o]) }'
    result = JsltTemplate.parse(template).transform({"o": {"a": [1, "x"]}})
    assert result["cast"] == result["texte"] == '{"a":[1,"x"]}'
