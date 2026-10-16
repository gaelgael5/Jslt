"""Débogage de template : trace d'évaluation + points d'arrêt.

Vérifie que ``JsltTemplate.debug`` produit une trace pas-à-pas (une étape par nœud
évalué, avec localisation et valeur produite), marque les points d'arrêt (par
fonction / par ligne), rapporte les erreurs, et reste sérialisable en JSON.
"""

from __future__ import annotations

import json

from urban_json import DebugResult, JsltTemplate, TraceStep


def test_trace_records_nodes_and_values() -> None:
    result = JsltTemplate.parse('{ "sum": $.a + $.b }').debug({"a": 1, "b": 2})
    assert isinstance(result, DebugResult)
    assert result.error is None
    assert result.result == {"sum": 3}
    assert result.steps  # non vide
    # Enregistrement en ordre d'évaluation (post-ordre) : la racine en dernier.
    root = result.steps[-1]
    assert root.kind == "JsltObject"
    assert root.result == {"sum": 3}
    # Les sous-expressions sont tracées avec leur valeur.
    assert any(s.kind == "JsltPath" and s.result == 1 for s in result.steps)
    assert any(s.kind == "JsltBinaryOperator" and s.result == 3 for s in result.steps)


def test_step_has_location() -> None:
    steps = JsltTemplate.parse('{ "n": $.x }').debug({"x": 5}).steps
    path = next(s for s in steps if s.kind == "JsltPath")
    assert isinstance(path, TraceStep)
    assert path.line == 1
    assert path.column is not None
    assert path.expression == "$.x"
    assert path.result == 5


def test_breakpoint_on_function() -> None:
    result = JsltTemplate.parse('{ "t": sum($.n) }').debug(
        {"n": [1, 2, 3]}, break_functions=["sum"]
    )
    assert result.result == {"t": 6}
    fn = next(s for s in result.steps if s.function == "sum")
    assert fn.breakpoint is True
    assert fn.result == 6
    # Un nœud non visé n'est pas marqué.
    assert all(not s.breakpoint for s in result.steps if s.kind == "JsltObject")


def test_breakpoint_on_line() -> None:
    template = '{\n  "t": sum($.n)\n}'
    result = JsltTemplate.parse(template).debug({"n": [1, 2]}, break_lines=[2])
    assert any(s.breakpoint and s.line == 2 for s in result.steps)


def test_error_is_reported_with_partial_trace() -> None:
    result = JsltTemplate.parse('{ "x": nope() }').debug(None)
    assert result.result is None
    assert result.error is not None
    assert "nope" in result.error


def test_debug_result_is_json_serialisable() -> None:
    result = JsltTemplate.parse('[ { "$source": $.items, "v": $.n } ]').debug(
        {"items": [{"n": 1}, {"n": 2}]}
    )
    assert result.result == [{"v": 1}, {"v": 2}]
    dumped = json.dumps(result.to_dict())  # ne doit pas lever
    assert '"steps"' in dumped
