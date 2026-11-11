"""Structures profondes — catégorie « structures profondes ».

On pouvait lire profond (`$..k`) et construire plat ; on ne pouvait pas
**transformer** en profondeur : ni aplatir vers des clés pointées (le pont vers
un CSV), ni appliquer une règle à chaque nœud, ni poser une valeur au bout d'un
chemin sans réécrire tout l'objet à la main.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


# --- flattenobject / unflatten ------------------------------------------------


def test_flattenobject_clefs_pointees():
    source = {"o": {"a": {"b": 1}, "c": 2}}
    assert run('{ "r": flattenobject($.o) }', source) == {"r": {"a.b": 1, "c": 2}}


def test_flattenobject_indexe_les_tableaux():
    source = {"o": {"l": [{"v": 1}, {"v": 2}]}}
    assert run('{ "r": flattenobject($.o) }', source) == {"r": {"l.0.v": 1, "l.1.v": 2}}


def test_flattenobject_separateur_personnalise():
    source = {"o": {"a": {"b": 1}}}
    assert run('{ "r": flattenobject($.o, "/") }', source) == {"r": {"a/b": 1}}


def test_flattenobject_conserve_les_conteneurs_vides():
    # Sans cela, une clé dont la valeur est {} disparaîtrait de l'aplati, et
    # l'aller-retour perdrait de l'information.
    source = {"o": {"a": {}, "b": [], "c": 1}}
    assert run('{ "r": flattenobject($.o) }', source) == {"r": {"a": {}, "b": [], "c": 1}}


def test_unflatten_reconstruit_les_objets():
    source = {"o": {"a.b": 1, "c": 2}}
    assert run('{ "r": unflatten($.o) }', source) == {"r": {"a": {"b": 1}, "c": 2}}


def test_unflatten_ne_fabrique_pas_de_tableau_par_defaut():
    # Une clé « 2026 » est un nom d'année dans bien des documents : en faire un
    # indice créerait un tableau de 2027 trous.
    source = {"o": {"ventes.2026": 1}}
    assert run('{ "r": unflatten($.o) }', source) == {"r": {"ventes": {"2026": 1}}}


def test_unflatten_reconstruit_les_tableaux_sur_demande():
    source = {"o": {"l.0.v": 1, "l.1.v": 2}}
    assert run('{ "r": unflatten($.o, ".", true) }', source) == {
        "r": {"l": [{"v": 1}, {"v": 2}]}
    }


def test_aller_retour_complet_avec_les_tableaux():
    source = {"o": {"a": {"b": [1, {"c": 2}]}, "d": 3}}
    template = '{ "r": unflatten(flattenobject($.o), ".", true) }'
    assert run(template, source) == {"r": source["o"]}


def test_unflatten_conflit_de_chemin_leve():
    # « a » ne peut pas être à la fois 1 et un objet portant « b ».
    with pytest.raises(JsltError, match="conflit"):
        run('{ "r": unflatten($.o) }', {"o": {"a": 1, "a.b": 2}})


# --- walk / prune -------------------------------------------------------------


def test_walk_applique_une_regle_a_chaque_noeud():
    source = {"o": {"a": " x ", "l": ["  y", {"b": "z  "}]}}
    template = '{ "r": walk($.o, when(isstring($)) { "true": trim($), "default": $ }) }'
    assert run(template, source) == {"r": {"a": "x", "l": ["y", {"b": "z"}]}}


def test_walk_voit_les_enfants_avant_les_parents():
    # Remontée : les feuilles sont transformées, puis leurs conteneurs.
    source = {"o": {"l": [1, 2]}}
    template = '{ "r": walk($.o, when(isnumber($)) { "true": $ + 1, "default": $ }) }'
    assert run(template, source) == {"r": {"l": [2, 3]}}


def test_walk_sur_un_scalaire_le_transforme_aussi():
    assert run('{ "r": walk($.v, $ * 2) }', {"v": 3}) == {"r": 6}


def test_prune_retire_les_nulls_en_profondeur():
    source = {"o": {"a": None, "b": {"c": None, "d": 1}, "l": [1, None, 2]}}
    assert run('{ "r": prune($.o) }', source) == {"r": {"b": {"d": 1}, "l": [1, 2]}}


def test_prune_garde_les_valeurs_vides_par_defaut():
    source = {"o": {"a": "", "b": [], "c": {}, "d": 0, "e": False}}
    assert run('{ "r": prune($.o) }', source) == {"r": {"a": "", "b": [], "c": {}, "d": 0, "e": False}}


def test_prune_retire_aussi_le_vide_sur_demande():
    source = {"o": {"a": "", "b": [], "c": {}, "d": 0}}
    # 0 et false ne sont pas « vides » : ce sont des valeurs.
    assert run('{ "r": prune($.o, "empty") }', source) == {"r": {"d": 0}}


def test_prune_option_inconnue_leve():
    with pytest.raises(JsltError, match="option"):
        run('{ "r": prune($.o, "zzz") }', {"o": {}})


# --- setpath / unsetpath ------------------------------------------------------


def test_setpath_pose_une_valeur_au_bout_d_un_chemin():
    source = {"o": {"a": {"b": 1}}}
    assert run('{ "r": setpath($.o, "a.c", 2) }', source) == {"r": {"a": {"b": 1, "c": 2}}}


def test_setpath_cree_les_niveaux_manquants():
    assert run('{ "r": setpath($.o, "a.b.c", 1) }', {"o": {}}) == {"r": {"a": {"b": {"c": 1}}}}


def test_setpath_ne_modifie_pas_la_source():
    template = '{ "modifie": setpath($.o, "a", 2), "origine": $.o }'
    assert run(template, {"o": {"a": 1}}) == {"modifie": {"a": 2}, "origine": {"a": 1}}


def test_setpath_traverse_un_tableau_par_indice():
    source = {"o": {"l": [{"v": 1}, {"v": 2}]}}
    assert run('{ "r": setpath($.o, "l.1.v", 9) }', source) == {
        "r": {"l": [{"v": 1}, {"v": 9}]}
    }


def test_setpath_refuse_de_traverser_un_scalaire():
    with pytest.raises(JsltError, match="conflit"):
        run('{ "r": setpath($.o, "a.b", 1) }', {"o": {"a": 1}})


def test_unsetpath():
    source = {"o": {"a": {"b": 1, "c": 2}}}
    assert run('{ "r": unsetpath($.o, "a.b") }', source) == {"r": {"a": {"c": 2}}}


def test_unsetpath_chemin_absent_rend_l_objet_tel_quel():
    assert run('{ "r": unsetpath($.o, "zz.yy") }', {"o": {"a": 1}}) == {"r": {"a": 1}}


def test_unsetpath_retire_un_element_de_tableau():
    source = {"o": {"l": [1, 2, 3]}}
    assert run('{ "r": unsetpath($.o, "l.1") }', source) == {"r": {"l": [1, 3]}}


# --- merge des tableaux -------------------------------------------------------


def test_merge_profond_concatene_les_tableaux_sur_demande():
    source = {"a": {"l": [1]}, "b": {"l": [2]}}
    assert run('{ "r": merge($.a, $.b, true, true) }', source) == {"r": {"l": [1, 2]}}


def test_merge_profond_remplace_les_tableaux_par_defaut():
    source = {"a": {"l": [1]}, "b": {"l": [2]}}
    assert run('{ "r": merge($.a, $.b, true) }', source) == {"r": {"l": [2]}}


# --- conventions --------------------------------------------------------------


@pytest.mark.parametrize(
    "call",
    ['flattenobject($.x)', 'unflatten($.x)', 'setpath($.x, "a", 1)', 'unsetpath($.x, "a")'],
)
def test_non_objet_et_null(call):
    assert run('{ "r": ' + call + ' }', {"x": None}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"x": 42}) == {"r": None}


def test_exemple_complet_vers_un_tableau_plat():
    template = '{ "lignes": [ { "$source": $.clients, "p": flattenobject($) } ] }'
    source = {"clients": [{"id": 1, "adr": {"ville": "Lyon"}}]}
    assert run(template, source) == {"lignes": [{"p": {"id": 1, "adr.ville": "Lyon"}}]}
