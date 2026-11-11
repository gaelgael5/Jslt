"""``parsexml`` : même conversion que ``loadxml``, depuis une chaîne."""

from __future__ import annotations

import pytest
from urban_json import JsltTemplate, default_registry
from urban_json.errors import JsltError

from urban_json_xml import register


@pytest.fixture(autouse=True)
def _registre():
    register(default_registry)


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


def test_parsexml_convertit_un_texte():
    xml = '<racine><item id="1">a</item></racine>'
    assert run('{ "r": parsexml($.t) }', {"t": xml}) == {
        "r": {"racine": {"item": {"@id": "1", "#text": "a"}}}
    }


def test_parsexml_donne_le_meme_resultat_que_loadxml(tmp_path):
    xml = "<a><b>1</b><b>2</b></a>"
    chemin = tmp_path / "x.xml"
    chemin.write_text(xml, encoding="utf-8")
    depuis_fichier = run('{ "r": loadxml($.p) }', {"p": str(chemin)})
    assert run('{ "r": parsexml($.t) }', {"t": xml}) == depuis_fichier


def test_parsexml_null_reste_null():
    assert run('{ "r": parsexml($.t) }', {}) == {"r": None}


def test_parsexml_texte_invalide_leve_une_erreur_jslt():
    with pytest.raises(JsltError, match="XML invalide"):
        run('{ "r": parsexml($.t) }', {"t": "<a>"})


def test_parsexml_non_chaine_leve():
    with pytest.raises(JsltError, match="texte XML"):
        run('{ "r": parsexml($.t) }', {"t": 42})


def test_parsexml_rattrapable_par_trydefault():
    assert run('{ "r": trydefault(parsexml($.t), "ko") }', {"t": "<a>"}) == {"r": "ko"}
