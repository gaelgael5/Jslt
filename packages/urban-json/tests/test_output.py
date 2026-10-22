"""Directive ``$directives.output`` et ``JsltTemplate.render`` (port de ``ApplyOutput``,
``CustomServices/Outputs.cs`` : ``to_json`` / ``to_block``)."""

from __future__ import annotations

import json

import pytest

from urban_json import (
    FunctionRegistry,
    JsltError,
    JsltSemanticError,
    JsltTemplate,
    default_registry,
)


def render(template: str, source=None, *, build: bool = False) -> str:
    parsed = JsltTemplate.parse(template)
    text = parsed.render(source if source is not None else {})
    if build:  # le chemin compilé doit rendre exactement le même texte
        assert parsed.build().render(source if source is not None else {}) == text
    return text


def directive(output: str) -> str:
    return '"$directives": { "output": ' + output + " }"


# --- la directive n'est jamais dans le résultat ------------------------------------------


def test_directive_absente_du_resultat_de_transform() -> None:
    template = JsltTemplate.parse('{ ' + directive('{ "mode": to_json() }') + ', "a": $.x }')
    assert template.transform({"x": 1}) == {"a": 1}
    assert template.build().transform({"x": 1}) == {"a": 1}


def test_directive_autres_cles_ignorees() -> None:
    template = JsltTemplate.parse('{ "$DIRECTIVES": { "culture": "fr-FR", "packages": [] }, "a": 1 }')
    assert template.transform({}) == {"a": 1}
    assert template.render({}) == '{\n  "a": 1\n}'


def test_directive_re_serialisee_par_to_source() -> None:
    source = '{ ' + directive('{ "filter": $.a, "mode": to_block() }') + ', "a": [ { "k": 1 } ] }'
    template = JsltTemplate.parse(source)
    again = JsltTemplate.parse(template.to_source())
    assert again.render({}) == template.render({}) == '{"k":1}\n'


# --- render ------------------------------------------------------------------------


def test_render_sans_directive_json_indente() -> None:
    assert render('{ "a": [1, 2], "b": "é" }') == '{\n  "a": [\n    1,\n    2\n  ],\n  "b": "é"\n}'


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ("", '{"a":1,"b":"","c":null}\n'),
        ("false", '{"a":1,"b":"","c":null}\n'),
        ("true", '{\n  "a": 1,\n  "b": "",\n  "c": null\n}\n'),
        ("false, true", '{"a":1}\n'),
    ],
)
def test_to_json(args, expected) -> None:
    template = '{ ' + directive('{ "mode": to_json(' + args + ") }") + ', "a": 1, "b": "", "c": null }'
    assert render(template, build=True) == expected


def test_to_json_ignore_null_recursif_tableaux_gardes() -> None:
    template = (
        '{ ' + directive('{ "mode": to_json(false, true) }')
        + ', "o": { "k": "", "v": 2, "n": null }, "t": [ "", null, 3, { "z": null } ] }'
    )
    assert json.loads(render(template)) == {"o": {"v": 2}, "t": [None, None, 3, {}]}


def test_to_json_ne_modifie_pas_le_resultat() -> None:
    template = JsltTemplate.parse('{ ' + directive('{ "mode": to_json(false, true) }') + ', "a": $.v }')
    source = {"v": ""}
    template.render(source)
    assert source == {"v": ""}
    assert template.transform(source) == {"a": ""}


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ('"t": [ { "a": 1 }, { "a": 2 } ]', '{"a":1}\n{"a":2}\n'),
        ('"t": []', ""),
        ('"t": { "a": 1 }', '{"a":1}\n'),
        ('"t": 3', ""),
    ],
)
def test_to_block(body, expected) -> None:
    template = '{ ' + directive('{ "filter": $.t, "mode": to_block() }') + ", " + body + " }"
    assert render(template, build=True) == expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("$.a", "1\n"),  # 1 nœud -> ce nœud
        ("$.l[*]", "[1,2]\n"),  # plusieurs -> tableau
        ("$.absent", "null\n"),  # aucun -> null
        ('"$.a"', "1\n"),  # chemin en chaîne (forme .NET)
    ],
)
def test_filter(path, expected) -> None:
    template = '{ ' + directive('{ "filter": ' + path + ', "mode": to_json() }') + ', "a": 1, "l": [1, 2] }'
    assert render(template, build=True) == expected


