"""Statistiques et agrégation par groupe — catégorie « statistiques ».

Le descriptif de base existait (`count`, `sum`, `avg`, `median`, `product`,
`min`, `max`) ; la dispersion et les quantiles manquaient, et `group` rendait
des sous-tableaux sans jamais pouvoir les réduire en une passe.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


# --- dispersion ---------------------------------------------------------------


def test_variance_et_stddev_de_population():
    # [2,4,4,4,5,5,7,9] : moyenne 5, variance 4, écart-type 2.
    source = {"v": [2, 4, 4, 4, 5, 5, 7, 9]}
    assert run('{ "var": variance($.v), "sd": stddev($.v) }', source) == {"var": 4.0, "sd": 2.0}


def test_variance_d_echantillon():
    source = {"v": [2, 4, 4, 4, 5, 5, 7, 9]}
    # Correction de Bessel : n-1 au dénominateur.
    assert run('{ "r": variance($.v, true) }', source) == {"r": 32 / 7}


def test_stddev_d_un_seul_element():
    # Population : la dispersion d'une valeur unique est nulle.
    assert run('{ "r": stddev($.v) }', {"v": [5]}) == {"r": 0.0}


def test_variance_d_echantillon_d_un_seul_element_rend_null():
    # n-1 = 0 : la question n'a pas de réponse, on le dit.
    assert run('{ "r": variance($.v, true) }', {"v": [5]}) == {"r": None}


@pytest.mark.parametrize("call", ["variance($.v)", "stddev($.v)", "percentile($.v, 50)"])
def test_tableau_vide_rend_null(call):
    assert run('{ "r": ' + call + ' }', {"v": []}) == {"r": None}


@pytest.mark.parametrize("call", ["variance($.v)", "stddev($.v)", "percentile($.v, 50)"])
def test_element_non_numerique_leve(call):
    with pytest.raises(JsltError):
        run('{ "r": ' + call + ' }', {"v": [1, "x"]})


# --- quantiles ----------------------------------------------------------------


@pytest.mark.parametrize(
    "p, expected",
    [(0, 1), (50, 3), (100, 5), (25, 2), (75, 4), (10, 1.4)],
)
def test_percentile_interpolation_lineaire(p, expected):
    source = {"v": [1, 2, 3, 4, 5]}
    assert run('{ "r": percentile($.v, ' + str(p) + ") }", source) == {"r": expected}


def test_percentile_median_coincide_avec_median():
    source = {"v": [4, 1, 3, 2]}
    assert run('{ "a": percentile($.v, 50), "b": median($.v) }', source) == {"a": 2.5, "b": 2.5}


@pytest.mark.parametrize("p", [-1, 101])
def test_percentile_hors_bornes_leve(p):
    with pytest.raises(JsltError, match="centile"):
        run('{ "r": percentile($.v, ' + str(p) + ") }", {"v": [1, 2]})


# --- mode ---------------------------------------------------------------------


def test_mode_valeur_la_plus_frequente():
    assert run('{ "r": mode($.v) }', {"v": [1, 2, 2, 3]}) == {"r": 2}


def test_mode_fonctionne_sur_des_textes():
    # Contrairement aux autres agrégats : la valeur modale d'un libellé a un sens.
    assert run('{ "r": mode($.v) }', {"v": ["b", "a", "b"]}) == {"r": "b"}


def test_mode_egalite_le_premier_apparu_gagne():
    assert run('{ "r": mode($.v) }', {"v": ["z", "a", "a", "z"]}) == {"r": "z"}


def test_mode_tableau_vide_rend_null():
    assert run('{ "r": mode($.v) }', {"v": []}) == {"r": None}


# --- agrégation par groupe ----------------------------------------------------


def test_groupby_rend_un_objet_de_sous_tableaux():
    source = {"l": [
        {"ville": "Lyon", "m": 10},
        {"ville": "Nice", "m": 20},
        {"ville": "Lyon", "m": 5},
    ]}
    assert run('{ "r": groupby($.l, $.ville) }', source) == {
        "r": {
            "Lyon": [{"ville": "Lyon", "m": 10}, {"ville": "Lyon", "m": 5}],
            "Nice": [{"ville": "Nice", "m": 20}],
        }
    }


def test_groupby_clef_non_textuelle_devient_du_texte():
    # Une clé d'objet JSON est forcément une chaîne.
    source = {"l": [{"an": 2026}, {"an": 2026}]}
    assert run('{ "r": groupby($.l, $.an) }', source) == {"r": {"2026": [{"an": 2026}, {"an": 2026}]}}


def test_countby_compte_par_groupe():
    source = {"l": [{"t": "a"}, {"t": "b"}, {"t": "a"}]}
    assert run('{ "r": countby($.l, $.t) }', source) == {"r": {"a": 2, "b": 1}}


def test_groupby_puis_somme_par_groupe():
    # L'agrégation par groupe, en une expression.
    template = (
        '{ "totaux": fromentries([ { "$source": entries(groupby($.l, $.ville)), '
        '"key": $.key, "value": sum(selectmany($.value, $.*.m)) } ]) }'
    )
    source = {"l": [
        {"ville": "Lyon", "m": 10},
        {"ville": "Nice", "m": 20},
        {"ville": "Lyon", "m": 5},
    ]}
    assert run(template, source) == {"totaux": {"Lyon": 15, "Nice": 20}}


@pytest.mark.parametrize("call", ["groupby($.x, $)", "countby($.x, $)", "mode($.x)"])
def test_non_tableau_et_null(call):
    assert run('{ "r": ' + call + ' }', {"x": None}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"x": 42}) == {"r": None}
