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
from .operation import OperationEnum

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


class JsltVariable(JsltProperty):
    """Variable jslt (port de ``Bb.Jslt.Asts.JsltVariable``).

    En .NET, une variable *est* une propriété (``JsltVariable : JsltProperty``) :
        * déclaration — ``value`` renseignée, clé ``"name:"`` dans un objet ;
        * référence — ``value`` à ``None``, forme ``name:`` en position de valeur.
    """

    def __init__(self, name: str | None = None, value: JsltBase | None = None) -> None:
        super().__init__(name=name, value=value)
        self.kind = JsltKind.JVARIABLE
        self.target_type: Any = None
        self.to_destruct: bool = False

    @property
    def is_reference(self) -> bool:
        """Vrai si c'est une référence (sans valeur), faux pour une déclaration."""
        return self.value is None

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_jvariable(self)

    def __repr__(self) -> str:
        if self.value is None:
            return f"JsltVariable(ref {self.name!r})"
        return f"JsltVariable({self.name!r} : {self.value!r})"


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
        self._variables: dict[str, JsltVariable] = {}

    @property
    def properties(self):
        return self._items.values()

    @property
    def variables(self):
        """Variables déclarées dans l'objet (port de ``JsltObject.Variables``)."""
        return self._variables.values()

    def append(self, item: JsltProperty) -> JsltObject:
        """Ajoute une propriété ou variable, en aiguillant les clés spéciales."""
        if isinstance(item, JsltVariable):
            self._variables[item.name] = item
            return self
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

    def __init__(self, value: str, compiled: JsonPath, variable: str | None = None) -> None:
        super().__init__()
        self.kind = JsltKind.JPATH
        self.value = value
        self.compiled = compiled
        #: Variable source du chemin (forme ``name:$.path``) ; None = source courante.
        self.variable = variable

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_jpath(self)

    def __repr__(self) -> str:
        prefix = f"{self.variable}:" if self.variable else ""
        return f"JsltPath({prefix}{self.value!r})"


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


class JsltFunctionCall(JsltBase):
    """Appel de fonction (port de ``Bb.Jslt.Asts.JsltFunctionCall``).

    Simplification vs .NET : les arguments sont une liste unique de nœuds (le
    .NET distingue ``Arguments`` et ``ArgumentsBis`` pour les besoins de sa
    génération de code). ``inject`` insère un argument à une position donnée, ce
    qui sert au chaînage ``->`` (injection de l'opérande gauche en tête).
    """

    def __init__(self, name: str, arguments: list[JsltBase] | None = None) -> None:
        super().__init__()
        self.kind = JsltKind.FUNCTION
        self.name = name
        self.arguments: list[JsltBase] = list(arguments) if arguments else []

    def inject(self, argument: JsltBase, position: int = 0) -> None:
        self.arguments.insert(position, argument)

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_function(self)

    def __repr__(self) -> str:
        return f"JsltFunctionCall({self.name!r}, {self.arguments!r})"


class JsltSwitchCase(JsltBase):
    """Un cas d'un switch/when (port de ``Bb.Jslt.Asts.JsltSwitchCase``).

    ``right_expression`` est la valeur comparée à l'expression du switch ; ``block``
    est le résultat produit si le cas correspond.
    """

    def __init__(self, right_expression: JsltBase, block: JsltBase) -> None:
        super().__init__()
        self.right_expression = right_expression
        self.block = block

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_case(self)

    def __repr__(self) -> str:
        return f"JsltSwitchCase({self.right_expression!r} -> {self.block!r})"


class JsltSwitch(JsltBase):
    """Switch / when (port de ``Bb.Jslt.Asts.JsltSwitch``).

    Construit depuis la syntaxe ``when(expr) { "cas1": …, "default": … }`` :
    l'expression est comparée (``==``) à chaque nom de cas ; le bloc du premier
    cas correspondant est produit, sinon ``default`` (sinon ``null``).
    """

    def __init__(
        self,
        expression: JsltBase,
        cases: list[JsltSwitchCase] | None = None,
        default: JsltBase | None = None,
    ) -> None:
        super().__init__()
        self.expression = expression
        self.cases: list[JsltSwitchCase] = list(cases) if cases else []
        self.default = default

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_switch(self)

    def __repr__(self) -> str:
        return f"JsltSwitch({self.expression!r}, {self.cases!r}, default={self.default!r})"


class JsltBinaryOperator(JsltBase):
    """Opérateur binaire (port de ``Bb.Jslt.Asts.JsltBinaryOperator``)."""

    def __init__(self, left: JsltBase, operator: OperationEnum, right: JsltBase) -> None:
        super().__init__()
        self.kind = JsltKind.OPERATOR
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_binary_operator(self)

    def __repr__(self) -> str:
        return f"JsltBinaryOperator({self.left!r} {self.operator.name} {self.right!r})"


class JsltOperator(JsltBase):
    """Opérateur unaire (port de ``Bb.Jslt.Asts.JsltOperator``), ex. la négation ``!``."""

    def __init__(self, left: JsltBase, operator: OperationEnum) -> None:
        super().__init__()
        self.kind = JsltKind.OPERATOR
        self.left = left
        self.operator = operator

    def accept(self, visitor: JsltJsonVisitor) -> Any:
        return visitor.visit_unary_operator(self)

    def __repr__(self) -> str:
        return f"JsltOperator({self.operator.name} {self.left!r})"
