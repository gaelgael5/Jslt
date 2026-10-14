"""Nœuds concrets de l'arbre jslt.

Port des classes de ``Bb.Jslt.Asts`` (un fichier C# par nœud dans le projet
.NET ; regroupés ici tant que le jeu de nœuds reste restreint — ils pourront
être éclatés par fichier au fil des phases).

Chaque nœud suit le pattern Visitor du code .NET : il règle son ``kind`` à la
construction et implémente ``accept`` en appelant la méthode ``visit_*``
correspondante du visiteur.

Couverture actuelle (Phase 1 — cas « défaut ») : objets, propriétés, tableaux,
constantes. Les autres nœuds (variables, chemins, fonctions, opérateurs,
switch…) seront ajoutés dans les phases suivantes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import JsltBase
from .kind import JsltKind

if TYPE_CHECKING:
    from jslt.jsonpath import JsonPath

    from .visitor import JsltJsonVisitor

# Noms de propriétés spéciales reconnues dans un objet (port de
# TransformJsonConstants / de la logique de ScriptBuilderVisitor.VisitObj).
SOURCE_KEY = "$source"
WHERE_KEY = "$where"
TYPE_KEY = "$type"


class JsltConstant(JsltBase):
    """Valeur constante (port de ``Bb.Jslt.Asts.JsltConstant``)."""

    def __init__(self, value: Any, kind: JsltKind) -> None:
        super().__init__()
        self.kind = kind
        self.value = value

    @staticmethod
    def resolve(value: Any) -> JsltKind:
        """Déduit le ``JsltKind`` d'une valeur Python (port de ``Resolve``)."""
        if value is None:
            return JsltKind.NULL
        if isinstance(value, bool):
            return JsltKind.BOOLEAN
        if isinstance(value, str):
            return JsltKind.STRING
        if isinstance(value, float):
            return JsltKind.FLOAT
        if isinstance(value, int):
            return JsltKind.INTEGER
        if isinstance(value, (bytes, bytearray)):
            return JsltKind.BYTES
        raise NotImplementedError(
            f"{type(value).__name__} n'est pas géré. Résoudre le JsltKind manuellement."
        )

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_constant(self)

    def __repr__(self) -> str:
        return f"JsltConstant({self.value!r}, {self.kind.name})"


class JsltProperty(JsltBase):
    """Propriété nommée d'un objet (port de ``Bb.Jslt.Asts.JsltProperty``)."""

    def __init__(self, name: str | None = None, value: JsltBase | None = None) -> None:
        super().__init__()
        self.kind = JsltKind.PROPERTY
        self.name = name
        self.value = value
        self._metadatas: dict[str, Any] = {}

    @property
    def metadatas(self) -> dict[str, Any]:
        return self._metadatas

    def add_metadata(self, name: str, value: Any) -> bool:
        if name in self._metadatas:
            return False
        self._metadatas[name] = value
        return True

    def get_metadata(self, name: str) -> Any | None:
        return self._metadatas.get(name)

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_property(self)

    def __repr__(self) -> str:
        return f"JsltProperty({self.name!r} : {self.value!r})"


class JsltObject(JsltBase):
    """Objet jslt (port de ``Bb.Jslt.Asts.JsltObject``).

    Les propriétés sont conservées dans l'ordre d'insertion (utile pour la
    sérialisation du résultat). La méthode ``append`` reprend l'aiguillage .NET :
    les clés spéciales ``$source`` / ``$where`` / ``$type`` ne deviennent pas des
    propriétés mais alimentent ``source`` / ``where`` / ``name``.
    """

    def __init__(self) -> None:
        super().__init__()
        self.kind = JsltKind.OBJECT
        self.name: str | None = None
        self._items: dict[str, JsltProperty] = {}

    @property
    def properties(self):
        return self._items.values()

    def append(self, item: JsltProperty) -> JsltObject:
        """Ajoute une propriété, en aiguillant les clés spéciales."""
        name = item.name
        if name == SOURCE_KEY:
            self.source = item.value
        elif name == WHERE_KEY:
            self.where = item.value
        elif name == TYPE_KEY:
            self.name = str(item.value)
        else:
            self._items[name] = item
        return self

    def has_property(self, name: str) -> bool:
        return name in self._items

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_object(self)

    def __repr__(self) -> str:
        return f"JsltObject({list(self._items.values())!r})"


class JsltPath(JsltBase):
    """Chemin JSONPath (port de ``Bb.Jslt.Asts.JsltPath``).

    En .NET le nœud ne stocke que la chaîne brute (``Value``), re-parsée à
    l'exécution. Ici — choix B2 — le chemin est compilé une seule fois à la
    construction de l'AST : ``compiled`` porte le :class:`jslt.jsonpath.JsonPath`,
    ``value`` conserve le texte d'origine pour la sérialisation et le debug.
    """

    def __init__(self, value: str, compiled: JsonPath) -> None:
        super().__init__()
        self.kind = JsltKind.JPATH
        self.value = value
        self.compiled = compiled

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_jpath(self)

    def __repr__(self) -> str:
        return f"JsltPath({self.value!r})"


class JsltArray(JsltBase):
    """Tableau jslt (port de ``Bb.Jslt.Asts.JsltArray``)."""

    def __init__(self, capacity: int = 0) -> None:
        super().__init__()
        self.kind = JsltKind.ARRAY
        self.items: list[JsltBase] = []

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_array(self)

    def __repr__(self) -> str:
        return f"JsltArray({self.items!r})"
