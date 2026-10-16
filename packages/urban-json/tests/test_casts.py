"""Phase 4b — casts ``#type``.

Un cast ``#type`` est porté, comme en .NET, par un appel à la fonction
``convert`` : ``valeur #integer`` devient ``convert(valeur, "integer")``.

Types JSON natifs pris en charge pleinement : ``integer``, ``decimal``,
``string``, ``boolean``. Les types ``uri`` / ``uuid`` / ``datetime`` / ``time``
sont rendus en chaîne (simplifié).
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate

CAST_CASES = [
    pytest.param('{ "x": "3" #integer }', {}, {"x": 3}, id="string-vers-integer"),
    pytest.param('{ "x": 3 #string }', {}, {"x": "3"}, id="integer-vers-string"),
    pytest.param('{ "x": 3 #decimal }', {}, {"x": 3.0}, id="integer-vers-decimal"),
    pytest.param('{ "x": $.n #integer }', {"n": "42"}, {"x": 42}, id="path-vers-integer"),
    pytest.param('{ "x": $.n #boolean }', {"n": "true"}, {"x": True}, id="path-vers-boolean"),
    pytest.param('{ "x": 0 #boolean }', {}, {"x": False}, id="zero-vers-boolean"),
    pytest.param('{ "x": $.missing #integer }', {}, {"x": 0}, id="null-vers-defaut"),
    pytest.param('{ "x": sum($.v) #string }', {"v": [1, 2]}, {"x": "3"}, id="fonction-vers-string"),
]


@pytest.mark.parametrize("template, source, expected", CAST_CASES)
def test_casts(template: str, source, expected) -> None:
    assert JsltTemplate.parse(template).transform(source) == expected


def test_dotnet_testvariable_with_cast() -> None:
    # Oracle complet de CompileUnitTest1.TestVariable (avec le cast #string) :
    #   { "var1:": 2, "propertyName": var1: #string }  =>  { "propertyName": "2" }
    template = '{ "var1:": 2, "propertyName": var1: #string }'
    assert JsltTemplate.parse(template).transform({}) == {"propertyName": "2"}
