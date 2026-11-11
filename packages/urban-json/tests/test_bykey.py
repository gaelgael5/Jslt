"""Agrégation par clef calculée — catégorie « tri et regroupement ».

`groupby` savait regrouper mais pas imbriquer : une clef composite devenait une
clef **textuelle** (`["FR","Lyon"]`) qu'il fallait re-analyser pour s'en servir.
Et sommer par groupe demandait trois fonctions (`entries`, `selectmany`, `sum`)
là où c'est l'usage le plus fréquent.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


VENTES = {
    "l": [
        {"pays": "FR", "ville": "Lyon", "m": 10},
        {"pays": "FR", "ville": "Nice", "m": 20},
        {"pays": "FR", "ville": "Lyon", "m": 5},
        {"pays": "BE", "ville": "Gand", "m": 7},
    ]
}


# --- groupby imbriqué ---------------------------------------------------------


def test_groupby_imbrique_un_niveau_par_clef():
    template = '{ "r": groupby($.l, [$.pays, $.ville], true) }'
    resultat = run(template, VENTES)["r"]
    assert sorted(resultat) == ["BE", "FR"]
    assert sorted(resultat["FR"]) == ["Lyon", "Nice"]
    assert resultat["FR"]["Lyon"] == [
        {"pays": "FR", "ville": "Lyon", "m": 10},
        {"pays": "FR", "ville": "Lyon", "m": 5},
    ]
    assert resultat["BE"]["Gand"] == [{"pays": "BE", "ville": "Gand", "m": 7}]


def test_groupby_imbrique_est_interrogeable_par_chemin():
    # L'intérêt de l'imbrication : le résultat se relit comme un document.
    template = '{ "r": count(select(groupby($.l, [$.pays, $.ville], true), $.FR.Lyon)) }'
    assert run(template, VENTES) == {"r": 2}


def test_groupby_imbrique_une_seule_clef_fait_un_niveau():
    template = '{ "r": groupby($.l, [$.pays], true) }'
    resultat = run(template, VENTES)["r"]
    assert sorted(resultat) == ["BE", "FR"]
    assert len(resultat["FR"]) == 3


def test_groupby_plat_inchange():
    # Régression : sans le 3e argument, la forme plate d'avant.
    template = '{ "r": countby($.l, $.pays) }'
    assert run(template, VENTES) == {"r": {"FR": 3, "BE": 1}}


def test_groupby_imbrique_exige_un_tableau_de_clefs():
    with pytest.raises(JsltError, match="tableau de clefs"):
        run('{ "r": groupby($.l, $.pays, true) }', VENTES)


def test_groupby_imbrique_refuse_un_tableau_de_clefs_vide():
    with pytest.raises(JsltError, match="tableau de clefs"):
        run('{ "r": groupby($.l, [], true) }', VENTES)


def test_groupby_imbrique_profondeurs_incompatibles_leve():
    # Un élément range au niveau 1, l'autre au niveau 2 : la même clef porterait
    # à la fois des éléments et un sous-groupe.
    source = {"l": [{"a": "x"}, {"a": "x", "b": "y"}]}
    template = (
        '{ "r": groupby($.l, when($.b) { "y": [$.a, $.b], "default": [$.a] }, true) }'
    )
    with pytest.raises(JsltError, match="profondeur"):
        run(template, source)


def test_groupby_d_un_non_tableau_rend_null():
    assert run('{ "r": groupby($.l, $.a, true) }', {"l": "texte"}) == {"r": None}


# --- sumby / avgby ------------------------------------------------------------


def test_sumby_somme_par_groupe_en_un_appel():
    assert run('{ "r": sumby($.l, $.pays, $.m) }', VENTES) == {"r": {"FR": 35, "BE": 7}}


def test_sumby_vaut_la_composition_de_groupby_et_sum():
    long = (
        '{ "r": fromentries([ { "$source": entries(groupby($.l, $.pays)), '
        '"key": $.key, "value": sum(selectmany($.value, $.*.m)) } ]) }'
    )
    court = '{ "r": sumby($.l, $.pays, $.m) }'
    assert run(court, VENTES) == run(long, VENTES)


def test_avgby_moyenne_par_groupe():
    assert run('{ "r": avgby($.l, $.pays, $.m) }', VENTES) == {"r": {"FR": 35 / 3, "BE": 7.0}}


def test_sumby_sans_expression_de_valeur_somme_les_elements():
    # Argument paresseux omis = l'élément (convention de `sort`, `distinctby`) :
    # un tableau de nombres s'agrège donc par une clef calculée, sans 3e argument.
    source = {"n": [1, 2, 3, 10]}
    assert run('{ "r": sumby($.n, "tout") }', source) == {"r": {"tout": 16}}


def test_sumby_clef_composite_rend_du_json_lisible():
    # La clef textuelle passe par le JSON compact, pas par du `repr` Python.
    template = '{ "r": sumby($.l, [$.pays, $.ville], $.m) }'
    assert run(template, VENTES)["r"]['["BE","Gand"]'] == 7


@pytest.mark.parametrize("call", ["sumby($.l, $.pays, $.ville)", "avgby($.l, $.pays, $.ville)"])
def test_agregat_par_groupe_refuse_une_valeur_non_numerique(call):
    # Même refus que `sum` : sauter l'intrus rendrait un total plausible et faux.
    with pytest.raises(JsltError, match="nombre"):
        run('{ "r": ' + call + " }", VENTES)


@pytest.mark.parametrize("call", ["sumby($.l, $, $)", "avgby($.l, $, $)"])
def test_agregat_par_groupe_d_un_non_tableau_rend_null(call):
    assert run('{ "r": ' + call + " }", {"l": 3}) == {"r": None}


@pytest.mark.parametrize("call", ["sumby($.l, $, $)", "avgby($.l, $, $)"])
def test_agregat_par_groupe_d_un_tableau_vide_rend_un_objet_vide(call):
    assert run('{ "r": ' + call + " }", {"l": []}) == {"r": {}}
