"""Fonctions de dates : `parsedate` (masque explicite et fuseau), `dateadd`,
`datesub`, `datepart`.

Aucune contrepartie .NET : le .NET n'offrait que ``parsedate(texte, culture)``.
Les comportements fixés ici sont donc les décisions du portage, documentées dans
`docs/guide.md` : largeurs strictes des masques, date par défaut d'un masque sans
date, bornage du jour sur les mois courts, `dayofweek` à la .NET (dimanche = 0).
"""

from __future__ import annotations

import pytest

from urban_json import JsltError, JsltTemplate


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source if source is not None else {})["r"]


# --- parsedate : masque explicite --------------------------------------------


@pytest.mark.parametrize(
    ("mask", "culture", "value", "expected"),
    [
        pytest.param("dd/MM/yyyy", "", "22/10/2026", "2026-10-22T00:00:00", id="jour-mois-an"),
        pytest.param("MM/dd/yyyy", "", "10/22/2026", "2026-10-22T00:00:00", id="mois-jour-an"),
        pytest.param("yyyyMMdd", "", "20261022", "2026-10-22T00:00:00", id="compact-sans-separateur"),
        pytest.param("d/M/yyyy", "", "2/3/2026", "2026-03-02T00:00:00", id="largeurs-simples"),
        pytest.param("dd/MM/yyyy HH:mm:ss", "", "22/10/2026 14:05:09", "2026-10-22T14:05:09", id="avec-heure"),
        pytest.param("dd/MM/yyyy HH:mm", "", "22/10/2026 14:05", "2026-10-22T14:05:00", id="heure-minute"),
        pytest.param("yyyy'-'MM'-'dd", "", "2026-10-22", "2026-10-22T00:00:00", id="litteral-entre-quotes"),
        pytest.param("yyyy-MM-dd", "", "2026-10-22", "2026-10-22T00:00:00", id="tiret-litteral-implicite"),
        pytest.param("dddd d MMMM yyyy", "fr-FR", "jeudi 22 octobre 2026", "2026-10-22T00:00:00", id="noms-fr"),
        pytest.param("d MMM yyyy", "fr-FR", "22 oct. 2026", "2026-10-22T00:00:00", id="mois-abrege-fr"),
        pytest.param("dddd, MMMM d, yyyy", "en-US", "Thursday, October 22, 2026", "2026-10-22T00:00:00", id="noms-en"),
        pytest.param("MM/dd/yyyy h:mm tt", "en-US", "10/22/2026 2:05 PM", "2026-10-22T14:05:00", id="12h-pm"),
        pytest.param("MM/dd/yyyy h:mm tt", "en-US", "10/22/2026 2:05 AM", "2026-10-22T02:05:00", id="12h-am"),
        pytest.param("MM/dd/yyyy h:mm tt", "en-US", "10/22/2026 12:05 AM", "2026-10-22T00:05:00", id="12h-minuit"),
        pytest.param("dd/MM/yy", "", "22/10/26", "2026-10-22T00:00:00", id="annee-deux-chiffres-2000"),
        pytest.param("dd/MM/yy", "", "22/10/75", "1975-10-22T00:00:00", id="annee-deux-chiffres-1900"),
        pytest.param("HH:mm:ss", "", "14:05:09", "1970-01-01T14:05:09", id="heure-seule-date-epoque"),
        pytest.param("dd/MM/yyyy HH:mm:ss.fff", "", "22/10/2026 14:05:09.250", "2026-10-22T14:05:09.250000", id="millisecondes"),
        pytest.param("d", "fr-FR", "22/10/2026", "2026-10-22T00:00:00", id="masque-standard-d-fr"),
        pytest.param("d", "en-US", "10/22/2026", "2026-10-22T00:00:00", id="masque-standard-d-us"),
        pytest.param("s", "", "2026-10-22T14:05:09", "2026-10-22T14:05:09", id="masque-standard-s"),
    ],
)
def test_parsedate_masque_explicite(mask, culture, value, expected) -> None:
    template = '{ "r": parsedate($.s, "' + culture + '", "' + mask + '") }'
    assert run(template, {"s": value}) == expected


def test_parsedate_separateur_de_date_suit_la_culture() -> None:
    # Le '/' d'un masque est le séparateur de date de la culture (règle .NET),
    # comme à l'écriture dans `format` : de-DE écrit et lit donc '22.10.2026'.
    assert run('{ "r": parsedate($.s, "de-DE", "dd/MM/yyyy") }', {"s": "22.10.2026"}) == "2026-10-22T00:00:00"


