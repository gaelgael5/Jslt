"""loadxls / loadxlssheet — port de ServicesXls + ExcelReader (.NET)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import openpyxl
import pytest
from urban_json import FunctionRegistry, JsltError, JsltTemplate

from urban_json_excel import register


@pytest.fixture(scope="module")
def registry() -> FunctionRegistry:
    reg = FunctionRegistry()
    register(reg)
    return reg


def _book(tmp_path: Path, sheets: dict[str, list[list]]) -> str:
    workbook = openpyxl.Workbook()
    workbook.remove(workbook.active)
    for name, rows in sheets.items():
        sheet = workbook.create_sheet(name)
        for row in rows:
            sheet.append(row)
    path = tmp_path / "book.xlsx"
    workbook.save(path)
    return str(path)


def sheet(registry, path: str, config: dict):
    template = JsltTemplate.parse('{ "r": loadxlssheet($.p, $.c) }')
    return template.transform({"p": path, "c": config}, functions=registry)["r"]


# Excel ne stocke pas de fuseau : date « naïve » volontaire.
PEOPLE = [["Nom complet", "Âge", "Inscrit le"], ["  Ana ", 30, datetime(2026, 1, 2)], ["Bob", 41, None]]  # noqa: DTZ001


def test_en_tete_premiere_ligne(registry, tmp_path) -> None:
    path = _book(tmp_path, {"Gens": PEOPLE})
    out = sheet(registry, path, {"FirstRowHasColumnName": True})
    assert out == [
        {"Nom_complet": "Ana", "Age": 30, "Inscrit_le": "2026-01-02T00:00:00", "$row": 0},
        {"Nom_complet": "Bob", "Age": 41, "$row": 1},
    ]


def test_sans_en_tete_noms_column_n(registry, tmp_path) -> None:
    path = _book(tmp_path, {"S": [["a", 1], ["b", 2]]})
    out = sheet(registry, path, {"AddRowNumber": False})
    assert out == [{"Column0": "a", "Column1": 1}, {"Column0": "b", "Column1": 2}]


def test_colonne_decimale_reste_decimale(registry, tmp_path) -> None:
    path = _book(tmp_path, {"S": [["v"], [1.5], [2]]})
    assert [r["v"] for r in sheet(registry, path, {"FirstRowHasColumnName": True})] == [1.5, 2.0]


def test_header_line(registry, tmp_path) -> None:
    rows = [["titre du rapport"], [None], ["Code", "Libellé"], ["A1", "Un"], ["B2", "Deux"]]
    path = _book(tmp_path, {"S": rows})
    out = sheet(registry, path, {"HeaderLine": 2, "AddRowNumber": False})
    assert out == [{"Code": "A1", "Libelle": "Un"}, {"Code": "B2", "Libelle": "Deux"}]


def test_colonnes_explicites_types_et_filtre(registry, tmp_path) -> None:
    path = _book(tmp_path, {"S": [["id", "montant", "note"], ["7", "12.5", " x "], ["8", "3", ""]]})
    config = {
        "FirstRowHasColumnName": True, "AddRowNumber": False,
        "Columns": [
            {"Index": 0, "Name": "id", "Type": "integer"},
            {"Index": 1, "Name": "montant", "Type": "decimal"},
            {"Index": 2, "Name": "note", "Trimmed": False},
        ],
    }
    assert sheet(registry, path, config) == [
        {"id": 7, "montant": 12.5, "note": " x "},
        {"id": 8, "montant": 3.0},  # valeur vide omise (BypassEmptyValue par défaut)
    ]


def test_lignes_vides_omises_ou_gardees(registry, tmp_path) -> None:
    path = _book(tmp_path, {"S": [["a"], ["x"], [None], ["y"]]})
    kept = sheet(registry, path, {"FirstRowHasColumnName": True, "ByPassEmptyObject": False})
    assert kept == [{"a": "x", "$row": 0}, {"$row": 1}, {"a": "y", "$row": 2}]
    skipped = sheet(registry, path, {"FirstRowHasColumnName": True})
    assert [r["$row"] for r in skipped] == [0, 2]


def test_noms_de_colonnes_en_double(registry, tmp_path) -> None:
    path = _book(tmp_path, {"S": [["a", "a"], [1, 2]]})
    assert sheet(registry, path, {"FirstRowHasColumnName": True, "AddRowNumber": False}) == [{"a": 1, "a_renamed_1": 2}]


def test_choix_de_la_feuille(registry, tmp_path) -> None:
    path = _book(tmp_path, {"Un": [["v"], [1]], "Deux": [["v"], [2]]})
    assert sheet(registry, path, {"Tablename": "Deux", "FirstRowHasColumnName": True})[0]["v"] == 2
    with pytest.raises(JsltError, match="plusieurs feuilles"):
        sheet(registry, path, {"FirstRowHasColumnName": True})
    with pytest.raises(JsltError, match="feuille"):
        sheet(registry, path, {"Tablename": "Trois"})


def test_feuille_unique_sans_nom(registry, tmp_path) -> None:
    # Le .NET échouait toujours ici (bug) : la feuille unique est prise.
    path = _book(tmp_path, {"Seule": [["v"], [1]]})
    assert sheet(registry, path, {"FirstRowHasColumnName": True})[0]["v"] == 1


def test_cles_de_configuration_insensibles_a_la_casse(registry, tmp_path) -> None:
    path = _book(tmp_path, {"S": [["v"], [1]]})
    assert sheet(registry, path, {"firstRowHasColumnName": True, "addrownumber": False}) == [{"v": 1}]


def test_loadxls_avec_fichier_de_configuration(registry, tmp_path) -> None:
    path = _book(tmp_path, {"S": [["v"], [1]]})
    config = tmp_path / "conf.json"
    config.write_text(json.dumps({"FirstRowHasColumnName": True, "AddRowNumber": False}), encoding="utf-8")
    template = JsltTemplate.parse('{ "r": loadxls($.p, $.c) }')
    assert template.transform({"p": path, "c": str(config)}, functions=registry)["r"] == [{"v": 1}]


@pytest.mark.parametrize(
    ("expression", "message"),
    [
        ('loadxls($.p, "/absent/conf.json")', "configuration"),
        ('loadxlssheet("/absent/book.xlsx", {})', "introuvable"),
        ("loadxlssheet($.p, 3)", "configuration"),
    ],
)
def test_erreurs(registry, tmp_path, expression, message) -> None:
    path = _book(tmp_path, {"S": [["v"], [1]]})
    template = JsltTemplate.parse(f'{{ "r": {expression} }}')
    with pytest.raises(JsltError, match=message):
        template.transform({"p": path}, functions=registry)


def test_catalogue_et_decouverte(registry) -> None:
    from urban_json import default_registry, load_plugins

    assert {e["name"] for e in registry.catalog()} == {"loadxls", "loadxlssheet"}
    assert all(len(e["description"]) >= 15 for e in registry.catalog())
    load_plugins()
    assert "loadxlssheet" in default_registry
