"""Agrégats (`count`, `avg`, `median`, `product`, `min`/`max` sur tableau).

Sujet « agrégations ». `sum` existait seul ; `min`/`max` étaient **binaires**
(deux nombres), ce qui interdisait « le plus petit de la liste ».
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


@pytest.mark.parametrize(
    "value, expected",
    [
        ([1, 2, 3], 3),
        ([], 0),
        ({"a": 1, "b": 2}, 2),      # un objet : son nombre de clés
        ("abc", 3),                  # une chaîne : ses caractères
        (None, 0),
        (42, 1),                     # un scalaire : un élément
        (True, 1),
    ],
)
def test_count(value, expected):
    assert run('{ "r": count($.v) }', {"v": value}) == {"r": expected}


def test_avg():
    assert run('{ "r": avg($.n) }', {"n": [1, 2, 3, 4]}) == {"r": 2.5}


def test_avg_tableau_vide_rend_null():
    # La moyenne de rien n'est pas 0 : la rendre nulle dit « pas de réponse ».
    assert run('{ "r": avg($.n) }', {"n": []}) == {"r": None}


def test_median_impair_et_pair():
    assert run('{ "r": median($.n) }', {"n": [3, 1, 2]}) == {"r": 2}
    assert run('{ "r": median($.n) }', {"n": [4, 1, 3, 2]}) == {"r": 2.5}


def test_median_tableau_vide_rend_null():
    assert run('{ "r": median($.n) }', {"n": []}) == {"r": None}


def test_product():
    assert run('{ "r": product($.n) }', {"n": [2, 3, 4]}) == {"r": 24}


def test_product_tableau_vide_rend_un():
    # Élément neutre de la multiplication, comme sum([]) vaut 0.
    assert run('{ "r": product($.n) }', {"n": []}) == {"r": 1}


def test_entiers_preserves():
    assert run('{ "a": product($.n), "b": median($.n) }', {"n": [2, 4]}) == {"a": 8, "b": 3.0}


@pytest.mark.parametrize("call", ["avg($.n)", "median($.n)", "product($.n)"])
def test_agregats_refusent_un_element_non_numerique(call):
    # Même refus que `sum` : un agrégat qui ignore en silence les intrus fait
    # découvrir le problème de données très loin de sa cause.
    with pytest.raises(JsltError):
        run('{ "r": ' + call + ' }', {"n": [1, "x"]})


@pytest.mark.parametrize("call", ["avg($.n)", "median($.n)", "product($.n)", "count($.n)"])
def test_agregats_sur_null(call):
    expected = 0 if call.startswith("count") else None
    assert run('{ "r": ' + call + ' }', {}) == {"r": expected}


def test_min_et_max_sur_un_tableau():
    source = {"n": [3, 1, 2]}
    assert run('{ "a": min($.n), "b": max($.n) }', source) == {"a": 1, "b": 3}


def test_min_et_max_binaires_inchanges():
    # Comportement .NET conservé : deux arguments, résultat décimal.
    assert run('{ "a": min($.a, $.b), "b": max($.a, $.b) }', {"a": 2, "b": 5}) == {
        "a": 2.0, "b": 5.0
    }


def test_min_sur_tableau_vide_rend_null():
    assert run('{ "r": min($.n) }', {"n": []}) == {"r": None}


def test_min_refuse_un_tableau_avec_un_second_argument():
    # Sinon le second argument serait ignoré en silence.
    with pytest.raises(JsltError, match="tableau"):
        run('{ "r": min($.n, 2) }', {"n": [1, 3]})


def test_exemple_complet_statistiques():
    template = (
        '{ "n": count($.v), "total": sum($.v), "moyenne": avg($.v), '
        '"mini": min($.v), "maxi": max($.v) }'
    )
    assert run(template, {"v": [10, 20, 30]}) == {
        "n": 3, "total": 60, "moyenne": 20.0, "mini": 10, "maxi": 30
    }
