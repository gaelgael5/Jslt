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


@jslt_function("abs")
def execute_abs(ctx: Any, token: Any = None) -> Any:
    return number_result(token, abs)  # conserve int/float comme en .NET


@jslt_function("floor")
def execute_floor(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: float(math.floor(n)))


@jslt_function("round")
def execute_round(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: float(round(n)))  # arrondi bancaire


@jslt_function("truncate")
def execute_truncate(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: float(math.trunc(n)))


@jslt_function("sqrt")
def execute_sqrt(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.sqrt(n))


@jslt_function("exp")
def execute_exp(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.exp(n))


@jslt_function("logarithm")
def execute_log(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log(n))


@jslt_function("logarithm10")
def execute_log10(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log10(n))


@jslt_function("logarithm2")
def execute_log2(ctx: Any, token: Any = None) -> Any:
    return number_result(token, lambda n: math.log2(n))


# Trigonométrie (radians), port 1:1 des fonctions .NET du même nom.
def _register_unary_math(name: str, fn) -> None:
    @jslt_function(name)
    def _impl(ctx: Any, token: Any = None, _fn=fn) -> Any:
        return number_result(token, _fn)


for _name, _mathfn in (
    ("sin", math.sin), ("cos", math.cos), ("tan", math.tan),
    ("asin", math.asin), ("acos", math.acos), ("atan", math.atan),
    ("sinh", math.sinh), ("cosh", math.cosh), ("tanh", math.tanh),
    ("asinh", math.asinh), ("acosh", math.acosh), ("atanh", math.atanh),
):
    _register_unary_math(_name, _mathfn)


@jslt_function("atan2")
def execute_atan2(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if not is_number(left):
        return None
    return math.atan2(left, coerce_number(right))


@jslt_function("pow")
def execute_pow(ctx: Any, base: Any = None, exponent: Any = None) -> Any:
    if not is_number(base):
        return None
    return float(math.pow(base, coerce_number(exponent)))


@jslt_function("min")
def execute_min(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if not is_number(left):
        return None
    return float(min(left, coerce_number(right)))  # .NET renvoie un double


@jslt_function("max")
def execute_max(ctx: Any, left: Any = None, right: Any = None) -> Any:
    if not is_number(left):
        return None
    return float(max(left, coerce_number(right)))  # .NET renvoie un double


@jslt_function("pi")
def execute_pi(ctx: Any) -> float:
    return math.pi


@jslt_function("e")
def execute_e(ctx: Any) -> float:
    return math.e
