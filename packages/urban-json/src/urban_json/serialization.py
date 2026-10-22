"""Sérialisation d'un AST jslt vers du texte source (round-trip).

Analogue du pattern ``JsltBase.ToString`` / ``Writer`` du .NET, mais sous forme
d'un visiteur dédié (cohérent avec l'architecture à visiteurs). L'objectif est de
produire un template **valide et ré-analysable**, pas de reproduire au caractère
près la mise en forme du .NET.

Note : un cast ``x #type`` se re-sérialise sous sa forme fonctionnelle
``convert(x, "type")`` (sémantiquement équivalente), car le cast est porté comme
un appel à ``convert`` dans l'AST.
"""

from __future__ import annotations

import json
from typing import Any

from .ast import (
    JsltArray,
    JsltBinaryOperator,
    JsltConstant,
    JsltFunctionCall,
    JsltJsonVisitor,
    JsltObject,
    JsltOperator,
    JsltPath,
    JsltProperty,
    JsltSwitch,
    JsltSwitchCase,
    JsltVariable,
    OperationEnum,
)

# Symbole textuel de chaque opérateur (inverse du mapping du builder).
_OPERATOR_SYMBOLS = {
    OperationEnum.EQUAL: "==",
    OperationEnum.NOT_EQUAL: "!=",
    OperationEnum.GREATER_THAN: ">",
    OperationEnum.GREATER_THAN_OR_EQUAL: ">=",
    OperationEnum.LESS_THAN: "<",
    OperationEnum.LESS_THAN_OR_EQUAL: "<=",
    OperationEnum.ADD: "+",
    OperationEnum.SUBTRACT: "-",
    OperationEnum.DIVIDE: "/",
    OperationEnum.MODULO: "%",
    OperationEnum.MULTIPLY: "*",
    OperationEnum.POWER: "^",
    OperationEnum.CHAIN: "->",
    OperationEnum.AND: "&",
    OperationEnum.AND_EXCLUSIVE: "&&",
    OperationEnum.OR: "|",
    OperationEnum.OR_EXCLUSIVE: "||",
    OperationEnum.COALESCE: "??",
}


class SourceWriterVisitor(JsltJsonVisitor):
    """Rend un AST jslt sous forme de texte source compact et ré-analysable."""

    def visit_object(self, node: JsltObject) -> str:
        parts: list[str] = []
        if node.directives is not None:
            parts.append(f'"$directives": {node.directives.accept(self)}')
        if node.source is not None:
            parts.append(f'"$source": {node.source.accept(self)}')
        if node.where is not None:
            parts.append(f'"$where": {node.where.accept(self)}')
        for variable in node.variables:
            parts.append(f'{json.dumps(variable.name + ":")}: {variable.value.accept(self)}')
        for prop in node.properties:
            value = prop.value.accept(self) if prop.value is not None else "null"
            parts.append(f"{json.dumps(prop.name)}: {value}")
        return "{ " + ", ".join(parts) + " }" if parts else "{}"

    def visit_array(self, node: JsltArray) -> str:
        if not node.items:
            return "[]"
        return "[ " + ", ".join(item.accept(self) for item in node.items) + " ]"

    def visit_property(self, node: JsltProperty) -> str:
        value = node.value.accept(self) if node.value is not None else "null"
        return f"{json.dumps(node.name)}: {value}"

    def visit_constant(self, node: JsltConstant) -> str:
        return json.dumps(node.value)

    def visit_jpath(self, node: JsltPath) -> str:
        prefix = f"{node.variable}:" if node.variable else ""
        return f"{prefix}{node.value}"

    def visit_jvariable(self, node: JsltVariable) -> str:
        if node.value is None:
            return f"{node.name}:"  # référence
        return f'{json.dumps(node.name + ":")}: {node.value.accept(self)}'

    def visit_binary_operator(self, node: JsltBinaryOperator) -> str:
        symbol = _OPERATOR_SYMBOLS[node.operator]
        return f"{node.left.accept(self)} {symbol} {node.right.accept(self)}"

    def visit_unary_operator(self, node: JsltOperator) -> str:
        return f"!{node.left.accept(self)}"

    def visit_function(self, node: JsltFunctionCall) -> str:
        args = ", ".join(argument.accept(self) for argument in node.arguments)
        return f"{node.name}({args})"

    def visit_switch(self, node: JsltSwitch) -> str:
        cases = [
            f"{case.right_expression.accept(self)}: {case.block.accept(self)}"
            for case in node.cases
        ]
        if node.default is not None:
            cases.append(f'"default": {node.default.accept(self)}')
        return f"when({node.expression.accept(self)}) {{ " + ", ".join(cases) + " }"

    def visit_case(self, node: JsltSwitchCase) -> str:
        return f"{node.right_expression.accept(self)}: {node.block.accept(self)}"


def to_source(ast: Any) -> str:
    """Sérialise un AST jslt en texte source ré-analysable."""
    return ast.accept(SourceWriterVisitor())
