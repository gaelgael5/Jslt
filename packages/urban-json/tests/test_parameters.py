"""Paramètres externes d'un template — sujet « au niveau du langage ».

`transform(source)` ne prenait que le document : un template ne pouvait pas
recevoir « la date de référence » ou « l'identifiant du lot » autrement qu'en
les injectant dans la source, ce qui mélange données et réglages.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def test_param_lit_un_parametre_fourni():
    template = JsltTemplate.parse('{ "lot": param("lot") }')
    assert template.transform({}, parameters={"lot": "A-12"}) == {"lot": "A-12"}


def test_param_absent_rend_null():
    template = JsltTemplate.parse('{ "lot": param("lot") }')
    assert template.transform({}) == {"lot": None}


def test_param_avec_valeur_par_defaut():
    template = JsltTemplate.parse('{ "lot": param("lot", "aucun") }')
    assert template.transform({}) == {"lot": "aucun"}
    assert template.transform({}, parameters={"lot": "A"}) == {"lot": "A"}


def test_param_accepte_toute_valeur_json():
    template = JsltTemplate.parse('{ "r": param("cfg") }')
    assert template.transform({}, parameters={"cfg": {"a": [1, 2]}}) == {"r": {"a": [1, 2]}}


def test_param_valeur_nulle_explicite_n_est_pas_un_defaut():
    # Un paramètre fourni à null est fourni : le défaut ne doit pas le masquer.
    template = JsltTemplate.parse('{ "r": param("x", "defaut") }')
    assert template.transform({}, parameters={"x": None}) == {"r": None}


def test_param_sans_nom_leve():
    with pytest.raises(JsltError, match="nom"):
        JsltTemplate.parse('{ "r": param() }').transform({})


def test_params_rend_tous_les_parametres():
    template = JsltTemplate.parse('{ "r": params() }')
    assert template.transform({}, parameters={"a": 1}) == {"r": {"a": 1}}
    assert template.transform({}) == {"r": {}}


def test_parametres_disponibles_dans_une_boucle():
    template = JsltTemplate.parse('[ { "$source": $.l, "v": $, "lot": param("lot") } ]')
    assert template.transform({"l": [1]}, parameters={"lot": "A"}) == [{"v": 1, "lot": "A"}]


def test_parametres_sur_le_chemin_compile():
    template = JsltTemplate.parse('{ "lot": param("lot") }').build()
    assert template.transform({}, parameters={"lot": "A"}) == {"lot": "A"}


def test_parametres_dans_render():
    template = JsltTemplate.parse('{ "lot": param("lot") }')
    assert '"lot": "A"' in template.render({}, parameters={"lot": "A"})


def test_parametres_refusent_autre_chose_qu_un_objet():
    with pytest.raises(JsltError, match="paramètres"):
        JsltTemplate.parse('{ "r": 1 }').transform({}, parameters=[1, 2])


def test_parametres_ne_fuient_pas_entre_deux_executions():
    template = JsltTemplate.parse('{ "r": param("x") }')
    assert template.transform({}, parameters={"x": 1}) == {"r": 1}
    assert template.transform({}) == {"r": None}
