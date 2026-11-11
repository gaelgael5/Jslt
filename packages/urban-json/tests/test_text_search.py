"""Découpe fine, raccourcissement et similarité — catégorie « texte ».

Trois pièges plus que trois manques : `split` ne prenait que le **premier
caractère** du séparateur (silencieux et faux sur `", "`), `reverse` rendait
`null` sur une chaîne, et le nom `truncate` était déjà pris par la troncature
numérique.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


# --- découpe ------------------------------------------------------------------


def test_splitstring_separateur_multi_caracteres():
    assert run('{ "r": splitstring($.t, ", ") }', {"t": "a, b, c"}) == {"r": ["a", "b", "c"]}


def test_split_ne_prend_que_le_premier_caractere():
    # Comportement .NET conservé, documenté : c'est ce qui rend `splitstring`
    # nécessaire plutôt que facultatif.
    assert run('{ "r": split($.t, ", ") }', {"t": "a, b"}) == {"r": ["a", " b"]}


def test_splitstring_limite_le_nombre_de_coupes():
    assert run('{ "r": splitstring($.t, "-", 1) }', {"t": "a-b-c"}) == {"r": ["a", "b-c"]}


def test_splitstring_separateur_vide_rend_le_texte_entier():
    assert run('{ "r": splitstring($.t, "") }', {"t": "ab"}) == {"r": ["ab"]}


def test_splitregex():
    assert run('{ "r": splitregex($.t, "\\\\s*;\\\\s*") }', {"t": "a ; b;c"}) == {
        "r": ["a", "b", "c"]
    }


def test_splitregex_motif_invalide_leve():
    with pytest.raises(JsltError, match="motif regex invalide"):
        run('{ "r": splitregex($.t, "(") }', {"t": "a"})


# --- reverse sur une chaîne ---------------------------------------------------


def test_reverse_d_une_chaine():
    assert run('{ "r": reverse($.t) }', {"t": "abc"}) == {"r": "cba"}


def test_reverse_d_un_tableau_inchange():
    assert run('{ "r": reverse($.l) }', {"l": [1, 2]}) == {"r": [2, 1]}


def test_reverse_respecte_les_caracteres_composes():
    # « é » décomposé (e + accent) ne doit pas sortir l'accent du mauvais côté.
    assert run('{ "r": reverse($.t) }', {"t": "ané"}) == {"r": "éna"}


# --- raccourcir ---------------------------------------------------------------


def test_shorten_ajoute_une_ellipse():
    assert run('{ "r": shorten($.t, 8) }', {"t": "Paris Lyon Nice"}) == {"r": "Paris…"}


def test_shorten_laisse_un_texte_assez_court():
    assert run('{ "r": shorten($.t, 20) }', {"t": "Paris"}) == {"r": "Paris"}


def test_shorten_coupe_sur_un_mot_si_besoin():
    assert run('{ "r": shorten($.t, 4) }', {"t": "abcdefgh"}) == {"r": "abc…"}


def test_shorten_suffixe_personnalise():
    assert run('{ "r": shorten($.t, 8, " [...]") }', {"t": "Paris Lyon"}) == {"r": "Pa [...]"}


def test_shorten_longueur_trop_petite_leve():
    with pytest.raises(JsltError, match="longueur"):
        run('{ "r": shorten($.t, 0) }', {"t": "ab"})


# --- similarité ---------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [("chat", "chat", 0), ("chat", "chats", 1), ("chat", "chien", 3), ("", "abc", 3)],
)
def test_levenshtein(a, b, expected):
    assert run('{ "r": levenshtein($.a, $.b) }', {"a": a, "b": b}) == {"r": expected}


def test_similarity_entre_0_et_1():
    assert run('{ "r": similarity($.a, $.b) }', {"a": "chat", "b": "chat"}) == {"r": 1.0}
    assert run('{ "r": similarity($.a, $.b) }', {"a": "chat", "b": "chien"}) == {"r": 0.4}


def test_similarity_de_deux_chaines_vides_vaut_un():
    # Deux absences sont identiques : 0/0 vaut 1 ici, pas « indéfini ».
    assert run('{ "r": similarity($.a, $.b) }', {"a": "", "b": ""}) == {"r": 1.0}


def test_similarite_sur_clef_pliee_rapproche_les_ecritures():
    template = '{ "r": similarity(foldtext($.a), foldtext($.b)) }'
    assert run(template, {"a": "CRÈME", "b": "creme"}) == {"r": 1.0}


# --- slugify ------------------------------------------------------------------


def test_slugify():
    assert run('{ "r": slugify($.t) }', {"t": "Crème Brûlée à Paris !"}) == {
        "r": "creme-brulee-a-paris"
    }


def test_slugify_separateur_personnalise():
    assert run('{ "r": slugify($.t, "_") }', {"t": "a b"}) == {"r": "a_b"}


def test_slugify_rend_une_chaine_vide_si_rien_ne_survit():
    assert run('{ "r": slugify($.t) }', {"t": "!!!"}) == {"r": ""}


# --- conventions --------------------------------------------------------------


@pytest.mark.parametrize(
    "call",
    ['splitstring($.t, ",")', 'splitregex($.t, ",")', "shorten($.t, 5)", "slugify($.t)",
     'levenshtein($.t, "a")', 'similarity($.t, "a")'],
)
def test_null_reste_null(call):
    assert run('{ "r": ' + call + ' }', {}) == {"r": None}
