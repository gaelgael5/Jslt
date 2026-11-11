"""Dates : parties supplémentaires, bornes de période, fuseau, durée.

Complète `test_dates.py` sur le sujet « dates » : `datepart` ne donnait ni jour
de l'année, ni semaine, ni trimestre ; il n'existait ni début/fin de période, ni
jours ouvrés, ni conversion de fuseau explicite.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


@pytest.mark.parametrize(
    "part, expected",
    [
        ("dayofyear", 319), ("week", 46), ("quarter", 4), ("millisecond", 123),
        ("year", 2026), ("month", 11), ("day", 15), ("dayofweek", 0),
    ],
)
def test_datepart_parties(part, expected):
    source = {"d": "2026-11-15T08:30:05.123456"}
    assert run('{ "r": datepart($.d, "' + part + '") }', source) == {"r": expected}


def test_datepart_semaine_iso_du_1er_janvier():
    # 1er janvier 2027 = vendredi : semaine ISO 53 de 2026, pas semaine 1.
    assert run('{ "r": datepart($.d, "week") }', {"d": "2027-01-01T00:00:00"}) == {"r": 53}


def test_datepart_partie_inconnue_leve():
    with pytest.raises(JsltError, match="partie de date inconnue"):
        run('{ "r": datepart($.d, "fortnight") }', {"d": "2026-01-01T00:00:00"})


# --- bornes de période --------------------------------------------------------


@pytest.mark.parametrize(
    "unit, start, end",
    [
        ("year", "2026-01-01T00:00:00", "2026-12-31T23:59:59.999999"),
        ("quarter", "2026-10-01T00:00:00", "2026-12-31T23:59:59.999999"),
        ("month", "2026-11-01T00:00:00", "2026-11-30T23:59:59.999999"),
        ("week", "2026-11-09T00:00:00", "2026-11-15T23:59:59.999999"),
        ("day", "2026-11-15T00:00:00", "2026-11-15T23:59:59.999999"),
        ("hour", "2026-11-15T08:00:00", "2026-11-15T08:59:59.999999"),
        ("minute", "2026-11-15T08:30:00", "2026-11-15T08:30:59.999999"),
    ],
)
def test_datestartof_et_dateendof(unit, start, end):
    source = {"d": "2026-11-15T08:30:05.123456"}
    template = '{ "a": datestartof($.d, "' + unit + '"), "b": dateendof($.d, "' + unit + '") }'
    assert run(template, source) == {"a": start, "b": end}


def test_datestartof_semaine_commence_lundi():
    # 2026-11-15 est un dimanche : sa semaine ISO commence le lundi 9.
    assert run('{ "r": datestartof($.d, "week") }', {"d": "2026-11-15T12:00:00"}) == {
        "r": "2026-11-09T00:00:00"
    }


def test_datestartof_conserve_le_fuseau():
    source = {"d": "2026-11-15T08:30:00+02:00"}
    assert run('{ "r": datestartof($.d, "day") }', source) == {"r": "2026-11-15T00:00:00+02:00"}


def test_datestartof_unite_inconnue_leve():
    with pytest.raises(JsltError, match="unité"):
        run('{ "r": datestartof($.d, "second") }', {"d": "2026-01-01T00:00:00"})


# --- fuseau explicite ---------------------------------------------------------


def test_datezone_qualifie_une_date_naive():
    source = {"d": "2026-11-15T08:30:00"}
    assert run('{ "r": datezone($.d, "Europe/Paris") }', source) == {
        "r": "2026-11-15T08:30:00+01:00"
    }


def test_datezone_convertit_une_date_decalee():
    source = {"d": "2026-11-15T08:30:00+00:00"}
    assert run('{ "r": datezone($.d, "Europe/Paris") }', source) == {
        "r": "2026-11-15T09:30:00+01:00"
    }


def test_datezone_fuseau_inconnu_leve():
    with pytest.raises(JsltError, match="fuseau"):
        run('{ "r": datezone($.d, "Mars/Olympus") }', {"d": "2026-01-01T00:00:00"})


# --- jours ouvrés -------------------------------------------------------------


def test_dateadd_jours_ouvres_saute_le_week_end():
    # Vendredi 13 + 1 jour ouvré = lundi 16.
    assert run('{ "r": dateadd($.d, "weekday", 1) }', {"d": "2026-11-13T09:00:00"}) == {
        "r": "2026-11-16T09:00:00"
    }


def test_dateadd_jours_ouvres_une_semaine():
    assert run('{ "r": dateadd($.d, "weekday", 5) }', {"d": "2026-11-13T09:00:00"}) == {
        "r": "2026-11-20T09:00:00"
    }


def test_datesub_jours_ouvres():
    # Lundi 16 - 1 jour ouvré = vendredi 13.
    assert run('{ "r": datesub($.d, "weekday", 1) }', {"d": "2026-11-16T09:00:00"}) == {
        "r": "2026-11-13T09:00:00"
    }


def test_dateadd_depuis_un_samedi_atterrit_en_semaine():
    assert run('{ "r": dateadd($.d, "weekday", 1) }', {"d": "2026-11-14T09:00:00"}) == {
        "r": "2026-11-16T09:00:00"
    }


def test_datediff_jours_ouvres():
    source = {"a": "2026-11-13T09:00:00", "b": "2026-11-20T09:00:00"}
    assert run('{ "r": datediff($.a, $.b, "weekday") }', source) == {"r": 5}


def test_datediff_jours_ouvres_sur_un_week_end_seul():
    source = {"a": "2026-11-14T09:00:00", "b": "2026-11-15T09:00:00"}
    assert run('{ "r": datediff($.a, $.b, "weekday") }', source) == {"r": 0}


def test_datediff_jours_ouvres_negatif():
    source = {"a": "2026-11-20T09:00:00", "b": "2026-11-13T09:00:00"}
    assert run('{ "r": datediff($.a, $.b, "weekday") }', source) == {"r": -5}


# --- today / durée ------------------------------------------------------------


def test_today_est_minuit():
    result = run('{ "r": today() }')["r"]
    assert result.endswith("T00:00:00"), result


def test_today_utc_porte_le_decalage():
    assert run('{ "r": today(true) }')["r"].endswith("T00:00:00+00:00")


def test_dateduration_decompose():
    source = {"a": "2026-01-31T08:00:00", "b": "2027-03-02T09:30:10"}
    assert run('{ "r": dateduration($.a, $.b) }', source) == {
        "r": {
            "negative": False, "years": 1, "months": 1, "days": 2,
            "hours": 1, "minutes": 30, "seconds": 10,
        }
    }


def test_dateduration_signalee_negative():
    source = {"a": "2026-03-02T00:00:00", "b": "2026-03-01T00:00:00"}
    result = run('{ "r": dateduration($.a, $.b) }', source)["r"]
    assert result["negative"] is True and result["days"] == 1


def test_dateduration_null_propage():
    assert run('{ "r": dateduration($.a, $.b) }', {"a": "2026-01-01T00:00:00"}) == {"r": None}


def test_exemple_complet_fin_de_trimestre_en_jours_ouvres():
    template = (
        '{ "fin": dateendof($.d, "quarter") -> datestartof("day"), '
        '"ouvres": datediff($.d, dateendof($.d, "quarter"), "weekday") }'
    )
    assert run(template, {"d": "2026-11-15T00:00:00"}) == {
        "fin": "2026-12-31T00:00:00", "ouvres": 34
    }