@pytest.mark.parametrize(
    ("mask", "value"),
    [
        pytest.param("dd/MM/yyyy", "2/10/2026", id="dd-exige-deux-chiffres"),
        pytest.param("yyyy-MM-dd", "26-10-22", id="yyyy-exige-quatre-chiffres"),
        pytest.param("dd/MM/yyyy", "22/10/2026 14:05", id="texte-en-trop"),
        pytest.param("dd/MM/yyyy HH:mm", "22/10/2026", id="texte-manquant"),
        pytest.param("dd/MM/yyyy", "22-10-2026", id="separateur-different"),
        pytest.param("dddd d MMMM yyyy", "jeudi 22 ocotbre 2026", id="nom-de-mois-inconnu"),
        pytest.param("dd/MM/yyyy", "32/10/2026", id="jour-hors-bornes"),
    ],
)
def test_parsedate_masque_non_respecte_leve(mask, value) -> None:
    with pytest.raises(JsltError):
        run('{ "r": parsedate($.s, "", "' + mask + '") }', {"s": value})


def test_parsedate_masque_inconnu_leve() -> None:
    with pytest.raises(JsltError, match="masque"):
        run('{ "r": parsedate($.s, "", "Q") }', {"s": "22/10/2026"})


def test_parsedate_masque_vide_garde_la_detection_automatique() -> None:
    assert run('{ "r": parsedate($.s, "fr-FR", "") }', {"s": "22/10/2026"}) == "2026-10-22T00:00:00"


# --- parsedate : fuseau -------------------------------------------------------


@pytest.mark.parametrize(
    ("zone", "value", "expected"),
    [
        pytest.param("Europe/Paris", "2026-11-10T08:30:00", "2026-11-10T08:30:00+01:00", id="naif-hiver"),
        pytest.param("Europe/Paris", "2026-07-10T08:30:00", "2026-07-10T08:30:00+02:00", id="naif-ete"),
        pytest.param("Europe/Paris", "2026-11-10T07:30:00Z", "2026-11-10T08:30:00+01:00", id="converti-depuis-utc"),
        pytest.param("UTC", "2026-11-10T08:30:00+01:00", "2026-11-10T07:30:00+00:00", id="converti-vers-utc"),
        pytest.param("Z", "2026-11-10T08:30:00+01:00", "2026-11-10T07:30:00+00:00", id="z-vaut-utc"),
        pytest.param("+02:00", "2026-11-10T08:30:00", "2026-11-10T08:30:00+02:00", id="decalage-fixe"),
        pytest.param("-0500", "2026-11-10T08:30:00", "2026-11-10T08:30:00-05:00", id="decalage-fixe-compact"),
        pytest.param("+02:00", "2026-11-10T08:30:00Z", "2026-11-10T10:30:00+02:00", id="decalage-fixe-conversion"),
    ],
)
def test_parsedate_fuseau(zone, value, expected) -> None:
    assert run('{ "r": parsedate($.s, "", "", "' + zone + '") }', {"s": value}) == expected


def test_parsedate_fuseau_avec_masque() -> None:
    template = '{ "r": parsedate($.s, "fr-FR", "dd/MM/yyyy HH:mm", "Europe/Paris") }'
    assert run(template, {"s": "22/10/2026 14:05"}) == "2026-10-22T14:05:00+02:00"


def test_parsedate_sans_fuseau_reste_naif() -> None:
    assert run('{ "r": parsedate($.s, "") }', {"s": "2026-11-10T08:30:00"}) == "2026-11-10T08:30:00"


def test_parsedate_sans_fuseau_garde_le_decalage_de_lentree() -> None:
    assert run('{ "r": parsedate($.s, "") }', {"s": "2026-11-10T08:30:00+01:00"}) == "2026-11-10T08:30:00+01:00"


def test_parsedate_fuseau_inconnu_leve() -> None:
    with pytest.raises(JsltError, match="fuseau"):
        run('{ "r": parsedate($.s, "", "", "Europe/Atlantis") }', {"s": "2026-11-10T08:30:00"})


# --- dateadd / datesub -------------------------------------------------------


