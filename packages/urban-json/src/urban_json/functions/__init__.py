"""Fonctions intégrées et registre de services jslt.

Analogue Python du mécanisme ``CustomServices`` + ``ServiceContainer`` du .NET.
Là où le .NET résout les fonctions par nom **et types d'arguments** (nécessaire à
sa génération de code), le portage utilise un registre **par nom** : en Python
dynamique la fonction gère elle-même ses arguments, ce qui est plus simple et
suffisant.

Les fonctions exotiques / d'E-S du .NET (csv, httpapi, hash, randoms, group,
sql…) ne font pas partie du cœur et ne sont pas portées ici ; le registre reste
extensible pour les ajouter ou en enregistrer de nouvelles.
"""

# Chaque module importé enregistre ses fonctions dans le registre par défaut.
from . import builtins, collection, encoding, formatting, grouping, maths, misc, text  # noqa: F401
from .registry import (
    PLUGIN_GROUP,
    FunctionInfo,
    FunctionRegistry,
    ParameterInfo,
    default_registry,
    jslt_function,
    load_plugins,
)

__all__ = [
    "PLUGIN_GROUP",
    "FunctionInfo",
    "FunctionRegistry",
    "ParameterInfo",
    "default_registry",
    "jslt_function",
    "load_plugins",
]
