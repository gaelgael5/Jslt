"""Sorties CSV, XML et YAML — catégorie « sortie ».

Le moteur lisait JSON, XML et CSV depuis une chaîne et n'écrivait que du JSON :
la moitié du contrat d'un moteur de transformation manquait.
"""

from __future__ import annotations

import csv
import io
import json
import xml.etree.ElementTree as ET

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def render(template: str, source=None) -> str:
    return JsltTemplate.parse(template).render(source)


# --- CSV ----------------------------------------------------------------------

LIGNES = {"l": [{"nom": "Ana", "age": 30}, {"nom": "Bob", "age": 25}]}
CSV_TEMPLATE = (
    '{ "$directives": { "output": { "filter": "$.lignes", "mode": to_csv() } }, '
    '"lignes": [ { "$source": $.l, "nom": $.nom, "age": $.age } ] }'
)


def test_to_csv_entete_et_lignes():
    assert render(CSV_TEMPLATE, LIGNES) == "nom;age\r\nAna;30\r\nBob;25\r\n"


def test_to_csv_se_relit_avec_le_module_csv():
    texte = render(CSV_TEMPLATE, LIGNES)
    lignes = list(csv.DictReader(io.StringIO(texte), delimiter=";"))
    assert lignes == [{"nom": "Ana", "age": "30"}, {"nom": "Bob", "age": "25"}]


def test_to_csv_separateur_et_sans_entete():
    template = CSV_TEMPLATE.replace("to_csv()", 'to_csv(",", false)')
    assert render(template, LIGNES) == "Ana,30\r\nBob,25\r\n"


def test_to_csv_echappe_les_separateurs_et_les_guillemets():
    source = {"l": [{"t": 'a;b "c"'}]}
    template = (
        '{ "$directives": { "output": { "filter": "$.lignes", "mode": to_csv() } }, '
        '"lignes": [ { "$source": $.l, "t": $.t } ] }'
    )
    assert render(template, source) == 't\r\n"a;b ""c"""\r\n'


def test_to_csv_colonnes_de_l_union_des_clefs():
    # Documents hétérogènes : une colonne par clé rencontrée, dans l'ordre
    # d'apparition, et les cellules absentes restent vides.
    source = {"l": [{"a": 1}, {"b": 2}]}
    template = (
        '{ "$directives": { "output": { "filter": "$.lignes", "mode": to_csv() } }, '
        '"lignes": [ { "$source": $.l, "a": $.a, "b": $.b } ] }'
    )
    assert render(template, source) == "a;b\r\n1;\r\n;2\r\n"


def test_to_csv_aplatit_les_valeurs_imbriquees():
    source = {"l": [{"id": 1, "adr": {"ville": "Lyon"}}]}
    template = (
        '{ "$directives": { "output": { "filter": "$.lignes", "mode": to_csv() } }, '
        '"lignes": [ { "$source": $.l, "id": $.id, "adr": $.adr } ] }'
    )
    assert render(template, source) == "id;adr.ville\r\n1;Lyon\r\n"


def test_to_csv_refuse_autre_chose_qu_un_tableau_d_objets():
    template = '{ "$directives": { "output": { "mode": to_csv() } }, "x": 1 }'
    with pytest.raises(JsltError, match="tableau d'objets"):
        render(template, {})


# --- XML ----------------------------------------------------------------------


def test_to_xml_structure_et_attributs():
    source = {"o": {"id": 1, "nom": "Ana"}}
    template = (
        '{ "$directives": { "output": { "filter": "$.client", "mode": to_xml("client") } }, '
        '"client": { "@id": $.o.id, "nom": $.o.nom } }'
    )
    texte = render(template, source)
    racine = ET.fromstring(texte)
    assert racine.tag == "client"
    assert racine.attrib == {"id": "1"}
    assert racine.findtext("nom") == "Ana"


def test_to_xml_tableau_repete_l_element():
    source = {"l": [1, 2]}
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_xml("r") } }, '
        '"r": { "v": $.l } }'
    )
    racine = ET.fromstring(render(template, source))
    assert [e.text for e in racine.findall("v")] == ["1", "2"]


def test_to_xml_echappe_le_contenu():
    source = {"t": "<a> & b"}
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_xml("r") } }, '
        '"r": { "t": $.t } }'
    )
    texte = render(template, source)
    assert "&lt;a&gt; &amp; b" in texte
    assert ET.fromstring(texte).findtext("t") == "<a> & b"


def test_to_xml_texte_mixte_par_la_clef_dediee():
    source = {"t": "contenu"}
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_xml("r") } }, '
        '"r": { "@lang": "fr", "#text": $.t } }'
    )
    racine = ET.fromstring(render(template, source))
    assert racine.attrib == {"lang": "fr"} and racine.text == "contenu"


def test_to_xml_aller_retour_avec_parsexml_du_plugin():
    # Les conventions d'écriture sont celles que `parsexml` lit (@ et #text).
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_xml("r") } }, '
        '"r": { "@id": "1", "n": "x" } }'
    )
    assert render(template, {}).startswith('<?xml version="1.0" encoding="utf-8"?>')


def test_to_xml_nom_de_balise_invalide_leve():
    template = '{ "$directives": { "output": { "mode": to_xml("2mauvais") } }, "x": 1 }'
    with pytest.raises(JsltError, match="nom d'élément"):
        render(template, {})


# --- YAML ---------------------------------------------------------------------


def test_to_yaml_objet_imbrique():
    source = {"o": {"nom": "Ana", "adr": {"ville": "Lyon"}}}
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_yaml() } }, '
        '"r": { "nom": $.o.nom, "adr": { "ville": $.o.adr.ville } } }'
    )
    assert render(template, source) == "nom: Ana\nadr:\n  ville: Lyon\n"


def test_to_yaml_tableaux():
    source = {"l": [1, "deux", None]}
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_yaml() } }, '
        '"r": { "v": $.l } }'
    )
    assert render(template, source) == "v:\n  - 1\n  - deux\n  - null\n"


def test_to_yaml_cite_ce_qui_serait_relu_autrement():
    # « true », « 12 » et « null » en texte doivent rester du texte.
    source = {"l": ["true", "12", "null", "oui"]}
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_yaml() } }, '
        '"r": { "v": $.l } }'
    )
    assert render(template, source) == 'v:\n  - "true"\n  - "12"\n  - "null"\n  - oui\n'


def test_to_yaml_est_relisible_en_json_quand_on_demande_le_style_json():
    source = {"o": {"a": [1, 2]}}
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_yaml(true) } }, '
        '"r": { "a": $.o.a } }'
    )
    # YAML 1.2 est un sur-ensemble de JSON : le style JSON est un YAML valide.
    assert json.loads(render(template, source)) == {"a": [1, 2]}


def test_to_yaml_tableau_vide_et_objet_vide():
    template = (
        '{ "$directives": { "output": { "filter": "$.r", "mode": to_yaml() } }, '
        '"r": { "l": [], "o": {} } }'
    )
    assert render(template, {}) == "l: []\no: {}\n"


# --- refus dans le corps du template ------------------------------------------


@pytest.mark.parametrize("call", ["to_csv()", 'to_xml("r")', "to_yaml()"])
def test_les_sorties_restent_refusees_dans_le_corps(call):
    with pytest.raises(JsltError, match="sortie"):
        JsltTemplate.parse('{ "r": ' + call + " }").transform({})
