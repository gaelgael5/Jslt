"""Lecture et manipulation de nombres — sujet « nombres ».

`parsedate` savait lire une date selon une culture ; rien ne savait lire un
nombre (« 1 234,56 » en fr-FR), et `round` n'avait pas de précision.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


@pytest.mark.parametrize(
    "text, culture, expected",
    [
        ("1234.56", "", 1234.56),
        ("1,234.56", "en-US", 1234.56),
        ("1 234,56", "fr-FR", 1234.56),
        ("1.234,56", "de-DE", 1234.56),
        ("42", "fr-FR", 42),
        ("-7", "", -7),
        ("12 %", "fr-FR", 12),
        ("1 234,56 €", "fr-FR", 1234.56),
    ],
)
def test_parsenumber(text, culture, expected):
    template = '{ "r": parsenumber($.t, "' + culture + '") }'
    assert run(template, {"t": text}) == {"r": expected}


def test_parsenumber_garde_l_entier_entier():
    assert isinstance(run('{ "r": parsenumber($.t) }', {"t": "42"})["r"], int)


def test_parsenumber_null_reste_null():
    assert run('{ "r": parsenumber($.t) }', {}) == {"r": None}


def test_parsenumber_nombre_rendu_tel_quel():
    assert run('{ "r": parsenumber($.t) }', {"t": 1.5}) == {"r": 1.5}


def test_parsenumber_texte_illisible_leve():
    with pytest.raises(JsltError, match="nombre"):
        run('{ "r": parsenumber($.t, "fr-FR") }', {"t": "douze"})


def test_parsenumber_culture_inconnue_leve():
    with pytest.raises(JsltError, match="culture"):
        run('{ "r": parsenumber($.t, "xx-XX") }', {"t": "1"})


def test_parsenumber_ferme_l_aller_retour_avec_format():
    template = '{ "r": parsenumber(format($.v, "N2", "fr-FR"), "fr-FR") }'
    assert run(template, {"v": 1234.5}) == {"r": 1234.5}


def test_round_avec_precision():
    assert run('{ "r": round($.v, 2) }', {"v": 1.23456}) == {"r": 1.23}


def test_round_sans_precision_reste_le_comportement_dotnet():
    # Arrondi bancaire à l'entier, rendu en décimal : 2.5 -> 2.0, pas 3.0.
    assert run('{ "a": round($.a), "b": round($.b) }', {"a": 2.5, "b": 3.5}) == {
        "a": 2.0, "b": 4.0
    }


def test_round_precision_bancaire_aussi():
    assert run('{ "r": round($.v, 1) }', {"v": 0.25}) == {"r": 0.2}


def test_sign():
    template = '{ "a": sign($.a), "b": sign($.b), "c": sign($.c) }'
    assert run(template, {"a": -3.5, "b": 0, "c": 7}) == {"a": -1, "b": 0, "c": 1}


def test_clamp():
    template = '{ "a": clamp($.a, 0, 10), "b": clamp($.b, 0, 10), "c": clamp($.c, 0, 10) }'
    assert run(template, {"a": -5, "b": 5, "c": 50}) == {"a": 0, "b": 5, "c": 10}


def test_clamp_bornes_inversees_leve():
    with pytest.raises(JsltError, match="bornes"):
        run('{ "r": clamp($.v, 10, 0) }', {"v": 5})


def test_gcd():
    assert run('{ "r": gcd($.a, $.b) }', {"a": 12, "b": 18}) == {"r": 6}


def test_gcd_refuse_un_decimal():
    with pytest.raises(JsltError, match="entier"):
        run('{ "r": gcd($.a, $.b) }', {"a": 1.5, "b": 3})


def test_decalages_de_bits():
    template = '{ "g": shiftleft($.v, 3), "d": shiftright($.v, 2) }'
    assert run(template, {"v": 8}) == {"g": 64, "d": 2}


def test_decalage_refuse_un_decimal():
    with pytest.raises(JsltError, match="entier"):
        run('{ "r": shiftleft($.v, 1) }', {"v": 1.5})


def test_tohex_et_fromhex():
    assert run('{ "r": tohex($.v) }', {"v": 255}) == {"r": "ff"}
    assert run('{ "r": fromhex($.t) }', {"t": "ff"}) == {"r": 255}
    assert run('{ "r": fromhex($.t) }', {"t": "0xFF"}) == {"r": 255}


def test_tohex_largeur_minimale():
    assert run('{ "r": tohex($.v, 4) }', {"v": 255}) == {"r": "00ff"}


def test_tohex_negatif_garde_son_signe():
    assert run('{ "r": tohex($.v) }', {"v": -255}) == {"r": "-ff"}


def test_fromhex_texte_invalide_leve():
    with pytest.raises(JsltError, match="hexadécimal"):
        run('{ "r": fromhex($.t) }', {"t": "zz"})


@pytest.mark.parametrize(
    "call", ["sign($.v)", "clamp($.v, 0, 1)", "tohex($.v)", "round($.v, 1)"]
)
def test_convention_numerique_null(call):
    # Convention .NET des fonctions numériques : non-nombre (ou null) -> null.
    assert run('{ "r": ' + call + ' }', {}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"v": "x"}) == {"r": None}


def test_exemple_complet_montant_lu_puis_borne():
    template = '{ "montant": parsenumber($.t, "fr-FR") -> clamp(0, 1000) -> round(2) }'
    assert run(template, {"t": "1 234,567"}) == {"montant": 1000.0}
