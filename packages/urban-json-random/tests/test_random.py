"""Fonctions getrandom_* : on vérifie formats, types et bornes (les valeurs sont
aléatoires), sur plusieurs tirages pour rendre visibles les bornes fausses."""

from __future__ import annotations

import base64
import ipaddress
import re
from datetime import datetime

import pytest
from urban_json import FunctionRegistry, JsltError, JsltTemplate

from urban_json_random import NAUGHTY_STRINGS, register

DRAWS = 200


@pytest.fixture(scope="module")
def registry() -> FunctionRegistry:
    reg = FunctionRegistry()
    register(reg)
    return reg


def run(registry, expression: str, source=None):
    template = JsltTemplate.parse(f'{{ "r": {expression} }}')
    return template.transform(source or {}, functions=registry)["r"]


def draws(registry, expression: str, source=None, n: int = DRAWS) -> list:
    return [run(registry, expression, source) for _ in range(n)]


# --- nombres -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("expression", "low", "high", "kind"),
    [
        ("getrandom_integer(1, false, 6, false)", 1, 6, int),
        ("getrandom_integer(1, true, 6, true)", 2, 5, int),  # bornes exclues (JSON Schema)
        ("getrandom_long(-5, false, 5, false)", -5, 5, int),
        ("getrandom_short(10, false, 12, false)", 10, 12, int),
        ("getrandom_byte(250, false, 255, false)", 250, 255, int),
        ("getrandom_double(0.5, false, 0.75, false)", 0.5, 0.75, float),
        ("getrandom_float(-1, false, 1, false)", -1.0, 1.0, float),
    ],
)
def test_nombres_dans_les_bornes(registry, expression, low, high, kind) -> None:
    values = draws(registry, expression)
    assert all(isinstance(v, kind) and not isinstance(v, bool) for v in values)
    assert all(low <= v <= high for v in values)
    if kind is int:
        assert set(values) == set(range(low, high + 1)), "toutes les valeurs de l'intervalle doivent sortir"


def test_double_bornes_exclues(registry) -> None:
    values = draws(registry, "getrandom_double(0, true, 1, true)")
    assert all(0 < v < 1 for v in values)


@pytest.mark.parametrize(
    ("expression", "low", "high"),
    [
        ("getrandom_integer()", 0, 2**31 - 1),
        ("getrandom_long()", 0, 2**63 - 1),
        ("getrandom_short()", 0, 2**15 - 1),
        ("getrandom_byte()", 0, 255),
        ("getrandom_double()", 0.0, 1.0),
    ],
)
def test_bornes_par_defaut(registry, expression, low, high) -> None:
    values = draws(registry, expression, n=50)
    assert all(low <= v <= high for v in values)
    assert len(set(values)) > 1, "sans bornes, le résultat ne doit pas être constant"


@pytest.mark.parametrize(
    "expression",
    ["getrandom_integer(10, false, 1, false)", "getrandom_integer(3, true, 4, true)", "getrandom_byte(300)"],
)
def test_intervalle_impossible(registry, expression) -> None:
    with pytest.raises(JsltError, match="getrandom"):
        run(registry, expression)


# --- texte ---------------------------------------------------------------------


def test_string_longueur(registry) -> None:
    values = draws(registry, "getrandom_string(3, 8)")
    assert all(isinstance(v, str) and 3 <= len(v) <= 8 for v in values)
    assert all(re.fullmatch(r"[A-Za-z0-9 ]+", v) for v in values)


def test_string_longueur_par_defaut(registry) -> None:
    values = draws(registry, "getrandom_string()")
    assert all(1 <= len(v) <= 6 for v in values)  # min 1, max min + 5 (comme le .NET)


def test_string_motif_regex(registry) -> None:
    values = draws(registry, 'getrandom_string(0, 0, "^[A-Z]{3}-\\\\d{4}$")')
    assert all(re.fullmatch(r"[A-Z]{3}-\d{4}", v) for v in values)


def test_string_motif_invalide(registry) -> None:
    with pytest.raises(JsltError, match="motif"):
        run(registry, 'getrandom_string(1, 2, "(")')


def test_lipsum(registry) -> None:
    text = run(registry, "getrandom_lipsum(3)")
    assert len([p for p in text.split("\n") if p.strip()]) == 3
    assert len(run(registry, "getrandom_lipsum(0)").split("\n")) == 1  # 0 -> 1 paragraphe


def test_password(registry) -> None:
    values = draws(registry, 'getrandom_password(null, 20)', n=50)
    assert all(len(v) == 20 for v in values)
    assert len(set(values)) == 50
    assert all(len(v) == 12 for v in draws(registry, "getrandom_password(null, 0)", n=10))  # 0 -> 12


