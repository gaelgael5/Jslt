"""Extensibilité : ajout, isolation et découverte de fonctions.

Couvre l'équivalent Python du ``ServiceContainer`` / ``ServiceDiscovery`` du .NET :
décorateur d'enregistrement, registre isolé passé à ``transform``, introspection
du registre, et découverte de plugins tiers via entry points (:func:`load_plugins`).
"""

from __future__ import annotations

import pytest

from urban_json import (
    FunctionInfo,
    FunctionRegistry,
    JsltError,
    JsltTemplate,
    default_registry,
    jslt_function,
    load_plugins,
)
from urban_json.functions import registry as registry_module


# --- introspection / découverte -------------------------------------------
def test_default_registry_lists_builtins() -> None:
    names = default_registry.names()
    assert "sum" in names and "distinct" in names and "upper" in names
    assert len(default_registry) == len(names)
    assert "SUM" in default_registry  # insensible à la casse


def test_describe_exposes_metadata() -> None:
    info = default_registry.describe("distinct")
    assert isinstance(info, FunctionInfo)
    assert info.name == "distinct"
    assert info.path_args == (1,)
    assert [p.name for p in info.parameters] == ["source", "path"]  # ctx exclu
    assert info.signature() == "distinct(source, path)"
    assert info.description  # 1re ligne du docstring par défaut


def test_parameters_carry_name_type_and_path_flag() -> None:
    info = default_registry.describe("distinct")
    source, path = info.parameters
    assert source.name == "source" and source.type == "Any"
    # Le 2e argument de distinct est un argument « chemin » (path_args=(1,)).
    assert path.is_path is True
    assert source.is_path is False
    # Paramètres optionnels (valeur par défaut) -> non requis.
    assert source.required is False and source.has_default is True


def test_catalog_is_json_serialisable_for_an_editor() -> None:
    import json

    catalog = default_registry.catalog()
    assert isinstance(catalog, list)
    # Entièrement sérialisable en JSON (destiné à un éditeur de templates).
    dumped = json.dumps(catalog)
    assert dumped
    entry = next(e for e in catalog if e["name"] == "distinct")
    assert entry["signature"] == "distinct(source, path)"
    assert entry["parameters"][1]["is_path"] is True
    assert {"name", "type", "required", "is_path", "variadic"} <= entry["parameters"][0].keys()


def test_variadic_and_return_type_detected() -> None:
    reg = FunctionRegistry()

    def many(ctx, *values: int) -> list:
        return list(values)

    reg.register("many", many)
    info = reg.describe("many")
    assert info.accepts_varargs is True
    assert info.parameters[0].variadic is True
    assert info.parameters[0].required is False
    assert info.returns == "list"


def test_describe_unknown_returns_none() -> None:
    assert default_registry.describe("fonction_inexistante") is None


def test_registry_is_iterable() -> None:
    assert sorted(iter(default_registry)) == default_registry.names()


# --- ajout via décorateur --------------------------------------------------
def test_jslt_function_decorator_registers_and_is_usable() -> None:
    @jslt_function("mydouble", description="Double un nombre")
    def _mydouble(ctx, x=None):
        return x * 2

    assert "mydouble" in default_registry
    assert JsltTemplate.parse('{ "r": mydouble($.n) }').transform({"n": 21}) == {"r": 42}
    assert default_registry.describe("mydouble").description == "Double un nombre"


# --- registre isolé passé à transform -------------------------------------
def test_custom_registry_isolates_functions() -> None:
    sandbox = FunctionRegistry()
    sandbox.register("triple", lambda ctx, x=None: x * 3)

    assert JsltTemplate.parse('{ "r": triple($.n) }').transform({"n": 7}, functions=sandbox) == {
        "r": 21
    }
    # Les fonctions intégrées ne fuient pas dans le sandbox.
    with pytest.raises(JsltError):
        JsltTemplate.parse('{ "r": sum($.n) }').transform({"n": [1, 2]}, functions=sandbox)


def test_copy_derives_without_mutating_source() -> None:
    derived = default_registry.copy()
    derived.register("quadruple", lambda ctx, x=None: x * 4)
    assert "quadruple" in derived
    assert "quadruple" not in default_registry
    # La copie conserve les fonctions d'origine.
    assert "sum" in derived


# --- découverte de plugins via entry points -------------------------------
class _FakeEntryPoint:
    def __init__(self, name, register):
        self.name = name
        self._register = register

    def load(self):
        return self._register


class _FakeEntryPointsSelect:
    """Imite l'objet EntryPoints de Python 3.10+ (méthode .select)."""

    def __init__(self, mapping):
        self._mapping = mapping

    def select(self, group):
        return list(self._mapping.get(group, []))


def _plugin_register(registry: FunctionRegistry) -> None:
    registry.register("shout", lambda ctx, s=None: (s or "").upper() + "!")


def test_load_plugins_select_api(monkeypatch) -> None:
    ep = _FakeEntryPoint("demo", _plugin_register)
    fake = _FakeEntryPointsSelect({"urban_json.functions": [ep]})
    monkeypatch.setattr(registry_module.metadata, "entry_points", lambda: fake, raising=False)

    target = FunctionRegistry()
    loaded = load_plugins(target)
    assert loaded == ["demo"]
    assert "shout" in target
    assert JsltTemplate.parse('{ "r": shout($.s) }').transform({"s": "hi"}, functions=target) == {
        "r": "HI!"
    }
    # Idempotent : un second appel ne recharge pas.
    assert load_plugins(target) == []


def test_load_plugins_dict_api(monkeypatch) -> None:
    # Python 3.9 : entry_points() renvoie un dict groupe -> liste (pas de .select).
    ep = _FakeEntryPoint("legacy", _plugin_register)
    monkeypatch.setattr(
        registry_module.metadata,
        "entry_points",
        lambda: {"urban_json.functions": [ep]},
        raising=False,
    )
    target = FunctionRegistry()
    assert load_plugins(target) == ["legacy"]
    assert "shout" in target
