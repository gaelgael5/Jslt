"""Arrondis que `round` ne sait pas faire — sujet 4.

`round` est bancaire (demi vers le pair) : `round(0.125, 2)` rend 0.12 là où une
facture attend 0.13. Les valeurs choisies ici sont **discriminantes** : chacune
donnerait un autre résultat avec l'arrondi bancaire, ou avec un `Decimal`
construit sur le flottant plutôt que sur son écriture.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


# --- roundhalfup ----------------------------------------------------------------


def test_roundhalfup_arrondit_le_demi_vers_le_haut() -> None:
    """0.125 : `round` bancaire rend 0.12, le commerce attend 0.13."""
    assert run('{ "r": roundhalfup($.n, 2) }', {"n": 0.125}) == {"r": 0.13}


def test_roundhalfup_lit_le_nombre_tel_qu_il_est_ecrit() -> None:
    """2.675 vaut 2.67499999… en binaire : un `Decimal` construit sur le
    flottant rendrait 2.67, l'arrondi « faux » que tout le monde rencontre."""
    assert run('{ "r": roundhalfup($.n, 2) }', {"n": 2.675}) == {"r": 2.68}


def test_roundhalfup_entier_par_defaut() -> None:
    assert run('{ "a": roundhalfup(2.5), "b": roundhalfup(3.5) }') == {"a": 3.0, "b": 4.0}


def test_roundhalfup_eloigne_de_zero_les_negatifs() -> None:
    """Un avoir s'arrondit comme la facture qu'il annule."""
    assert run('{ "r": roundhalfup($.n) }', {"n": -0.5}) == {"r": -1.0}


def test_roundhalfup_accepte_une_precision_negative() -> None:
    assert run('{ "r": roundhalfup($.n, -2) }', {"n": 1250}) == {"r": 1300.0}


def test_roundhalfup_non_nombre_rend_null() -> None:
    assert run('{ "a": roundhalfup($.t), "b": roundhalfup($.absent) }', {"t": "x"}) == {"a": None, "b": None}


# --- roundto --------------------------------------------------------------------


def test_roundto_arrondit_au_multiple() -> None:
    assert run('{ "r": roundto($.n, 0.05) }', {"n": 2.34}) == {"r": 2.35}


def test_roundto_ne_traine_pas_l_erreur_du_contournement() -> None:
    """Le détour `round($.n * 20) / 20` passe par un flottant intermédiaire."""
    assert run('{ "r": roundto($.n, 0.1) }', {"n": 0.35}) == {"r": 0.4}


def test_roundto_au_quart_d_heure() -> None:
    assert run('{ "r": roundto($.minutes, 15) }', {"minutes": 38}) == {"r": 45.0}


def test_roundto_pas_nul_leve() -> None:
    with pytest.raises(JsltError, match="strictement positif"):
        run('{ "r": roundto($.n, 0) }', {"n": 2.34})


def test_roundto_pas_negatif_leve() -> None:
    with pytest.raises(JsltError, match="strictement positif"):
        run('{ "r": roundto($.n, -5) }', {"n": 2.34})


def test_roundto_pas_absent_leve() -> None:
    with pytest.raises(JsltError, match="pas d'arrondi"):
        run('{ "r": roundto($.n) }', {"n": 2.34})


def test_roundto_non_nombre_rend_null() -> None:
    assert run('{ "r": roundto($.t, 5) }', {"t": "x"}) == {"r": None}


# --- toprecision ----------------------------------------------------------------


def test_toprecision_garde_les_chiffres_significatifs() -> None:
    assert run('{ "r": toprecision($.n, 3) }', {"n": 1234.5}) == {"r": 1230.0}


def test_toprecision_suit_l_ordre_de_grandeur() -> None:
    """Ce que `round($.n, 2)` ne sait pas faire : la virgule n'est pas au même
    rang selon la valeur."""
    assert run('{ "a": toprecision($.a, 3), "b": toprecision($.b, 3) }', {"a": 0.00241348, "b": 24134.8}) == {
        "a": 0.00241,
        "b": 24100.0,
    }


def test_toprecision_de_zero() -> None:
    assert run('{ "r": toprecision(0, 3) }') == {"r": 0.0}


def test_toprecision_sans_chiffres_leve() -> None:
    with pytest.raises(JsltError, match="chiffres significatifs"):
        run('{ "r": toprecision($.n) }', {"n": 1.5})


def test_toprecision_zero_chiffre_leve() -> None:
    with pytest.raises(JsltError, match="au moins 1"):
        run('{ "r": toprecision($.n, 0) }', {"n": 1.5})


def test_toprecision_non_nombre_rend_null() -> None:
    assert run('{ "r": toprecision($.t, 3) }', {"t": "x"}) == {"r": None}

