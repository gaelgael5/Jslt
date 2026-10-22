"""Fonctions mathématiques intégrées (port des ``Services.Numbers`` .NET).

Convention : une valeur non numérique (ou ``None``) donne ``None``. Comme en
.NET, les fonctions transcendantes et ``floor``/``round``/``min``/``max``/``pow``
renvoient un flottant ; ``round`` est un arrondi bancaire (demi vers pair).
"""

from __future__ import annotations

import math
from typing import Any

from ._helpers import coerce_number, is_number, number_result
from .registry import jslt_function


@jslt_function("abs", description="Valeur absolue d'un nombre (null si ce n'est pas un nombre)")
def execute_abs(ctx: Any, token: Any = None) -> Any:
    return number_result(token, abs)  # conserve int/float comme en .NET


@jslt_function("floor", description="Arrondi à l'entier inférieur, rendu en décimal (2.7 -> 2.0)")
def execute_floor(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: float(math.floor(n)))


@jslt_function("round", description="Arrondi à l'entier le plus proche, demi vers le pair (2.5 -> 2.0, 3.5 -> 4.0), rendu en décimal")
def execute_round(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: float(round(n)))  # arrondi bancaire


@jslt_function("truncate", description="Partie entière d'un nombre, sans arrondi (-2.7 -> -2.0), rendue en décimal")
def execute_truncate(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: float(math.trunc(n)))


@jslt_function("sqrt", description="Racine carrée d'un nombre")
def execute_sqrt(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.sqrt(n))


@jslt_function("exp", description="Exponentielle : e élevé à la puissance du nombre")
def execute_exp(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.exp(n))


@jslt_function("logarithm", description="Logarithme népérien (base e) d'un nombre")
def execute_log(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log(n))


@jslt_function("logarithm10", description="Logarithme décimal (base 10) d'un nombre")
def execute_log10(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log10(n))


@jslt_function("logarithm2", description="Logarithme binaire (base 2) d'un nombre")
def execute_log2(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log2(n))


# Trigonométrie (radians), port 1:1 des fonctions .NET du même nom.
def _register_unary_math(name: str, fn, description: str) -> None:
    # `fn` est capturée par la fermeture, pas passée en paramètre par défaut : un
    # paramètre `_fn=fn` apparaissait au catalogue (`acos(token, _fn)`) et un 2e
    # argument du template remplaçait l'opération.
    @jslt_function(name, description=description)
    def _impl(ctx: Any, token: Any = None) -> Any:
        return number_result(token, fn)


_TRIG_DESCRIPTIONS = {
    "sin": "Sinus d'un angle en radians",
    "cos": "Cosinus d'un angle en radians",
    "tan": "Tangente d'un angle en radians",
    "asin": "Arc sinus, en radians",
    "acos": "Arc cosinus, en radians",
    "atan": "Arc tangente, en radians",
    "sinh": "Sinus hyperbolique",
    "cosh": "Cosinus hyperbolique",
    "tanh": "Tangente hyperbolique",
    "asinh": "Arc sinus hyperbolique",
    "acosh": "Arc cosinus hyperbolique",
    "atanh": "Arc tangente hyperbolique",
}

for _name, _mathfn in (
    ("sin", math.sin), ("cos", math.cos), ("tan", math.tan),
    ("asin", math.asin), ("acos", math.acos), ("atan", math.atan),
    ("sinh", math.sinh), ("cosh", math.cosh), ("tanh", math.tanh),
    ("asinh", math.asinh), ("acosh", math.acosh), ("atanh", math.atanh),
):
    _register_unary_math(_name, _mathfn, _TRIG_DESCRIPTIONS[_name])


@jslt_function("atan2", description="Angle en radians du point (x = right, y = left) : atan2(y, x)")
def execute_atan2(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if not is_number(left):
        return None
    return math.atan2(left, coerce_number(right))


@jslt_function("pow", description="Puissance : base élevée à l'exposant, rendue en décimal")
def execute_pow(ctx: Any, base: Any = None, exponent: Any = None) -> Any:
    if not is_number(base):
        return None
    return float(math.pow(base, coerce_number(exponent)))


@jslt_function("min", description="Plus petit de deux nombres, rendu en décimal (pas un agrégat de tableau)")
def execute_min(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if not is_number(left):
        return None
    return float(min(left, coerce_number(right)))  # .NET renvoie un double


@jslt_function("max", description="Plus grand de deux nombres, rendu en décimal (pas un agrégat de tableau)")
def execute_max(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if not is_number(left):
        return None
    return float(max(left, coerce_number(right)))  # .NET renvoie un double


@jslt_function("pi", description="Constante pi (3.14159…)")
def execute_pi(ctx: Any) -> float:
    return math.pi


@jslt_function("e", description="Constante e, base du logarithme népérien (2.71828…)")
def execute_e(ctx: Any) -> float:
    return math.e
