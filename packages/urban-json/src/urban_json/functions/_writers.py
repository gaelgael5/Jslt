"""Écriture d'un document JSON en CSV, XML et YAML.

Le pendant des lectures (`parsejson`, `parsecsv`, `parsexml`) : un moteur de
transformation qui ne sait écrire que du JSON ne tient que la moitié de son
contrat. Les trois émetteurs sont **sans dépendance** — stdlib seulement — parce
qu'une dépendance de plus dans le cœur se paie à chaque installation.

Les conventions d'écriture sont celles que les lectures attendent, pour que
l'aller-retour tienne : `@attribut` et `#text` en XML (conventions Newtonsoft,
celles de `parsexml`), clés pointées en CSV (celles de `flattenobject`).
"""

from __future__ import annotations

import csv
import io
import json
import re
from typing import Any
from xml.sax.saxutils import escape, quoteattr

from urban_json.errors import JsltError

from ._helpers import to_text

# --- CSV ----------------------------------------------------------------------


def to_csv_text(value: Any, separator: str, header: bool) -> str:
    """Tableau d'objets -> CSV (RFC 4180 : guillemets doublés, fins de ligne CRLF).

    Les colonnes sont l'**union des clés** rencontrées, dans l'ordre
    d'apparition : sur des documents hétérogènes, se limiter aux clés du premier
    perdrait des données en silence. Une cellule absente reste vide, ce qui est
    la façon dont un CSV dit « rien ».
    """
    rows = value if isinstance(value, list) else None
    if rows is None or any(not isinstance(row, dict) for row in rows):
        raise JsltError(
            "to_csv attend un tableau d'objets (une ligne par objet), reçu : "
            f"{type(value).__name__}"
        )
    flat = [_flat_row(row) for row in rows]
    columns: list[str] = []
    for row in flat:
        columns.extend(key for key in row if key not in columns)
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=separator, quoting=csv.QUOTE_MINIMAL)
    if header:
        writer.writerow(columns)
    for row in flat:
        writer.writerow([_cell(row.get(column)) for column in columns])
    return buffer.getvalue()


def _flat_row(row: dict) -> dict[str, Any]:
    """Aplatit une ligne en clés pointées — un CSV n'a pas de profondeur."""
    # Import différé : `deep` enregistre des fonctions, qui importent le registre.
    from .deep import execute_flattenobject

    return execute_flattenobject(None, row) or {}


def _cell(value: Any) -> str:
    return "" if value is None else to_text(value)


# --- XML ----------------------------------------------------------------------

_NAME = re.compile(r"^[A-Za-z_][\w.-]*$")
_ATTRIBUTE = "@"
_TEXT = "#text"


def to_xml_text(value: Any, root: str) -> str:
    """Document JSON -> XML, conventions Newtonsoft (celles que lit ``parsexml``).

    Une clé préfixée ``@`` devient un attribut, ``#text`` le contenu textuel, et
    une clé dont la valeur est un tableau **répète** l'élément — c'est ainsi que
    XML exprime une liste, et c'est ce que `parsexml` relit.
    """
    name = _checked(root or "root")
    body = "".join(_element(key, child) for key, child in _members(value))
    attributes = "".join(
        f" {_checked(key[1:])}={quoteattr(to_text(child))}"
        for key, child in _members(value)
        if key.startswith(_ATTRIBUTE)
    )
    text = _inner_text(value)
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f"<{name}{attributes}>{text}{body}</{name}>\n"
    )


def _members(value: Any) -> list[tuple[str, Any]]:
    return list(value.items()) if isinstance(value, dict) else []


def _inner_text(value: Any) -> str:
    if isinstance(value, dict):
        return escape(to_text(value[_TEXT])) if _TEXT in value else ""
    return escape(to_text(value))


