"""Tests de l'API du playground (FastAPI TestClient, sans réseau)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from urban_json_playground.app import app

client = TestClient(app)


def test_transform_ok() -> None:
    resp = client.post(
        "/api/transform",
        json={"template": '{ "n": $.user.name, "y": $.user.age + 1 }',
              "source": '{"user": {"name": "Alice", "age": 30}}'},
    )
    assert resp.status_code == 200
    assert resp.json() == {"result": {"n": "Alice", "y": 31}}


def test_transform_syntax_error() -> None:
    resp = client.post("/api/transform", json={"template": '{ "n": ~ }', "source": "null"})
    assert resp.status_code == 400
    assert "error" in resp.json()


def test_transform_invalid_source_json() -> None:
    resp = client.post("/api/transform", json={"template": "{}", "source": "{not json"})
    assert resp.status_code == 400
    assert "JSON source" in resp.json()["error"]


def test_sandbox_excludes_io_plugins() -> None:
    # Les fonctions d'E-S (plugins) ne doivent PAS être accessibles.
    resp = client.post(
        "/api/transform",
        json={"template": '{ "x": loadcsv("x") }', "source": "null"},
    )
    assert resp.status_code == 400


def test_functions_catalog_is_core_only() -> None:
    data = client.get("/api/functions").json()
    names = {f["name"] for f in data["functions"]}
    assert "sum" in names          # fonction cœur présente
    assert "loadcsv" not in names  # plugin d'E-S absent (bac à sable)


def test_index_served() -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert "<jslt-editor" in resp.text


def test_editor_assets_served() -> None:
    resp = client.get("/jslt-editor/jslt-editor.js")
    assert resp.status_code == 200
    assert "customElements.define" in resp.text


def test_examples_listed() -> None:
    data = client.get("/api/examples").json()
    assert len(data["examples"]) >= 5
    for ex in data["examples"]:
        assert {"name", "template", "source"} <= ex.keys()


def test_debug_returns_steps() -> None:
    resp = client.post(
        "/api/debug",
        json={"template": '{ "t": sum($.n) }', "source": '{"n": [1, 2, 3]}',
              "break_functions": ["sum"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == {"t": 6}
    assert data["steps"], "trace non vide attendue"
    fn = next(s for s in data["steps"] if s["function"] == "sum")
    assert fn["breakpoint"] is True and fn["result"] == 6


def test_debug_reports_error_with_partial_trace() -> None:
    resp = client.post("/api/debug", json={"template": '{ "x": nope() }', "source": "null"})
    assert resp.status_code == 200  # l'erreur d'exécution est rapportée dans le corps
    assert resp.json()["error"] is not None


def test_every_example_transforms_ok() -> None:
    # Les exemples servent aussi d'oracle : chacun doit transformer sans erreur.
    examples = client.get("/api/examples").json()["examples"]
    for ex in examples:
        resp = client.post(
            "/api/transform",
            json={"template": ex["template"], "source": ex["source"]},
        )
        assert resp.status_code == 200, f"exemple '{ex['name']}' échoue : {resp.json()}"
        assert "result" in resp.json()