def test_naughtystrings(registry) -> None:
    values = draws(registry, "getrandom_naughtystrings()")
    assert all(v in NAUGHTY_STRINGS for v in values)
    assert len(set(values)) > 5


# --- personnes, lieux, réseau, banque --------------------------------------------


@pytest.mark.parametrize(
    "name", ["getrandom_firstname", "getrandom_lastname", "getrandom_city", "getrandom_country"]
)
def test_textes_non_vides(registry, name) -> None:
    values = draws(registry, f"{name}()", n=30)
    assert all(isinstance(v, str) and v.strip() for v in values)
    assert len(set(values)) > 3


def test_fullname(registry) -> None:
    assert all(len(v.split()) >= 2 for v in draws(registry, "getrandom_fullname()", n=30))


def test_email(registry) -> None:
    assert all(re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", v) for v in draws(registry, "getrandom_email()", n=30))


def test_ip(registry) -> None:
    for v in draws(registry, "getrandom_ipv4()", n=30):
        assert isinstance(ipaddress.ip_address(v), ipaddress.IPv4Address)
    for v in draws(registry, "getrandom_ipv6()", n=30):
        assert isinstance(ipaddress.ip_address(v), ipaddress.IPv6Address)
        assert v == v.upper()  # majuscules comme le .NET


def test_macaddress(registry) -> None:
    values = draws(registry, "getrandom_macaddress()")
    assert all(re.fullmatch(r"([0-9A-F]{2}:){5}[0-9A-F]{2}", v) for v in values)


def test_macaddress_bornes(registry) -> None:
    values = draws(registry, 'getrandom_macaddress("00:00:00:00:00:10", "00:00:00:00:00:12")')
    assert set(values) == {"00:00:00:00:00:10", "00:00:00:00:00:11", "00:00:00:00:00:12"}


def _iban_valide(iban: str) -> bool:
    raw = iban.replace(" ", "")
    moved = raw[4:] + raw[:4]
    digits = "".join(str(int(c, 36)) for c in moved)
    return int(digits) % 97 == 1


@pytest.mark.parametrize("country", ["FR", "DE", "GB", "ES", "IT", "NL", "BE"])
def test_iban_par_pays(registry, country) -> None:
    for v in draws(registry, f'getrandom_iban("{country}")', n=10):
        assert v.startswith(country) and _iban_valide(v)


def test_iban_bban_seul(registry) -> None:
    values = draws(registry, 'getrandom_iban("FR", false, true)', n=10)
    assert all(not v.startswith("FR") and v.isalnum() for v in values)


def test_iban_pays_inconnu(registry) -> None:
    with pytest.raises(JsltError, match="pays"):
        run(registry, 'getrandom_iban("ZZ")')


# --- dates, durées, binaire, booléen, liste -----------------------------------------


def test_datatime(registry) -> None:
    for v in draws(registry, "getrandom_datatime()", n=50):
        moment = datetime.fromisoformat(v)
        assert 1970 <= moment.year <= 2050


def test_timespan(registry) -> None:
    assert all(re.fullmatch(r"\d{2}:\d{2}:\d{2}\.\d{3}", v) for v in draws(registry, "getrandom_timespan()"))


def test_binary(registry) -> None:
    for v in draws(registry, "getrandom_binary(2, 4)"):
        assert 2 <= len(base64.b64decode(v)) <= 4


def test_boolean(registry) -> None:
    assert set(draws(registry, "getrandom_boolean()")) == {True, False}


def test_in_list(registry) -> None:
    values = draws(registry, "getrandom_in_list($.l)", {"l": ["a", 1, {"k": 2}]})
    assert all(v in ["a", 1, {"k": 2}] for v in values)
    assert len({repr(v) for v in values}) == 3


@pytest.mark.parametrize("source", [{"l": []}, {"l": None}, {"l": "abc"}])
def test_in_list_vide_ou_invalide(registry, source) -> None:
    assert run(registry, "getrandom_in_list($.l)", source) is None


# --- intégration ------------------------------------------------------------------


def test_toutes_les_fonctions_sont_documentees(registry) -> None:
    catalog = registry.catalog()
    assert len(catalog) == 25
    for entry in catalog:
        assert entry["name"].startswith("getrandom_")
        assert len((entry["description"] or "").strip()) >= 15, entry["name"]


def test_decouverte_par_entry_point() -> None:
    from urban_json import default_registry, load_plugins

    load_plugins()
    assert "getrandom_email" in default_registry
