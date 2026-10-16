"""Tests du plugin urban-json-elastic (``esconnect`` / ``essearch``).

Aucun serveur Elasticsearch requis : on injecte un faux client via le point
d'injection ``_build_client``. Couvre : descripteur de connexion, recherche +
extraction des ``_source``, requête par défaut (match_all), paramètre size,
erreurs, découverte entry point, usage en template.
"""

from __future__ import annotations

import pytest
from urban_json import FunctionRegistry, JsltTemplate

import urban_json_elastic
from urban_json_elastic import execute_esconnect, execute_essearch, register


class _FakeClient:
    def __init__(self, hits):
        self._hits = hits
        self.calls = []

    def search(self, **kwargs):
        self.calls.append(kwargs)
        return {"hits": {"hits": [{"_source": h} for h in self._hits]}}


@pytest.fixture
def fake_es(monkeypatch):
    """Installe un faux client ; renvoie l'instance pour inspecter les appels."""
    client = _FakeClient([{"title": "A", "price": 10}, {"title": "B", "price": 20}])
    monkeypatch.setattr(urban_json_elastic, "_build_client", lambda connection: client)
    return client


def test_esconnect_descriptor() -> None:
    cx = execute_esconnect(None, "https://localhost:9200", api_key="k")
    assert cx == {"hosts": "https://localhost:9200", "verify_certs": True, "api_key": "k"}


def test_esconnect_basic_auth() -> None:
    cx = execute_esconnect(None, "https://es:9200", username="u", password="p")
    assert cx["basic_auth"] == ["u", "p"]


def test_esconnect_requires_hosts() -> None:
    with pytest.raises(ValueError, match="hosts"):
        execute_esconnect(None)


def test_essearch_returns_sources(fake_es) -> None:
    cx = {"hosts": "https://es:9200"}
    docs = execute_essearch(None, cx, "products", {"match": {"category": "book"}})
    assert docs == [{"title": "A", "price": 10}, {"title": "B", "price": 20}]


def test_essearch_default_query_is_match_all(fake_es) -> None:
    execute_essearch(None, {"hosts": "x"}, "products")
    assert fake_es.calls[0]["query"] == {"match_all": {}}


def test_essearch_passes_index_and_size(fake_es) -> None:
    execute_essearch(None, {"hosts": "x"}, "products", {"match_all": {}}, size=50)
    call = fake_es.calls[0]
    assert call["index"] == "products"
    assert call["size"] == 50


def test_essearch_requires_descriptor() -> None:
    with pytest.raises(ValueError, match="descripteur"):
        execute_essearch(None, "nope", "products")


def test_essearch_requires_index(fake_es) -> None:
    with pytest.raises(ValueError, match="index"):
        execute_essearch(None, {"hosts": "x"}, None)


def test_register_into_custom_registry() -> None:
    reg = FunctionRegistry()
    register(reg)
    assert "esconnect" in reg and "essearch" in reg


def test_discovered_via_entry_point() -> None:
    from urban_json import default_registry, load_plugins

    load_plugins(default_registry)
    assert "esconnect" in default_registry and "essearch" in default_registry


def test_in_template(fake_es) -> None:
    template = (
        '{ "es:": esconnect("https://es:9200"),'
        '  "docs": [ { "$source": essearch(es:, "products"), "n": $.title } ] }'
    )
    assert JsltTemplate.parse(template).transform({}) == {
        "docs": [{"n": "A"}, {"n": "B"}]
    }
