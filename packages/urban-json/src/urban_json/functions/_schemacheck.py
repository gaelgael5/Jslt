"""Validation d'un document contre un JSON Schema (sous-ensemble draft-04).

Pendant de :mod:`.schema`, qui **déduit** un schéma d'un exemple : on valide
contre le même vocabulaire, plus les mots-clés qu'un schéma écrit à la main
porte couramment. Les mots-clés **inconnus sont ignorés** — un schéma complet
(``allOf``, ``oneOf``, ``$dynamicRef``…) n'est pas refusé, il est validé sur ce
qui est compris. L'inverse, lever sur un mot-clé non géré, rendrait la fonction
inutilisable sur les schémas réels ; le prix est qu'un document peut être
déclaré valide alors qu'un mot-clé non géré l'aurait rejeté, et c'est dit dans
la documentation.
"""

from __future__ import annotations

import re
from typing import Any

from ._dateread import from_iso
from .types import type_name

# Mots-clés effectivement vérifiés — le reste est ignoré en connaissance de cause.
SUPPORTED = (
    "$ref", "type", "enum", "properties", "additionalProperties", "required",
    "items", "minItems", "maxItems", "uniqueItems", "minimum", "maximum",
    "exclusiveMinimum", "exclusiveMaximum", "minLength", "maxLength", "pattern",
    "format",
)

_FORMATS = {
    "date": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "duration": re.compile(r"^\d{2}:\d{2}(:\d{2})?$"),
}


def errors(document: Any, schema: Any, root: Any = None) -> list[str]:
    """Liste des erreurs de validation, vide si le document est conforme."""
    collected: list[str] = []
    _check(document, schema, root if root is not None else schema, "$", collected)
    return collected


def _resolve(schema: dict, root: Any) -> dict:
    """Suit un ``$ref`` interne (``#/definitions/Nom``)."""
    reference = schema.get("$ref")
    if not isinstance(reference, str) or not reference.startswith("#/"):
        return schema
    target: Any = root
    for step in reference[2:].split("/"):
        if not isinstance(target, dict) or step not in target:
            return schema  # référence pendante : on ne valide pas ce nœud
        target = target[step]
    return target if isinstance(target, dict) else schema


def _check(value: Any, schema: Any, root: Any, path: str, out: list[str]) -> None:
    if not isinstance(schema, dict):
        return
    schema = _resolve(schema, root)
    actual = type_name(value)

    expected = schema.get("type")
    if expected is not None and not _type_ok(value, actual, expected):
        names = expected if isinstance(expected, str) else ", ".join(expected)
        out.append(f"{path} : attendu {_french(names)}, reçu {_french(actual)}")
        return  # inutile d'empiler des erreurs de bornes sur un mauvais type

    if "enum" in schema and value not in schema["enum"]:
        out.append(f"{path} : valeur hors enum {schema['enum']!r} (reçu {value!r})")

    if actual == "object":
        _check_object(value, schema, root, path, out)
    elif actual == "array":
        _check_array(value, schema, root, path, out)
    elif actual == "number":
        _check_number(value, schema, path, out)
    elif actual == "string":
        _check_string(value, schema, path, out)


def _type_ok(value: Any, actual: str, expected: Any) -> bool:
    names = [expected] if isinstance(expected, str) else list(expected)
    for name in names:
        if name == actual:
            return True
        # `integer` n'est pas un type JSON : c'est `number` sans partie décimale.
        if name == "integer" and actual == "number" and float(value).is_integer():
            return True
        if name == "number" and actual == "number":
            return True
    return False


def _check_object(value: dict, schema: dict, root: Any, path: str, out: list[str]) -> None:
    properties = schema.get("properties") or {}
    for name in schema.get("required") or []:
        if name not in value:
            out.append(f"{path} : propriété requise absente : {name}")
    for name, child in value.items():
        if name in properties:
            _check(child, properties[name], root, f"{path}.{name}", out)
        elif schema.get("additionalProperties") is False:
            out.append(f"{path} : propriété non autorisée : {name}")


