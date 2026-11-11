"""Épingle la surface d'intégration documentée (`docs/integration.md`).

Une intégration du dépôt importe des pièces **internes** du moteur
(`parse_to_tree`, `ScriptBuilderVisitor`, `JsltEvaluationVisitor`,
`RuntimeContext`, `Sources`, `JsltKind`, les sélecteurs JSONPath). Tant que rien
ne les testait, la seule façon de vérifier qu'une montée de version ne les
cassait pas était de comparer les sources de deux versions. Ce fichier est le
contrat : si un de ces noms disparaît ou change de place, la suite rougit ici,
et le CHANGELOG doit l'annoncer.
"""

from __future__ import annotations

import urban_json
from urban_json import JsltTemplate
from urban_json.ast import JsltBaseVisitor, JsltFunctionCall, JsltKind
from urban_json.jsonpath import ISelector, JsonPath, NameSelector, Node, PathScope
from urban_json.parsing import ScriptBuilderVisitor, parse_to_tree
from urban_json.runtime import JsltEvaluationVisitor, Program, RuntimeContext, Sources

PUBLIC = {
    "DebugResult", "FunctionInfo", "FunctionRegistry", "JsltError",
    "JsltSemanticError", "JsltSyntaxError", "JsltTemplate", "ParameterInfo",
    "Program", "TraceStep", "default_registry", "jslt_function", "load_plugins",
}


def test_surface_publique_inchangee() -> None:
    # Les retraits sont des ruptures ; les ajouts, non. On ne vérifie donc que
    # l'inclusion, mais on la vérifie.
    assert PUBLIC <= set(urban_json.__all__)
    for name in PUBLIC:
        assert hasattr(urban_json, name), name


def test_pipeline_manuel_donne_le_meme_resultat_que_transform() -> None:
    texte = '{ "a": $.x + 1, "lot": param("lot") }'
    document, parametres = {"x": 2}, {"lot": "A-12"}

    ast = ScriptBuilderVisitor().visit(parse_to_tree(texte))
    manuel = ast.accept(JsltEvaluationVisitor(RuntimeContext(Sources(document), None, parametres)))

    assert manuel == JsltTemplate.parse(texte).transform(document, parameters=parametres)


def test_noeuds_et_nature_exposes() -> None:
    ast = JsltTemplate.parse('{ "a": 1 }').ast
    assert ast.kind is JsltKind.OBJECT
    assert isinstance(JsltKind.FUNCTION, JsltKind)


def test_visiteur_d_ast_permet_l_inventaire_des_fonctions() -> None:
    class Noms(JsltBaseVisitor):
        def __init__(self) -> None:
            self.noms: set[str] = set()

        def visit_function(self, node: JsltFunctionCall):
            self.noms.add(node.name)
            return super().visit_function(node)

    visiteur = Noms()
    JsltTemplate.parse('{ "a": upper($.x), "b": sort($.l, foldtext($)) }').ast.accept(visiteur)
    assert visiteur.noms == {"upper", "sort", "foldtext"}


def test_jsonpath_expose_ses_selecteurs_et_ses_deux_lectures() -> None:
    # `properties` est une vue (pas une liste) : on prend la première propriété.
    propriete = next(iter(JsltTemplate.parse('{ "r": $.a.b }').ast.properties))
    path = propriete.value.compiled
    assert isinstance(path, JsonPath)
    assert path.scope is PathScope.GLOBAL
    assert path.select_values({"a": {"b": 7}}) == [7]
    assert all(isinstance(node, Node) for node in path.evaluate({"a": {"b": 7}}))
    assert issubclass(NameSelector, ISelector)


def test_chemin_compile_expose_son_type() -> None:
    template = JsltTemplate.parse('{ "a": 1 }').build()
    assert template.transform({}) == {"a": 1}
    assert Program is not None  # type exporté pour annoter un programme compilé


def test_registre_restreint_refuse_la_fonction_retiree() -> None:
    sandbox = urban_json.default_registry.copy()
    assert sandbox.remove("upper") is True
    assert "upper" not in sandbox.names()
