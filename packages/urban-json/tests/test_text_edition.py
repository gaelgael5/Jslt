"""Extraction, remplacement et pliage de chaînes (sujets « chaînes » et « i18n »).

Ces fonctions n'ont pas de contrepartie .NET : le moteur savait mesurer une
chaîne (`indexof`, `stringlenght`) mais pas en découper un morceau. On fixe donc
la sémantique ici, et ces tests en sont la définition.
"""

from __future__ import annotations

import json

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


# --- substring ----------------------------------------------------------------


@pytest.mark.parametrize(
    "start, length, expected",
    [
        (0, 5, "Paris"),
        (6, 6, "France"),
        (6, None, "France"),
        (0, 0, ""),
        (0, 99, "Paris France"),      # longueur qui dépasse : jusqu'à la fin
        (99, 3, ""),                  # début hors bornes : chaîne vide, pas d'erreur
        (-6, None, "France"),         # début négatif : depuis la fin
        (-6, 3, "Fra"),
    ],
)
def test_substring(start, length, expected):
    args = f'$.t, {start}' + ("" if length is None else f", {length}")
    assert run('{ "r": substring(' + args + ') }', {"t": "Paris France"}) == {"r": expected}


def test_substring_propage_null_et_refuse_le_reste():
    assert run('{ "r": substring($.t, 0, 2) }', {"t": None}) == {"r": None}
    assert run('{ "r": substring($.t, 0, 2) }', {"t": 42}) == {"r": False}


def test_substring_longueur_negative_leve():
    with pytest.raises(JsltError, match="longueur"):
        run('{ "r": substring($.t, 0, -1) }', {"t": "abc"})


# --- replace / regexreplace ---------------------------------------------------


def test_replace_toutes_les_occurrences():
    assert run('{ "r": replace($.t, "a", "o") }', {"t": "banana"}) == {"r": "bonono"}


def test_replace_chaine_vide_cherchee_rend_le_texte_intact():
    # Remplacer « rien » insérerait entre chaque caractère en Python : refusé.
    assert run('{ "r": replace($.t, "", "x") }', {"t": "ab"}) == {"r": "ab"}


def test_replace_supprime_quand_le_remplacement_est_absent():
    assert run('{ "r": replace($.t, "-", "") }', {"t": "01-02-03"}) == {"r": "010203"}


def test_regexreplace_avec_groupes_numerotes_dotnet():
    template = '{ "r": regexreplace($.t, "(\\\\d{2})/(\\\\d{2})", "$2-$1") }'
    assert run(template, {"t": "24/12"}) == {"r": "12-24"}


def test_regexreplace_avec_groupe_nomme_dotnet():
    template = '{ "r": regexreplace($.t, "(?<mois>\\\\d{2})/(?<jour>\\\\d{2})", "${jour}") }'
    assert run(template, {"t": "24/12"}) == {"r": "12"}


def test_regexreplace_motif_invalide_leve():
    with pytest.raises(JsltError, match="motif regex invalide"):
        run('{ "r": regexreplace($.t, "(", "x") }', {"t": "a"})


# --- trimstart / trimend / repeat / titlecase ---------------------------------


def test_trimstart_et_trimend():
    assert run('{ "a": trimstart($.t), "b": trimend($.t) }', {"t": "  x  "}) == {
        "a": "x  ", "b": "  x"
    }


def test_trimstart_avec_caracteres_donnes():
    assert run('{ "r": trimstart($.t, "0") }', {"t": "000042"}) == {"r": "42"}


def test_repeat():
    assert run('{ "r": repeat($.t, 3) }', {"t": "ab"}) == {"r": "ababab"}


def test_repeat_zero_ou_negatif_rend_vide():
    assert run('{ "a": repeat($.t, 0), "b": repeat($.t, -2) }', {"t": "ab"}) == {"a": "", "b": ""}


def test_titlecase_met_la_premiere_lettre_de_chaque_mot():
    # Seule la 1re lettre bouge : « McDonald » ne devient pas « Mcdonald ».
    assert run('{ "r": titlecase($.t) }', {"t": "jean McDonald de la tour"}) == {
        "r": "Jean McDonald De La Tour"
    }


