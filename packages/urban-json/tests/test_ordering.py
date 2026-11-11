"""Tri et ordre (`sort`, `reverse`, `first`, `last`) — sujet « tri et ordre ».

Sans contrepartie .NET. Le point délicat est l'ordre **total** : un tableau de
données réelles mélange les types, et un tri qui lève sur `None < str` serait
inutilisable. Ces tests fixent l'ordre entre types.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


def test_sort_de_scalaires():
    assert run('{ "r": sort($.n) }', {"n": [3, 1, 2]}) == {"r": [1, 2, 3]}


def test_sort_descendant():
    # Pour trier sur les éléments eux-mêmes en précisant le sens, la clef est
    # `$` : il n'y a pas de place-tenant « pas de clef ».
    assert run('{ "r": sort($.n, $, true) }', {"n": [3, 1, 2]}) == {"r": [3, 2, 1]}


def test_sort_par_chemin_applique_a_chaque_element():
    template = '{ "r": sort($.items, $.prix) }'
    source = {"items": [{"prix": 30}, {"prix": 10}, {"prix": 20}]}
    assert run(template, source) == {"r": [{"prix": 10}, {"prix": 20}, {"prix": 30}]}


def test_sort_par_chemin_descendant():
    template = '{ "r": selectmany(sort($.items, $.prix, true), $.*.prix) }'
    source = {"items": [{"prix": 30}, {"prix": 10}, {"prix": 20}]}
    assert run(template, source) == {"r": [30, 20, 10]}


def test_sort_element_sans_la_clef_passe_devant():
    # Clef absente = null, et null est le plus petit : les trous se regroupent
    # au début, là où on les voit, plutôt que de lever.
    template = '{ "r": selectmany(sort($.items, $.prix), $.*.id) }'
    source = {"items": [{"id": 1, "prix": 5}, {"id": 2}, {"id": 3, "prix": 1}]}
    assert run(template, source) == {"r": [2, 3, 1]}


def test_sort_est_stable():
    template = '{ "r": selectmany(sort($.items, $.k), $.*.id) }'
    source = {"items": [{"id": 1, "k": 1}, {"id": 2, "k": 1}, {"id": 3, "k": 0}]}
    assert run(template, source) == {"r": [3, 1, 2]}


def test_sort_ordre_total_entre_types():
    # null < booléens < nombres < chaînes < tableaux < objets.
    source = {"n": ["b", 2, None, True, {"o": 1}, [1], 1, "a", False]}
    assert run('{ "r": sort($.n) }', source) == {
        "r": [None, False, True, 1, 2, "a", "b", [1], {"o": 1}]
    }


def test_sort_chaines_par_points_de_code():
    # Pas de collation locale : « Zoé » avant « école ». Pour un tri humain,
    # trier sur une clef pliée (cf. foldtext).
    assert run('{ "r": sort($.n) }', {"n": ["école", "Zoé"]}) == {"r": ["Zoé", "école"]}


def test_sort_sur_clef_pliee_donne_l_ordre_humain():
    template = '{ "r": sort($.n, foldtext($)) }'
    assert run(template, {"n": ["école", "Zoé"]}) == {"r": ["école", "Zoé"]}


@pytest.mark.parametrize("call", ["sort($.x)", "reverse($.x)"])
def test_non_tableau_et_null(call):
    assert run('{ "r": ' + call + ' }', {"x": None}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"x": 42}) == {"r": None}


def test_sort_refuse_un_tri_descendant_non_booleen():
    with pytest.raises(JsltError, match="descending"):
        run('{ "r": sort($.n, $, "oui") }', {"n": [1]})


def test_sort_descendant_reste_stable():
    # À clefs égales, l'ordre d'origine survit dans les deux sens.
    template = '{ "r": selectmany(sort($.items, $.k, true), $.*.id) }'
    source = {"items": [{"id": 1, "k": 1}, {"id": 2, "k": 1}, {"id": 3, "k": 9}]}
    assert run(template, source) == {"r": [3, 1, 2]}


def test_reverse():
    assert run('{ "r": reverse($.n) }', {"n": [1, 2, 3]}) == {"r": [3, 2, 1]}


def test_reverse_ne_modifie_pas_la_source():
    template = '{ "inverse": reverse($.n), "origine": $.n }'
    assert run(template, {"n": [1, 2]}) == {"inverse": [2, 1], "origine": [1, 2]}


def test_first_et_last():
    assert run('{ "a": first($.n), "b": last($.n) }', {"n": [1, 2, 3]}) == {"a": 1, "b": 3}


def test_first_et_last_sur_tableau_vide_ou_null():
    assert run('{ "a": first($.n), "b": last($.n) }', {"n": []}) == {"a": None, "b": None}
    assert run('{ "a": first($.n), "b": last($.n) }', {}) == {"a": None, "b": None}


def test_first_et_last_sur_non_tableau():
    assert run('{ "a": first($.n), "b": last($.n) }', {"n": 42}) == {"a": None, "b": None}


def test_sort_puis_limit_donne_un_top_n():
    # Le cas qui motivait le sujet : « les 2 plus gros montants ».
    template = '{ "top": selectmany(limit(sort($.v, $, true), 2), $.*) }'
    assert run(template, {"v": [5, 50, 15, 2]}) == {"top": [50, 15]}