def test_arguments_de_mode_evalues() -> None:
    template = '{ ' + directive('{ "mode": to_json($.indente) }') + ', "a": 1 }'
    assert render(template, {"indente": True}) == '{\n  "a": 1\n}\n'


def test_registre_isole() -> None:
    template = JsltTemplate.parse('{ ' + directive('{ "mode": to_json() }') + ', "a": 1 }')
    with pytest.raises(JsltError, match="fonction de sortie inconnue : to_json"):
        template.render({}, functions=FunctionRegistry())
    assert template.render({}, functions=default_registry.copy()) == '{"a":1}\n'


# --- erreurs -----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("template", "error", "message"),
    [
        ('{ "a": to_json() }', JsltError, "fonction de sortie"),
        ('{ "a": to_block() }', JsltError, r'"\$directives"'),
        ('{ ' + directive('{ "mode": upper("x") }') + " }", JsltError, "n'est pas une fonction de sortie"),
        ('{ ' + directive('{ "mode": inconnue() }') + " }", JsltError, "fonction de sortie inconnue"),
    ],
)
def test_erreurs_a_l_execution(template, error, message) -> None:
    parsed = JsltTemplate.parse(template)
    with pytest.raises(error, match=message):
        parsed.render({})


@pytest.mark.parametrize(
    ("template", "error", "message"),
    [
        ('{ ' + directive('{ "filter": $.a }') + " }", JsltSemanticError, "'mode'"),
        ('{ ' + directive('{ "mode": "to_json" }') + " }", JsltSemanticError, "fonction de sortie"),
        ('{ ' + directive("3") + " }", JsltSemanticError, "output' attend un objet"),
        ('{ "$directives": 3 }', JsltSemanticError, "attend un objet"),
        ('{ ' + directive('{ "mode": to_json(), "filter": 3 }') + " }", JsltSemanticError, "filter"),
        ('{ ' + directive('{ "mode": to_json(), "filter": "pas un chemin" }') + " }", JsltSemanticError, "JSONPath"),
        ('{ ' + directive('{ "mode": to_json(), "write": 1 }') + " }", NotImplementedError, "écriture"),
    ],
)
def test_erreurs_a_l_analyse(template, error, message) -> None:
    with pytest.raises(error, match=message):
        JsltTemplate.parse(template)


def test_trop_d_arguments() -> None:
    template = JsltTemplate.parse('{ ' + directive('{ "mode": to_block(1) }') + " }")
    with pytest.raises(JsltError, match="to_block attend au plus 0 argument"):
        template.render({})


# --- catalogue ---------------------------------------------------------------------


def test_catalogue_indique_le_kind() -> None:
    kinds = {entry["name"]: entry["kind"] for entry in default_registry.catalog()}
    assert kinds["to_json"] == kinds["to_block"] == "output"
    assert kinds["upper"] == "function"


def test_kind_inconnu_refuse() -> None:
    with pytest.raises(ValueError, match="kind"):
        FunctionRegistry().register("f", lambda ctx: None, kind="writer")


# --- exemple du guide ----------------------------------------------------------------


def test_exemple_du_guide() -> None:
    template = (
        '{ "$directives": { "output": { "filter": $.lignes, "mode": to_block() } },\n'
        '  "lignes": $.commandes[*] }'
    )
    assert render(template, {"commandes": [{"id": 1}, {"id": 2}]}) == '{"id":1}\n{"id":2}\n'
