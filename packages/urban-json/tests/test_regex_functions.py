"""Fonctions regex ``regexismatch`` / ``regexmatches`` (port de ``Services.strings`` .NET).

Écarts volontaires vs .NET : ``null`` -> ``null`` (le .NET levait une
NullReferenceException) ; motif invalide -> ``JsltError`` (ArgumentException .NET).
"""

from __future__ import annotations

import pytest

from urban_json import JsltError, JsltTemplate


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source if source is not None else {})["r"]


@pytest.mark.parametrize(
    ("template", "source", "expected"),
    [
        pytest.param('{ "r": regexismatch($.s, "^[a-z]+@[a-z]+\\\\.fr$") }', {"s": "bob@ex.fr"}, True, id="match-email"),
        pytest.param('{ "r": regexismatch($.s, "^\\\\d+$") }', {"s": "12a"}, False, id="no-match"),
        pytest.param('{ "r": regexismatch($.s, "b") }', {"s": "abc"}, True, id="recherche-pas-ancree"),
        pytest.param('{ "r": regexismatch($.n, "^\\\\d{3}$") }', {"n": 123}, True, id="entier-converti-en-texte"),
        pytest.param('{ "r": regexismatch($.n, "^2\\\\.5$") }', {"n": 2.5}, True, id="flottant-converti-en-texte"),
        pytest.param('{ "r": regexismatch($.b, "^True$") }', {"b": True}, True, id="booleen-a-la-dotnet"),
        pytest.param('{ "r": regexismatch($.s, "x") }', {"s": None}, None, id="null"),
        pytest.param('{ "r": regexismatch($.o, "x") }', {"o": {"a": 1}}, None, id="objet-null"),
        pytest.param('{ "r": regexismatch($.s, "") }', {"s": ""}, True, id="motif-vide"),
    ],
)
def test_regexismatch(template, source, expected) -> None:
    assert run(template, source) == expected


@pytest.mark.parametrize(
    ("template", "source", "expected"),
    [
        pytest.param('{ "r": regexmatches($.s, "\\\\d+") }', {"s": "a1b22c333"}, ["1", "22", "333"], id="toutes"),
        pytest.param('{ "r": regexmatches($.s, "\\\\d+") }', {"s": "abc"}, [], id="aucune"),
        # Correspondance complète (Match.Value .NET), pas les groupes capturés.
        pytest.param('{ "r": regexmatches($.s, "(\\\\w)=(\\\\d)") }', {"s": "a=1 b=2"}, ["a=1", "b=2"], id="groupes-ignores"),
        pytest.param('{ "r": regexmatches($.n, "\\\\d") }', {"n": 405}, ["4", "0", "5"], id="nombre"),
        pytest.param('{ "r": regexmatches($.s, "x") }', {"s": None}, None, id="null"),
        pytest.param('{ "r": regexmatches($.a, "x") }', {"a": ["x"]}, None, id="tableau-null"),
        # Syntaxe .NET des groupes nommés, traduite ; lookbehind laissé intact.
        pytest.param('{ "r": regexmatches($.s, "(?<k>\\\\w)=\\\\d") }', {"s": "a=1 b=2"}, ["a=1", "b=2"], id="groupe-nomme-dotnet"),
        pytest.param('{ "r": regexmatches($.s, "(?<=\\\\$)\\\\d+") }', {"s": "$12 et 7"}, ["12"], id="lookbehind"),
        pytest.param('{ "r": regexmatches($.s, "(?<!\\\\d)\\\\d") }', {"s": "12 3"}, ["1", "3"], id="lookbehind-negatif"),
    ],
)
def test_regexmatches(template, source, expected) -> None:
    assert run(template, source) == expected


@pytest.mark.parametrize("name", ["regexismatch", "regexmatches"])
def test_motif_invalide_leve_une_erreur_claire(name) -> None:
    with pytest.raises(JsltError, match="regex"):
        run(f'{{ "r": {name}($.s, "(abc") }}', {"s": "abc"})


def test_regex_au_catalogue() -> None:
    from urban_json import default_registry

    names = {e["name"] for e in default_registry.catalog()}
    assert {"regexismatch", "regexmatches"} <= names
