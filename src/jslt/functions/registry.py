"""Registre des fonctions jslt (résolution par nom) + découverte de plugins.

Analogue du ``ServiceContainer`` / ``ServiceDiscovery`` du .NET, rendu idiomatique
Python :

* **enregistrer** une fonction = décorateur :func:`jslt_function` (équivalent de
  l'attribut ``[JsltExtensionMethod]``) ou :meth:`FunctionRegistry.register`.
* **isoler** un jeu de fonctions = un :class:`FunctionRegistry` dédié (passé à
  ``JsltTemplate.transform(..., functions=...)``), plutôt que le singleton global.
* **découvrir** les fonctions disponibles = :meth:`FunctionRegistry.names` /
  :meth:`describe` / itération (utile aux messages d'erreur, à la doc, à
  l'outillage éditeur).
* **plugins tiers** = :func:`load_plugins`, qui découvre les paquets déclarant le
  groupe d'entry points ``jslt.functions`` (équivalent Python du scan d'assembly
  ``AddAssembly`` du .NET : installer un paquet suffit à exposer ses fonctions).

Une fonction est une callable ``(ctx, *args) -> valeur`` enregistrée sous un nom
insensible à la casse (comme le ``name.ToLower()`` du .NET).
"""

from __future__ import annotations

import inspect
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from importlib import metadata
from typing import Any

JsltFunction = Callable[..., Any]

#: Groupe d'entry points scruté par :func:`load_plugins` pour les plugins tiers.
PLUGIN_GROUP = "jslt.functions"


@dataclass(frozen=True)
class FunctionInfo:
    """Description introspectable d'une fonction enregistrée.

    Utilisée pour la découverte : nom, paramètres (hors ``ctx``), positions des
    arguments « chemin », description libre et acceptation d'arguments variadiques.
    """

    name: str
    function: JsltFunction = field(repr=False)
    path_args: tuple[int, ...] = ()
    description: str = ""
    parameters: tuple[str, ...] = ()
    accepts_varargs: bool = False

    def signature(self) -> str:
        """Signature lisible côté template, p.ex. ``distinct(source, path)``."""
        params = list(self.parameters)
        if self.accepts_varargs:
            params.append("...")
        return f"{self.name}({', '.join(params)})"


def _introspect(function: JsltFunction) -> tuple[tuple[str, ...], bool]:
    """Extrait les noms de paramètres (hors ``ctx``) et l'acceptation de ``*args``."""
    try:
        sig = inspect.signature(function)
    except (ValueError, TypeError):
        return (), False
    names: list[str] = []
    accepts_varargs = False
    for index, param in enumerate(sig.parameters.values()):
        if index == 0:
            continue  # le premier paramètre est toujours le contexte (ctx)
        if param.kind is inspect.Parameter.VAR_POSITIONAL:
            accepts_varargs = True
        elif param.kind is inspect.Parameter.VAR_KEYWORD:
            continue
        else:
            names.append(param.name)
    return tuple(names), accepts_varargs


class FunctionRegistry:
    """Table nom -> fonction, avec métadonnées de découverte."""

    def __init__(self) -> None:
        self._functions: dict[str, FunctionInfo] = {}
        #: Noms d'entry points déjà chargés dans ce registre (idempotence).
        self._loaded_plugins: set[str] = set()

    # -- enregistrement -----------------------------------------------------
    def register(
        self,
        name: str,
        function: JsltFunction,
        path_args: tuple[int, ...] = (),
        description: str = "",
    ) -> None:
        """Enregistre (ou remplace) une fonction sous ``name`` (casse ignorée)."""
        parameters, accepts_varargs = _introspect(function)
        self._functions[name.lower()] = FunctionInfo(
            name=name,
            function=function,
            path_args=path_args,
            description=description or (inspect.getdoc(function) or "").split("\n", 1)[0],
            parameters=parameters,
            accepts_varargs=accepts_varargs,
        )

    # -- résolution (exécution) --------------------------------------------
    def get(self, name: str) -> JsltFunction | None:
        info = self._functions.get(name.lower())
        return info.function if info is not None else None

    def path_args_of(self, name: str) -> tuple[int, ...]:
        """Indices des arguments passés comme chemin JSONPath brut (non évalué)."""
        info = self._functions.get(name.lower())
        return info.path_args if info is not None else ()

    # -- découverte / introspection ----------------------------------------
    def describe(self, name: str) -> FunctionInfo | None:
        """Métadonnées d'une fonction, ou ``None`` si inconnue."""
        return self._functions.get(name.lower())

    def names(self) -> list[str]:
        """Noms des fonctions disponibles, triés (nom d'origine, casse conservée)."""
        return sorted(info.name for info in self._functions.values())

    def describe_all(self) -> list[FunctionInfo]:
        """Métadonnées de toutes les fonctions, triées par nom."""
        return sorted(self._functions.values(), key=lambda info: info.name.lower())

    def copy(self) -> FunctionRegistry:
        """Nouveau registre indépendant, pré-rempli avec les fonctions courantes.

        Idiomatique pour dériver un jeu de fonctions isolé des valeurs par défaut
        sans muter le registre global.
        """
        clone = FunctionRegistry()
        clone._functions = dict(self._functions)
        clone._loaded_plugins = set(self._loaded_plugins)
        return clone

    def __contains__(self, name: str) -> bool:
        return name.lower() in self._functions

    def __iter__(self) -> Iterator[str]:
        return iter(self.names())

    def __len__(self) -> int:
        return len(self._functions)


#: Registre par défaut, peuplé par les modules de :mod:`jslt.functions`.
default_registry = FunctionRegistry()


def jslt_function(
    name: str, path_args: tuple[int, ...] = (), description: str = ""
) -> Callable[[JsltFunction], JsltFunction]:
    """Décorateur enregistrant une fonction dans le registre par défaut.

    ``path_args`` liste les indices d'arguments (0 = premier argument du template)
    reçus comme chemin JSONPath compilé plutôt que comme valeur évaluée.
    ``description`` documente la fonction (sinon la 1re ligne du docstring sert).
    """

    def decorator(function: JsltFunction) -> JsltFunction:
        default_registry.register(name, function, path_args, description)
        return function

    return decorator


def load_plugins(registry: FunctionRegistry | None = None) -> list[str]:
    """Découvre et charge les plugins déclarant le groupe d'entry points ``jslt.functions``.

    Chaque entry point doit pointer vers une callable ``register(registry)`` qui
    enregistre ses fonctions dans le registre reçu. Équivalent idiomatique Python
    du scan d'assembly ``AddAssembly`` du .NET : il suffit d'installer un paquet
    déclarant cet entry point pour que ses fonctions deviennent disponibles.

    Idempotent : un même entry point n'est chargé qu'une fois par registre.

    Args:
        registry: registre cible (par défaut, le registre global).

    Returns:
        Les noms des entry points chargés lors de cet appel.
    """
    target = registry if registry is not None else default_registry

    # API de sélection par groupe : `select` (Python 3.10+) ou dict (3.9).
    entry_points = metadata.entry_points()
    if hasattr(entry_points, "select"):
        group = entry_points.select(group=PLUGIN_GROUP)
    else:  # Python 3.9 : entry_points() renvoie un dict groupe -> liste
        group = entry_points.get(PLUGIN_GROUP, [])

    loaded: list[str] = []
    for entry_point in group:
        if entry_point.name in target._loaded_plugins:
            continue
        register = entry_point.load()
        if callable(register):
            register(target)
        target._loaded_plugins.add(entry_point.name)
        loaded.append(entry_point.name)
    return loaded
