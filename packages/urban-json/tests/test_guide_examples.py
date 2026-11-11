"""Exécute **tous** les exemples testables du guide (`docs/`).

Le guide est découpé en documents thématiques (`guide.md` et les thèmes :
`dates.md`, `texte.md`, `collections.md`…), chacun doublé en anglais. Ce test
extrait chaque triplet *template → entrée → sortie* et vérifie que
``parse(template).transform(entrée) == sortie``. Les exemples de la doc ne
peuvent donc pas diverger du comportement réel du moteur.

L'extraction et la liste des documents vivent dans ``_docs.py``, partagées avec
``test_compiler.py``.
"""

from __future__ import annotations

import json

import pytest

from _docs import DOCS, NO_DOCS, counts_by_language, doc_triples
from urban_json import JsltTemplate

# Sans `docs/`, ces tests n'ont pas de matière : on le dit au lieu de les faire
# échouer (cf. `_docs.find_docs`).
pytestmark = pytest.mark.skipif(DOCS is None, reason=NO_DOCS)


CASES = doc_triples()


def test_guide_has_examples() -> None:
    # Garde-fou : si l'extraction casse, on ne veut pas « 0 test » silencieux.
    assert len(CASES) >= 100


def test_guide_examples_are_bilingual() -> None:
    french, english = counts_by_language()
    assert french == english, (
        f"{french} exemples en français, {english} en anglais : "
        "une documentation bilingue n'est pas finie tant que les deux ne se répondent pas"
    )


@pytest.mark.parametrize("template, source, expected", CASES)
def test_guide_example(template: str, source: str, expected: str) -> None:
    result = JsltTemplate.parse(template).transform(json.loads(source))
    assert result == json.loads(expected)
