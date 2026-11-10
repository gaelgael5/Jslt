"""``format(valeur, masque, culture)`` — port de ``ExecuteFormat`` (.NET
``ToString(mask, culture)``), masques .NET traduits en Python.

Une chaîne ISO 8601 est formatée comme une date : Newtonsoft (.NET) convertit
les chaînes ISO en dates à la lecture du JSON source.
"""

from __future__ import annotations

import pytest

from urban_json import JsltError, JsltTemplate


def fmt(value, mask, culture=""):
    template = '{ "r": format($.v, $.m, $.c) }'
    return JsltTemplate.parse(template).transform({"v": value, "m": mask, "c": culture})["r"]


NBSP = "\u202f"  # séparateur de milliers fr-FR (.NET / ICU)
SP = "\u00a0"  # espace insécable avant € et % (fr-FR, de-DE)


@pytest.mark.parametrize(
    ("value", "mask", "culture", "expected"),
    [
        # formats standards
        pytest.param(1234.5, "N2", "", "1,234.50", id="N2-invariant"),
        pytest.param(1234.5, "N2", "fr-FR", f"1{NBSP}234,50", id="N2-fr"),
        pytest.param(1234.5, "N2", "de-DE", "1.234,50", id="N2-de"),
        pytest.param(1234.5, "N0", "en-US", "1,235", id="N0-arrondi"),
        pytest.param(3.14159, "F3", "", "3.142", id="F3"),
        pytest.param(42, "D5", "", "00042", id="D5"),
        pytest.param(-42, "D5", "", "-00042", id="D5-negatif"),
        pytest.param(0.256, "P1", "", "25.6 %", id="P1-invariant"),
        pytest.param(0.256, "P1", "en-US", "25.6%", id="P1-us"),
        pytest.param(1234.5, "C", "en-US", "$1,234.50", id="C-us"),
        pytest.param(1234.5, "C", "fr-FR", f"1{NBSP}234,50{SP}€", id="C-fr"),
        pytest.param(255, "X", "", "FF", id="X"),
        pytest.param(255, "x4", "", "00ff", id="x4"),
        pytest.param(1234.5, "E2", "", "1.23E+003", id="E2"),
        pytest.param(1.5, "G", "fr-FR", "1,5", id="G-fr"),
        # masques personnalisés
        pytest.param(1234.567, "0.00", "", "1234.57", id="0.00"),
        pytest.param(1234.567, "#,##0.00", "", "1,234.57", id="groupes"),
        pytest.param(1234.567, "#,##0.00", "fr-FR", f"1{NBSP}234,57", id="groupes-fr"),
        pytest.param(7, "000", "", "007", id="zeros"),
        pytest.param(1.5, "0.##", "", "1.5", id="dièses"),
        pytest.param(2, "0.##", "", "2", id="dièses-entier"),
        pytest.param(0.5, "0%", "", "50%", id="pourcent"),
        pytest.param(12, "'n°' 0", "", "n° 12", id="litteral"),
        # dates (chaîne ISO)
        pytest.param("2026-10-22T14:05:09", "yyyy-MM-dd", "", "2026-10-22", id="date-iso"),
        pytest.param("2026-10-22T14:05:09", "dd/MM/yyyy HH:mm", "", "22/10/2026 14:05", id="date-heure"),
        pytest.param("2026-10-22T14:05:09", "dddd d MMMM yyyy", "fr-FR", "jeudi 22 octobre 2026", id="noms-fr"),
        pytest.param("2026-10-22T14:05:09", "ddd, MMM d", "en-US", "Thu, Oct 22", id="abreges-en"),
        pytest.param("2026-10-22T14:05:09", "h:mm tt", "en-US", "2:05 PM", id="12h"),
        pytest.param("2026-10-22T14:05:09.123", "HH:mm:ss.fff", "", "14:05:09.123", id="millisecondes"),
        pytest.param("2026-10-22T14:05:09", "d", "fr-FR", "22/10/2026", id="d-fr"),
        pytest.param("2026-10-22T14:05:09", "d", "en-US", "10/22/2026", id="d-us"),
        pytest.param("2026-10-22T14:05:09", "d", "de-DE", "22.10.2026", id="d-de"),
        pytest.param("2026-10-22T14:05:09", "D", "fr-FR", "jeudi 22 octobre 2026", id="D-fr"),
        pytest.param("2026-10-22T14:05:09", "s", "", "2026-10-22T14:05:09", id="s"),
        pytest.param("2026-10-22T14:05:09", "yyyy'-S'ss", "", "2026-S09", id="date-litteral"),
        # valeurs non formatables : rendues en texte, comme en .NET
        pytest.param("bonjour", "N2", "", "bonjour", id="chaine"),
        pytest.param(True, "N2", "", "True", id="booleen"),
        pytest.param(None, "N2", "", None, id="null"),
    ],
)
def test_format(value, mask, culture, expected) -> None:
    assert fmt(value, mask, culture) == expected


