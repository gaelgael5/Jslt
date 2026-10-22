"""loadhtml — port de ServiceHtml (HtmlAgilityPack -> JSON)."""

from __future__ import annotations

from pathlib import Path

import pytest
from urban_json import FunctionRegistry, JsltError, JsltTemplate

from urban_json_html import html_to_json, register


@pytest.fixture(scope="module")
def registry() -> FunctionRegistry:
    reg = FunctionRegistry()
    register(reg)
    return reg


def test_structure_element_attributs_contenu() -> None:
    out = html_to_json('<div id="a" class="x"><p>Bonjour</p><p>le <b>monde</b></p></div>')
    assert out == {
        "#id": "#document",
        "content": {
            "#id": "div", "id": "a", "class": "x",
            "content": [
                {"#id": "p", "content": "#text: Bonjour"},
                {"#id": "p", "content": ["#text: le ", {"#id": "b", "content": "#text: monde"}]},
            ],
        },
    }


def test_texte_blanc_ignore_commentaire_et_doctype() -> None:
    out = html_to_json("<!DOCTYPE html>\n<p> <!-- note --> </p>")
    assert out["content"] == [
        "#comment: <!DOCTYPE html>",
        {"#id": "p", "content": "#comment: <!-- note -->"},
    ]


def test_elements_vides_et_casse_des_balises() -> None:
    out = html_to_json('<DIV>a<br>b<IMG src="x.png"></DIV>')
    assert out["content"] == {
        "#id": "DIV",
        "content": ["#text: a", {"#id": "br"}, "#text: b", {"#id": "IMG", "src": "x.png"}],
    }


def test_balise_non_fermee_et_attribut_sans_valeur() -> None:
    out = html_to_json("<ul><li>1<li>2</ul><input disabled>")
    assert out["content"][0]["#id"] == "ul"
    assert out["content"][1] == {"#id": "input", "disabled": ""}


def test_entites_conservees_comme_html_agility_pack() -> None:
    assert html_to_json("<p>a &amp; b</p>")["content"]["content"] == "#text: a &amp; b"


def test_loadhtml_fichier(registry, tmp_path: Path) -> None:
    page = tmp_path / "p.html"
    page.write_text("<h1>Titre</h1>", encoding="utf-8")
    template = JsltTemplate.parse('{ "r": loadhtml($.p) }')
    out = template.transform({"p": str(page)}, functions=registry)["r"]
    assert out["content"] == {"#id": "h1", "content": "#text: Titre"}


def test_loadhtml_uri_fichier(registry, tmp_path: Path) -> None:
    page = tmp_path / "p.html"
    page.write_text("<i>x</i>", encoding="utf-8")
    template = JsltTemplate.parse('{ "r": loadhtml($.p) }')
    assert template.transform({"p": page.as_uri()}, functions=registry)["r"]["content"]["#id"] == "i"


def test_loadhtml_url(registry, monkeypatch) -> None:
    import urban_json_html

    monkeypatch.setattr(urban_json_html, "_fetch_url", lambda url: "<em>web</em>")
    template = JsltTemplate.parse('{ "r": loadhtml("https://exemple.test/page") }')
    assert template.transform({}, functions=registry)["r"]["content"] == {"#id": "em", "content": "#text: web"}


@pytest.mark.parametrize("value", [None, "/chemin/absent.html"])
def test_loadhtml_erreurs(registry, value) -> None:
    template = JsltTemplate.parse('{ "r": loadhtml($.p) }')
    with pytest.raises(JsltError, match="loadhtml"):
        template.transform({"p": value}, functions=registry)


def test_catalogue_et_decouverte(registry) -> None:
    from urban_json import default_registry, load_plugins

    assert len(registry.catalog()[0]["description"]) >= 15
    load_plugins()
    assert "loadhtml" in default_registry
