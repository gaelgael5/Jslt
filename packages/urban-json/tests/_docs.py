"""Localise les documents du guide et en extrait les exemples exécutables.

Partagé par ``test_guide_examples.py`` (le résultat attendu) et
``test_compiler.py`` (l'équivalence du chemin compilé) : depuis le découpage du
guide en documents thématiques, la liste des fichiers à balayer ne doit exister
qu'à **un seul** endroit — sinon un nouveau document rejoindrait une suite et
pas l'autre, et l'on croirait l'avoir couvert.

Un exemple testable est une suite de trois blocs de code balisés consécutifs :

    ```jslt      <- le template
    ```json      <- l'entrée (document source)
    ```json      <- la sortie attendue
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


def find_docs() -> Path:
    """Localise le dossier ``docs/`` du projet (à la racine du dépôt).

    Robuste à l'emplacement du paquet dans le monorepo : remonte les parents
    jusqu'à trouver un ``docs/guide.md``.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "docs"
        if (candidate / "guide.md").is_file():
            return candidate
    raise FileNotFoundError("dossier docs/ introuvable (docs/guide.md attendu)")


DOCS = find_docs()
# Tous les documents du guide, pas seulement `guide*.md` : les thèmes (dates,
# texte, collections…) portent désormais l'essentiel des exemples.
GUIDES = sorted(DOCS.glob("*.md"))

# Capture (langage, contenu) de chaque bloc ``` ... ``` du document.
_BLOCK_RE = re.compile(r"```(\w+)[^\n]*\n(.*?)```", re.DOTALL)


def extract_triples(markdown: str) -> list[tuple[str, str, str]]:
    blocks = _BLOCK_RE.findall(markdown)
    triples: list[tuple[str, str, str]] = []
    for i in range(len(blocks) - 2):
        (lang0, tpl), (lang1, src), (lang2, out) = blocks[i], blocks[i + 1], blocks[i + 2]
        if lang0 == "jslt" and lang1 == "json" and lang2 == "json":
            triples.append((tpl.strip(), src.strip(), out.strip()))
    return triples


def doc_triples() -> list:
    """Tous les triplets de tous les documents, en paramètres pytest."""
    cases = []
    for guide in GUIDES:
        for idx, (tpl, src, out) in enumerate(extract_triples(guide.read_text(encoding="utf-8"))):
            cases.append(pytest.param(tpl, src, out, id=f"{guide.name}-{idx}"))
    return cases


def counts_by_language() -> tuple[int, int]:
    """Nombre d'exemples côté français et côté anglais.

    Les deux doivent être égaux : la documentation est bilingue, un exemple
    ajouté d'un seul côté est une documentation inachevée (cf. CLAUDE.md).
    """
    french = english = 0
    for guide in GUIDES:
        found = len(extract_triples(guide.read_text(encoding="utf-8")))
        if guide.name.endswith(".en.md"):
            english += found
        else:
            french += found
    return french, english
