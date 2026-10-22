"""``schema(fragment)`` — JSON Schema (draft-04) déduit d'un exemple.

Port de ``LoadSchema`` (.NET), qui délègue à ``JsonSchema.FromSampleJson`` de
NJsonSchema (``SampleJsonSchemaGenerator``, dont le source est embarqué dans le
dépôt .NET). L'algorithme est reproduit tel quel, y compris ses choix de
nommage, pour qu'un même exemple donne le même schéma :

* un objet imbriqué devient une définition nommée d'après sa propriété
  (UpperCamelCase, singulier pour un tableau : ``orders`` -> ``Order``),
  référencée par ``$ref`` ; une définition existante est réutilisée si elle
  contient déjà toutes les propriétés de l'objet ;
* un tableau homogène fusionne ses éléments dans une définition ; hétérogène,
  il prend le schéma du premier élément ;
* formats déduits des chaînes : ``date``, ``date-time``, ``duration``. Les
  chaînes ISO 8601 avec heure sont des dates, comme Newtonsoft les lit.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from .registry import jslt_function

_DRAFT4 = "http://json-schema.org/draft-04/schema#"

# Chaîne que Newtonsoft (DateParseHandling par défaut) convertit en date.
_ISO_DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?$")
_DATE = re.compile(r"^[0-2][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$")
_DATE_TIME = re.compile(r"^[0-2][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9](:[0-9][0-9])?$")
_DURATION = re.compile(r"^[0-9][0-9]:[0-9][0-9](:[0-9][0-9])?$")


class _Schema:
    __slots__ = ("format", "item", "properties", "reference", "type")

    def __init__(self) -> None:
        self.type: str | None = None
        self.format: str | None = None
        self.properties: dict[str, _Schema] = {}
        self.item: _Schema | None = None
        self.reference: _Schema | None = None


class _Generator:
    def __init__(self) -> None:
        self.root = _Schema()
        self.definitions: dict[str, _Schema] = {}

    def generate(self, token: Any, schema: _Schema, hint: str) -> None:
        if schema is not self.root and isinstance(token, dict):
            referenced = next(
                (
                    s for s in self.definitions.values()
                    if s.type == "object" and all(name in s.properties for name in token)
                ),
                None,
            )
            if referenced is None:
                referenced = _Schema()
                self._add_definition(referenced, hint)
            schema.reference = referenced
            self._without_reference(token, referenced, hint)
            return
        self._without_reference(token, schema, hint)

    def _without_reference(self, token: Any, schema: _Schema, hint: str) -> None:
        if token is None:
            return
        if isinstance(token, dict):
            self._object(token, schema)
        elif isinstance(token, list):
            self._array(token, schema, hint)
        elif isinstance(token, bool):
            schema.type = "boolean"
        elif isinstance(token, int):
            schema.type = "integer"
        elif isinstance(token, float):
            schema.type = "number"
        elif isinstance(token, str):
            schema.type = "string"
            if _ISO_DATETIME.match(token):
                moment = datetime.fromisoformat(token.replace("Z", "+00:00"))
                is_midnight = (moment.hour, moment.minute, moment.second, moment.microsecond) == (0, 0, 0, 0)
                schema.format = "date" if is_midnight else "date-time"
            elif _DATE.match(token):
                schema.format = "date"
            elif _DATE_TIME.match(token):
                schema.format = "date-time"
            elif _DURATION.match(token):
                schema.format = "duration"

    def _object(self, token: dict, schema: _Schema) -> None:
        schema.type = "object"
        for name, value in token.items():
            prop = _Schema()
            base = _singularize(name) if isinstance(value, list) else name
            self.generate(value, prop, _upper_camel_case(base))
            schema.properties[name] = prop

    def _array(self, token: list, schema: _Schema, hint: str) -> None:
        schema.type = "array"
        items = []
        for value in token:
            item = _Schema()
            self._without_reference(value, item, hint)
            items.append(item)
        if not items:
            schema.item = _Schema()
        elif len({s.type for s in items}) == 1:
            merged = _Schema()
            merged.type = items[0].type
            if merged.type == "object":
                for item in items:
                    for name, prop in item.properties.items():
                        merged.properties.setdefault(name, prop)
            self._add_definition(merged, hint)
            holder = _Schema()
            holder.reference = merged
            schema.item = holder
        else:
            schema.item = items[0]

    def _add_definition(self, schema: _Schema, hint: str) -> None:
        if not hint or hint in self.definitions:
            hint = f"Anonymous{len(self.definitions) + 1}"
        self.definitions[hint] = schema

    def to_json(self, schema: _Schema) -> dict:
        if schema.reference is not None:
            name = next(n for n, s in self.definitions.items() if s is schema.reference)
            return {"$ref": f"#/definitions/{name}"}
        out: dict[str, Any] = {}
        if schema.type is not None:
            out["type"] = schema.type
        if schema.format is not None:
            out["format"] = schema.format
        if schema.properties:
            out["properties"] = {name: self.to_json(p) for name, p in schema.properties.items()}
        if schema.item is not None:
            out["items"] = self.to_json(schema.item)
        return out


def _singularize(word: str) -> str:
    if word == "people":
        return "Person"
    return word.removesuffix("s")


def _upper_camel_case(text: str) -> str:
    """``ConversionUtilities.ConvertToUpperCamelCase(texte, true)`` de NJsonSchema."""
    if not text:
        return ""
    text = (text[0].upper() + text[1:]).replace(" ", "_").replace("/", "_")
    parts = text.split("-")
    text = parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])
    return "_" + text if text[:1].isdigit() else text


@jslt_function("schema", description="JSON Schema (draft-04) déduit d'un fragment JSON d'exemple")
def execute_schema(ctx: Any, fragment: Any = None) -> dict:
    generator = _Generator()
    generator.generate(fragment, generator.root, "Anonymous")
    result = {"$schema": _DRAFT4, **generator.to_json(generator.root)}
    if generator.definitions:
        result["definitions"] = {name: generator.to_json(s) for name, s in generator.definitions.items()}
    return result
