"""Extensibilité : ajout, isolation et découverte de fonctions.

Couvre l'équivalent Python du ``ServiceContainer`` / ``ServiceDiscovery`` du .NET :
décorateur d'enregistrement, registre isolé passé à ``transform``, introspection
du registre, et découverte de plugins tiers via entry points (:func:`load_plugins`).
"""

from __future__ import annotations

import pytest

from jslt import (
    FunctionInfo,
    FunctionRegistry,
    JsltError,
    JsltTemplate,
    default_registry,
    jslt_function,
    load_plugins,
)
from jslt.functions import registry as registry_module


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
    assert info.parameters == ("source", "path")  # ctx exclu
    assert info.signature() == "distinct(source, path)"
    assert info.description  # 1re ligne du docstring par défaut


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
    fake = _FakeEntryPointsSelect({"jslt.functions": [ep]})
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
        lambda: {"jslt.functions": [ep]},
        raising=False,
    )
    target = FunctionRegistry()
    assert load_plugins(target) == ["legacy"]
    assert "shout" in target
