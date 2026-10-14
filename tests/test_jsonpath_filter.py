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
