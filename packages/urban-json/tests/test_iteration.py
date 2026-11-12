"""Parcours d'un tableau par expression — sujet « boîte à outils des tableaux ».

Le moteur savait trier, grouper et agréger, mais pas **parcourir** : pas de
`map`, pas de `filter`, et surtout pas de `reduce`, qui n'avait aucun équivalent.
La boucle `{"$source": …}` fait l'office de `map` mais seulement en position de
valeur — jamais en argument d'une fonction.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


def run_compiled(template: str, source=None):
    return JsltTemplate.parse(template).build().transform(source)


GENS = {"l": [{"n": "Ana", "age": 30, "ok": True}, {"n": "Bo", "age": 25, "ok": False}]}
NOMBRES = {"l": [1, 2, 3, 4]}


# --- map / filter ---------------------------------------------------------------


@pytest.mark.parametrize("moteur", [run, run_compiled])
def test_map_applique_une_expression_par_element(moteur) -> None:
    assert moteur('{ "r": map($.l, $.n) }', GENS) == {"r": ["Ana", "Bo"]}
    assert moteur('{ "r": map($.l, $ * 2) }', NOMBRES) == {"r": [2, 4, 6, 8]}


def test_map_peut_servir_d_argument() -> None:
    """C'est ce que la boucle ne sait pas faire : elle n'existe qu'en valeur."""
    assert run('{ "r": sum(map($.l, $.age)) }', GENS) == {"r": 55}


@pytest.mark.parametrize("moteur", [run, run_compiled])
def test_filter_garde_les_elements_vrais(moteur) -> None:
    assert moteur('{ "r": map(filter($.l, $.ok), $.n) }', GENS) == {"r": ["Ana"]}
    assert moteur('{ "r": filter($.l, $ > 2) }', NOMBRES) == {"r": [3, 4]}


def test_map_et_filter_sans_expression_rendent_les_elements() -> None:
    # Convention des arguments paresseux : omis, l'expression vaut l'élément.
    assert run('{ "r": map($.l) }', NOMBRES) == {"r": [1, 2, 3, 4]}
    assert run('{ "r": filter($.l) }', {"l": [0, 1, 2]}) == {"r": [1, 2]}


# --- find / some / every --------------------------------------------------------


def test_find_rend_le_premier_element_qui_convient() -> None:
    assert run('{ "r": find($.l, $.age < 28) }', GENS) == {"r": GENS["l"][1]}
    assert run('{ "r": find($.l, $.age > 99) }', GENS) == {"r": None}


def test_findindex_rend_la_position_ou_moins_un() -> None:
    assert run('{ "a": findindex($.l, $ > 2), "b": findindex($.l, $ > 9) }', NOMBRES) == {
        "a": 2,
        "b": -1,
    }


def test_some_et_every() -> None:
    template = '{ "some": some($.l, $.ok), "every": every($.l, $.ok) }'
    assert run(template, GENS) == {"some": True, "every": False}


def test_sur_un_tableau_vide_every_est_vrai_et_some_est_faux() -> None:
    """Convention universelle : « tous » d'un ensemble vide est vrai (il n'y a
    aucun contre-exemple), « au moins un » est faux."""
    assert run('{ "e": every($.l, $), "s": some($.l, $) }', {"l": []}) == {"e": True, "s": False}


def test_some_ne_remplace_pas_any() -> None:
    # `any` dit « tableau non vide » (fidélité .NET) ; `some` teste un prédicat.
    assert run('{ "any": any($.l), "some": some($.l, $ > 9) }', NOMBRES) == {
        "any": True,
        "some": False,
    }


# --- reduce ---------------------------------------------------------------------


@pytest.mark.parametrize("moteur", [run, run_compiled])
def test_reduce_accumule(moteur) -> None:
    # L'expression voit `{acc, value, index}` : il faut bien nommer les deux
    # côtés, et le langage n'a pas de second paramètre.
    assert moteur('{ "r": reduce($.l, $.acc + $.value, 0) }', NOMBRES) == {"r": 10}


def test_reduce_voit_l_index_et_sait_construire_autre_chose_qu_un_nombre() -> None:
    template = '{ "r": reduce($.l, $.acc + $.value.n, "") }'
    assert run(template, GENS) == {"r": "AnaBo"}
    assert run('{ "r": reduce($.l, $.acc + $.index, 0) }', NOMBRES) == {"r": 6}


def test_reduce_sans_valeur_initiale_part_du_premier_element() -> None:
    assert run('{ "r": reduce($.l, $.acc + $.value) }', NOMBRES) == {"r": 10}
    # Tableau vide et pas d'initiale : `null`, il n'y a rien à rendre.
    assert run('{ "r": reduce($.l, $.acc + $.value) }', {"l": []}) == {"r": None}


def test_reduce_d_un_tableau_vide_rend_la_valeur_initiale() -> None:
    assert run('{ "r": reduce($.l, $.acc + $.value, 7) }', {"l": []}) == {"r": 7}


# --- minby / maxby / cumsum -----------------------------------------------------


def test_minby_et_maxby_rendent_l_element_pas_la_clef() -> None:
    template = '{ "min": minby($.l, $.age).n, "max": maxby($.l, $.age).n }'
    # L'accès à une clé sur un résultat de fonction n'existe pas : on passe par map.
    template = '{ "min": map([minby($.l, $.age)], $.n), "max": map([maxby($.l, $.age)], $.n) }'
    assert run(template, GENS) == {"min": ["Bo"], "max": ["Ana"]}


def test_minby_d_un_tableau_vide_rend_null() -> None:
    assert run('{ "a": minby($.l, $), "b": maxby($.l, $) }', {"l": []}) == {"a": None, "b": None}


def test_a_egalite_minby_garde_le_premier() -> None:
    source = {"l": [{"k": 1, "i": "a"}, {"k": 1, "i": "b"}]}
    assert run('{ "r": map([minby($.l, $.k)], $.i) }', source) == {"r": ["a"]}


def test_cumsum_rend_les_totaux_courants() -> None:
    assert run('{ "r": cumsum($.l) }', NOMBRES) == {"r": [1, 3, 6, 10]}


def test_cumsum_refuse_un_intrus_comme_sum() -> None:
    with pytest.raises(JsltError, match="cumsum"):
        run('{ "r": cumsum($.l) }', {"l": [1, "deux"]})


# --- conventions de la famille ---------------------------------------------------


@pytest.mark.parametrize(
    "appel",
    ["map($.l, $)", "filter($.l, $)", "find($.l, $)", "every($.l, $)", "some($.l, $)",
     "minby($.l, $)", "maxby($.l, $)", "cumsum($.l)", "reduce($.l, $.acc, 0)"],
)
def test_un_non_tableau_rend_null(appel) -> None:
    assert run('{ "r": ' + appel + " }", {"l": "texte"}) == {"r": None}
