"""``schema(fragment)`` — port de ``LoadSchema`` (NJsonSchema
``JsonSchema.FromSampleJson``, draft-04) : JSON Schema déduit d'un exemple."""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate

DRAFT = "http://json-schema.org/draft-04/schema#"


def schema(fragment):
    return JsltTemplate.parse('{ "r": schema($.f) }').transform({"f": fragment})["r"]


def test_scalaires() -> None:
    assert schema({"s": "a", "i": 1, "n": 1.5, "b": True, "z": None}) == {
        "$schema": DRAFT,
        "type": "object",
        "properties": {
            "s": {"type": "string"},
            "i": {"type": "integer"},
            "n": {"type": "number"},
            "b": {"type": "boolean"},
            "z": {},
        },
    }


@pytest.mark.parametrize(
    ("value", "fmt"),
    [
        pytest.param("2026-10-22", "date", id="date"),
        pytest.param("2026-10-22T14:05:00", "date-time", id="iso-datetime"),
        pytest.param("2026-10-22T00:00:00", "date", id="iso-minuit-est-une-date"),
        pytest.param("2026-10-22 14:05", "date-time", id="date-heure-espace"),
        pytest.param("14:05:09", "duration", id="duree"),
    ],
)
def test_formats_de_chaines(value, fmt) -> None:
    assert schema({"d": value})["properties"]["d"] == {"type": "string", "format": fmt}


def test_objet_imbrique_en_definition() -> None:
    out = schema({"owner": {"first-name": "Ana"}})
    assert out["properties"]["owner"] == {"$ref": "#/definitions/Owner"}
    assert out["definitions"] == {
        "Owner": {"type": "object", "properties": {"first-name": {"type": "string"}}}
    }


def test_tableau_d_objets_singularise_et_fusionne() -> None:
    out = schema({"orders": [{"id": 1}, {"id": 2, "total": 9.5}]})
    assert out["properties"]["orders"] == {"type": "array", "items": {"$ref": "#/definitions/Order"}}
    assert out["definitions"]["Order"] == {
        "type": "object",
        "properties": {"id": {"type": "integer"}, "total": {"type": "number"}},
    }


def test_tableau_de_chaines_a_aussi_sa_definition() -> None:
    # Comportement NJsonSchema conservé : tout tableau homogène reçoit une définition.
    out = schema({"tags": ["a", "b"]})
    assert out["properties"]["tags"] == {"type": "array", "items": {"$ref": "#/definitions/Tag"}}
    assert out["definitions"]["Tag"] == {"type": "string"}


def test_tableau_vide_et_heterogene() -> None:
    out = schema({"vide": [], "mix": [1, "a"]})
    assert out["properties"]["vide"] == {"type": "array", "items": {}}
    assert out["properties"]["mix"] == {"type": "array", "items": {"type": "integer"}}


def test_definition_reutilisee_si_elle_couvre_les_proprietes() -> None:
    out = schema({"home": {"city": "Lyon"}, "work": {"city": "Paris"}})
    assert out["properties"]["home"] == {"$ref": "#/definitions/Home"}
    assert out["properties"]["work"] == {"$ref": "#/definitions/Home"}
    assert list(out["definitions"]) == ["Home"]


def test_collision_de_nom_anonymous() -> None:
    out = schema({"a": {"x": 1}, "b": {"a": {"y": 2}}})
    # « A » existe déjà (autres propriétés) : la 2e reçoit un nom Anonymous<n>.
    assert set(out["definitions"]) == {"A", "B", "Anonymous3"}


def test_racine_tableau() -> None:
    out = schema([{"id": 1}])
    assert out["type"] == "array"
    assert out["items"] == {"$ref": "#/definitions/Anonymous"}
    assert out["definitions"]["Anonymous"]["properties"] == {"id": {"type": "integer"}}


def test_racine_scalaire() -> None:
    assert schema(3) == {"$schema": DRAFT, "type": "integer"}