def _check_array(value: list, schema: dict, root: Any, path: str, out: list[str]) -> None:
    minimum, maximum = schema.get("minItems"), schema.get("maxItems")
    if isinstance(minimum, int) and len(value) < minimum:
        out.append(f"{path} : minItems {minimum} non atteint ({len(value)} élément(s))")
    if isinstance(maximum, int) and len(value) > maximum:
        out.append(f"{path} : maxItems {maximum} dépassé ({len(value)} élément(s))")
    if schema.get("uniqueItems") is True and _has_duplicate(value):
        out.append(f"{path} : uniqueItems, le tableau contient des doublons")
    items = schema.get("items")
    if isinstance(items, dict):
        for index, item in enumerate(value):
            _check(item, items, root, f"{path}[{index}]", out)
    elif isinstance(items, list):
        # Forme « tuple » : un schéma par position.
        for index, (item, child) in enumerate(zip(value, items)):
            _check(item, child, root, f"{path}[{index}]", out)


def _has_duplicate(value: list) -> bool:
    seen: list[Any] = []
    for item in value:
        if item in seen:
            return True
        seen.append(item)
    return False


def _check_number(value: Any, schema: dict, path: str, out: list[str]) -> None:
    minimum, maximum = schema.get("minimum"), schema.get("maximum")
    # draft-04 : `exclusiveMinimum` est un booléen qui qualifie `minimum` ;
    # draft-06+ : c'est une borne à part entière. Les deux sont acceptées.
    low_exclusive = schema.get("exclusiveMinimum")
    high_exclusive = schema.get("exclusiveMaximum")
    if _is_bound(minimum) and (value < minimum or (low_exclusive is True and value == minimum)):
        out.append(f"{path} : minimum {minimum} non respecté (reçu {value})")
    if _is_bound(maximum) and (value > maximum or (high_exclusive is True and value == maximum)):
        out.append(f"{path} : maximum {maximum} dépassé (reçu {value})")
    if _is_bound(low_exclusive) and value <= low_exclusive:
        out.append(f"{path} : exclusiveMinimum {low_exclusive} non respecté (reçu {value})")
    if _is_bound(high_exclusive) and value >= high_exclusive:
        out.append(f"{path} : exclusiveMaximum {high_exclusive} dépassé (reçu {value})")


def _is_bound(value: Any) -> bool:
    """Vraie borne numérique : un booléen n'en est pas une (forme draft-04 de
    ``exclusiveMinimum``, qui qualifie ``minimum`` au lieu de le remplacer)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_string(value: str, schema: dict, path: str, out: list[str]) -> None:
    minimum, maximum = schema.get("minLength"), schema.get("maxLength")
    if isinstance(minimum, int) and len(value) < minimum:
        out.append(f"{path} : minLength {minimum} non atteint ({len(value)} caractère(s))")
    if isinstance(maximum, int) and len(value) > maximum:
        out.append(f"{path} : maxLength {maximum} dépassé ({len(value)} caractère(s))")
    pattern = schema.get("pattern")
    if isinstance(pattern, str):
        try:
            matched = re.search(pattern, value) is not None
        except re.error:
            matched = True  # motif du schéma illisible : on ne condamne pas le document
        if not matched:
            out.append(f"{path} : pattern {pattern!r} non respecté (reçu {value!r})")
    fmt = schema.get("format")
    if fmt == "date-time":
        if from_iso(value) is None:
            out.append(f"{path} : format date-time attendu (reçu {value!r})")
    elif fmt in _FORMATS and not _FORMATS[fmt].match(value):
        out.append(f"{path} : format {fmt} attendu (reçu {value!r})")


_FRENCH = {
    "null": "null", "boolean": "un booléen", "number": "un nombre",
    "integer": "un entier", "string": "une chaîne", "array": "un tableau",
    "object": "un objet",
}


def _french(names: str) -> str:
    return ", ".join(_FRENCH.get(name.strip(), name.strip()) for name in names.split(","))
