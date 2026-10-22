"""group, join, createindex, index — port de ``Services.group.cs`` (.NET).

Écarts volontaires :
* ``group`` multi-niveaux : le .NET perdait les sous-groupes (``Collect`` ne les
  ajoutait que si le niveau avait des éléments directs) ; ici ils sont imbriqués.
* ``join`` ne modifie pas la source (le .NET mutait les objets de gauche).
"""

from __future__ import annotations

import pytest

from urban_json import JsltError, JsltTemplate


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source if source is not None else {})


PEOPLE = [
    {"name": "Ana", "city": "Lyon", "team": "a"},
    {"name": "Bob", "city": "Paris", "team": "b"},
    {"name": "Cid", "city": "Lyon", "team": "b"},
]


def test_group_un_niveau() -> None:
    out = run('{ "r": group($.p, ["$.city"]) }', {"p": PEOPLE})["r"]
    assert out == [
        {"Label": "Lyon", "Items": [PEOPLE[0], PEOPLE[2]]},
        {"Label": "Paris", "Items": [PEOPLE[1]]},
    ]


def test_group_deux_niveaux_imbrique_les_sous_groupes() -> None:
    out = run('{ "r": group($.p, ["$.city", "$.team"]) }', {"p": PEOPLE})["r"]
    assert out == [
        {"Label": "Lyon", "Items": [
            {"Label": "a", "Items": [PEOPLE[0]]},
            {"Label": "b", "Items": [PEOPLE[2]]},
        ]},
        {"Label": "Paris", "Items": [{"Label": "b", "Items": [PEOPLE[1]]}]},
    ]


def test_group_cle_numerique_en_texte() -> None:
    out = run('{ "r": group($.p, ["$.n"]) }', {"p": [{"n": 1}, {"n": 1}, {"n": 2}]})["r"]
    assert [g["Label"] for g in out] == ["1", "2"]


def test_group_elements_sans_cle_ignores() -> None:
    out = run('{ "r": group($.p, ["$.city"]) }', {"p": [{"city": "Lyon"}, {"x": 1}]})["r"]
    assert out == [{"Label": "Lyon", "Items": [{"city": "Lyon"}]}]


@pytest.mark.parametrize(("source", "paths"), [({"p": None}, '["$.city"]'), ({"p": PEOPLE}, "null"), ({"p": []}, '["$.city"]')])
def test_group_vide(source, paths) -> None:
    assert run(f'{{ "r": group($.p, {paths}) }}', source)["r"] == []


ORDERS = [
    {"id": 1, "customer": 10, "lines": "x"},
    {"id": 2, "customer": 10, "lines": "y"},
    {"id": 3, "customer": 30, "lines": "z"},
]
CUSTOMERS = [{"cid": 10, "name": "Ana"}, {"cid": 20, "name": "Bob"}]


def test_join_rattache_les_elements_de_droite() -> None:
    template = '{ "r": join($.c, $.cid, false, [{ "Name": "orders", "Key": "$.customer", "Source": $.o }]) }'
    out = run(template, {"c": CUSTOMERS, "o": ORDERS})["r"]
    assert out == [
        {"cid": 10, "name": "Ana", "orders": [{"id": 1, "lines": "x"}, {"id": 2, "lines": "y"}]},
        {"cid": 20, "name": "Bob"},  # aucune correspondance : pas de propriété ajoutée
    ]


def test_join_ne_modifie_pas_la_source() -> None:
    template = (
        '{ "r": join($.c, $.cid, false, [{ "Name": "orders", "Key": "$.customer", "Source": $.o }]),'
        ' "c": $.c }'
    )
    out = run(template, {"c": CUSTOMERS, "o": ORDERS})
    assert "orders" not in out["c"][0]
    assert ORDERS[0]["customer"] == 10  # la clé retirée l'est sur une copie


def test_join_plusieurs_droites_et_cle_chaine() -> None:
    template = (
        '{ "r": join($.c, "$.cid", true, ['
        '{ "Name": "orders", "Key": "$.customer", "Source": $.o },'
        '{ "Name": "tags", "Key": "$.owner", "Source": $.t }]) }'
    )
    out = run(template, {"c": CUSTOMERS[:1], "o": ORDERS, "t": [{"owner": "10", "tag": "vip"}]})["r"]
    assert out[0]["tags"] == [{"tag": "vip"}]  # 10 et "10" : clés comparées en texte
    assert len(out[0]["orders"]) == 2


def test_join_source_gauche_null() -> None:
    assert run('{ "r": join($.c, $.cid, false, []) }', {"c": None})["r"] is None


def test_createindex_et_index() -> None:
    template = '{ "i:": createindex($.c, "", "$.cid"), "ana": index(i:, "10"), "absent": index(i:, "99") }'
    out = run(template, {"c": CUSTOMERS})
    assert out["ana"] == CUSTOMERS[0]
    assert out["absent"] is None


def test_createindex_avec_chemin_de_decoupe() -> None:
    template = '{ "r": createindex($, "$.data[*]", "$.cid") }'
    out = run(template, {"data": CUSTOMERS})["r"]
    assert out == {"10": CUSTOMERS[0], "20": CUSTOMERS[1]}


def test_createindex_premiere_cle_gagne_et_sans_cle_ignore() -> None:
    template = '{ "r": createindex($.c, "", "$.k") }'
    out = run(template, {"c": [{"k": "a", "v": 1}, {"k": "a", "v": 2}, {"v": 3}]})["r"]
    assert out == {"a": {"k": "a", "v": 1}}


@pytest.mark.parametrize("source", [None, []])
def test_createindex_vide(source) -> None:
    assert run('{ "r": createindex($.c, "", "$.k") }', {"c": source})["r"] == {}


def test_index_sur_autre_chose_qu_un_index() -> None:
    assert run('{ "r": index($.x, "a") }', {"x": [1]})["r"] is None


def test_join_regle_de_droite_invalide() -> None:
    with pytest.raises(JsltError, match="join"):
        run('{ "r": join($.c, $.cid, false, [{ "Name": "o" }]) }', {"c": CUSTOMERS})
