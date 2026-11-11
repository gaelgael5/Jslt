"""Découper et nettoyer un texte — sujet « texte ».

`splitstring($.t, "")` rendait le texte entier, `trimstart` retire un **jeu de
caractères** et non un préfixe, et `titlecase` met toutes les initiales. Trois
besoins élémentaires sans réponse, dont deux qui ressemblaient à une réponse.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


def test_chars_decoupe_en_caracteres() -> None:
    assert run('{ "r": chars($.t) }', {"t": "abc"}) == {"r": ["a", "b", "c"]}


def test_chars_travaille_par_grapheme() -> None:
    """« é » écrit en forme décomposée (e + accent) est **un** caractère perçu :
    le découper en deux collerait l'accent sur la lettre voisine, comme pour
    `reverse`."""
    assert run('{ "r": chars($.t) }', {"t": "été"}) == {"r": ["é", "t", "é"]}


def test_lines_coupe_sur_les_trois_fins_de_ligne() -> None:
    assert run('{ "r": lines($.t) }', {"t": "a\nb\r\nc\rd"}) == {"r": ["a", "b", "c", "d"]}


def test_lines_garde_les_lignes_vides() -> None:
    # Une ligne vide est une ligne : la retirer décalerait une numérotation.
    assert run('{ "r": lines($.t) }', {"t": "a\n\nb"}) == {"r": ["a", "", "b"]}


def test_words_coupe_sur_les_espaces_et_ignore_les_vides() -> None:
    assert run('{ "r": words($.t) }', {"t": "  le   petit\tchat\n"}) == {
        "r": ["le", "petit", "chat"]
    }


def test_removeprefix_et_removesuffix_retirent_un_affixe_entier() -> None:
    source = {"t": "bacab"}
    assert run('{ "a": removeprefix($.t, "ba"), "b": removesuffix($.t, "ab") }', source) == {
        "a": "cab",
        "b": "bac",
    }


def test_un_affixe_absent_laisse_le_texte_intact() -> None:
    # C'est la différence avec `trimstart`, qui retire des caractères : sur
    # « bacab », `trimstart(t, "ab")` rend « cab » alors que le préfixe « ab »
    # n'y est pas.
    source = {"t": "bacab"}
    assert run('{ "affixe": removeprefix($.t, "ab"), "jeu": trimstart($.t, "ab") }', source) == {
        "affixe": "bacab",
        "jeu": "cab",
    }


def test_capitalize_ne_touche_que_la_premiere_lettre() -> None:
    source = {"t": "bonjour le MONDE"}
    assert run('{ "cap": capitalize($.t), "titre": titlecase($.t) }', source) == {
        "cap": "Bonjour le MONDE",
        "titre": "Bonjour Le MONDE",
    }


def test_indexof_accepte_une_position_de_depart() -> None:
    source = {"t": "abcab", "l": ["a", "b", "a"]}
    assert run('{ "t": indexof($.t, "a", 1), "l": indexof($.l, "a", 1) }', source) == {
        "t": 3,
        "l": 2,
    }


def test_indexof_sans_position_est_inchange() -> None:
    assert run('{ "r": indexof($.t, "a") }', {"t": "abcab"}) == {"r": 0}


@pytest.mark.parametrize(
    "appel",
    ["chars($.t)", "lines($.t)", "words($.t)", "capitalize($.t)",
     "removeprefix($.t, \"a\")", "removesuffix($.t, \"a\")"],
)
def test_null_reste_null(appel) -> None:
    assert run('{ "r": ' + appel + " }", {}) == {"r": None}
