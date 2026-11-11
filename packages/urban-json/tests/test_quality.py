"""Refuser, observer, valider — catégorie « qualité et diagnostic ».

Un template ne pouvait ni **échouer exprès** avec un message métier (il
produisait une sortie fausse, ou déclenchait une erreur par accident), ni
observer une valeur intermédiaire sans la mettre dans la sortie.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None, **kwargs):
    return JsltTemplate.parse(template).transform(source, **kwargs)


# --- require / requirethat ----------------------------------------------------


def test_require_rend_la_valeur_quand_elle_est_la():
    assert run('{ "r": require($.x, "x obligatoire") }', {"x": 7}) == {"r": 7}


def test_require_leve_avec_le_message_metier():
    with pytest.raises(JsltError, match="identifiant client obligatoire"):
        run('{ "r": require($.id, "identifiant client obligatoire") }', {})


@pytest.mark.parametrize("value", [0, False, "", [], {}])
def test_require_accepte_les_valeurs_falsy(value):
    # Seule l'**absence** est refusée : un montant 0 ou un drapeau false sont des
    # valeurs, et les refuser rendrait la fonction inutilisable.
    assert run('{ "r": require($.x, "manquant") }', {"x": value}) == {"r": value}


def test_requirethat_verifie_une_condition():
    assert run('{ "r": requirethat($.n > 0, "n doit être positif") }', {"n": 2}) == {"r": True}


def test_requirethat_leve_quand_la_condition_est_fausse():
    with pytest.raises(JsltError, match="n doit être positif"):
        run('{ "r": requirethat($.n > 0, "n doit être positif") }', {"n": -1})


def test_requirethat_sur_une_condition_absente_leve():
    with pytest.raises(JsltError, match="obligatoire"):
        run('{ "r": requirethat($.zz, "champ obligatoire") }', {})


def test_require_sans_message_leve_quand_meme_lisiblement():
    with pytest.raises(JsltError, match="valeur obligatoire absente"):
        run('{ "r": require($.zz) }', {})


def test_require_rattrapable_par_trydefault():
    # Même famille d'erreurs que le reste du moteur.
    template = '{ "r": trydefault(require($.zz, "absent"), "repli") }'
    assert run(template, {}) == {"r": "repli"}


# --- trace / traces -----------------------------------------------------------


def test_trace_rend_la_valeur_inchangee():
    assert run('{ "r": trace($.x, "x") }', {"x": 7}) == {"r": 7}


def test_traces_collecte_les_observations():
    template = '{ "r": trace($.x, "lu") + 1, "journal": traces() }'
    assert run(template, {"x": 1}) == {
        "r": 2, "journal": [{"label": "lu", "value": 1}]
    }


def test_trace_dans_une_boucle_garde_l_ordre():
    template = '{ "l": [ { "$source": $.v, "x": trace($, "element") } ], "journal": traces() }'
    result = run(template, {"v": [1, 2]})
    assert [t["value"] for t in result["journal"]] == [1, 2]


def test_trace_sans_etiquette():
    assert run('{ "r": trace($.x), "j": traces() }', {"x": 1}) == {
        "r": 1, "j": [{"label": "", "value": 1}]
    }


def test_les_traces_ne_fuient_pas_entre_deux_executions():
    template = JsltTemplate.parse('{ "r": trace($.x, "x"), "j": traces() }')
    assert len(template.transform({"x": 1})["j"]) == 1
    assert len(template.transform({"x": 2})["j"]) == 1


def test_traces_lisibles_depuis_le_contexte_par_un_integrateur():
    from urban_json.runtime import JsltEvaluationVisitor, RuntimeContext, Sources

    contexte = RuntimeContext(Sources({"x": 5}))
    JsltTemplate.parse('{ "r": trace($.x, "vu") }').ast.accept(
        JsltEvaluationVisitor(contexte)
    )
    assert contexte.traces == [{"label": "vu", "value": 5}]


# --- validateurs de format ----------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [("a@b.fr", True), ("prenom.nom+tag@sous.domaine.com", True),
     ("a@b", False), ("a b@c.fr", False), ("@b.fr", False), ("", False)],
)
def test_isemail(value, expected):
    assert run('{ "r": isemail($.t) }', {"t": value}) == {"r": expected}


@pytest.mark.parametrize(
    "value, expected",
    [("https://x.fr/a?b=1", True), ("http://localhost:8080", True),
     ("ftp://h/f", True), ("x.fr", False), ("https://", False)],
)
def test_isurl(value, expected):
    assert run('{ "r": isurl($.t) }', {"t": value}) == {"r": expected}


@pytest.mark.parametrize(
    "value, expected",
    [("4e9f1b2a-6c3d-4f8e-9a1b-2c3d4e5f6a7b", True),
     ("{4e9f1b2a-6c3d-4f8e-9a1b-2c3d4e5f6a7b}", True),
     ("4e9f1b2a6c3d4f8e9a1b2c3d4e5f6a7b", False), ("pas-un-uuid", False)],
)
def test_isuuid(value, expected):
    assert run('{ "r": isuuid($.t) }', {"t": value}) == {"r": expected}


def test_isuuid_accepte_ce_que_uuid_produit():
    assert run('{ "r": isuuid(uuid()) }') == {"r": True}


@pytest.mark.parametrize(
    "value, expected",
    [("FR1420041010050500013M02606", True), ("GB82 WEST 1234 5698 7654 32", True),
     ("FR1420041010050500013M02607", False), ("XX00", False)],
)
def test_isiban(value, expected):
    assert run('{ "r": isiban($.t) }', {"t": value}) == {"r": expected}


@pytest.mark.parametrize(
    "call", ["isemail($.t)", "isurl($.t)", "isuuid($.t)", "isiban($.t)"]
)
def test_validateurs_sur_null_et_non_chaine(call):
    # Un prédicat rend un booléen : `null` n'est pas une adresse valide.
    assert run('{ "r": ' + call + ' }', {}) == {"r": False}
    assert run('{ "r": ' + call + ' }', {"t": 42}) == {"r": False}


def test_exemple_complet_refus_explique():
    template = (
        '{ "mail": requirethat(isemail($.mail), "adresse électronique invalide") }'
    )
    with pytest.raises(JsltError, match="adresse électronique invalide"):
        run(template, {"mail": "a@b"})
