"""Fonctions .NET portées : any, contains, selectany, normalize, parsedate.

Sources .NET : ``Services.distinct.cs`` (any/contains/selectany),
``Services.strings.cs`` (normalize), ``Services.cs`` (parsedate).
"""

from __future__ import annotations

import pytest

from urban_json import JsltError, JsltTemplate


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source if source is not None else {})["r"]


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        pytest.param({"a": [1]}, True, id="tableau-non-vide"),
        pytest.param({"a": []}, False, id="tableau-vide"),
        pytest.param({"a": None}, False, id="null"),
        pytest.param({}, False, id="absent"),
        pytest.param({"a": "abc"}, False, id="chaine-pas-un-tableau"),
        pytest.param({"a": {"k": 1}}, False, id="objet-pas-un-tableau"),
    ],
)
def test_any(source, expected) -> None:
    assert run('{ "r": any($.a) }', source) is expected


@pytest.mark.parametrize(
    ("template", "source", "expected"),
    [
        pytest.param('{ "r": contains($.a, "b") }', {"a": ["a", "b"]}, True, id="chaine"),
        pytest.param('{ "r": contains($.a, "z") }', {"a": ["a", "b"]}, False, id="absente"),
        pytest.param('{ "r": contains($.a, 2) }', {"a": [1, 2]}, True, id="nombre"),
        # Égalité de l'opérateur == du langage : "2" == 2 est vrai côté chaîne.
        pytest.param('{ "r": contains($.a, 2) }', {"a": ["2"]}, True, id="egalite-du-langage"),
        pytest.param('{ "r": contains($.a, $.x) }', {"a": [1, None], "x": None}, True, id="null"),
        pytest.param('{ "r": contains($.a, 1) }', {"a": []}, False, id="vide"),
        pytest.param('{ "r": contains($.a, "a") }', {"a": "abc"}, False, id="pas-un-tableau"),
    ],
)
def test_contains(template, source, expected) -> None:
    assert run(template, source) is expected


@pytest.mark.parametrize(
    ("template", "source", "expected"),
    [
        pytest.param('{ "r": selectany($.a, "$[?(@.x > 1)]") }', {"a": [{"x": 1}, {"x": 3}]}, True, id="filtre-vrai"),
        pytest.param('{ "r": selectany($.a, "$[?(@.x > 5)]") }', {"a": [{"x": 1}, {"x": 3}]}, False, id="filtre-faux"),
        pytest.param('{ "r": selectany($.o, "$.k") }', {"o": {"k": 0}}, True, id="valeur-falsy-trouvee"),
        pytest.param('{ "r": selectany($.o, "$.z") }', {"o": {"k": 1}}, False, id="chemin-absent"),
        pytest.param('{ "r": selectany($.o, "$..id") }', {"o": {"a": {"id": 1}}}, True, id="descente"),
        pytest.param('{ "r": selectany($.n, "$.k") }', {"n": None}, False, id="source-null"),
    ],
)
def test_selectany(template, source, expected) -> None:
    assert run(template, source) is expected


def test_selectany_chemin_invalide() -> None:
    with pytest.raises(JsltError, match="chemin"):
        run('{ "r": selectany($.a, "pas un chemin") }', {"a": [1]})


def test_distinct_accepte_un_chemin_en_chaine() -> None:
    # Le .NET reçoit le chemin en chaîne ; avant, le portage levait AttributeError.
    source = {"a": [{"k": 1}, {"k": 2}, {"k": 1}]}
    assert run('{ "r": distinct($.a, "$..k") }', source) == [1, 2]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        # « é » décomposé (e + accent combinant) -> composé (forme C, défaut .NET).
        pytest.param("été", "été", id="compose"),
        pytest.param("deja", "deja", id="inchange"),
        pytest.param(None, None, id="null"),
        pytest.param(12, False, id="pas-une-chaine"),
    ],
)
def test_normalize(value, expected) -> None:
    assert run('{ "r": normalize($.s) }', {"s": value}) == expected


@pytest.mark.parametrize(
    ("template", "value", "expected"),
    [
        pytest.param('parsedate($.s, "")', "2026-10-22", "2026-10-22T00:00:00", id="iso-date"),
        pytest.param('parsedate($.s, "")', "2026-10-22T08:15:30", "2026-10-22T08:15:30", id="iso-datetime"),
        pytest.param('parsedate($.s, "")', "10/22/2026", "2026-10-22T00:00:00", id="invariante-mois-jour"),
        pytest.param('parsedate($.s, "fr-FR")', "22/10/2026", "2026-10-22T00:00:00", id="fr-jour-mois"),
        pytest.param('parsedate($.s, "fr-FR")', "22/10/2026 14:05", "2026-10-22T14:05:00", id="fr-avec-heure"),
        pytest.param('parsedate($.s, "de-DE")', "22.10.2026", "2026-10-22T00:00:00", id="de-points"),
        pytest.param('parsedate($.s, "en-US")', "10/22/2026 2:05:09", "2026-10-22T02:05:09", id="us-heure"),
        pytest.param('parsedate($.s, "")', 42, 42, id="non-chaine-rendue-telle-quelle"),
        pytest.param('parsedate($.s, "")', None, None, id="null"),
    ],
)
def test_parsedate(template, value, expected) -> None:
    assert run(f'{{ "r": {template} }}', {"s": value}) == expected


@pytest.mark.parametrize("value", ["pas une date", "31/02/2026", "2026-13-01"])
def test_parsedate_invalide(value) -> None:
    with pytest.raises(JsltError, match="date"):
        run('{ "r": parsedate($.s, "fr-FR") }', {"s": value})
