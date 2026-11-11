"""Arrondis que ``round`` ne sait pas faire : ``roundhalfup``, ``roundto``,
``toprecision``.

Sans contrepartie .NET. ``round`` est l'arrondi **bancaire** (demi vers le pair,
quirk conservé) : ``round(0.125, 2)`` rend ``0.12``, là où une facture attend
``0.13``. Le moteur ne savait donc pas écrire l'arrondi le plus courant du
commerce, ni arrondir à un multiple (le pas de 0,05 d'une caisse), ni à un nombre
de **chiffres significatifs** (une mesure). Les contournements existaient —
``round($.n * 20) / 20`` pour le pas de 0,05 — mais ils ramènent l'erreur de
représentation binaire que ces fonctions sont précisément là pour éviter.

Tout passe par :class:`decimal.Decimal` construit sur le **texte** du nombre, et
non sur le flottant : ``Decimal("2.675")`` est 2,675, alors que
``Decimal(2.675)`` vaut 2,674999999999999822… et rendrait 2,67 — l'arrondi
« faux » que tout le monde rencontre une fois.

Comme ``round``, ``floor`` et ``ceil``, ces trois fonctions rendent un
**décimal** : la famille entière le fait, et une exception ici obligerait à
vérifier au cas par cas ce qu'on reçoit.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, localcontext
from typing import Any

from urban_json.errors import JsltError

from ._helpers import coerce_number, is_number, number_result
from .registry import jslt_function


def _exact(value: Any) -> Decimal:
    """Le nombre tel qu'il est **écrit**, pas tel qu'il est stocké."""
    return Decimal(str(value))


@jslt_function(
    "roundhalfup",
    description="Arrondi commercial : les demis s'éloignent de zéro (0.125 -> 0.13), à l'entier ou à digits décimales",
    description_en="Commercial rounding: halves go away from zero (0.125 -> 0.13), to the integer or to digits decimals",
)
def execute_roundhalfup(ctx: Any, token: Any = None, digits: Any = None) -> Any:
    """L'arrondi qu'attend une facture, celui que ``round`` ne fait pas.

    « Demi vers le haut » se dit mal des négatifs : la règle appliquée est
    *demi en s'éloignant de zéro* (``-0.5`` donne ``-1``), celle du commerce et
    celle de ``Math.Round(…, MidpointRounding.AwayFromZero)``. L'alternative —
    demi vers +∞, donc ``-0.5`` à ``0`` — rendrait l'arrondi d'un avoir
    différent de celui de la facture qu'il annule.
    """
    places = 0 if digits is None else int(coerce_number(digits))
    return number_result(token, lambda n: float(_quantize(_exact(n), places)))


def _quantize(value: Decimal, places: int) -> Decimal:
    # `places` négatif (arrondir aux dizaines) : `Decimal(1).scaleb` donne
    # l'exposant voulu sans construire une chaîne de zéros.
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


@jslt_function(
    "roundto",
    description="Arrondi au multiple le plus proche (roundto(2.34, 0.05) -> 2.35), demi en s'éloignant de zéro",
    description_en="Rounds to the nearest multiple (roundto(2.34, 0.05) -> 2.35), halves away from zero",
)
def execute_roundto(ctx: Any, token: Any = None, step: Any = None) -> Any:
    """Arrondi à un **pas** : prix au centime de 5, durée au quart d'heure.

    Le pas doit être strictement positif. Un pas nul **lève** plutôt que de
    rendre la valeur inchangée : écrire ``roundto($.n, $.pas)`` avec un pas
    absent donnerait sinon un résultat d'apparence juste, qui n'a pourtant
    arrondi à rien. Un pas négatif lève pour la même raison — il n'a pas de
    sens, donc il vient d'une erreur de données.
    """
    if not is_number(token):
        return None
    if step is None:
        raise JsltError("roundto attend un pas d'arrondi (roundto($.n, 0.05))")
    size = _exact(coerce_number(step))
    if size <= 0:
        raise JsltError(f"le pas d'arrondi doit être strictement positif, reçu : {step!r}")
    units = _quantize(_exact(token) / size, 0)
    return float(units * size)


@jslt_function(
    "toprecision",
    description="Arrondi à un nombre de chiffres significatifs (toprecision(1234.5, 3) -> 1230)",
    description_en="Rounds to a number of significant digits (toprecision(1234.5, 3) -> 1230)",
)
def execute_toprecision(ctx: Any, token: Any = None, digits: Any = None) -> Any:
    """Chiffres **significatifs**, pas décimales : ce que demande une mesure.

    ``round($.n, 2)`` fixe le rang de la virgule, ce qui n'a pas de sens sur des
    valeurs dont l'ordre de grandeur varie (0,00241 et 24 100 dans la même
    colonne). Zéro a, lui, autant de chiffres significatifs qu'on veut : il est
    rendu tel quel, sans passer par la mise à l'échelle.
    """
    if not is_number(token):
        return None
    if digits is None:
        raise JsltError("toprecision attend un nombre de chiffres significatifs")
    count = int(coerce_number(digits))
    if count < 1:
        raise JsltError(f"le nombre de chiffres significatifs doit valoir au moins 1, reçu : {count}")
    if token == 0:
        return 0.0
    with localcontext() as context:
        context.prec = count
        context.rounding = ROUND_HALF_UP
        try:
            # L'opérateur unaire applique la précision du contexte : c'est la
            # seule opération Decimal qui arrondit sans rien changer d'autre.
            return float(+_exact(token))
        except InvalidOperation as exc:  # pragma: no cover - garde-fou
            raise JsltError(f"arrondi impossible : {token!r}") from exc
