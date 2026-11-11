"""Parcours et découpage de tableaux — catégorie « collections ».

`limit` était un `take` sans son complément, `indexof` ne savait chercher que
dans une chaîne, et `union` n'aplatissait qu'un niveau.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


# --- skip ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "n, expected",
    [(0, [1, 2, 3]), (1, [2, 3]), (3, []), (9, []), (-2, [1, 2, 3])],
)
def test_skip(n, expected):
    assert run('{ "r": skip($.l, ' + str(n) + ") }", {"l": [1, 2, 3]}) == {"r": expected}


def test_skip_et_limit_font_une_page():
    template = '{ "page": limit(skip($.l, 2), 2) }'
    assert run(template, {"l": [1, 2, 3, 4, 5]}) == {"page": [3, 4]}


# --- indexof / lastindexof sur un tableau -------------------------------------


def test_indexof_dans_un_tableau():
    source = {"l": ["a", "b", "a"]}
    assert run('{ "a": indexof($.l, "b"), "b": lastindexof($.l, "a") }', source) == {
        "a": 1, "b": 2
    }


def test_indexof_absent_rend_moins_un():
    assert run('{ "r": indexof($.l, "zz") }', {"l": ["a"]}) == {"r": -1}


def test_indexof_dans_un_tableau_d_objets():
    source = {"l": [{"k": 1}, {"k": 2}]}
    assert run('{ "r": indexof($.l, { "k": 2 }) }', source) == {"r": 1}


def test_indexof_sur_une_chaine_inchange():
    assert run('{ "r": indexof($.t, "ri") }', {"t": "Paris"}) == {"r": 2}


# --- flatten ------------------------------------------------------------------


def test_flatten_descend_a_fond_par_defaut():
    source = {"l": [1, [2, [3, [4]]]]}
    assert run('{ "r": flatten($.l) }', source) == {"r": [1, 2, 3, 4]}


def test_flatten_profondeur_limitee():
    source = {"l": [1, [2, [3, [4]]]]}
    assert run('{ "r": flatten($.l, 1) }', source) == {"r": [1, 2, [3, [4]]]}


def test_flatten_un_niveau_equivaut_a_union():
    source = {"l": [[1, 2], [3]]}
    assert run('{ "a": flatten($.l, 1), "b": union($.l) }', source) == {
        "a": [1, 2, 3], "b": [1, 2, 3]
    }


def test_flatten_profondeur_invalide_leve():
    with pytest.raises(JsltError, match="profondeur"):
        run('{ "r": flatten($.l, -1) }', {"l": [1]})


# --- zip / chunk / window -----------------------------------------------------


def test_zip_apparie():
    source = {"a": [1, 2], "b": ["x", "y"]}
    assert run('{ "r": zip($.a, $.b) }', source) == {"r": [[1, "x"], [2, "y"]]}


def test_zip_s_arrete_au_plus_court():
    source = {"a": [1, 2, 3], "b": ["x"]}
    assert run('{ "r": zip($.a, $.b) }', source) == {"r": [[1, "x"]]}


def test_chunk():
    assert run('{ "r": chunk($.l, 2) }', {"l": [1, 2, 3, 4, 5]}) == {
        "r": [[1, 2], [3, 4], [5]]
    }


def test_window():
    assert run('{ "r": window($.l, 2) }', {"l": [1, 2, 3]}) == {"r": [[1, 2], [2, 3]]}


def test_window_plus_grande_que_le_tableau_rend_vide():
    assert run('{ "r": window($.l, 5) }', {"l": [1, 2]}) == {"r": []}


@pytest.mark.parametrize("call", ["chunk($.l, 0)", "window($.l, 0)", "chunk($.l, -1)"])
def test_taille_nulle_ou_negative_leve(call):
    with pytest.raises(JsltError, match="taille"):
        run('{ "r": ' + call + ' }', {"l": [1, 2]})


# --- partition / distinctby ---------------------------------------------------


def test_partition_separe_selon_un_predicat():
    source = {"l": [1, 2, 3, 4]}
    assert run('{ "r": partition($.l, $ > 2) }', source) == {
        "r": {"true": [3, 4], "false": [1, 2]}
    }


def test_partition_sur_un_champ():
    source = {"l": [{"ok": True}, {"ok": False}]}
    assert run('{ "r": partition($.l, $.ok) }', source) == {
        "r": {"true": [{"ok": True}], "false": [{"ok": False}]}
    }


def test_distinctby_garde_le_premier_de_chaque_clef():
    source = {"l": [{"k": 1, "v": "a"}, {"k": 2, "v": "b"}, {"k": 1, "v": "c"}]}
    assert run('{ "r": selectmany(distinctby($.l, $.k), $.*.v) }', source) == {
        "r": ["a", "b"]
    }


def test_distinctby_sans_clef_deduplique_les_valeurs():
    assert run('{ "r": distinctby($.l, $) }', {"l": [1, 1, 2]}) == {"r": [1, 2]}


def test_distinctby_distingue_les_objets_identiques_de_structure():
    source = {"l": [{"a": 1}, {"a": 1}, {"a": 2}]}
    assert run('{ "r": distinctby($.l, $) }', source) == {"r": [{"a": 1}, {"a": 2}]}


# --- intersect / difference ---------------------------------------------------


def test_intersect_et_difference():
    source = {"a": [1, 2, 3], "b": [2, 3, 4]}
    assert run('{ "i": intersect($.a, $.b), "d": difference($.a, $.b) }', source) == {
        "i": [2, 3], "d": [1]
    }


def test_intersect_conserve_l_ordre_de_gauche_et_deduplique():
    source = {"a": [3, 1, 3], "b": [1, 3]}
    assert run('{ "r": intersect($.a, $.b) }', source) == {"r": [3, 1]}


def test_operations_ensemblistes_comparent_la_structure():
    # Égalité structurelle, pas celle de `==` du langage (où "2" == 2) : sur un
    # ensemble, confondre 2 et "2" rendrait le résultat imprévisible.
    source = {"a": [2, "2"], "b": [2]}
    assert run('{ "r": intersect($.a, $.b) }', source) == {"r": [2]}


def test_intersect_sur_des_objets():
    source = {"a": [{"k": 1}, {"k": 2}], "b": [{"k": 2}]}
    assert run('{ "r": intersect($.a, $.b) }', source) == {"r": [{"k": 2}]}


# --- conventions --------------------------------------------------------------


@pytest.mark.parametrize(
    "call",
    ["skip($.x, 1)", "flatten($.x)", "chunk($.x, 2)", "window($.x, 2)",
     "zip($.x, $.x)", "distinctby($.x, $)", "intersect($.x, $.x)", "difference($.x, $.x)",
     "partition($.x, $)"],
)
def test_non_tableau_et_null(call):
    assert run('{ "r": ' + call + ' }', {"x": None}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"x": 42}) == {"r": None}


# --- unzip --------------------------------------------------------------------


def test_unzip_separe_les_paires():
    source = {"l": [[1, "a"], [2, "b"], [3, "c"]]}
    assert run('{ "r": unzip($.l) }', source) == {"r": [[1, 2, 3], ["a", "b", "c"]]}


def test_zip_puis_unzip_rend_les_deux_tableaux():
    source = {"a": [1, 2], "b": ["x", "y"]}
    assert run('{ "r": unzip(zip($.a, $.b)) }', source) == {"r": [[1, 2], ["x", "y"]]}


def test_unzip_s_arrete_a_la_rangee_la_plus_courte():
    # Symétrique de `zip`, qui s'arrête au plus court : pas de `null` inventé.
    source = {"l": [[1, "a", True], [2, "b"]]}
    assert run('{ "r": unzip($.l) }', source) == {"r": [[1, 2], ["a", "b"]]}


def test_unzip_d_un_tableau_vide():
    assert run('{ "r": unzip($.l) }', {"l": []}) == {"r": []}


def test_unzip_d_un_non_tableau_rend_null():
    assert run('{ "r": unzip($.l) }', {"l": "texte"}) == {"r": None}


def test_unzip_rangee_non_tableau_leve():
    with pytest.raises(JsltError, match="unzip"):
        run('{ "r": unzip($.l) }', {"l": [[1, 2], 3]})
