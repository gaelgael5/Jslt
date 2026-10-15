"""Phase 3a — boucles (``$source`` / ``$where``).

Un item (objet) d'un tableau porteur d'un ``$source`` itère sur le tableau
source : une entrée de sortie par élément, l'élément devenant la source courante
des chemins internes. ``$where`` filtre (conversion booléenne stricte : seul le
booléen ``True`` passe, conforme à ``RuntimeContext.ConvertToBool``). Un objet
porteur d'un ``$source`` hors tableau construit un objet unique sur la projection.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate

LOOP_CASES = [
    pytest.param(
        '[ { "$source": $.items, "Key": $.name } ]',
        {"items": [{"name": "a"}, {"name": "b"}, {"name": "c"}]},
        [{"Key": "a"}, {"Key": "b"}, {"Key": "c"}],
        id="boucle-readme",
    ),
    pytest.param(
        '[ { "$source": $, "key": $.Key } ]',
        [{"Key": 2}, {"Key": 3}],
        [{"key": 2}, {"key": 3}],
        id="boucle-sur-racine",
    ),
    pytest.param(
        '[ { "$source": $.items, "n": $.n } ]',
        {"items": []},
        [],
        id="boucle-vide",
    ),
    pytest.param(
        '[ { "$source": $.items, "$where": $.ok, "n": $.n } ]',
        {"items": [{"ok": True, "n": 1}, {"ok": False, "n": 2}, {"ok": True, "n": 3}]},
        [{"n": 1}, {"n": 3}],
        id="where-filtre",
    ),
    pytest.param(
        '[ { "$source": $.groups, "vals": [ { "$source": $.items, "v": $.v } ] } ]',
        {"groups": [{"items": [{"v": 1}, {"v": 2}]}, {"items": [{"v": 3}]}]},
        [{"vals": [{"v": 1}, {"v": 2}]}, {"vals": [{"v": 3}]}],
        id="boucle-imbriquee",
    ),
]


@pytest.mark.parametrize("template, source, expected", LOOP_CASES)
def test_loops(template: str, source, expected) -> None:
    assert JsltTemplate.parse(template).transform(source) == expected


def test_object_source_projection() -> None:
    # Objet avec $source hors tableau : un seul objet, chemins résolus dans $.a.
    template = '{ "$source": $.a, "xx": $.x, "yy": $.y }'
    source = {"a": {"x": 1, "y": 2}}
    assert JsltTemplate.parse(template).transform(source) == {"xx": 1, "yy": 2}


def test_current_source_restored_after_loop() -> None:
    # Après une boucle, les chemins du niveau parent se résolvent à nouveau sur
    # la source racine.
    template = '{ "list": [ { "$source": $.items, "v": $.v } ], "top": $.title }'
    source = {"items": [{"v": 1}], "title": "T"}
    assert JsltTemplate.parse(template).transform(source) == {"list": [{"v": 1}], "top": "T"}
