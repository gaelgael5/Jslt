"""Qualité et diagnostic : ``require``, ``requirethat``, ``trace``, ``traces``,
et les validateurs de format (``isemail``, ``isurl``, ``isuuid``, ``isiban``).

Deux manques que rien ne contournait :

* **refuser une donnée.** Un template ne pouvait qu'en produire une sortie
  fausse, ou provoquer une erreur par accident (une division par zéro bien
  placée). Avec ``require``, le refus est explicite et porte un message métier,
  dans la même famille d'erreurs que le reste du moteur — donc rattrapable par
  ``trydefault`` quand c'est voulu.
* **observer sans polluer.** Le pas-à-pas existe au niveau de l'API
  (``JsltTemplate.debug``), pas au niveau du langage : impossible de regarder une
  valeur intermédiaire sans l'ajouter au résultat, donc sans changer ce qu'on
  mesure.
"""

from __future__ import annotations

import re
from typing import Any

from urban_json.errors import JsltError

from ._helpers import to_text
from .registry import jslt_function


@jslt_function(
    "require",
    description="Rend la valeur si elle est présente, sinon lève avec le message donné",
    description_en="Returns the value when it is present, otherwise raises with the given message",
)
def execute_require(ctx: Any, value: Any = None, message: Any = None) -> Any:
    """Exige une valeur **présente**, et la rend telle quelle.

    Seule l'absence (``null``) est refusée : ``0``, ``false``, ``""`` et ``[]``
    sont des valeurs, et les refuser rendrait la fonction inutilisable sur un
    montant nul ou un drapeau à faux. Pour une condition, c'est
    ``requirethat``.
    """
    if value is None:
        raise JsltError(to_text(message) or "valeur obligatoire absente")
    return value


@jslt_function(
    "requirethat",
    description="Vérifie une condition et lève avec le message donné si elle n'est pas vraie",
    description_en="Checks a condition and raises with the given message when it is not true",
)
def execute_requirethat(ctx: Any, condition: Any = None, message: Any = None) -> bool:
    """Exige une condition **vraie**.

    Strictement ``true``, et non « véridique » : une condition qui vaut ``0`` ou
    ``""`` est presque toujours une expression qu'on croyait booléenne, et la
    laisser passer pour fausse masquerait l'erreur d'écriture.
    """
    if condition is not True:
        raise JsltError(to_text(message) or f"condition non satisfaite : {condition!r}")
    return True


@jslt_function(
    "trace",
    description="Rend la valeur inchangée et l'enregistre dans le journal, lisible par traces()",
    description_en="Returns the value unchanged and records it in the journal, readable through traces()",
)
def execute_trace(ctx: Any, value: Any = None, label: Any = None) -> Any:
    """Observe une valeur **sans** la mettre dans le résultat.

    Le journal vit sur le contexte d'exécution, donc une exécution ne voit jamais
    les traces d'une autre, et un intégrateur peut le lire après coup
    (``context.traces``) sans que le template ait à le recopier dans sa sortie.
    """
    traces = getattr(ctx, "traces", None)
    if traces is not None:
        traces.append({"label": to_text(label), "value": value})
    return value


@jslt_function("traces", description="Journal des valeurs observées par trace() dans cette exécution", description_en="Journal of the values observed by trace() in this run")
def execute_traces(ctx: Any) -> list:
    return list(getattr(ctx, "traces", []))


# --- validateurs de format ----------------------------------------------------
# Volontairement **pragmatiques** : une adresse conforme à la RFC 5322 complète
# accepte des formes que personne n'utilise (commentaires, guillemets), et un
# validateur qui les accepte laisse passer ce qu'un système en aval refusera.

_EMAIL = re.compile(r"^[^\s@,;<>\"]+@[^\s@.,;<>\"]+(\.[^\s@.,;<>\"]+)+$")
_URL = re.compile(r"^[a-z][a-z0-9+.-]*://[^\s/?#]+[^\s]*$", re.IGNORECASE)
_UUID = re.compile(
    r"^\{?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}?$", re.IGNORECASE
)
_IBAN = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$")


def _text_of(value: Any) -> str | None:
    """Texte à valider, ou ``None`` si la valeur n'est pas un texte.

    Un prédicat rend un booléen : ``null`` et un nombre ne sont pas des adresses
    valides, et rendre ``null`` obligerait l'appelant à distinguer trois cas là
    où la question est fermée.
    """
    return value if isinstance(value, str) else None


@jslt_function("isemail", description="Vrai si le texte a la forme d'une adresse électronique", description_en="True when the text has the shape of an email address")
def execute_isemail(ctx: Any, token: Any = None) -> bool:
    text = _text_of(token)
    return bool(text and _EMAIL.match(text))


@jslt_function("isurl", description="Vrai si le texte a la forme d'une URL avec son schéma", description_en="True when the text has the shape of a URL with its scheme")
def execute_isurl(ctx: Any, token: Any = None) -> bool:
    text = _text_of(token)
    return bool(text and _URL.match(text))


@jslt_function("isuuid", description="Vrai si le texte a la forme d'un UUID (accolades tolérées)", description_en="True when the text has the shape of a UUID (braces tolerated)")
def execute_isuuid(ctx: Any, token: Any = None) -> bool:
    text = _text_of(token)
    return bool(text and _UUID.match(text))


@jslt_function(
    "isiban",
    description="Vrai si le texte est un IBAN dont la clé de contrôle (modulo 97) est juste",
    description_en="True when the text is an IBAN whose check digits (modulo 97) are right",
)
def execute_isiban(ctx: Any, token: Any = None) -> bool:
    """Structure **et** clé de contrôle.

    La longueur attendue par pays n'est pas vérifiée : ce serait une table de
    plus de soixante entrées à maintenir, et sa péremption ferait refuser un
    IBAN valide — un faux refus coûte plus cher ici qu'un faux accord, que la
    banque rejettera de toute façon. Le modulo 97 attrape les fautes de frappe,
    qui sont le vrai sujet.
    """
    text = _text_of(token)
    if text is None:
        return False
    compact = text.replace(" ", "").replace("-", "").upper()
    if not _IBAN.match(compact):
        return False
    # Les quatre premiers caractères passent à la fin, puis chaque lettre devient
    # sa position dans l'alphabet + 9 (A = 10).
    rotated = compact[4:] + compact[:4]
    digits = "".join(str(ord(c) - 55) if c.isalpha() else c for c in rotated)
    return int(digits) % 97 == 1