def test_format_culture_inconnue() -> None:
    with pytest.raises(JsltError, match="culture"):
        fmt(1.5, "N2", "xx-YY")


def test_format_masque_non_pris_en_charge() -> None:
    with pytest.raises(JsltError, match="masque"):
        fmt(1.5, "R", "")


def test_format_culture_absente_ou_null_vaut_invariante() -> None:
    template = '{ "r": format($.v, "N1") }'
    assert JsltTemplate.parse(template).transform({"v": 1234.5})["r"] == "1,234.5"


@pytest.mark.parametrize(
    ("value", "mask", "expected"),
    [
        pytest.param(-1234.5, "#,##0.00", "-1,234.50", id="negatif-perso"),
        pytest.param(-1234.5, "N1", "-1,234.5", id="negatif-N"),
        pytest.param(0.5, "#.##", ".5", id="partie-entiere-vide"),
        pytest.param(2.5, "0", "3", id="arrondi-loin-de-zero"),
        pytest.param(-2.5, "0", "-3", id="arrondi-loin-de-zero-negatif"),
        pytest.param(1234.5, "", "1234.5", id="masque-vide"),
    ],
)
def test_format_cas_limites(value, mask, expected) -> None:
    assert fmt(value, mask) == expected


def test_format_X_refuse_un_decimal() -> None:
    with pytest.raises(JsltError, match="entiers"):
        fmt(1.5, "X")


# --- décalage horaire ---------------------------------------------------------
# `parsedate(..., fuseau)` rend des dates avec décalage : `format` doit savoir
# les lire et les écrire, sinon l'aller-retour est impossible.


@pytest.mark.parametrize(
    ("value", "mask", "expected"),
    [
        pytest.param("2026-11-10T08:30:00+01:00", "zzz", "+01:00", id="zzz-positif"),
        pytest.param("2026-11-10T08:30:00-05:00", "zzz", "-05:00", id="zzz-negatif"),
        pytest.param("2026-11-10T08:30:00+05:30", "zzz", "+05:30", id="zzz-demi-heure"),
        pytest.param("2026-11-10T08:30:00+01:00", "zz", "+01", id="zz"),
        pytest.param("2026-11-10T08:30:00+01:00", "HH'h'z", "08h+1", id="z-dans-un-masque"),
        pytest.param("2026-11-10T08:30:00+01:00", "HH:mmK", "08:30+01:00", id="K-avec-decalage"),
        pytest.param("2026-11-10T08:30:00Z", "HH:mmK", "08:30Z", id="K-utc"),
        pytest.param("2026-11-10T08:30:00", "HH:mmK", "08:30", id="K-naif-vide"),
        pytest.param("2026-11-10T08:30:00", "zzz", "+00:00", id="zzz-naif-vaut-zero"),
        pytest.param(
            "2026-11-10T08:30:00+01:00",
            "yyyy-MM-dd'T'HH:mm:sszzz",
            "2026-11-10T08:30:00+01:00",
            id="aller-retour-iso-complet",
        ),
    ],
)
def test_format_decalage_horaire(value, mask, expected) -> None:
    assert fmt(value, mask) == expected


def test_format_lit_le_z_finale_comme_utc() -> None:
    # `fromisoformat` n'accepte le 'Z' final qu'à partir de Python 3.11 : sans
    # normalisation, une date UTC n'était pas reconnue comme date et ressortait
    # telle quelle au lieu d'être formatée.
    assert fmt("2026-11-10T08:30:00Z", "HH:mm") == "08:30"


@pytest.mark.parametrize("mask", ["z", "K"])
def test_format_specificateur_de_fuseau_seul_refuse(mask) -> None:
    # Fidèle au .NET : un masque d'une seule lettre est un masque *standard*,
    # et ni 'z' ni 'K' n'en sont — il faut les écrire dans un masque plus long.
    with pytest.raises(JsltError, match="masque"):
        fmt("2026-11-10T08:30:00+01:00", mask)
