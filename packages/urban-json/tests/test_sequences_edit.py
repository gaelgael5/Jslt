"""Construire et découper un tableau — sujets « tableaux » et « range ».

Rien ne **créait** une série : tout le moteur transformait ce qui entrait. Et
ajouter un élément à un tableau n'avait pas d'écriture simple.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


L = {"l": [1, 2, 3, 4, 5]}


# --- range ----------------------------------------------------------------------


def test_range_depuis_zero() -> None:
    assert run('{ "r": range(5) }') == {"r": [0, 1, 2, 3, 4]}


def test_range_avec_debut_et_fin_exclue() -> None:
    assert run('{ "r": range(2, 5) }') == {"r": [2, 3, 4]}


def test_range_avec_pas() -> None:
    assert run('{ "r": range(0, 10, 3) }') == {"r": [0, 3, 6, 9]}


def test_range_descendant() -> None:
    assert run('{ "r": range(5, 0, -1) }') == {"r": [5, 4, 3, 2, 1]}


def test_range_vide_quand_les_bornes_se_croisent() -> None:
    assert run('{ "a": range(0), "b": range(5, 2) }') == {"a": [], "b": []}


def test_range_de_pas_nul_leve() -> None:
    with pytest.raises(JsltError, match="pas"):
        run('{ "r": range(0, 5, 0) }')


def test_range_trop_grand_leve() -> None:
    """Un template tourne souvent sur une entrée qu'on ne choisit pas : `range`
    est le seul endroit où elle peut demander un tableau d'un milliard."""
    with pytest.raises(JsltError, match="trop"):
        run('{ "r": range(100000000) }')


def test_range_sert_de_compteur() -> None:
    assert run('{ "r": map(range(1, 4), $ * $) }') == {"r": [1, 4, 9]}


# --- slice / append / insert / removeat ------------------------------------------


def test_slice_borne_de_fin_exclue() -> None:
    assert run('{ "r": slice($.l, 1, 3) }', L) == {"r": [2, 3]}


def test_slice_sans_fin_va_au_bout() -> None:
    assert run('{ "r": slice($.l, 3) }', L) == {"r": [4, 5]}


def test_slice_compte_depuis_la_fin_avec_un_indice_negatif() -> None:
    assert run('{ "a": slice($.l, -2), "b": slice($.l, 0, -3) }', L) == {"a": [4, 5], "b": [1, 2]}


def test_slice_tolere_des_bornes_trop_larges() -> None:
    # Même doctrine que `substring` : un template transforme des données qu'il
    # ne choisit pas, il ne doit pas échouer sur un tableau plus court.
    assert run('{ "a": slice($.l, 9), "b": slice($.l, 0, 99) }', L) == {"a": [], "b": [1, 2, 3, 4, 5]}


def test_append_ajoute_sans_modifier_la_source() -> None:
    assert run('{ "r": append($.l, 6), "source": $.l }', {"l": [1, 2]}) == {
        "r": [1, 2, 6],
        "source": [1, 2],
    }


def test_append_ajoute_un_tableau_comme_un_seul_element() -> None:
    # `append` ajoute UNE valeur ; concaténer, c'est `+` ou `union`.
    assert run('{ "r": append($.l, [3, 4]) }', {"l": [1]}) == {"r": [1, [3, 4]]}


def test_insert_place_a_l_indice() -> None:
    assert run('{ "a": insert($.l, 0, 9), "b": insert($.l, 2, 9) }', {"l": [1, 2]}) == {
        "a": [9, 1, 2],
        "b": [1, 2, 9],
    }


def test_insert_tolere_un_indice_hors_bornes_et_accepte_les_negatifs() -> None:
    assert run('{ "a": insert($.l, 99, 9), "b": insert($.l, -1, 9) }', {"l": [1, 2]}) == {
        "a": [1, 2, 9],
        "b": [1, 9, 2],
    }


def test_removeat_retire_un_element() -> None:
    assert run('{ "a": removeat($.l, 1), "b": removeat($.l, -1) }', {"l": [1, 2, 3]}) == {
        "a": [1, 3],
        "b": [1, 2],
    }


def test_removeat_hors_bornes_rend_une_copie_inchangee() -> None:
    assert run('{ "r": removeat($.l, 9), "source": $.l }', {"l": [1, 2]}) == {
        "r": [1, 2],
        "source": [1, 2],
    }


@pytest.mark.parametrize(
    "appel", ["slice($.l, 0)", "append($.l, 1)", "insert($.l, 0, 1)", "removeat($.l, 0)"]
)
def test_un_non_tableau_rend_null(appel) -> None:
    assert run('{ "r": ' + appel + " }", {"l": "texte"}) == {"r": None}
