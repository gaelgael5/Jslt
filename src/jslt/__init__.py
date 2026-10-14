"""jslt — portage Python du langage JSLT (JSON Stylesheet Language Transformations).

API publique :

    >>> from jslt import JsltTemplate
    >>> template = JsltTemplate.parse('{ "name": "x" }')
    >>> template.transform({})            # (disponible à partir de la Phase 1)

État d'avancement du portage (cœur) :
    * Phase 0 — analyse syntaxique (parser ANTLR)                [FAIT]
    * Phase 1 — AST + transformation « défaut »                 [à venir]
    * Phase 2 — variables + JSONPath simple                     [à venir]
    * Phase 3 — boucles, opérateurs, casts                      [à venir]
    * Phase 4 — fonctions intégrées + when/switch               [à venir]
    * Phase 5 — JSONPath avancé                                 [à venir]
"""

from __future__ import annotations

from typing import Any

from .errors import JsltError, JsltSyntaxError
from .parsing import parse_to_tree

__all__ = ["JsltError", "JsltSyntaxError", "JsltTemplate"]

__version__ = "0.0.1"


class JsltTemplate:
    """Un template jslt compilé, prêt à transformer des documents JSON.

    On n'instancie pas la classe directement : on passe par :meth:`parse`.
    """

    def __init__(self, parse_tree: Any, source: str) -> None:
        self._parse_tree = parse_tree
        self._source = source

    @classmethod
    def parse(cls, template: str) -> JsltTemplate:
        """Analyse un template jslt.

        Args:
            template: le template jslt sous forme de chaîne.

        Returns:
            Un :class:`JsltTemplate` prêt à l'emploi.

        Raises:
            JsltSyntaxError: si le template est syntaxiquement invalide.
        """
        tree = parse_to_tree(template)
        return cls(tree, template)

    def transform(self, source: Any) -> Any:
        """Applique le template au document JSON source et renvoie le résultat.

        Args:
            source: le document source (structures Python issues de ``json.loads``).

        Returns:
            Le document transformé.
        """
        raise NotImplementedError(
            "La transformation sera implémentée à partir de la Phase 1 du portage."
        )