@pytest.mark.parametrize(
    ("unit", "amount", "expected"),
    [
        pytest.param("second", 30, "2026-11-10T08:30:30", id="seconde"),
        pytest.param("minute", 45, "2026-11-10T09:15:00", id="minute"),
        pytest.param("hour", 20, "2026-11-11T04:30:00", id="heure-change-le-jour"),
        pytest.param("day", 21, "2026-12-01T08:30:00", id="jour-change-le-mois"),
        pytest.param("week", 2, "2026-11-24T08:30:00", id="semaine"),
        pytest.param("month", 3, "2027-02-10T08:30:00", id="mois-change-lannee"),
        pytest.param("year", 4, "2030-11-10T08:30:00", id="annee"),
        pytest.param("day", -11, "2026-10-30T08:30:00", id="montant-negatif-retranche"),
        pytest.param("month", 0, "2026-11-10T08:30:00", id="montant-nul"),
    ],
)
def test_dateadd(unit, amount, expected) -> None:
    template = '{ "r": dateadd($.d, "' + unit + '", ' + str(amount) + ') }'
    assert run(template, {"d": "2026-11-10T08:30:00"}) == expected


@pytest.mark.parametrize(
    ("unit", "amount", "expected"),
    [
        pytest.param("week", 2, "2026-10-27T08:30:00", id="semaine"),
        pytest.param("month", 11, "2025-12-10T08:30:00", id="mois-change-lannee"),
        pytest.param("second", 30, "2026-11-10T08:29:30", id="seconde"),
        pytest.param("day", -5, "2026-11-15T08:30:00", id="montant-negatif-ajoute"),
    ],
)
def test_datesub(unit, amount, expected) -> None:
    template = '{ "r": datesub($.d, "' + unit + '", ' + str(amount) + ') }'
    assert run(template, {"d": "2026-11-10T08:30:00"}) == expected


@pytest.mark.parametrize(
    ("value", "unit", "amount", "expected"),
    [
        pytest.param("2026-01-31T00:00:00", "month", 1, "2026-02-28T00:00:00", id="31-janvier-plus-un-mois"),
        pytest.param("2024-01-31T00:00:00", "month", 1, "2024-02-29T00:00:00", id="annee-bissextile"),
        pytest.param("2026-03-31T00:00:00", "month", -1, "2026-02-28T00:00:00", id="31-mars-moins-un-mois"),
        pytest.param("2024-02-29T00:00:00", "year", 1, "2025-02-28T00:00:00", id="29-fevrier-plus-un-an"),
        pytest.param("2026-05-31T00:00:00", "month", 13, "2027-06-30T00:00:00", id="plus-de-douze-mois"),
    ],
)
def test_dateadd_borne_le_jour_sur_les_mois_courts(value, unit, amount, expected) -> None:
    template = '{ "r": dateadd($.d, "' + unit + '", ' + str(amount) + ') }'
    assert run(template, {"d": value}) == expected


def test_dateadd_conserve_le_decalage() -> None:
    template = '{ "r": dateadd($.d, "hour", 2) }'
    assert run(template, {"d": "2026-11-10T08:30:00+01:00"}) == "2026-11-10T10:30:00+01:00"


def test_dateadd_conserve_la_precision_fractionnaire() -> None:
    template = '{ "r": dateadd($.d, "day", 1) }'
    assert run(template, {"d": "2026-11-10T08:30:00.250000"}) == "2026-11-11T08:30:00.250000"


@pytest.mark.parametrize("unit", ["days", "MONTHS", "Year", "seconds"])
def test_dateadd_accepte_pluriel_et_casse(unit) -> None:
    template = '{ "r": dateadd($.d, "' + unit + '", 1) }'
    assert isinstance(run(template, {"d": "2026-11-10T08:30:00"}), str)


def test_dateadd_unite_inconnue_leve_en_listant_les_unites() -> None:
    with pytest.raises(JsltError, match="week"):
        run('{ "r": dateadd($.d, "fortnight", 1) }', {"d": "2026-11-10T08:30:00"})


def test_dateadd_montant_fractionnaire_leve() -> None:
    with pytest.raises(JsltError, match="entier"):
        run('{ "r": dateadd($.d, "day", 1.5) }', {"d": "2026-11-10T08:30:00"})


def test_dateadd_montant_non_numerique_leve() -> None:
    with pytest.raises(JsltError, match="entier"):
        run('{ "r": dateadd($.d, "day", "demain") }', {"d": "2026-11-10T08:30:00"})


