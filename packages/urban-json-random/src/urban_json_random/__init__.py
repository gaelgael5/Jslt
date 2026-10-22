"""Plugin urban-json : génération de données aléatoires (``getrandom_*``).

Port des 25 fonctions de ``Services.randoms.cs`` (.NET), qui s'appuyaient sur
``RandomDataGenerator`` ; ici, Faker (noms, lieux, e-mails, IBAN, réseau,
lorem ipsum) et rstr (chaîne conforme à un motif regex). Les noms d'origine sont
conservés, y compris ``getrandom_datatime`` (faute de frappe du .NET), pour que
les templates existants fonctionnent tels quels.

Découvert automatiquement via l'entry point ``urban_json.functions`` ; aussi
enregistrable à la main : ``from urban_json_random import register``.

Écarts volontaires vs .NET (comportement voulu, pas les bugs) :

* ``exclusiveMinimum`` / ``exclusiveMaximum`` suivent JSON Schema (borne
  exclue). Le .NET faisait ``min--`` / ``max++`` : il *élargissait* l'intervalle.
* Bornes absentes : étendue du type (``integer`` 0..2³¹−1, ``double`` [0, 1)…).
  Le .NET générait souvent ``[0, 0]``, donc toujours 0.
* Intervalle impossible (min > max) : ``JsltError`` au lieu d'une exception .NET.
* ``getrandom_boolean`` / ``getrandom_in_list`` : vrai tirage aléatoire (le .NET
  prenait la parité des millisecondes de l'horloge) ; liste vide -> ``null``.
* ``getrandom_password`` : générateur cryptographique (``secrets``), même
  alphabet que le .NET.
* Dates et durées rendues en texte (le portage n'a pas de type date) :
  ``getrandom_datatime`` en ISO 8601, ``getrandom_timespan`` en ``hh:mm:ss.fff``.
"""

from __future__ import annotations

import base64
import random
import secrets
import string
from datetime import datetime, timedelta
from functools import cache
from typing import Any

from urban_json import JsltError

from ._naughty import NAUGHTY_STRINGS

__version__ = "0.1.0"

__all__ = ["NAUGHTY_STRINGS", "register"]

_RNG = random.SystemRandom()

# Étendue par défaut de chaque type entier (bornes .NET des types d'origine).
_INT_RANGES = {
    "getrandom_byte": (0, 255),
    "getrandom_short": (-(2**15), 2**15 - 1),
    "getrandom_integer": (-(2**31), 2**31 - 1),
    "getrandom_long": (-(2**63), 2**63 - 1),
}


@cache
def _faker(locale: str = "en_US") -> Any:
    from faker import Faker  # import différé : Faker charge beaucoup de données

    return Faker(locale)


def _flag(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() == "true")


def _int_bounds(name: str, minimum: Any, exclusive_min: Any, maximum: Any, exclusive_max: Any) -> tuple[int, int]:
    type_low, type_high = _INT_RANGES[name]
    low = 0 if minimum is None else int(minimum)
    high = type_high if maximum is None else int(maximum)
    if _flag(exclusive_min):
        low += 1
    if _flag(exclusive_max):
        high -= 1
    if not (type_low <= low <= type_high and type_low <= high <= type_high):
        raise JsltError(f"{name} : bornes hors de l'étendue du type [{type_low}, {type_high}]")
    if low > high:
        raise JsltError(f"{name} : intervalle vide (minimum {low} > maximum {high})")
    return low, high


def _make_int(name: str):
    def generate(ctx: Any, minimum: Any = None, exclusive_minimum: Any = None,
                 maximum: Any = None, exclusive_maximum: Any = None) -> int:
        low, high = _int_bounds(name, minimum, exclusive_minimum, maximum, exclusive_maximum)
        return _RNG.randint(low, high)

    return generate


def _make_real(name: str, single: bool):
    def generate(ctx: Any, minimum: Any = None, exclusive_minimum: Any = None,
                 maximum: Any = None, exclusive_maximum: Any = None) -> float:
        low = 0.0 if minimum is None else float(minimum)
        high = 1.0 if maximum is None else float(maximum)
        excl_low, excl_high = _flag(exclusive_minimum), _flag(exclusive_maximum)
        if low > high or (low == high and (excl_low or excl_high)):
            raise JsltError(f"{name} : intervalle vide (minimum {low}, maximum {high})")
        while True:
            value = _RNG.uniform(low, high)
            if single:
                value = float(f"{value:.7g}")  # précision d'un float .NET (simple)
            if (excl_low and value <= low) or (excl_high and value >= high):
                continue
            if low <= value <= high:
                return value

    return generate


