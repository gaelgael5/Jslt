"""Types, repli sur erreur, validation de schéma et lecture de JSON.

Sujets « types et validation » et « désérialisation entrante ». Le moteur ne
savait dire que `isnull` / `isnotnull` ; `schema` **déduisait** un schéma sans
jamais pouvoir valider contre lui ; et une chaîne contenant du JSON restait une
chaîne.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


@pytest.mark.parametrize(
    "value, kind",
    [
        (None, "null"), (True, "boolean"), (1, "number"), (1.5, "number"),
        ("x", "string"), ([1], "array"), ({"a": 1}, "object"),
    ],
)
def test_typeof(value, kind):
    assert run('{ "r": typeof($.v) }', {"v": value}) == {"r": kind}


def test_typeof_clef_absente_vaut_null():
    assert run('{ "r": typeof($.zz) }', {}) == {"r": "null"}


@pytest.mark.parametrize(
    "call, value, expected",
    [
        ("isarray", [1], True), ("isarray", {"a": 1}, False),
        ("isobject", {"a": 1}, True), ("isobject", [1], False),
        ("isstring", "x", True), ("isstring", 1, False),
        ("isnumber", 1, True), ("isnumber", "1", False), ("isnumber", True, False),
        ("isboolean", False, True), ("isboolean", 0, False),
    ],
)
def test_predicats(call, value, expected):
    assert run('{ "r": ' + call + "($.v) }", {"v": value}) == {"r": expected}


def test_predicats_sur_null_sont_faux():
    template = (
        '{ "a": isarray($.zz), "b": isobject($.zz), "c": isstring($.zz), '
        '"d": isnumber($.zz), "e": isboolean($.zz) }'
    )
    assert run(template, {}) == {"a": False, "b": False, "c": False, "d": False, "e": False}


# --- trydefault ---------------------------------------------------------------


def test_trydefault_rend_la_valeur_quand_tout_va_bien():
    assert run('{ "r": trydefault($.a + 1, 0) }', {"a": 1}) == {"r": 2}


def test_trydefault_rattrape_une_erreur_de_calcul():
    assert run('{ "r": trydefault($.a / $.b, 0) }', {"a": 1, "b": 0}) == {"r": 0}


def test_trydefault_rattrape_un_cast_impossible():
    assert run('{ "r": trydefault($.s #integer, -1) }', {"s": "abc"}) == {"r": -1}


def test_trydefault_rattrape_une_fonction_qui_leve():
    assert run('{ "r": trydefault(sum($.v), 0) }', {"v": ["x"]}) == {"r": 0}


def test_trydefault_n_evalue_le_repli_que_si_besoin():
    # Si le repli était évalué d'office, ce template lèverait.
    assert run('{ "r": trydefault($.a, sum($.bad)) }', {"a": 7, "bad": ["x"]}) == {"r": 7}


def test_trydefault_ne_masque_pas_une_construction_non_portee():
    # NotImplementedError signale une fonctionnalité absente du portage, pas une
    # donnée fautive : la rattraper ferait passer un trou pour un cas limite.
    with pytest.raises(NotImplementedError):
        run('{ "r": trydefault($.a[?(@.x contains 1)], 0) }', {"a": []})


def test_une_division_par_zero_est_une_erreur_jslt():
    # Elle sortait en ZeroDivisionError brute, incatchable par un template.
    with pytest.raises(JsltError, match="division par zéro"):
        run('{ "r": $.a / $.b }', {"a": 1, "b": 0})


def test_un_calcul_sur_du_texte_est_une_erreur_jslt():
    with pytest.raises(JsltError, match="conversion numérique impossible"):
        run('{ "r": $.a + $.b }', {"a": 1, "b": "x"})


# --- parsejson ----------------------------------------------------------------


def test_parsejson_objet_et_tableau():
    assert run('{ "r": parsejson($.t) }', {"t": '{"a":[1,2]}'}) == {"r": {"a": [1, 2]}}
    assert run('{ "r": parsejson($.t) }', {"t": "[1,2]"}) == {"r": [1, 2]}


def test_parsejson_scalaires():
    assert run('{ "r": parsejson($.t) }', {"t": "42"}) == {"r": 42}
    assert run('{ "r": parsejson($.t) }', {"t": "null"}) == {"r": None}


def test_parsejson_null_reste_null():
    assert run('{ "r": parsejson($.t) }', {}) == {"r": None}


def test_parsejson_texte_invalide_leve():
    with pytest.raises(JsltError, match="JSON invalide"):
        run('{ "r": parsejson($.t) }', {"t": "{oops"})


def test_parsejson_non_chaine_leve():
    with pytest.raises(JsltError, match="texte"):
        run('{ "r": parsejson($.t) }', {"t": 42})


def test_parsejson_puis_chemin():
    template = '{ "ville": parsejson($.payload) -> select($.adresse.ville) }'
    assert run(template, {"payload": '{"adresse":{"ville":"Lyon"}}'}) == {"ville": "Lyon"}


# --- validation de schéma -----------------------------------------------------


SCHEMA = {
    "type": "object",
    "required": ["nom", "age"],
    "properties": {
        "nom": {"type": "string", "minLength": 1},
        "age": {"type": "integer", "minimum": 0, "maximum": 130},
        "mail": {"type": "string", "pattern": "@"},
        "tags": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "role": {"enum": ["admin", "user"]},
    },
}


def test_schemaisvalid_document_conforme():
    source = {"s": SCHEMA, "d": {"nom": "A", "age": 3, "tags": ["x"], "role": "user"}}
    assert run('{ "r": schemaisvalid($.d, $.s) }', source) == {"r": True}


@pytest.mark.parametrize(
    "document, fragment",
    [
        ({"nom": "A"}, "age"),                                   # requis manquant
        ({"nom": 1, "age": 3}, "chaîne"),                        # mauvais type
        ({"nom": "A", "age": 1.5}, "entier"),                    # entier attendu
        ({"nom": "A", "age": -1}, "minimum"),                    # borne basse
        ({"nom": "", "age": 1}, "minLength"),                    # longueur
        ({"nom": "A", "age": 1, "mail": "x"}, "pattern"),        # motif
        ({"nom": "A", "age": 1, "tags": [1]}, "chaîne"),         # type d'élément
        ({"nom": "A", "age": 1, "tags": []}, "minItems"),        # tableau vide
        ({"nom": "A", "age": 1, "role": "root"}, "enum"),        # valeur hors liste
    ],
)
def test_schemaerrors_nomme_le_probleme(document, fragment):
    source = {"s": SCHEMA, "d": document}
    errors = run('{ "r": schemaerrors($.d, $.s) }', source)["r"]
    assert errors, "aucune erreur signalée"
    assert any(fragment in message for message in errors), errors


def test_schemaerrors_localise_l_erreur():
    source = {"s": SCHEMA, "d": {"nom": "A", "age": 1, "tags": ["ok", 2]}}
    errors = run('{ "r": schemaerrors($.d, $.s) }', source)["r"]
    assert any("tags[1]" in message for message in errors), errors


def test_schemaerrors_document_conforme_rend_un_tableau_vide():
    source = {"s": SCHEMA, "d": {"nom": "A", "age": 3}}
    assert run('{ "r": schemaerrors($.d, $.s) }', source) == {"r": []}


def test_validation_du_schema_deduit_par_schema():
    # Boucle fermée : ce que `schema` déduit valide l'exemple dont il est tiré.
    template = '{ "r": schemaisvalid($.d, schema($.d)) }'
    assert run(template, {"d": {"nom": "A", "liste": [{"k": 1}]}}) == {"r": True}


def test_validation_suit_les_references_de_definitions():
    template = '{ "r": schemaerrors($.autre, schema($.modele)) }'
    source = {"modele": {"cmds": [{"id": 1}]}, "autre": {"cmds": [{"id": "x"}]}}
    assert run(template, source)["r"], "la $ref n'a pas été suivie"


def test_schemaisvalid_schema_absent_leve():
    with pytest.raises(JsltError, match="schéma"):
        run('{ "r": schemaisvalid($.d, $.s) }', {"d": {}})


def test_mots_clefs_inconnus_ignores():
    source = {"s": {"type": "object", "x-interne": 1, "title": "t"}, "d": {}}
    assert run('{ "r": schemaisvalid($.d, $.s) }', source) == {"r": True}