# --- datepart ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("part", "expected"),
    [
        pytest.param("year", 2026, id="annee"),
        pytest.param("month", 11, id="mois"),
        pytest.param("day", 10, id="jour"),
        pytest.param("dayofweek", 2, id="jour-de-semaine-mardi"),
        pytest.param("hour", 8, id="heure"),
        pytest.param("minute", 30, id="minute"),
        pytest.param("second", 9, id="seconde"),
    ],
)
def test_datepart(part, expected) -> None:
    template = '{ "r": datepart($.d, "' + part + '") }'
    assert run(template, {"d": "2026-11-10T08:30:09"}) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("2026-11-08T00:00:00", 0, id="dimanche-vaut-zero"),
        pytest.param("2026-11-09T00:00:00", 1, id="lundi-vaut-un"),
        pytest.param("2026-11-14T00:00:00", 6, id="samedi-vaut-six"),
    ],
)
def test_datepart_dayofweek_convention_dotnet(value, expected) -> None:
    # Convention .NET ``DayOfWeek`` (dimanche = 0), pas ISO (lundi = 1).
    assert run('{ "r": datepart($.d, "dayofweek") }', {"d": value}) == expected


def test_datepart_sur_une_date_seule() -> None:
    assert run('{ "r": datepart($.d, "hour") }', {"d": "2026-11-10"}) == 0


def test_datepart_partie_inconnue_leve_en_listant_les_parties() -> None:
    # `quarter` tenait ce rôle avant de devenir une partie reconnue : le message
    # doit toujours énumérer les parties disponibles.
    with pytest.raises(JsltError, match="dayofweek"):
        run('{ "r": datepart($.d, "fortnight") }', {"d": "2026-11-10T08:30:00"})


# --- null et valeurs non datables --------------------------------------------


@pytest.mark.parametrize(
    "template",
    [
        '{ "r": dateadd($.d, "day", 1) }',
        '{ "r": datesub($.d, "day", 1) }',
        '{ "r": datepart($.d, "year") }',
    ],
)
def test_null_rend_null(template) -> None:
    assert run(template, {"d": None}) is None


@pytest.mark.parametrize(
    "template",
    [
        '{ "r": dateadd($.d, "day", 1) }',
        '{ "r": datesub($.d, "day", 1) }',
        '{ "r": datepart($.d, "year") }',
    ],
)
@pytest.mark.parametrize("value", ["pas une date", 42, True, [1], {"a": 1}])
def test_valeur_non_datable_leve(template, value) -> None:
    # Pas de repli silencieux : une valeur qui n'est pas une date ISO est une
    # erreur de données, la masquer en null la ferait découvrir bien plus loin.
    with pytest.raises(JsltError, match="date"):
        run(template, {"d": value})


# --- chaînage avec les fonctions existantes ----------------------------------


def test_chainage_parsedate_dateadd_format() -> None:
    template = (
        '{ "r": format(dateadd(parsedate($.d, "fr-FR"), "month", 1), "dddd d MMMM yyyy", "fr-FR") }'
    )
    assert run(template, {"d": "22/10/2026"}) == "dimanche 22 novembre 2026"


def test_datepart_sur_le_resultat_de_parsedate_avec_fuseau() -> None:
    template = '{ "r": datepart(parsedate($.d, "", "", "Europe/Paris"), "hour") }'
    assert run(template, {"d": "2026-11-10T07:30:00Z"}) == 8


# --- datediff ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("end", "unit", "expected"),
    [
        pytest.param("2026-11-10T08:30:00", "day", 0, id="meme-instant"),
        pytest.param("2026-11-10T08:30:30", "second", 30, id="secondes"),
        pytest.param("2026-11-10T09:15:00", "minute", 45, id="minutes"),
        pytest.param("2026-11-11T04:30:00", "hour", 20, id="heures"),
        pytest.param("2026-12-01T08:30:00", "day", 21, id="jours-sur-deux-mois"),
        pytest.param("2026-11-24T08:30:00", "week", 2, id="semaines"),
        pytest.param("2027-02-10T08:30:00", "month", 3, id="mois-sur-deux-annees"),
        pytest.param("2030-11-10T08:30:00", "year", 4, id="annees"),
    ],
)
def test_datediff(end, unit, expected) -> None:
    template = '{ "r": datediff($.a, $.b, "' + unit + '") }'
    assert run(template, {"a": "2026-11-10T08:30:00", "b": end}) == expected


