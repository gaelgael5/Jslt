"""``parsecsv`` : même lecture que ``loadcsv``, depuis une chaîne."""

from __future__ import annotations

import pytest
from urban_json import JsltTemplate, default_registry
from urban_json.errors import JsltError

from urban_json_csv import register


@pytest.fixture(autouse=True)
def _registre():
    register(default_registry)


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


CSV = "nom;age\nAna;30\nBob;25\n"


def test_parsecsv_lit_un_texte():
    assert run('{ "r": parsecsv($.t) }', {"t": CSV}) == {
        "r": [{"nom": "Ana", "age": 30}, {"nom": "Bob", "age": 25}]
    }


def test_parsecsv_donne_le_meme_resultat_que_loadcsv(tmp_path):
    chemin = tmp_path / "x.csv"
    chemin.write_text(CSV, encoding="utf-8")
    assert run('{ "r": parsecsv($.t) }', {"t": CSV}) == run(
        '{ "r": loadcsv($.p) }', {"p": str(chemin)}
    )


def test_parsecsv_separateur_et_entete():
    texte = "a,b\n1,2\n"
    assert run('{ "r": parsecsv($.t, true, ",") }', {"t": texte}) == {"r": [{"a": 1, "b": 2}]}


def test_parsecsv_sans_entete():
    assert run('{ "r": parsecsv($.t, false) }', {"t": "1;2\n"}) == {
        "r": [{"Column0": 1, "Column1": 2}]
    }


def test_parsecsv_null_reste_null():
    assert run('{ "r": parsecsv($.t) }', {}) == {"r": None}


def test_parsecsv_non_chaine_leve():
    with pytest.raises(JsltError, match="texte CSV"):
        run('{ "r": parsecsv($.t) }', {"t": 42})


def test_parsecsv_texte_vide_rend_un_tableau_vide():
    assert run('{ "r": parsecsv($.t) }', {"t": ""}) == {"r": []}