def getrandom_string(ctx: Any, min_length: Any = None, max_length: Any = None, pattern: Any = None) -> str:
    if pattern:
        import re

        import rstr

        try:
            re.compile(pattern)
        except re.error as exc:
            raise JsltError(f"getrandom_string : motif regex invalide {pattern!r} : {exc}") from exc
        # Les ancres ^ $ délimitent déjà la chaîne produite : on les retire avant de générer.
        body = pattern.removeprefix("^")
        if body.endswith("$") and not body.endswith("\\$"):
            body = body[:-1]
        return rstr.xeger(body)
    low = 1 if not min_length else int(min_length)
    high = low + 5 if not max_length else int(max_length)
    if low > high:
        raise JsltError(f"getrandom_string : intervalle de longueur vide ({low} > {high})")
    alphabet = string.ascii_letters + string.digits + " "
    length = _RNG.randint(low, high)
    # Pas d'espace en tête ni en fin : le texte reste lisible et sa longueur exacte.
    inner = "".join(_RNG.choice(alphabet) for _ in range(max(0, length - 2)))
    edge = string.ascii_letters + string.digits
    if length == 1:
        return _RNG.choice(edge)
    return _RNG.choice(edge) + inner + _RNG.choice(edge)


def getrandom_datatime(ctx: Any) -> str:
    # Sans fuseau, comme les dates « Unspecified » du .NET et `now()` du cœur.
    start = datetime(1970, 1, 1)  # noqa: DTZ001
    span = (datetime(2050, 12, 31, 23, 59, 59) - start).total_seconds()  # noqa: DTZ001
    return (start + timedelta(seconds=_RNG.randint(0, int(span)))).isoformat()


def getrandom_timespan(ctx: Any) -> str:
    total_ms = _RNG.randint(0, 24 * 3600 * 1000 - 1)
    seconds, ms = divmod(total_ms, 1000)
    minutes, sec = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    return f"{hours:02d}:{minute:02d}:{sec:02d}.{ms:03d}"


def getrandom_email(ctx: Any) -> str:
    return _faker().email()


def getrandom_ipv4(ctx: Any) -> str:
    return _faker().ipv4()


def getrandom_ipv6(ctx: Any) -> str:
    return _faker().ipv6().upper()


def getrandom_binary(ctx: Any, min_length: Any = None, max_length: Any = None) -> str:
    low = 1 if min_length is None else int(min_length)
    high = low + 5 if max_length is None else int(max_length)
    if low > high or low < 0:
        raise JsltError(f"getrandom_binary : intervalle de longueur invalide ({low}, {high})")
    return base64.b64encode(secrets.token_bytes(_RNG.randint(low, high))).decode("ascii")


def getrandom_boolean(ctx: Any) -> bool:
    return _RNG.random() < 0.5


def getrandom_city(ctx: Any) -> str:
    return _faker().city()


def getrandom_country(ctx: Any) -> str:
    return _faker().country()


def getrandom_lastname(ctx: Any) -> str:
    return _faker().last_name()


def getrandom_firstname(ctx: Any) -> str:
    return _faker().first_name()


def getrandom_fullname(ctx: Any) -> str:
    fake = _faker()
    return f"{fake.first_name()} {fake.last_name()}"


# Pays ISO 3166-1 alpha-2 -> locale Faker qui sait produire son IBAN.
_IBAN_LOCALES = {
    "AT": "de_AT", "BE": "nl_BE", "CH": "de_CH", "CZ": "cs_CZ", "DE": "de_DE", "DK": "da_DK",
    "ES": "es_ES", "FI": "fi_FI", "FR": "fr_FR", "GB": "en_GB", "GR": "el_GR", "IE": "en_IE",
    "IT": "it_IT", "NL": "nl_NL", "NO": "no_NO", "PL": "pl_PL", "PT": "pt_PT", "SE": "sv_SE",
}


def getrandom_iban(ctx: Any, country_code_iso2: Any = None, include_iban: Any = None, include_bban: Any = None) -> str:
    country = (str(country_code_iso2).strip().upper() if country_code_iso2 else "GB")
    locale = _IBAN_LOCALES.get(country)
    if locale is None:
        raise JsltError(
            f"getrandom_iban : pays non pris en charge {country_code_iso2!r} "
            f"(codes : {', '.join(sorted(_IBAN_LOCALES))})"
        )
    fake = _faker(locale)
    if _flag(include_bban):
        # .NET : BBAN seul si l'IBAN est explicitement exclu, sinon l'un ou l'autre.
        if include_iban is not None and not _flag(include_iban):
            return fake.bban()
        return fake.iban() if _RNG.random() < 0.5 else fake.bban()
    return fake.iban()


def _mac_int(text: Any, default: int) -> int:
    if text is None or text == "":
        return default
    digits = str(text).replace(":", "").replace("-", "")
    try:
        value = int(digits, 16)
    except ValueError as exc:
        raise JsltError(f"getrandom_macaddress : adresse MAC invalide {text!r}") from exc
    if len(digits) != 12:
        raise JsltError(f"getrandom_macaddress : adresse MAC invalide {text!r}")
    return value


