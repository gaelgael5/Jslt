"""Fonctions mathématiques intégrées (port des ``Services.Numbers`` .NET).

Convention : une valeur non numérique (ou ``None``) donne ``None``. Comme en
.NET, les fonctions transcendantes et ``floor``/``round``/``min``/``max``/``pow``
renvoient un flottant ; ``round`` est un arrondi bancaire (demi vers pair).
"""

from __future__ import annotations

import math
from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_number, is_number, number_result
from .aggregate import numbers_of
from .registry import jslt_function


@jslt_function("abs", description="Valeur absolue d'un nombre (null si ce n'est pas un nombre)", description_en="Absolute value of a number (null when it is not a number)")
def execute_abs(ctx: Any, token: Any = None) -> Any:
    return number_result(token, abs)  # conserve int/float comme en .NET


@jslt_function(
    "floor",
    description="Arrondi vers le bas, à l'entier (2.7 -> 2.0) ou à digits décimales",
    description_en="Rounds down, to the integer (2.7 -> 2.0) or to digits decimals",
)
def execute_floor(ctx: Any, token: Any = None, digits: Any = None) -> Any:
    return _directed(token, math.floor, digits)


@jslt_function(
    "ceil",
    description="Arrondi vers le haut, à l'entier (2.1 -> 3.0) ou à digits décimales",
    description_en="Rounds up, to the integer (2.1 -> 3.0) or to digits decimals",
)
def execute_ceil(ctx: Any, token: Any = None, digits: Any = None) -> Any:
    """Symétrique de ``floor``, qui existait seul — l'asymétrie la plus visible
    du portage, et celle qui obligeait à écrire ``0 - floor(0 - x)``."""
    return _directed(token, math.ceil, digits)


def _directed(token: Any, operation: Any, digits: Any) -> Any:
    """Arrondi dirigé, à l'entier ou à ``digits`` décimales.

    Un facteur 10^digits plutôt qu'un passage par le texte : on reste dans le
    numérique, et le quirk .NET du résultat décimal est conservé.
    """
    if digits is None:
        return number_result(token, lambda n: float(operation(n)))
    factor = 10 ** int(coerce_number(digits))
    return number_result(token, lambda n: operation(n * factor) / factor)


@jslt_function("round", description="Arrondi à l'entier le plus proche, demi vers le pair (2.5 -> 2.0, 3.5 -> 4.0), rendu en décimal", description_en="Rounds to the nearest integer, halves to even (2.5 -> 2.0, 3.5 -> 4.0), returned as a decimal")
def execute_round(ctx: Any, token: Any = None, digits: Any = None) -> Any:
    """Arrondi bancaire, à l'entier par défaut ou à ``digits`` décimales.

    L'argument de précision est une extension : sans lui, arrondir un montant à
    deux décimales demandait de multiplier par 100, arrondir et rediviser — avec
    l'erreur de représentation que ça traîne.
    """
    if digits is None:
        return number_result(token, lambda n: float(round(n)))  # arrondi bancaire
    places = int(coerce_number(digits))
    return number_result(token, lambda n: round(float(n), places))


@jslt_function(
    "truncate",
    description="Coupe vers zéro (-2.7 -> -2.0), à l'entier ou à digits décimales",
    description_en="Cuts towards zero (-2.7 -> -2.0), to the integer or to digits decimals",
)
def execute_truncate(ctx: Any, token: Any = None, digits: Any = None) -> Any:
    return _directed(token, math.trunc, digits)


@jslt_function("sqrt", description="Racine carrée d'un nombre", description_en="Square root of a number")
def execute_sqrt(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.sqrt(n))


@jslt_function("exp", description="Exponentielle : e élevé à la puissance du nombre", description_en="Exponential: e raised to the power of the number")
def execute_exp(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.exp(n))


@jslt_function("logarithm", description="Logarithme népérien (base e) d'un nombre", description_en="Natural logarithm (base e) of a number")
def execute_log(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log(n))


@jslt_function("logarithm10", description="Logarithme décimal (base 10) d'un nombre", description_en="Common logarithm (base 10) of a number")
def execute_log10(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log10(n))


@jslt_function("logarithm2", description="Logarithme binaire (base 2) d'un nombre", description_en="Binary logarithm (base 2) of a number")
def execute_log2(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log2(n))


