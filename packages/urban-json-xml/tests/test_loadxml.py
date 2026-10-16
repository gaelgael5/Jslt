"""Tests du plugin urban-json-xml (fonction ``loadxml``).

Couvre : conventions de conversion (attributs ``@``, texte ``#text``, frères
homonymes → tableau, élément vide → null), namespaces, découverte via entry point,
usage en template, et sécurité (XXE / entités désactivées via defusedxml).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from defusedxml.common import EntitiesForbidden
from urban_json import FunctionRegistry, JsltTemplate

from urban_json_xml import execute_loadxml, register


def _write(tmp_path: Path, name: str, content: str) -> str:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return str(path)


def test_text_only_element(tmp_path: Path) -> None:
    path = _write(tmp_path, "a.xml", "<a>v</a>")
    assert execute_loadxml(None, path) == {"a": "v"}


def test_attributes_and_text(tmp_path: Path) -> None:
    path = _write(tmp_path, "a.xml", '<a x="1">v</a>')
    assert execute_loadxml(None, path) == {"a": {"@x": "1", "#text": "v"}}


def test_empty_element_is_null(tmp_path: Path) -> None:
    path = _write(tmp_path, "a.xml", "<a/>")
    assert execute_loadxml(None, path) == {"a": None}


def test_repeated_siblings_become_array(tmp_path: Path) -> None:
    path = _write(tmp_path, "a.xml", "<a><b>1</b><b>2</b></a>")
    assert execute_loadxml(None, path) == {"a": {"b": ["1", "2"]}}


def test_single_child_is_not_array(tmp_path: Path) -> None:
    path = _write(tmp_path, "a.xml", "<a><b>1</b></a>")
    assert execute_loadxml(None, path) == {"a": {"b": "1"}}


def test_nested_structure(tmp_path: Path) -> None:
    xml = '<catalog><book id="1"><title>A</title></book><book id="2"><title>B</title></book></catalog>'
    path = _write(tmp_path, "c.xml", xml)
    assert execute_loadxml(None, path) == {
        "catalog": {
            "book": [
                {"@id": "1", "title": "A"},
                {"@id": "2", "title": "B"},
            ]
        }
    }


def test_values_stay_strings(tmp_path: Path) -> None:
    # Fidèle à Newtonsoft : pas de coercition de type (10 reste "10").
    path = _write(tmp_path, "a.xml", "<a><n>10</n><b>true</b></a>")
    assert execute_loadxml(None, path) == {"a": {"n": "10", "b": "true"}}


def test_strip_namespaces_default(tmp_path: Path) -> None:
    xml = '<root xmlns:ns="http://ex"><ns:item>v</ns:item></root>'
    path = _write(tmp_path, "ns.xml", xml)
    assert execute_loadxml(None, path) == {"root": {"item": "v"}}


def test_keep_namespaces_when_disabled(tmp_path: Path) -> None:
    xml = '<root xmlns:ns="http://ex"><ns:item>v</ns:item></root>'
    path = _write(tmp_path, "ns.xml", xml)
    result = execute_loadxml(None, path, strip_namespaces=False)
    assert result == {"root": {"{http://ex}item": "v"}}


def test_custom_prefix_and_text_key(tmp_path: Path) -> None:
    path = _write(tmp_path, "a.xml", '<a x="1">v</a>')
    result = execute_loadxml(None, path, attribute_prefix="_", text_key="value")
    assert result == {"a": {"_x": "1", "value": "v"}}


def test_register_into_custom_registry() -> None:
    reg = FunctionRegistry()
    register(reg)
    assert "loadxml" in reg
    assert reg.describe("loadxml").description


def test_discovered_via_entry_point() -> None:
    from urban_json import default_registry, load_plugins

    load_plugins(default_registry)
    assert "loadxml" in default_registry


def test_loadxml_in_template(tmp_path: Path) -> None:
    xml = "<catalog><book><title>A</title></book><book><title>B</title></book></catalog>"
    path = _write(tmp_path, "c.xml", xml)
    template = (
        f'[ {{ "$source": select(loadxml("{path}"), $.catalog.book), "t": $.title }} ]'
    )
    assert JsltTemplate.parse(template).transform({}) == [{"t": "A"}, {"t": "B"}]


def test_xxe_external_entity_is_blocked(tmp_path: Path) -> None:
    secret = _write(tmp_path, "secret.txt", "TOP SECRET")
    xml = (
        '<?xml version="1.0"?>'
        f'<!DOCTYPE r [<!ENTITY xxe SYSTEM "file://{secret}">]>'
        "<r>&xxe;</r>"
    )
    path = _write(tmp_path, "evil.xml", xml)
    # defusedxml doit refuser l'entité (pas d'exfiltration du secret).
    with pytest.raises(EntitiesForbidden):
        execute_loadxml(None, path)
