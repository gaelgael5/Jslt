"""Fonctions d'encodage et de hachage (port des ``Services.hash`` .NET).

Elles opèrent sur la représentation chaîne de la valeur (``token.ToString()``).
``None`` donne ``None``.

Note de fidélité : ``sha256``/``sha512`` renvoient un condensé hexadécimal en
minuscules et ``crc32`` un CRC-32 standard ; la casse exacte / l'implémentation
peuvent différer marginalement du moteur .NET.
"""

from __future__ import annotations

import base64
import hashlib
import zlib
from typing import Any

from ._helpers import stringify
from .registry import jslt_function


@jslt_function("tobase64")
def execute_tobase64(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return base64.b64encode(stringify(token).encode("utf-8")).decode("ascii")


@jslt_function("frombase64")
def execute_frombase64(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return base64.b64decode(stringify(token)).decode("utf-8")


@jslt_function("crc32")
def execute_crc32(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return zlib.crc32(stringify(token).encode("utf-8")) & 0xFFFFFFFF


@jslt_function("sha256")
def execute_sha256(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return hashlib.sha256(stringify(token).encode("utf-8")).hexdigest()


@jslt_function("sha512")
def execute_sha512(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return hashlib.sha512(stringify(token).encode("utf-8")).hexdigest()