@pytest.mark.parametrize(
    ("start", "end", "unit", "expected"),
    [
        pytest.param("2026-11-10T00:00:00", "2026-11-23T23:00:00", "week", 1, id="13-jours-font-1-semaine"),
        pytest.param("2026-11-10T08:00:00", "2026-11-11T07:59:00", "day", 0, id="moins-de-24h-fait-0-jour"),
        pytest.param("2026-01-31T00:00:00", "2026-03-01T00:00:00", "month", 1, id="un-mois-et-un-jour"),
        pytest.param("2026-01-31T00:00:00", "2026-02-28T00:00:00", "month", 0, id="mois-incomplet"),
        pytest.param("2024-02-29T00:00:00", "2025-02-28T00:00:00", "year", 0, id="annee-incomplete"),
        pytest.param("2024-02-29T00:00:00", "2025-03-01T00:00:00", "year", 1, id="annee-complete"),
        pytest.param("2026-11-10T08:00:00", "2026-12-10T07:00:00", "month", 0, id="mois-a-une-heure-pres"),
    ],
)
def test_datediff_compte_les_unites_entieres(start, end, unit, expected) -> None:
    template = '{ "r": datediff($.a, $.b, "' + unit + '") }'
    assert run(template, {"a": start, "b": end}) == expected


@pytest.mark.parametrize(
    ("start", "end", "unit", "expected"),
    [
        pytest.param("2026-11-10T08:30:00", "2026-11-09T08:30:00", "day", -1, id="un-jour-avant"),
        pytest.param("2026-11-10T08:30:00", "2026-11-09T20:30:00", "day", 0, id="douze-heures-avant"),
        pytest.param("2026-11-10T08:30:00", "2026-11-08T20:30:00", "day", -1, id="trente-six-heures-avant"),
        pytest.param("2027-02-10T08:30:00", "2026-11-10T08:30:00", "month", -3, id="trois-mois-avant"),
        pytest.param("2026-03-01T00:00:00", "2026-01-31T00:00:00", "month", -1, id="mois-negatif-incomplet"),
    ],
)
def test_datediff_negatif_tronque_vers_zero(start, end, unit, expected) -> None:
    # Troncature vers zéro, pas vers moins l'infini : -36 h font -1 jour et
    # -12 h en font 0, comme +36 h font 1 et +12 h font 0.
    template = '{ "r": datediff($.a, $.b, "' + unit + '") }'
    assert run(template, {"a": start, "b": end}) == expected


def test_datediff_entre_deux_decalages_differents() -> None:
    template = '{ "r": datediff($.a, $.b, "hour") }'
    # 08:30+01:00 et 08:30+02:00 sont à une heure d'écart réel.
    assert run(template, {"a": "2026-11-10T08:30:00+01:00", "b": "2026-11-10T08:30:00+02:00"}) == -1


def test_datediff_mois_entre_deux_decalages_differents() -> None:
    template = '{ "r": datediff($.a, $.b, "month") }'
    assert run(template, {"a": "2026-11-10T00:30:00+01:00", "b": "2026-12-09T23:45:00-01:00"}) == 1


@pytest.mark.parametrize("unit", ["day", "month"])
def test_datediff_refuse_de_melanger_avec_et_sans_fuseau(unit) -> None:
    template = '{ "r": datediff($.a, $.b, "' + unit + '") }'
    with pytest.raises(JsltError, match="fuseau"):
        run(template, {"a": "2026-11-10T08:30:00+01:00", "b": "2026-12-10T08:30:00"})


def test_datediff_unite_inconnue_leve_en_listant_les_unites() -> None:
    with pytest.raises(JsltError, match="week"):
        run('{ "r": datediff($.a, $.b, "fortnight") }', {"a": "2026-11-10", "b": "2026-11-11"})


def test_datediff_unite_absente_leve() -> None:
    with pytest.raises(JsltError, match="unité"):
        run('{ "r": datediff($.a, $.b) }', {"a": "2026-11-10", "b": "2026-11-11"})


@pytest.mark.parametrize("source", [{"a": None, "b": "2026-11-10"}, {"a": "2026-11-10", "b": None}])
def test_datediff_null_rend_null(source) -> None:
    assert run('{ "r": datediff($.a, $.b, "day") }', source) is None


def test_datediff_valeur_non_datable_leve() -> None:
    with pytest.raises(JsltError, match="date"):
        run('{ "r": datediff($.a, $.b, "day") }', {"a": "2026-11-10", "b": "pas une date"})


def test_datediff_inverse_dateadd_sur_les_unites_fixes() -> None:
    template = '{ "r": datediff($.d, dateadd($.d, "week", 6), "week") }'
    assert run(template, {"d": "2026-11-10T08:30:00"}) == 6