def getrandom_macaddress(ctx: Any, minimum: Any = None, maximum: Any = None) -> str:
    low, high = _mac_int(minimum, 0), _mac_int(maximum, 2**48 - 1)
    if low > high:
        raise JsltError("getrandom_macaddress : intervalle vide (minimum > maximum)")
    raw = f"{_RNG.randint(low, high):012X}"
    return ":".join(raw[i:i + 2] for i in range(0, 12, 2))


def getrandom_lipsum(ctx: Any, paragraphs: Any = None) -> str:
    count = max(1, int(paragraphs or 0))
    return "\n".join(_faker().paragraphs(nb=count))


def getrandom_naughtystrings(ctx: Any) -> str:
    return _RNG.choice(NAUGHTY_STRINGS)


def getrandom_in_list(ctx: Any, items: Any = None) -> Any:
    if not isinstance(items, list) or not items:
        return None
    return _RNG.choice(items)


# Alphabet du .NET (Services.randoms.cs), conservé pour des mots de passe comparables.
_PASSWORD_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890&é'(-è_çà)=$ù%*µ,?;:/.?'"


def getrandom_password(ctx: Any, token: Any = None, length: Any = None) -> str:
    # `token` est ignoré, comme en .NET : il est gardé pour la compatibilité des templates.
    size = int(length or 0) or 12
    return "".join(secrets.choice(_PASSWORD_ALPHABET) for _ in range(size))


_RANGE = "(minimum, exclusiveMinimum, maximum, exclusiveMaximum ; bornes exclues si les drapeaux valent true)"

_FUNCTIONS: list[tuple[str, Any, str]] = [
    ("getrandom_integer", _make_int("getrandom_integer"), f"Entier aléatoire 32 bits {_RANGE}"),
    ("getrandom_long", _make_int("getrandom_long"), f"Entier aléatoire 64 bits {_RANGE}"),
    ("getrandom_short", _make_int("getrandom_short"), f"Entier aléatoire 16 bits {_RANGE}"),
    ("getrandom_byte", _make_int("getrandom_byte"), f"Entier aléatoire de 0 à 255 {_RANGE}"),
    ("getrandom_double", _make_real("getrandom_double", single=False), f"Décimal aléatoire, [0, 1) par défaut {_RANGE}"),
    ("getrandom_float", _make_real("getrandom_float", single=True), f"Décimal aléatoire en simple précision {_RANGE}"),
    ("getrandom_string", getrandom_string,
     "Texte aléatoire (lettres, chiffres, espaces) de min_length à max_length caractères, ou conforme au motif regex"),
    ("getrandom_datatime", getrandom_datatime, "Date et heure aléatoires entre 1970 et 2050, en ISO 8601"),
    ("getrandom_timespan", getrandom_timespan, "Durée aléatoire de moins d'un jour, au format hh:mm:ss.fff"),
    ("getrandom_email", getrandom_email, "Adresse e-mail aléatoire"),
    ("getrandom_ipv4", getrandom_ipv4, "Adresse IPv4 aléatoire"),
    ("getrandom_ipv6", getrandom_ipv6, "Adresse IPv6 aléatoire, en majuscules"),
    ("getrandom_binary", getrandom_binary, "Octets aléatoires de min_length à max_length, encodés en Base64"),
    ("getrandom_boolean", getrandom_boolean, "Booléen aléatoire, true ou false"),
    ("getrandom_city", getrandom_city, "Nom de ville aléatoire"),
    ("getrandom_country", getrandom_country, "Nom de pays aléatoire"),
    ("getrandom_lastname", getrandom_lastname, "Nom de famille aléatoire"),
    ("getrandom_firstname", getrandom_firstname, "Prénom aléatoire"),
    ("getrandom_fullname", getrandom_fullname, "Prénom et nom aléatoires"),
    ("getrandom_iban", getrandom_iban,
     "IBAN valide aléatoire pour un pays ISO (FR, DE, GB…) ; BBAN si include_bban vaut true et include_iban false"),
    ("getrandom_macaddress", getrandom_macaddress,
     "Adresse MAC aléatoire (AA:BB:…), éventuellement entre deux adresses minimum et maximum"),
    ("getrandom_lipsum", getrandom_lipsum, "Texte lorem ipsum de n paragraphes (1 par défaut)"),
    ("getrandom_naughtystrings", getrandom_naughtystrings,
     "Chaîne piégeuse pour les tests (Unicode, injection, formats limites)"),
    ("getrandom_in_list", getrandom_in_list, "Élément tiré au hasard dans un tableau (null s'il est vide)"),
    ("getrandom_password", getrandom_password,
     "Mot de passe aléatoire de length caractères (12 par défaut) ; le 1er argument est ignoré"),
]


def register(registry: Any) -> None:
    """Enregistre les 25 fonctions ``getrandom_*`` dans un registre jslt."""
    for name, function, description in _FUNCTIONS:
        registry.register(name, function, description=description)
