"""Nombre d'arguments des fonctions : signature exacte au catalogue et refus
lisible d'un argument en trop.

Régression : les fonctions trigonométriques recevaient un paramètre caché
``_fn`` (la vraie opération) ; le catalogue affichait ``acos(token, _fn)`` et un
2e argument remplaçait l'opération (``'str' object is not callable``).
"""

from __future__ import annotations

import pytest

from urban_json import JsltError, JsltTemplate, default_registry

TRIGO = ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh"]


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source if source is not None else {})["r"]


@pytest.mark.parametrize("name", TRIGO)
def test_signature_trigo_sans_parametre_cache(name) -> None:
    info = {e["name"]: e for e in default_registry.catalog()}[name]
    assert [p["name"] for p in info["parameters"]] == ["token"]
    assert "_fn" not in info["signature"]


def test_aucun_parametre_prive_au_catalogue() -> None:
    leaks = [e["signature"] for e in default_registry.catalog() if any(p["name"].startswith("_") for p in e["parameters"])]
    assert leaks == []


def test_trigo_calcule_toujours() -> None:
    assert run('{ "r": acos($.x) }', {"x": 1}) == 0.0


@pytest.mark.parametrize(
    "template",
    [
        '{ "r": acos($.x, $.y) }',
        '{ "r": upper($.s, 1) }',
        '{ "r": pi(1) }',
    ],
)
def test_argument_en_trop_refuse_lisiblement(template) -> None:
    with pytest.raises(JsltError, match="argument"):
        run(template, {"x": 0.5, "y": "bonjour", "s": "a"})


def test_arguments_optionnels_toujours_acceptes() -> None:
    assert run('{ "r": trim($.s) }', {"s": " a "}) == "a"
    assert run('{ "r": trim($.s, "x") }', {"s": "xax"}) == "a"