def _element(key: str, value: Any) -> str:
    if key.startswith(_ATTRIBUTE) or key == _TEXT:
        return ""  # déjà portés par l'élément parent
    name = _checked(key)
    if isinstance(value, list):
        return "".join(_element(key, item) for item in value)
    if isinstance(value, dict):
        attributes = "".join(
            f" {_checked(k[1:])}={quoteattr(to_text(v))}"
            for k, v in value.items()
            if k.startswith(_ATTRIBUTE)
        )
        inner = _inner_text(value) + "".join(_element(k, v) for k, v in value.items())
        return f"<{name}{attributes}>{inner}</{name}>"
    if value is None:
        # Élément vide plutôt que `null` écrit en texte : XML n'a pas de null, et
        # une balise vide est ce que tous les lecteurs comprennent.
        return f"<{name} />"
    return f"<{name}>{escape(to_text(value))}</{name}>"


def _checked(name: str) -> str:
    if not _NAME.match(name):
        raise JsltError(
            f"nom d'élément XML invalide : {name!r} (lettre ou _ en tête, puis "
            "lettres, chiffres, point, tiret)"
        )
    return name


# --- YAML ---------------------------------------------------------------------

# Scalaires qu'un lecteur YAML relirait comme un autre type : il faut les citer
# pour qu'un texte « true » reste un texte.
_AMBIGUOUS = re.compile(
    r"""^(
        | ~ | null | Null | NULL | true | True | TRUE | false | False | FALSE
        | [-+]?\d+ | [-+]?\d*\.\d+([eE][-+]?\d+)? | 0[xXoObB][0-9a-fA-F_]+
        | \d{4}-\d{2}-\d{2}.*
    )$""",
    re.VERBOSE,
)
_SPECIAL_START = tuple("-?:,[]{}#&*!|>'\"%@` \t")


def to_yaml_text(value: Any, json_style: bool) -> str:
    """Document JSON -> YAML en style bloc, ou en style JSON (qui est du YAML
    valide, YAML 1.2 étant un sur-ensemble de JSON).

    Sous-ensemble assumé : pas d'ancres, pas de tags, pas de style littéral
    multi-ligne — une chaîne à retours à la ligne est citée et échappée. C'est
    du YAML valide et relisible, pas le plus élégant possible.
    """
    if json_style:
        return json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    lines: list[str] = []
    _yaml_node(value, 0, lines)
    return "".join(f"{line}\n" for line in lines)


def _yaml_node(value: Any, depth: int, lines: list[str]) -> None:
    pad = "  " * depth
    if isinstance(value, dict):
        if not value:
            lines.append(f"{pad}{{}}")
            return
        for key, child in value.items():
            _yaml_member(f"{pad}{_yaml_key(key)}:", child, depth, lines)
        return
    if isinstance(value, list):
        if not value:
            lines.append(f"{pad}[]")
            return
        for item in value:
            _yaml_member(f"{pad}-", item, depth, lines)
        return
    lines.append(f"{pad}{_yaml_scalar(value)}")


def _yaml_member(prefix: str, child: Any, depth: int, lines: list[str]) -> None:
    """Écrit `clef:` ou `-` puis la valeur, en ligne si elle est scalaire."""
    if isinstance(child, (dict, list)) and child:
        lines.append(prefix)
        _yaml_node(child, depth + 1, lines)
    else:
        inline = "{}" if isinstance(child, dict) else "[]" if isinstance(child, list) else _yaml_scalar(child)
        lines.append(f"{prefix} {inline}")


def _yaml_key(key: Any) -> str:
    text = to_text(key)
    return _yaml_scalar(text) if not text or _needs_quotes(text) else text


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    text = to_text(value)
    return json.dumps(text, ensure_ascii=False) if _needs_quotes(text) else text


def _needs_quotes(text: str) -> bool:
    return (
        not text
        or _AMBIGUOUS.match(text) is not None
        or text.startswith(_SPECIAL_START)
        or text != text.strip()
        or any(char in text for char in ('"', "'", "\n", "\r", "\t", ": ", " #"))
        or text.endswith(":")
    )
