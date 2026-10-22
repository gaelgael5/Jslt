"""phoneisvalid — port de Services.cs (libphonenumber, comme le .NET)."""

from __future__ import annotations

import pytest
from urban_json import FunctionRegistry, JsltTemplate

from urban_json_phone import register


@pytest.fixture(scope="module")
def registry() -> FunctionRegistry:
    reg = FunctionRegistry()
    register(reg)
    return reg


def valid(registry, number, region=""):
    template = JsltTemplate.parse('{ "r": phoneisvalid($.n, $.r) }')
    return template.transform({"n": number, "r": region}, functions=registry)["r"]


@pytest.mark.parametrize(
    ("number", "region", "expected"),
    [
        pytest.param("+33 6 12 34 56 78", "", True, id="international-fr-mobile"),
        pytest.param("0033612345678", "", True, id="prefixe-00"),
        pytest.param("+1 650-253-0000", "", True, id="us"),
        pytest.param("06 12 34 56 78", "FR", True, id="national-avec-region"),
        pytest.param("06 12 34 56 78", "US", False, id="national-mauvaise-region"),
        pytest.param("+33 6 12", "", False, id="trop-court"),
        pytest.param("pas un numero", "FR", False, id="illisible"),
        pytest.param("0612345678", "", False, id="national-sans-region"),
    ],
)
def test_phoneisvalid(registry, number, region, expected) -> None:
    assert valid(registry, number, region) is expected


@pytest.mark.parametrize("number", [None, ""])
def test_phoneisvalid_vide(registry, number) -> None:
    assert valid(registry, number, "FR") is False


def test_nombre_converti_en_texte(registry) -> None:
    assert valid(registry, 612345678, "FR") is True


def test_catalogue_et_decouverte(registry) -> None:
    from urban_json import default_registry, load_plugins

    entry = registry.catalog()[0]
    assert entry["name"] == "phoneisvalid" and len(entry["description"]) >= 15
    load_plugins()
    assert "phoneisvalid" in default_registry
