"""Phase 2b — variables locales.

Couverture :
    * déclaration ``"name:": valeur`` (non émise dans la sortie) ;
    * référence ``name:`` ;
    * projection ``name:$.path`` (JSONPath enraciné sur la valeur de la variable) ;
    * scope lexical (chaîne de résolveurs) : un objet imbriqué voit les variables
      du parent et peut les masquer ;
    * variable inconnue -> ``None`` (conforme à ``RuntimeContext.GetVariable``).

Inclut un cas porté de ``CompileUnitTest1.TestVariable`` (sans le cast ``#string``
qui relève de la Phase 3).
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.runtime.variables import VariableManager


# --- scope isolé -----------------------------------------------------------
def test_scope_resolves_locally() -> None:
    scope = VariableManager()
    scope.add("a", 1)
    assert scope.get("a") == (True, 1)


def test_scope_falls_back_to_parent() -> None:
    parent = VariableManager()
    parent.add("a", 1)
    child = VariableManager(parent)
    child.add("b", 2)
    assert child.get("a") == (True, 1)  # hérité du parent
    assert child.get("b") == (True, 2)  # local


def test_scope_child_masks_parent() -> None:
    parent = VariableManager()
    parent.add("a", 1)
    child = VariableManager(parent)
    child.add("a", 99)
    assert child.get("a") == (True, 99)
    assert parent.get("a") == (True, 1)


def test_scope_unknown_returns_not_found() -> None:
    assert VariableManager().get("nope") == (False, None)


# --- via la transformation -------------------------------------------------
TRANSFORM_CASES = [
    pytest.param('{ "var1:": 2, "propertyName": var1: }', {}, {"propertyName": 2}, id="decl-ref"),
    pytest.param('{ "x:": $.n, "out": x: }', {"n": "Alice"}, {"out": "Alice"}, id="ref-depuis-path"),
    pytest.param(
        '{ "b:": $.obj, "bb": b:$.Test1.Test2 }',
        {"obj": {"Test1": {"Test2": 8}}},
        {"bb": 8},
        id="projection",
    ),
    pytest.param('{ "v:": 1, "keep": "k" }', {}, {"keep": "k"}, id="declaration-non-emise"),
    pytest.param('{ "out": nope: }', {}, {"out": None}, id="inconnue-null"),
    pytest.param(
        '{ "a:": 1, "inner": { "a:": 2, "v": a: } }',
        {},
        {"inner": {"v": 2}},
        id="scope-masquage",
    ),
    pytest.param(
        '{ "a:": 1, "inner": { "v": a: } }',
        {},
        {"inner": {"v": 1}},
        id="scope-heritage",
    ),
]


@pytest.mark.parametrize("template, source, expected", TRANSFORM_CASES)
def test_transform_variables(template: str, source, expected) -> None:
    assert JsltTemplate.parse(template).transform(source) == expected


def test_dotnet_testvariable_without_cast() -> None:
    # Porté de CompileUnitTest1.TestVariable (le cast #string arrive en Phase 3) :
    #   { "var1:": 2, "propertyName": var1: }  =>  { "propertyName": 2 }
    template = '{ "var1:": 2, "propertyName": var1: }'
    assert JsltTemplate.parse(template).transform({}) == {"propertyName": 2}
