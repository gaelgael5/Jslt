"""Introspection et remodelage d'objets — sujet « objets ».

Sans contrepartie .NET : on ne pouvait construire un objet que clé par clé,
littéralement, donc un objet dont les clés ne sont pas connues à l'écriture du
template était hors de portée.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


def test_keys_et_values_dans_l_ordre_du_document():
    source = {"o": {"b": 2, "a": 1}}
    assert run('{ "k": keys($.o), "v": values($.o) }', source) == {"k": ["b", "a"], "v": [2, 1]}


def test_entries_et_fromentries_font_l_aller_retour():
    source = {"o": {"a": 1, "b": 2}}
    assert run('{ "e": entries($.o) }', source) == {
        "e": [{"key": "a", "value": 1}, {"key": "b", "value": 2}]
    }
    assert run('{ "o": fromentries(entries($.o)) }', source) == {"o": {"a": 1, "b": 2}}


def test_fromentries_accepte_aussi_des_paires():
    assert run('{ "o": fromentries($.p) }', {"p": [["a", 1], ["b", 2]]}) == {"o": {"a": 1, "b": 2}}


def test_fromentries_refuse_une_entree_informe():
    with pytest.raises(JsltError, match="entrée"):
        run('{ "o": fromentries($.p) }', {"p": [{"k": "a"}]})


@pytest.mark.parametrize("call", ["keys($.x)", "values($.x)", "entries($.x)"])
def test_non_objet_et_null(call):
    assert run('{ "r": ' + call + ' }', {"x": None}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"x": [1, 2]}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"x": "ab"}) == {"r": None}


def test_merge_la_droite_gagne():
    source = {"a": {"x": 1, "y": 2}, "b": {"y": 9, "z": 3}}
    assert run('{ "r": merge($.a, $.b) }', source) == {"r": {"x": 1, "y": 9, "z": 3}}


def test_merge_est_plat_par_defaut():
    source = {"a": {"o": {"x": 1}}, "b": {"o": {"y": 2}}}
    assert run('{ "r": merge($.a, $.b) }', source) == {"r": {"o": {"y": 2}}}


def test_merge_profond_sur_demande():
    source = {"a": {"o": {"x": 1}}, "b": {"o": {"y": 2}}}
    assert run('{ "r": merge($.a, $.b, true) }', source) == {"r": {"o": {"x": 1, "y": 2}}}


def test_merge_ne_modifie_pas_ses_sources():
    template = '{ "f": merge($.a, $.b), "a": $.a }'
    assert run(template, {"a": {"x": 1}, "b": {"x": 2}}) == {"f": {"x": 2}, "a": {"x": 1}}


def test_merge_avec_null_rend_l_autre_cote():
    assert run('{ "r": merge($.a, $.b) }', {"a": {"x": 1}}) == {"r": {"x": 1}}
    assert run('{ "r": merge($.a, $.b) }', {"b": {"x": 1}}) == {"r": {"x": 1}}


def test_merge_refuse_un_non_objet():
    with pytest.raises(JsltError, match="objet"):
        run('{ "r": merge($.a, $.b) }', {"a": {"x": 1}, "b": [1]})


def test_pick_et_omit():
    source = {"o": {"a": 1, "b": 2, "c": 3}}
    assert run('{ "r": pick($.o, $.l) }', {**source, "l": ["a", "c"]}) == {"r": {"a": 1, "c": 3}}
    assert run('{ "r": omit($.o, $.l) }', {**source, "l": ["a", "c"]}) == {"r": {"b": 2}}


def test_pick_accepte_une_clef_seule():
    assert run('{ "r": pick($.o, "a") }', {"o": {"a": 1, "b": 2}}) == {"r": {"a": 1}}


def test_pick_ignore_une_clef_absente():
    # Un `pick` qui lèverait sur une clé absente serait inutilisable sur des
    # documents hétérogènes, ce qui est précisément son usage.
    assert run('{ "r": pick($.o, $.l) }', {"o": {"a": 1}, "l": ["a", "zz"]}) == {"r": {"a": 1}}


def test_pick_conserve_l_ordre_de_l_objet():
    source = {"o": {"c": 3, "a": 1, "b": 2}, "l": ["a", "c"]}
    assert list(run('{ "r": pick($.o, $.l) }', source)["r"]) == ["c", "a"]


def test_has_distingue_l_absence_de_la_valeur_nulle():
    source = {"o": {"a": None}}
    assert run('{ "a": has($.o, "a"), "b": has($.o, "zz") }', source) == {"a": True, "b": False}
    # C'est ce qu'`isnull` ne sait pas dire : les deux cas y donnent vrai.
    assert run('{ "a": isnull($.o.a), "b": isnull($.o.zz) }', source) == {"a": True, "b": True}


def test_renamekeys():
    source = {"o": {"nom": "A", "age": 3}, "m": {"nom": "name"}}
    assert run('{ "r": renamekeys($.o, $.m) }', source) == {"r": {"name": "A", "age": 3}}


def test_renamekeys_collision_le_dernier_ecrit_gagne():
    source = {"o": {"a": 1, "b": 2}, "m": {"a": "b"}}
    assert run('{ "r": renamekeys($.o, $.m) }', source) == {"r": {"b": 2}}


def test_renamekeys_mapping_vide_rend_l_objet_tel_quel():
    assert run('{ "r": renamekeys($.o, $.m) }', {"o": {"a": 1}, "m": {}}) == {"r": {"a": 1}}


def test_exemple_complet_inverser_un_dictionnaire():
    # Le cas qui motivait le sujet : des clés inconnues à l'écriture.
    template = (
        '{ "inverse": fromentries([ { "$source": entries($.tarifs), '
        '"key": $.value #string, "value": $.key } ]) }'
    )
    assert run(template, {"tarifs": {"a": 10, "b": 20}}) == {
        "inverse": {"10": "a", "20": "b"}
    }


def test_exemple_complet_normaliser_les_clefs():
    template = '{ "r": keys($.o) -> count() }'
    assert run(template, {"o": {"a": 1, "b": 2, "c": 3}}) == {"r": 3}
