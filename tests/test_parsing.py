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


@pytest.mark.parametrize("template", VALID_TEMPLATES)
def test_jslttemplate_parse_accepts_valid(template: str) -> None:
    # L'API publique accepte les templates valides sans lever.
    assert JsltTemplate.parse(template) is not None


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


def test_transform_not_yet_implemented() -> None:
    # Garde-fou : tant que la transformation n'est pas portée, l'API l'annonce
    # explicitement plutôt que de renvoyer un résultat faux.
    template = JsltTemplate.parse('{ "n": "x" }')
    with pytest.raises(NotImplementedError):
        template.transform({})
