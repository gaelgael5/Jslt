"""Tests du plugin urban-json-http (``http`` / ``httpget``).

Aucune requête réseau réelle : on injecte un ``httpx.MockTransport`` via le point
d'injection ``_build_client``. Couvre : GET/POST, en-têtes, query, corps JSON,
réponse texte, convenance httpget, erreurs, découverte entry point, template.
"""

from __future__ import annotations

import json

import httpx
import pytest
from urban_json import FunctionRegistry, JsltTemplate

import urban_json_http
from urban_json_http import execute_http, execute_httpget, register


@pytest.fixture
def mock_http(monkeypatch):
    """Installe un transport mocké ; renvoie la liste des requêtes capturées."""
    captured = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        if request.url.path == "/text":
            return httpx.Response(200, text="plain", headers={"content-type": "text/plain"})
        if request.url.path == "/boom":
            return httpx.Response(500, json={"error": "nope"})
        return httpx.Response(
            200,
            json={"ok": True, "path": request.url.path},
            headers={"x-demo": "1"},
        )

    transport = httpx.MockTransport(handler)
    monkeypatch.setattr(
        urban_json_http, "_build_client", lambda timeout: httpx.Client(transport=transport, timeout=timeout)
    )
    return captured


def test_get_returns_structured_response(mock_http) -> None:
    r = execute_http(None, {"method": "GET", "url": "https://api/x"})
    assert r["status"] == 200
    assert r["body"] == {"ok": True, "path": "/x"}
    assert r["headers"]["x-demo"] == "1"


def test_default_method_is_get(mock_http) -> None:
    execute_http(None, {"url": "https://api/x"})
    assert mock_http[0].method == "GET"


def test_headers_and_query_are_sent(mock_http) -> None:
    execute_http(
        None,
        {"url": "https://api/x", "headers": {"Authorization": "Bearer z"}, "query": {"page": 1}},
    )
    req = mock_http[0]
    assert req.headers["authorization"] == "Bearer z"
    assert req.url.params.get("page") == "1"


def test_post_sends_json_body(mock_http) -> None:
    execute_http(None, {"method": "POST", "url": "https://api/x", "body": {"a": 1}})
    req = mock_http[0]
    assert req.method == "POST"
    assert json.loads(req.content) == {"a": 1}
    assert "application/json" in req.headers["content-type"]


def test_text_response_body(mock_http) -> None:
    r = execute_http(None, {"url": "https://api/text"})
    assert r["body"] == "plain"


def test_httpget_returns_body(mock_http) -> None:
    body = execute_httpget(None, "https://api/users")
    assert body == {"ok": True, "path": "/users"}


def test_error_status_still_returned(mock_http) -> None:
    r = execute_http(None, {"url": "https://api/boom"})
    assert r["status"] == 500
    assert r["body"] == {"error": "nope"}


def test_request_must_be_object() -> None:
    with pytest.raises(ValueError, match="objet"):
        execute_http(None, "not-an-object")


def test_url_required() -> None:
    with pytest.raises(ValueError, match="url"):
        execute_http(None, {"method": "GET"})


def test_register_into_custom_registry() -> None:
    reg = FunctionRegistry()
    register(reg)
    assert "http" in reg and "httpget" in reg


def test_discovered_via_entry_point() -> None:
    from urban_json import default_registry, load_plugins

    load_plugins(default_registry)
    assert "http" in default_registry and "httpget" in default_registry


def test_in_template(mock_http) -> None:
    template = '{ "r:": http({ "url": "https://api/items" }), "code": r:$.status, "ok": r:$.body.ok }'
    assert JsltTemplate.parse(template).transform({}) == {"code": 200, "ok": True}


# --- loadhttpgetjson : compatibilité avec le .NET (loadhttpgetJson) ----------------


def test_loadhttpgetjson_url_de_base_et_methode(mock_http) -> None:
    from urban_json_http import execute_loadhttpgetjson

    assert execute_loadhttpgetjson(None, "https://api/v1/", "users") == {"ok": True, "path": "/v1/users"}
    assert mock_http[0].headers["accept"] == "application/json"


def test_loadhttpgetjson_echec_http_donne_null(mock_http) -> None:
    from urban_json_http import execute_loadhttpgetjson

    assert execute_loadhttpgetjson(None, "https://api/", "boom") is None


def test_loadhttpgetjson_reponse_non_json_donne_null(mock_http) -> None:
    from urban_json_http import execute_loadhttpgetjson

    assert execute_loadhttpgetjson(None, "https://api/", "text") is None


@pytest.mark.parametrize("error", [httpx.ConnectError("refused"), httpx.ReadTimeout("slow")])
def test_loadhttpgetjson_hote_injoignable_erreur_lisible(monkeypatch, error) -> None:
    from urban_json import JsltError

    from urban_json_http import execute_loadhttpgetjson

    def handler(request: httpx.Request) -> httpx.Response:
        raise error

    transport = httpx.MockTransport(handler)
    monkeypatch.setattr(
        urban_json_http, "_build_client", lambda timeout: httpx.Client(transport=transport, timeout=timeout)
    )
    with pytest.raises(JsltError, match=r"loadhttpgetjson : appel impossible vers 'https://api/x'"):
        execute_loadhttpgetjson(None, "https://api/", "x")


def test_loadhttpgetjson_url_requise() -> None:
    from urban_json import JsltError

    from urban_json_http import execute_loadhttpgetjson

    with pytest.raises(JsltError, match="loadhttpgetjson"):
        execute_loadhttpgetjson(None, None, "x")


def test_loadhttpgetjson_dans_un_template(mock_http) -> None:
    registry = FunctionRegistry()
    register(registry)
    template = JsltTemplate.parse('{ "r": loadhttpgetJson("https://api/", "x") }')
    assert template.transform({}, functions=registry)["r"] == {"ok": True, "path": "/x"}