# --- Unicode : normalize, deaccent, foldtext ----------------------------------


def test_normalize_formes():
    decompose = "été"          # e + accent combinant
    assert run('{ "r": normalize($.t) }', {"t": decompose}) == {"r": "été"}
    assert run('{ "r": normalize($.t, "D") }', {"t": "été"}) == {"r": decompose}


def test_normalize_forme_inconnue_leve():
    with pytest.raises(JsltError, match="forme Unicode"):
        run('{ "r": normalize($.t, "Z") }', {"t": "a"})


def test_deaccent_retire_les_diacritiques_sans_toucher_a_la_casse():
    assert run('{ "r": deaccent($.t) }', {"t": "Élève à Nîmes"}) == {"r": "Eleve a Nimes"}


def test_foldtext_rend_une_clef_de_comparaison():
    assert run('{ "r": foldtext($.t) }', {"t": "Élève"}) == {"r": "eleve"}


def test_foldtext_options_separees():
    source = {"t": "Élève"}
    assert run('{ "r": foldtext($.t, "case") }', source) == {"r": "élève"}
    assert run('{ "r": foldtext($.t, "accents") }', source) == {"r": "Eleve"}


def test_foldtext_option_inconnue_leve():
    with pytest.raises(JsltError, match="option de pliage"):
        run('{ "r": foldtext($.t, "zzz") }', {"t": "a"})


def test_foldtext_sert_a_comparer_deux_ecritures():
    template = '{ "egal": foldtext($.a) == foldtext($.b) }'
    assert run(template, {"a": "CRÈME", "b": "creme"}) == {"egal": True}


# --- conventions partagées ----------------------------------------------------


@pytest.mark.parametrize(
    "call",
    [
        'replace($.t, "a", "b")', 'trimstart($.t)', 'trimend($.t)', 'repeat($.t, 2)',
        'titlecase($.t)', 'deaccent($.t)', 'foldtext($.t)', 'normalize($.t)',
    ],
)
def test_convention_null_et_non_chaine(call):
    # Convention .NET des fonctions de chaîne, déjà celle de upper/lower/trim.
    assert run('{ "r": ' + call + ' }', {"t": None}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"t": 42}) == {"r": False}


def test_regexreplace_suit_la_convention_des_regex_pas_des_chaines():
    # `regexreplace` vit avec `regexismatch`/`regexmatches` : un scalaire est
    # converti en texte (chercher un motif dans un nombre a un sens), là où
    # `replace` rendrait `false`. L'écart est volontaire et documenté.
    assert run('{ "r": regexreplace($.t, "2", "x") }', {"t": 42}) == {"r": "4x"}
    assert run('{ "r": regexreplace($.t, "2", "x") }', {"t": None}) == {"r": None}
    assert run('{ "r": regexreplace($.t, "2", "x") }', {"t": [1]}) == {"r": None}


def test_chainage_extraction_puis_pliage():
    template = '{ "r": substring($.t, 0, 5) -> foldtext() }'
    assert run(template, {"t": "ÉLÈVE de troisième"}) == {"r": "eleve"}


def test_exemple_complet_code_postal():
    # Le cas qui motivait le sujet : extraire sans séparateur.
    template = json.dumps({"cp": "substring($.adresse, -5, 5)"})[1:-1]
    template = '{ "cp": substring($.adresse, -5, 5) }'
    assert run(template, {"adresse": "12 rue des Lilas 75011"}) == {"cp": "75011"}


# --- sujet 8 : deux noms, une seule implémentation -------------------------------


def test_stringlength_et_stringlenght_sont_la_meme_fonction() -> None:
    """La faute d'origine reste appelable ; l'orthographe juste aussi."""
    assert run('{ "a": stringlength($.t), "b": stringlenght($.t) }', {"t": "abcé"}) == {"a": 4, "b": 4}


def test_les_deux_noms_pointent_la_meme_callable() -> None:
    """Deux enregistrements, une implémentation : s'ils cessaient de pointer la
    même fonction, les deux noms pourraient diverger en silence."""
    from urban_json.functions import default_registry

    assert (
        default_registry.describe("stringlength").function
        is default_registry.describe("stringlenght").function
    )

