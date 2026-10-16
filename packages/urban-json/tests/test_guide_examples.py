"""Exécute **tous** les exemples testables du guide (`docs/guide.md`).

Un exemple testable est une suite de trois blocs de code balisés consécutifs :

    ```jslt      <- le template
    ```json      <- l'entrée (document source)
    ```json      <- la sortie attendue

Ce test extrait chaque triplet et vérifie que
``parse(template).transform(entrée) == sortie``. Les exemples de la doc ne
peuvent donc pas diverger du comportement réel du moteur.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from urban_json import JsltTemplate


def _find_docs() -> Path:
    """Localise le dossier ``docs/`` du projet (à la racine du dépôt).

    Robuste à l'emplacement du paquet dans le monorepo : remonte les parents
    jusqu'à trouver un ``docs/guide.md``.
    """
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "docs"
        if (candidate / "guide.md").is_file():
            return candidate
    raise FileNotFoundError("dossier docs/ introuvable (docs/guide.md attendu)")


DOCS = _find_docs()
# Guides versionnés (français canonique + doublage anglais) : mêmes triplets.
GUIDES = sorted(DOCS.glob("guide*.md"))

# Capture (langage, contenu) de chaque bloc ``` ... ``` du document.
_BLOCK_RE = re.compile(r"```(\w+)[^\n]*\n(.*?)```", re.DOTALL)


def _extract_triples(markdown: str) -> list[tuple[str, str, str]]:
    blocks = _BLOCK_RE.findall(markdown)
    triples: list[tuple[str, str, str]] = []
    for i in range(len(blocks) - 2):
        (lang0, tpl), (lang1, src), (lang2, out) = blocks[i], blocks[i + 1], blocks[i + 2]
        if lang0 == "jslt" and lang1 == "json" and lang2 == "json":
            triples.append((tpl.strip(), src.strip(), out.strip()))
    return triples


def _load_cases() -> list:
    cases = []
    for guide in GUIDES:
        triples = _extract_triples(guide.read_text(encoding="utf-8"))
        for idx, (tpl, src, out) in enumerate(triples):
            cases.append(pytest.param(tpl, src, out, id=f"{guide.name}-{idx}"))
    return cases


CASES = _load_cases()


def test_guide_has_examples() -> None:
    # Garde-fou : si l'extraction casse, on ne veut pas « 0 test » silencieux.
    assert len(CASES) >= 20


@pytest.mark.parametrize("template, source, expected", CASES)
def test_guide_example(template: str, source: str, expected: str) -> None:
    result = JsltTemplate.parse(template).transform(json.loads(source))
    assert result == json.loads(expected)