# Trigonométrie (radians), port 1:1 des fonctions .NET du même nom.
def _register_unary_math(name: str, fn, description: str, description_en: str) -> None:
    # `fn` est capturée par la fermeture, pas passée en paramètre par défaut : un
    # paramètre `_fn=fn` apparaissait au catalogue (`acos(token, _fn)`) et un 2e
    # argument du template remplaçait l'opération.
    @jslt_function(name, description=description, description_en=description_en)
    def _impl(ctx: Any, token: Any = None) -> Any:
        return number_result(token, fn)


#: Description de chaque fonction trigonométrique, dans les deux langues.
_TRIG_DESCRIPTIONS = {
    "sin": ("Sinus d'un angle en radians", "Sine of an angle in radians"),
    "cos": ("Cosinus d'un angle en radians", "Cosine of an angle in radians"),
    "tan": ("Tangente d'un angle en radians", "Tangent of an angle in radians"),
    "asin": ("Arc sinus, en radians", "Arc sine, in radians"),
    "acos": ("Arc cosinus, en radians", "Arc cosine, in radians"),
    "atan": ("Arc tangente, en radians", "Arc tangent, in radians"),
    "sinh": ("Sinus hyperbolique", "Hyperbolic sine"),
    "cosh": ("Cosinus hyperbolique", "Hyperbolic cosine"),
    "tanh": ("Tangente hyperbolique", "Hyperbolic tangent"),
    "asinh": ("Arc sinus hyperbolique", "Hyperbolic arc sine"),
    "acosh": ("Arc cosinus hyperbolique", "Hyperbolic arc cosine"),
    "atanh": ("Arc tangente hyperbolique", "Hyperbolic arc tangent"),
}

for _name, _mathfn in (
    ("sin", math.sin), ("cos", math.cos), ("tan", math.tan),
    ("asin", math.asin), ("acos", math.acos), ("atan", math.atan),
    ("sinh", math.sinh), ("cosh", math.cosh), ("tanh", math.tanh),
    ("asinh", math.asinh), ("acosh", math.acosh), ("atanh", math.atanh),
):
    _register_unary_math(_name, _mathfn, *_TRIG_DESCRIPTIONS[_name])


@jslt_function("atan2", description="Angle en radians du point (x = right, y = left) : atan2(y, x)", description_en="Angle in radians of the point (x = right, y = left): atan2(y, x)")
def execute_atan2(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if not is_number(left):
        return None
    return math.atan2(left, coerce_number(right))


@jslt_function("pow", description="Puissance : base élevée à l'exposant, rendue en décimal", description_en="Power: base raised to the exponent, returned as a decimal")
def execute_pow(ctx: Any, base: Any = None, exponent: Any = None) -> Any:
    if not is_number(base):
        return None
    return float(math.pow(base, coerce_number(exponent)))


@jslt_function("min", description="Plus petit de deux nombres, ou du tableau donné (décimal pour deux nombres)", description_en="Smaller of two numbers, or of the given array (decimal for two numbers)")
def execute_min(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if isinstance(left, list):
        return _extreme(left, min, "min", right)
    if not is_number(left):
        return None
    return float(min(left, coerce_number(right)))  # .NET renvoie un double


@jslt_function("max", description="Plus grand de deux nombres, ou du tableau donné (décimal pour deux nombres)", description_en="Larger of two numbers, or of the given array (decimal for two numbers)")
def execute_max(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if isinstance(left, list):
        return _extreme(left, max, "max", right)
    if not is_number(left):
        return None
    return float(max(left, coerce_number(right)))  # .NET renvoie un double


def _extreme(values: list, pick, name: str, right: Any) -> Any:
    """Agrégat sur un tableau, ajouté à la forme binaire .NET.

    Deux formes dans une fonction plutôt qu'un `minof` / `maxof` de plus : c'est
    la même question (« le plus petit »), et `sum($.n)` agrège déjà un tableau.
    Le type est conservé ici (un entier reste entier), là où la forme binaire
    garde le quirk .NET du décalage en décimal — passer un tableau est un usage
    neuf, il n'a pas de compatibilité à respecter.
    """
    if right is not None:
        # Sinon le second argument serait ignoré en silence.
        raise JsltError(f"{name} sur un tableau n'attend pas de second argument : {right!r}")
    numbers = numbers_of(values, name)
    return pick(numbers) if numbers else None


@jslt_function("pi", description="Constante pi (3.14159…)", description_en="The constant pi (3.14159…)")
def execute_pi(ctx: Any) -> float:
    return math.pi


@jslt_function("e", description="Constante e, base du logarithme népérien (2.71828…)", description_en="The constant e, base of the natural logarithm (2.71828…)")
def execute_e(ctx: Any) -> float:
    return math.e
