"""Plugin urban-json : validation de numéros de téléphone (``phoneisvalid``).

Port de ``ExecutePhoneIsValid`` (.NET), avec la même bibliothèque de référence :
``phonenumbers`` est le portage Python de libphonenumber (Google), utilisé côté
.NET via ``PhoneNumbers``. Les règles de validité sont donc identiques.

Logique reprise du .NET : un numéro qui commence par ``+`` ou ``00`` est
international (``00`` remplacé par ``+``) et validé pour la région qu'il désigne ;
sinon il est lu avec ``default_region`` (code ISO à deux lettres) et validé.
Numéro illisible, vide ou région inconnue : ``false``.

Découvert automatiquement via l'entry point ``urban_json.functions``.
"""

from __future__ import annotations

from typing import Any

import phonenumbers

__version__ = "0.1.1"

__all__ = ["execute_phoneisvalid", "register"]


def execute_phoneisvalid(ctx: Any, phone_number: Any = None, default_region: Any = None) -> bool:
    if phone_number is None:
        return False
    text = str(phone_number).strip()
    if not text:
        return False
    try:
        if text.startswith(("+", "00")):
            if text.startswith("00"):
                text = "+" + text[2:]
            number = phonenumbers.parse(text, None)
            region = phonenumbers.region_code_for_number(number)
            return bool(region) and phonenumbers.is_valid_number_for_region(number, region)
        region = str(default_region).strip().upper() if default_region else None
        if not region:
            return False  # sans indicatif ni région, rien ne permet de lire le numéro
        return phonenumbers.is_valid_number(phonenumbers.parse(text, region))
    except phonenumbers.NumberParseException:
        return False


def register(registry: Any) -> None:
    """Enregistre ``phoneisvalid``."""
    registry.register(
        "phoneisvalid",
        execute_phoneisvalid,
        description="Vrai si le numéro de téléphone est valide (international avec + ou 00, sinon selon la région ISO donnée)",
    )
