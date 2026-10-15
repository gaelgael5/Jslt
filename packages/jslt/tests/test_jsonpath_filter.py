"""Phase 5b — filtres JSONPath ``[?(...)]``.

Opérandes : chemins ``@`` (élément courant) / ``$`` (racine) et littéraux.
Opérateurs : comparaisons ``== != < <= > >=``, logiques ``&`` / ``|``, négation.

Rappel de sémantique (0/1/N, comme ``GetContentByJPath``) : un filtre qui ne
retient qu'un seul élément renvoie cet élément, pas une liste d'un élément.
"""

from __future__ import annotations

import pytest

from jslt import JsltTemplate

SRC = {
    "items": [{"n": 1, "ok": True}, {"n": 2, "ok": False}, {"n": 3, "ok": True}],
    "t": 2,
}

FILTER_CASES = [
    pytest.param(
        '{ "r": $.items[?(@.n > 1)] }',
        {"r": [{"n": 2, "ok": False}, {"n": 3, "ok": True}]},
        id="comparaison",
    ),
    pytest.param(
        '{ "r": $.items[?(@.ok == true)] }',
        {"r": [{"n": 1, "ok": True}, {"n": 3, "ok": True}]},
        id="egalite-booleen",
    ),
    pytest.param(
        '{ "r": $.items[?(@.n > 1 & @.ok == true)] }',
        {"r": {"n": 3, "ok": True}},  # 1 seule correspondance -> la valeur
        id="et-logique",
    ),
    pytest.param(
        '{ "r": $.items[?(@.n == 1 | @.n == 3)] }',
        {"r": [{"n": 1, "ok": True}, {"n": 3, "ok": True}]},
        id="ou-logique",
    ),
    pytest.param(
        '{ "r": $.items[?(@.n >= $.t)] }',
        {"r": [{"n": 2, "ok": False}, {"n": 3, "ok": True}]},
        id="comparaison-a-la-racine",
    ),
]


@pytest.mark.parametrize("template, expected", FILTER_CASES)
def test_filters(template: str, expected) -> None:
    assert JsltTemplate.parse(template).transform(SRC) == expected


def test_filter_in_loop() -> None:
    # Un filtre alimente couramment une boucle.
    template = '[ { "$source": $.items[?(@.ok == true)], "v": $.n } ]'
    assert JsltTemplate.parse(template).transform(SRC) == [{"v": 1}, {"v": 3}]


IN_SRC = {"items": [{"n": 1}, {"n": 2}, {"n": 3}, {"n": 4}], "allowed": [2, 4]}

IN_CASES = [
    pytest.param(
        '{ "r": $.items[?(@.n in [2, 4])] }',
        {"r": [{"n": 2}, {"n": 4}]},
        id="in-litteral-tableau",
    ),
    pytest.param(
        '{ "r": $.items[?(@.n in $.allowed)] }',
        {"r": [{"n": 2}, {"n": 4}]},
        id="in-chemin",
    ),
    pytest.param('{ "r": $.items[?(@.n in [3])] }', {"r": {"n": 3}}, id="in-un-match"),
]


@pytest.mark.parametrize("template, expected", IN_CASES)
def test_filter_in(template: str, expected) -> None:
    assert JsltTemplate.parse(template).transform(IN_SRC) == expected


@pytest.mark.parametrize(
    "template",
    [
        '{ "r": $.a[?(@.x contains 1)] }',
        '{ "r": $.a[?(@.x nin [1])] }',
        '{ "r": $.a[?(@.x subsetof [1])] }',
    ],
)
def test_unsupported_set_operators_raise(template: str) -> None:
    # Non implémentés côté .NET non plus : NotImplementedError explicite.
    with pytest.raises(NotImplementedError):
        JsltTemplate.parse(template)


# --- fonctions de chemin (length, value) ----------------------------------
PATH_FUNCTION_CASES = [
    pytest.param('{ "r": $.tags.length() }', {"tags": ["a", "b", "c"]}, 3, id="length-tableau"),
    pytest.param('{ "r": $.obj.length() }', {"obj": {"a": 1, "b": 2}}, 2, id="length-objet"),
    pytest.param('{ "r": $.s.length() }', {"s": "hello"}, 5, id="length-chaine"),
    pytest.param('{ "r": $.n.length() }', {"n": 5}, None, id="length-non-collection"),
    pytest.param('{ "r": $.v.value() }', {"v": 42}, 42, id="value-identite"),
    pytest.param(
        '{ "r": $.items[?(@.tags.length() > 1)] }',
        {"items": [{"tags": ["x"]}, {"tags": ["y", "z"]}]},
        {"r": {"tags": ["y", "z"]}}["r"],
        id="length-dans-filtre",
    ),
]


@pytest.mark.parametrize("template, source, expected", PATH_FUNCTION_CASES)
def test_path_functions(template: str, source, expected) -> None:
    assert JsltTemplate.parse(template).transform(source) == {"r": expected}


@pytest.mark.parametrize(
    "template",
    [
        '{ "r": $.a.size() }',  # size n'existe pas côté .NET
        '{ "r": $.a.count() }',
        '{ "r": $.a.match("x") }',
    ],
)
def test_unsupported_path_functions_raise(template: str) -> None:
    with pytest.raises(NotImplementedError):
        JsltTemplate.parse(template)
