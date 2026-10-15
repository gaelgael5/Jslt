"""Fonction ``distinct`` + mécanisme « argument = chemin ».

``distinct(source, path)`` reçoit ``path`` comme chemin JSONPath **compilé**
(non évalué), grâce au marquage ``path_args`` du registre. ``path`` est appliqué
à ``source`` pour sélectionner les clés dédupliquées (scalaires par valeur ;
objets et ``null`` ignorés ; ordre conservé).
"""

from __future__ import annotations

import pytest

from jslt import JsltTemplate

DISTINCT_CASES = [
    pytest.param("{ 'r': distinct($, $.*) }", [1, 1, 2, 2, 3], {"r": [1, 2, 3]}, id="racine"),
    pytest.param(
        "{ 'r': distinct($.list, $.*) }", {"list": [3, 3, 1, 2, 2]}, {"r": [3, 1, 2]}, id="sous-liste"
    ),
    pytest.param(
        "{ 'r': distinct($.items, $.*.k) }",
        {"items": [{"k": "a"}, {"k": "b"}, {"k": "a"}]},
        {"r": ["a", "b"]},
        id="cle-projetee",
    ),
    pytest.param("{ 'r': distinct($, $.*) }", [1, None, 1, 2], {"r": [1, 2]}, id="null-ignore"),
]


def q(template: str) -> str:
    return template.replace("'", '"')


@pytest.mark.parametrize("template, source, expected", DISTINCT_CASES)
def test_distinct(template: str, source, expected) -> None:
    assert JsltTemplate.parse(q(template)).transform(source) == expected


def test_path_argument_is_not_evaluated() -> None:
    # Garde-fou du mécanisme : l'argument chemin arrive compilé, pas évalué.
    # (Si $.* était évalué comme valeur, distinct recevrait une liste, pas un chemin.)
    from jslt.functions import default_registry

    assert default_registry.path_args_of("distinct") == (1,)
    assert default_registry.path_args_of("sum") == ()  # args normaux évalués
