"""Phase 0 — analyse syntaxique : le parser ANTLR accepte les templates valides
et rejette les templates invalides via JsltSyntaxError.

Ces tests ne vérifient pas encore la *transformation* (phases suivantes), mais la
seule capacité à construire l'arbre d'analyse à partir des constructions du
langage décrites par les grammaires .g4.
"""

from __future__ import annotations

import pytest

from jslt import JsltSyntaxError, JsltTemplate
from jslt.parsing import parse_to_tree

# Templates syntaxiquement valides couvrant les grandes constructions du langage.
VALID_TEMPLATES = [
    pytest.param('{ "n": "x" }', id="objet-propriete-string"),
    pytest.param('{"n":"x"}', id="sans-espaces"),
    pytest.param('{\n  "n": "x"\n}', id="retours-ligne"),
    pytest.param("{ }", id="objet-vide"),
    pytest.param("[ ]", id="tableau-vide"),
    pytest.param('{ "propertyName": 6 }', id="valeur-entier"),
    pytest.param('{ "propertyName": 6.7 }', id="valeur-decimal"),
    pytest.param('{ "flag": true }', id="valeur-booleen"),
    pytest.param('{ "nothing": null }', id="valeur-null"),
    pytest.param('{ "name": $.n }', id="jsonpath-simple"),
    pytest.param('{ "deep": $..n }', id="jsonpath-descente-recursive"),
    pytest.param('{ "prices": sum($..n) }', id="appel-fonction"),
    pytest.param('[ { "$source": $.items, "Key": $.name } ]', id="boucle-tableau"),
    pytest.param('{ "a": var: }', id="variable"),
    pytest.param('{ "bb": var:$.Test1.Test2 }', id="variable-jsonpath"),
    pytest.param('{ "casted": $.n #integer }', id="cast-integer"),
    pytest.param('{ "sum": $.a + $.b }', id="operation-binaire"),
]

# Sous-ensemble des templates valides dont la construction d'AST est déjà portée
# (Phase 1 — cas « défaut »). Les autres constructions (JSONPath, fonctions,
# variables, opérateurs, casts) parsent au niveau ANTLR mais ne construisent pas
# encore d'AST : voir test_ast_build_not_yet_supported.
PHASE1_TEMPLATES = [
    pytest.param('{ "n": "x" }', id="objet-propriete-string"),
    pytest.param('{"n":"x"}', id="sans-espaces"),
    pytest.param("{ }", id="objet-vide"),
    pytest.param("[ ]", id="tableau-vide"),
    pytest.param('{ "propertyName": 6 }', id="valeur-entier"),
    pytest.param('{ "propertyName": 6.7 }', id="valeur-decimal"),
    pytest.param('{ "flag": true }', id="valeur-booleen"),
    pytest.param('{ "nothing": null }', id="valeur-null"),
    pytest.param('{ "name": $.n }', id="jsonpath-simple"),
    pytest.param('{ "deep": $.a.b }', id="jsonpath-chaine"),
    pytest.param('{ "idx": $.list[0] }', id="jsonpath-indice"),
    pytest.param('{ "v:": 1, "a": v: }', id="variable-decl-ref"),
    pytest.param('{ "b:": $.obj, "bb": b:$.x }', id="variable-projection"),
    pytest.param('{ "sum": $.a + $.b }', id="operation-binaire"),
    pytest.param('{ "neg": !$.flag }', id="negation"),
    pytest.param('[ { "$source": $.items, "k": $.n } ]', id="boucle"),
    pytest.param('{ "prices": sum($.n) }', id="appel-fonction"),
    pytest.param('{ "chain": $.a -> sum() }', id="chainage"),
]

# Constructions qui parsent (ANTLR) mais dont l'AST n'est pas encore porté.
NOT_YET_BUILT_TEMPLATES = [
    pytest.param('{ "deep": $..n }', id="jsonpath-descente-recursive"),
    pytest.param('{ "casted": $.n #integer }', id="cast"),
    pytest.param('{ "w": when($.a) { "case1": 1 } }', id="when-switch"),
]

# Templates qui doivent être rejetés.
INVALID_TEMPLATES = [
    pytest.param('{ "n": "x" ', id="accolade-non-fermee"),
    pytest.param('{ "n": ~~~ }', id="caractere-invalide"),
    pytest.param('{ "n" "x" }', id="deux-points-manquant"),
    pytest.param("", id="vide"),
]


@pytest.mark.parametrize("template", VALID_TEMPLATES)
def test_valid_template_parses(template: str) -> None:
    tree = parse_to_tree(template)
    assert tree is not None


@pytest.mark.parametrize("template", PHASE1_TEMPLATES)
def test_jslttemplate_parse_builds_phase1(template: str) -> None:
    # L'API publique construit l'AST des constructions portées en Phase 1.
    assert JsltTemplate.parse(template).ast is not None


@pytest.mark.parametrize("template", NOT_YET_BUILT_TEMPLATES)
def test_ast_build_not_yet_supported(template: str) -> None:
    # Les constructions des phases suivantes parsent au niveau ANTLR…
    assert parse_to_tree(template) is not None
    # …mais leur construction d'AST lève explicitement NotImplementedError.
    with pytest.raises(NotImplementedError):
        JsltTemplate.parse(template)


@pytest.mark.parametrize("template", INVALID_TEMPLATES)
def test_invalid_template_raises(template: str) -> None:
    with pytest.raises(JsltSyntaxError):
        parse_to_tree(template)


def test_syntax_error_reports_position() -> None:
    with pytest.raises(JsltSyntaxError) as exc_info:
        parse_to_tree('{ "n": ~ }')
    err = exc_info.value
    assert err.line == 1
    assert err.column is not None


def test_parse_builds_ast() -> None:
    # L'API publique construit un AST exploitable à partir d'un template valide.
    template = JsltTemplate.parse('{ "n": "x" }')
    assert template.ast is not None
