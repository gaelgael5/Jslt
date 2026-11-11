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


# --- ordre des tableaux et des objets ----------------------------------------
# Régression : l'ordre total comparait tableaux et objets par leur **JSON
# compact**, donc par points de code. Un tri multi-clefs (clef = tableau de
# clefs, usage naturel puisque la clef est une expression) ordonnait alors
# « [10] » avant « [2] ». Comparaison élément par élément désormais.


def test_tri_multi_clefs_ordonne_les_nombres_numeriquement():
    template = '{ "r": selectmany(sort($.l, [$.a, $.b]), $.*.a) }'
    source = {"l": [{"a": 9, "b": 1}, {"a": 10, "b": 1}, {"a": 2, "b": 1}]}
    assert run(template, source) == {"r": [2, 9, 10]}


def test_tri_multi_clefs_departage_sur_la_seconde_clef():
    template = '{ "r": selectmany(sort($.l, [$.a, $.b]), $.*.id) }'
    source = {"l": [
        {"id": 1, "a": 1, "b": 20},
        {"id": 2, "a": 1, "b": 3},
        {"id": 3, "a": 0, "b": 99},
    ]}
    assert run(template, source) == {"r": [3, 2, 1]}


def test_tableaux_compares_element_par_element():
    source = {"n": [[2], [10], [1, 1], [1], []]}
    assert run('{ "r": sort($.n) }', source) == {"r": [[], [1], [1, 1], [2], [10]]}


def test_tableaux_de_types_differents_restent_comparables():
    # Le rang du premier élément départage, sans jamais lever.
    source = {"n": [["b"], [2], [None], [True]]}
    assert run('{ "r": sort($.n) }', source) == {"r": [[None], [True], [2], ["b"]]}


def test_objets_compares_par_clefs_puis_valeurs():
    source = {"n": [{"a": 10}, {"a": 2}, {"a": 2, "b": 1}, {"b": 0}]}
    assert run('{ "r": sort($.n) }', source) == {
        "r": [{"a": 2}, {"a": 2, "b": 1}, {"a": 10}, {"b": 0}]
    }


def test_tri_imbrique_profondement_ne_leve_pas():
    source = {"n": [{"a": [{"b": [2]}]}, {"a": [{"b": [10]}]}]}
    assert run('{ "r": sort($.n) }', source) == {
        "r": [{"a": [{"b": [2]}]}, {"a": [{"b": [10]}]}]
    }


# --- sens de tri par clef (catégorie « tri et regroupement ») ------------------


def test_sort_un_sens_par_clef():
    # Ville croissante, montant décroissant : impossible avec un seul `reverse`.
    source = {
        "l": [
            {"id": 1, "ville": "Lyon", "montant": 20},
            {"id": 2, "ville": "Brest", "montant": 9},
            {"id": 3, "ville": "Lyon", "montant": 50},
        ]
    }
    template = '{ "r": selectmany(sort($.l, [$.ville, $.montant], [false, true]), $.*.id) }'
    assert run(template, source) == {"r": [2, 3, 1]}


def test_sort_tous_les_sens_descendants_vaut_le_booleen():
    source = {"l": [{"a": 1}, {"a": 3}, {"a": 2}]}
    par_liste = run('{ "r": selectmany(sort($.l, [$.a], [true]), $.*.a) }', source)
    par_booleen = run('{ "r": selectmany(sort($.l, $.a, true), $.*.a) }', source)
    assert par_liste == par_booleen == {"r": [3, 2, 1]}


def test_sort_sens_manquant_est_croissant():
    # Deux clefs, un seul sens donné : la seconde reste croissante.
    source = {"l": [{"a": 1, "b": 2}, {"a": 1, "b": 1}, {"a": 2, "b": 9}]}
    template = '{ "r": selectmany(sort($.l, [$.a, $.b], [true]), $.*.b) }'
    assert run(template, source) == {"r": [9, 1, 2]}


def test_sort_par_sens_reste_stable():
    source = {"l": [{"a": 1, "i": 1}, {"a": 1, "i": 2}, {"a": 1, "i": 3}]}
    template = '{ "r": selectmany(sort($.l, [$.a], [true]), $.*.i) }'
    assert run(template, source) == {"r": [1, 2, 3]}


def test_sort_sens_non_booleen_leve():
    with pytest.raises(JsltError, match="sens de tri"):
        run('{ "r": sort($.l, [$.a], ["oui"]) }', {"l": [{"a": 1}]})


def test_sort_plus_de_sens_que_de_clefs_leve():
    # La faute d'écriture la plus probable : un sens de trop passerait inaperçu.
    with pytest.raises(JsltError, match="sens de tri"):
        run('{ "r": sort($.l, [$.a], [true, false]) }', {"l": [{"a": 1}]})


def test_sort_sens_par_clef_exige_une_clef_en_tableau():
    with pytest.raises(JsltError, match="tableau"):
        run('{ "r": sort($.l, $.a, [true]) }', {"l": [{"a": 1}]})


def test_sort_sens_par_clef_ordonne_aussi_les_textes():
    source = {"l": [{"n": "b"}, {"n": "a"}, {"n": "c"}]}
    template = '{ "r": selectmany(sort($.l, [$.n], [true]), $.*.n) }'
    assert run(template, source) == {"r": ["c", "b", "a"]}
