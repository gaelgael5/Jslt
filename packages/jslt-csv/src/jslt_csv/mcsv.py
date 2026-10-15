"""Lecture de CSV multi-enregistrements (``loadmcsv``).

Port de ``Bb.CustomServices.ServicesMultiCsv.LoadMultiCsv`` + la bibliothèque
``Bb.MultiCsv`` (lexer, règles d'indentation, blocs, visiteur JSON).

Format de fichier (``;``-délimité) :

* ``#DEF;<schema>:<NOM>;col1;col2;…`` — définit les colonnes du type ``NOM`` ;
* ``#END`` — fin du fichier ;
* ``#CLE;v1;v2`` — métadonnée ``CLE`` (valeurs jointes par ``;``) ;
* ligne de données : 1er champ = type d'enregistrement, puis les valeurs des
  colonnes définies par le ``#DEF`` correspondant.

Un ``rule_payload`` ``"PARENT:ENF1|ENF2; AUTRE:…"`` (règles séparées par ``;``)
décrit la **hiérarchie** : un bloc dont le nom est enfant du parent courant s'y
imbrique, sinon il remonte. Le résultat JSON groupe les enfants homonymes en
tableaux ; ``loadmcsv`` ajoute un objet ``_metadatas`` (nom de fichier, encodage,
métadonnées du fichier).

Écarts volontaires vs .NET (documentés) :

* **Encodage** : lecture en ``utf-8`` (comme le .NET, qui lit en UTF-8 malgré sa
  détection Ude) ; ``_encodingFile``/``_encodingFileBody`` rapportent ``utf-8``.
* **Dernier champ** : le .NET ignore le dernier champ de chaque ligne (il suppose
  un ``;`` final). Le portage mappe les colonnes par position jusqu'au nombre de
  colonnes déclarées — tolérant au ``;`` final comme à son absence.
* Noms de types et de règles comparés en **majuscules** (le .NET met les libellés
  en majuscules ; on fait de même côté règles pour éviter les surprises de casse).
"""

from __future__ import annotations

import os
from typing import Any

__all__ = ["execute_loadmcsv"]


class _Block:
    """Un enregistrement : nom de type, champs (colonne→valeur), sous-blocs."""

    __slots__ = ("fields", "name", "subs")

    def __init__(self, name: str, fields: dict[str, str]) -> None:
        self.name = name
        self.fields = fields
        self.subs: list[_Block] = []


def _parse_rules(payload: str | None) -> dict[str, set[str]]:
    """Parse le DSL de règles ``"PARENT:ENF1|ENF2; …"`` (port d'``IndentationRules``)."""
    rules: dict[str, set[str]] = {}
    for rule in (payload or "").strip().split(";"):
        rule = rule.strip()
        if not rule or ":" not in rule:
            continue
        key, children = rule.split(":", 1)
        kids = {c.strip().upper() for c in children.split("|") if c.strip()}
        rules.setdefault(key.strip().upper(), set()).update(kids)
    return rules


def _read_blocks(path: str, encoding: str) -> tuple[list[_Block], dict[str, str]]:
    """Lit le fichier en blocs de données + métadonnées (port du ``Lexer``)."""
    headers: dict[str, list[str]] = {}
    metadata: dict[str, str] = {}
    blocks: list[_Block] = []

    with open(path, encoding=encoding, newline="") as handle:
        for raw in handle:
            line = raw.rstrip("\r\n")
            if line == "":
                continue
            fields = line.split(";")
            tag = fields[0]

            if tag.startswith("#"):
                if tag == "#DEF":
                    # fields[1] = "<schema>:<NOM>" ; fields[2:] = colonnes
                    name = fields[1].split(":")[-1].strip().upper() if len(fields) > 1 else ""
                    headers[name] = [c.strip() for c in fields[2:] if c.strip()]
                elif tag == "#END":
                    break
                else:
                    metadata[tag[1:]] = ";".join(fields[1:]).strip(";")
                continue

            name = tag.strip().upper()
            columns = headers.get(name)
            field_map: dict[str, str] = {}
            if columns:
                for index, column in enumerate(columns):
                    field_map[column] = fields[index + 1] if index + 1 < len(fields) else ""
            blocks.append(_Block(name, field_map))

    return blocks, metadata


def _build_tree(blocks: list[_Block], rules: dict[str, set[str]]) -> list[_Block]:
    """Construit l'arbre de blocs par pile (port de ``FileReader.Read``)."""
    if not blocks:
        return []

    def embedded(parent: _Block, child: _Block) -> bool:
        return child.name in rules.get(parent.name, ())

    stack: list[_Block] = [blocks[0]]
    for current in blocks[1:]:
        parent = stack[-1]
        if embedded(parent, current):
            parent.subs.append(current)
            stack.append(current)
        else:
            parent = stack.pop()
            while stack and not embedded(parent, current):
                parent = stack.pop()
            parent.subs.append(current)
            stack.append(parent)
            stack.append(current)

    items: list[_Block] = []
    while stack:
        current = stack.pop()
        if not stack or all(current is not sub for sub in stack[-1].subs):
            items.append(current)
    return items


def _to_json(block: _Block, seen: set[int], ignore_empty: bool) -> dict[str, Any]:
    """Convertit un bloc en objet JSON (port de ``JsonVisitor``)."""
    result: dict[str, Any] = {}
    for sub in block.subs:
        array = result.setdefault(sub.name, [])
        if id(sub) not in seen:
            seen.add(id(sub))
            array.append(_to_json(sub, seen, ignore_empty))
    for key, value in block.fields.items():
        if not ignore_empty or value != "":
            result[key] = value
    return result


def execute_loadmcsv(
    ctx: Any,
    source_path: str | None = None,
    rule_payload: str | None = None,
    encoding: str = "utf-8-sig",
    ignore_empty: bool = False,
) -> Any:
    """Lit un CSV multi-enregistrements et le convertit en arbre JSON (port ``loadmcsv``).

    Args:
        source_path: chemin du fichier.
        rule_payload: règles d'imbrication ``"PARENT:ENF1|ENF2; …"``.
        encoding: encodage de lecture (défaut ``utf-8-sig``, retire le BOM).
        ignore_empty: omet les propriétés vides.

    Returns:
        ``None`` si aucun enregistrement, l'objet racine s'il y en a un seul,
        sinon la liste des objets racines. Chaque racine porte ``_metadatas``.
    """
    if not source_path:
        raise ValueError("loadmcsv: source_path est requis")

    blocks, metadata = _read_blocks(source_path, encoding)
    rules = _parse_rules(rule_payload)
    items = _build_tree(blocks, rules)

    meta_obj: dict[str, Any] = {
        "_filename": os.path.abspath(source_path),
        "_encodingFile": "utf-8",
        "_encodingFileBody": "utf-8",
    }
    meta_obj.update(metadata)

    seen: set[int] = set()
    datas: list[Any] = []
    for block in items:
        obj = _to_json(block, seen, ignore_empty)
        obj["_metadatas"] = meta_obj
        datas.append(obj)

    if not datas:
        return None
    if len(datas) == 1:
        return datas[0]
    return datas
