"""Accès par clef **calculée** — sujet 2.

`$.o[$.k]` lève (« sélecteur de chemin non pris en charge ») et `select` n'accepte
qu'un chemin littéral : lire une clef venue des données demandait un détour par
`entries` + `filter` + une variable. Les tests du détour restent ailleurs ; ici on
éprouve son remplaçant, et surtout ses bords (clef absente, hors bornes, source
qui n'est pas un conteneur).
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


S = {
    "o": {"a": 2, "b": 3, "nul": None},
    "k": "b",
    "l": [10, 20, 30],
    "deep": {"client": {"ville": "Lyon", "lignes": [{"ref": "X1"}]}},
    "champ": "client.ville",
}


# --- get ------------------------------------------------------------------------


def test_get_lit_une_clef_calculee() -> None:
    assert run('{ "r": get($.o, $.k) }', S) == {"r": 3}


def test_get_lit_un_indice_de_tableau() -> None:
    assert run('{ "r": get($.l, 1) }', S) == {"r": 20}


def test_get_accepte_un_indice_negatif_depuis_la_fin() -> None:
    assert run('{ "r": get($.l, -1) }', S) == {"r": 30}


def test_get_hors_bornes_rend_null() -> None:
    assert run('{ "a": get($.l, 9), "b": get($.l, -9) }', S) == {"a": None, "b": None}


def test_get_clef_absente_rend_null() -> None:
    assert run('{ "r": get($.o, "zz") }', S) == {"r": None}


def test_get_distingue_la_clef_absente_par_has() -> None:
    """`get` rend `null` dans les deux cas ; c'est `has` qui tranche, et c'est
    pour ça que `get` n'a pas besoin d'un argument de repli."""
    assert run('{ "v": get($.o, "nul"), "presente": has($.o, "nul") }', S) == {"v": None, "presente": True}


def test_get_sur_un_scalaire_ou_null_rend_null() -> None:
    """Convention de la famille des objets : ni objet ni tableau -> `null`."""
    assert run('{ "a": get($.t, "x"), "b": get($.absent, "x") }', {"t": "texte"}) == {"a": None, "b": None}


def test_get_clef_textuelle_sur_un_tableau_rend_null() -> None:
    assert run('{ "r": get($.l, "a") }', S) == {"r": None}


def test_get_convertit_une_clef_numerique_en_texte_pour_un_objet() -> None:
    assert run('{ "r": get($.o, 1) }', {"o": {"1": "un"}}) == {"r": "un"}


def test_get_se_replie_par_la_coalescence() -> None:
    assert run('{ "r": get($.o, "zz") ?? "inconnu" }', S) == {"r": "inconnu"}


def test_get_exige_la_valeur_par_require() -> None:
    with pytest.raises(JsltError, match="tarif inconnu"):
        run('{ "r": require(get($.o, "zz"), "tarif inconnu") }', S)


def test_get_remplace_le_detour_par_entries() -> None:
    """Le contournement et la fonction doivent dire la même chose."""
    detour = '{ "k:": $.k, "r": first(map(filter(entries($.o), $.key == k:), $.value)) }'
    assert run(detour, S) == run('{ "r": get($.o, $.k) }', S)


# --- getpath --------------------------------------------------------------------


def test_getpath_descend_un_chemin_calcule() -> None:
    assert run('{ "r": getpath($.deep, $.champ) }', S) == {"r": "Lyon"}


def test_getpath_etape_manquante_rend_null() -> None:
    assert run('{ "r": getpath($.deep, "client.pays") }', S) == {"r": None}


def test_getpath_traverse_un_indice_de_tableau() -> None:
    assert run('{ "r": getpath($.deep, "client.lignes.0.ref") }', S) == {"r": "X1"}


def test_getpath_s_arrete_sur_un_scalaire_intermediaire() -> None:
    assert run('{ "r": getpath($.deep, "client.ville.pays") }', S) == {"r": None}


def test_getpath_accepte_un_autre_separateur() -> None:
    assert run('{ "r": getpath($.deep, "client/ville", "/") }', S) == {"r": "Lyon"}


def test_getpath_separateur_vide_leve() -> None:
    with pytest.raises(JsltError, match="séparateur de chemin vide"):
        run('{ "r": getpath($.deep, "client.ville", "") }', S)


def test_getpath_sur_un_scalaire_rend_null() -> None:
    assert run('{ "r": getpath($.t, "a.b") }', {"t": "texte"}) == {"r": None}


def test_getpath_est_la_reciproque_de_setpath() -> None:
    template = '{ "r": getpath(setpath($.o, "x.y", 7), "x.y") }'
    assert run(template, {"o": {}}) == {"r": 7}
