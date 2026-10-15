"""Débogage de template : trace d'évaluation + points d'arrêt (tree-walk).

Le portage étant un **interpréteur d'AST** (pas de génération de code comme le
.NET/Roslyn), il n'y a pas de « code source généré » à stepper : on déboge
directement au niveau du template en instrumentant l'évaluateur.

:class:`DebugEvaluationVisitor` enveloppe chaque ``visit_*`` de
:class:`urban_json.runtime.evaluator.JsltEvaluationVisitor` et notifie un :class:`Tracer`
à l'entrée et à la sortie de chaque nœud. :class:`TraceCollector` en tire une liste
d'étapes (:class:`TraceStep`) — l'équivalent du pas-à-pas — et marque celles qui
correspondent à un **point d'arrêt** (par nom de fonction / « méthode du
contexte », ou par ligne).

Les étapes sont enregistrées en **ordre d'évaluation** (post-ordre : la valeur d'un
nœud n'est connue qu'après ses enfants).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from .evaluator import JsltEvaluationVisitor


def _label(node: Any) -> str | None:
    """Étiquette courte et lisible d'un nœud (sans re-sérialiser tout l'AST)."""
    kind = type(node).__name__
    if kind == "JsltFunctionCall":
        return f"{node.name}(…)" if getattr(node, "arguments", None) else f"{node.name}()"
    if kind == "JsltPath":
        prefix = f"{node.variable}:" if getattr(node, "variable", None) else ""
        return f"{prefix}{getattr(node, 'value', '')}"
    if kind == "JsltVariable":
        return f"{node.name}:"
    if kind == "JsltConstant":
        return repr(getattr(node, "value", None))
    return None


@dataclass
class TraceStep:
    """Une étape d'évaluation (un nœud évalué)."""

    index: int
    depth: int
    kind: str
    line: int | None
    column: int | None
    expression: str | None
    function: str | None
    source: Any
    result: Any
    breakpoint: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "depth": self.depth,
            "kind": self.kind,
            "line": self.line,
            "column": self.column,
            "expression": self.expression,
            "function": self.function,
            "source": self.source,
            "result": self.result,
            "breakpoint": self.breakpoint,
        }


@dataclass
class DebugResult:
    """Résultat d'une exécution instrumentée : valeur finale + étapes (+ erreur)."""

    result: Any
    steps: list[TraceStep] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "result": self.result,
            "steps": [s.to_dict() for s in self.steps],
            "error": self.error,
        }


class Tracer:
    """Observateur d'évaluation. À surcharger ; par défaut ne fait rien."""

    def on_enter(self, node: Any, context: Any) -> None:
        """Appelé avant d'évaluer ``node``."""

    def on_exit(self, node: Any, context: Any, result: Any) -> None:
        """Appelé après l'évaluation de ``node`` (``result`` = valeur produite)."""


class TraceCollector(Tracer):
    """Collecte la trace d'évaluation et marque les points d'arrêt."""

    def __init__(
        self,
        break_functions: Iterable[str] = (),
        break_lines: Iterable[int] = (),
        max_steps: int = 10_000,
    ) -> None:
        self.steps: list[TraceStep] = []
        self._depth = 0
        self._break_functions = {f.lower() for f in break_functions}
        self._break_lines = set(break_lines)
        self._max_steps = max_steps

    def on_enter(self, node: Any, context: Any) -> None:
        self._depth += 1

    def on_exit(self, node: Any, context: Any, result: Any) -> None:
        self._depth -= 1
        if len(self.steps) >= self._max_steps:
            return
        kind = type(node).__name__
        location = getattr(node, "location", None)
        line = location.line if location is not None else None
        function = node.name if kind == "JsltFunctionCall" else None
        is_break = (function is not None and function.lower() in self._break_functions) or (
            line is not None and line in self._break_lines
        )
        self.steps.append(
            TraceStep(
                index=len(self.steps),
                depth=self._depth,
                kind=kind,
                line=line,
                column=location.column if location is not None else None,
                expression=_label(node),
                function=function,
                source=context.current_source,
                result=result,
                breakpoint=is_break,
            )
        )


class DebugEvaluationVisitor(JsltEvaluationVisitor):
    """Évaluateur instrumenté : notifie un :class:`Tracer` autour de chaque nœud.

    Enveloppe chaque méthode ``visit_*`` au niveau de l'instance — aucune
    modification de l'évaluateur de base, et tout nœud (y compris imbriqué) est
    capturé puisque chaque ``accept`` redispatche sur ces méthodes.
    """

    def __init__(self, context: Any, tracer: Tracer) -> None:
        super().__init__(context)
        self._tracer = tracer
        for name in [n for n in dir(self) if n.startswith("visit_")]:
            original = getattr(JsltEvaluationVisitor, name).__get__(self, type(self))
            setattr(self, name, self._instrument(original))

    def _instrument(self, original: Any) -> Any:
        def wrapped(node: Any) -> Any:
            self._tracer.on_enter(node, self.context)
            result = original(node)
            self._tracer.on_exit(node, self.context, result)
            return result

        return wrapped


def evaluate_with_trace(
    ast: Any,
    context: Any,
    break_functions: Iterable[str] = (),
    break_lines: Iterable[int] = (),
    max_steps: int = 10_000,
) -> DebugResult:
    """Évalue ``ast`` en collectant la trace ; renvoie un :class:`DebugResult`.

    Les erreurs d'évaluation sont capturées dans ``DebugResult.error`` (la trace
    partielle reste disponible) — c'est un utilitaire de diagnostic.
    """
    collector = TraceCollector(break_functions, break_lines, max_steps)
    visitor = DebugEvaluationVisitor(context, collector)
    result: Any = None
    error: str | None = None
    try:
        result = ast.accept(visitor)
    except Exception as exc:  # noqa: BLE001 — diagnostic : l'erreur est rapportée, pas levée
        error = f"{type(exc).__name__}: {exc}"
    return DebugResult(result=result, steps=collector.steps, error=error)
