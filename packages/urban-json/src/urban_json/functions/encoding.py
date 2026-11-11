"""Encodage, empreintes et échappement (port des ``Services.hash`` .NET, étendu).

Elles opèrent sur la représentation chaîne de la valeur (``token.ToString()``).
``None`` donne ``None``.

Note de fidélité : ``sha256``/``sha512`` renvoient un condensé hexadécimal en
minuscules et ``crc32`` un CRC-32 standard ; la casse exacte / l'implémentation
peuvent différer marginalement du moteur .NET.

Au-delà du .NET : ``md5``, ``sha1``, ``hmacsha256``, ``urlencode`` /
``urldecode``, ``htmlescape`` / ``htmlunescape``, ``hexencode`` / ``hexdecode``.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import html
import zlib
from typing import Any
from urllib.parse import quote, unquote

from urban_json.errors import JsltError

from ._helpers import stringify
from .registry import jslt_function


@jslt_function("tobase64", description="Encode une valeur en Base64 (texte UTF-8 ; objet ou tableau sérialisé en JSON)", description_en="Encodes a value in Base64 (UTF-8 text; object or array serialised as JSON)")
def execute_tobase64(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return base64.b64encode(stringify(token).encode("utf-8")).decode("ascii")


@jslt_function("frombase64", description="Décode un texte Base64 en texte UTF-8", description_en="Decodes Base64 text into UTF-8 text")
def execute_frombase64(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return base64.b64decode(stringify(token)).decode("utf-8")


@jslt_function("crc32", description="Somme de contrôle CRC32 d'une valeur (entier non signé)", description_en="CRC32 checksum of a value (unsigned integer)")
def execute_crc32(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return zlib.crc32(stringify(token).encode("utf-8")) & 0xFFFFFFFF


@jslt_function("sha256", description="Empreinte SHA-256 d'une valeur, en hexadécimal", description_en="SHA-256 digest of a value, in hexadecimal")
def execute_sha256(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return hashlib.sha256(stringify(token).encode("utf-8")).hexdigest()


@jslt_function("sha512", description="Empreinte SHA-512 d'une valeur, en hexadécimal", description_en="SHA-512 digest of a value, in hexadecimal")
def execute_sha512(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return hashlib.sha512(stringify(token).encode("utf-8")).hexdigest()


# --- Empreintes supplémentaires ----------------------------------------------
# md5 et sha1 sont **cassés pour la signature** : ils ne servent ici qu'à
# l'identité (clé de déduplication, nom de fichier stable, comparaison avec un
# système existant qui les impose). Pour signer, c'est hmacsha256.


@jslt_function("md5", description="Empreinte MD5 d'une valeur, en hexadécimal (identité, pas signature)", description_en="MD5 digest of a value, in hexadecimal (identity, not signature)")
def execute_md5(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    # usedforsecurity=False : Python 3.9+ sur distribution durcie (FIPS) refuse
    # sinon l'algorithme ; l'usage visé n'est pas cryptographique.
    return hashlib.md5(stringify(token).encode("utf-8"), usedforsecurity=False).hexdigest()


@jslt_function("sha1", description="Empreinte SHA-1 d'une valeur, en hexadécimal (identité, pas signature)", description_en="SHA-1 digest of a value, in hexadecimal (identity, not signature)")
def execute_sha1(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return hashlib.sha1(stringify(token).encode("utf-8"), usedforsecurity=False).hexdigest()


@jslt_function(
    "hmacsha256",
    description="Signature HMAC-SHA256 d'une valeur avec une clé secrète, en hexadécimal",
    description_en="HMAC-SHA256 signature of a value with a secret key, in hexadecimal",
)
def execute_hmacsha256(ctx: Any, token: Any = None, key: Any = None) -> Any:
    """HMAC-SHA256 — la façon correcte de signer un message avec un secret.

    Concaténer le secret et le message avant un ``sha256`` (ce qu'on écrit
    faute de HMAC) expose à l'extension de longueur : la fonction manquait, donc
    les templates faisaient le mauvais montage.
    """
    if token is None:
        return None
    if key is None or stringify(key) == "":
        # Une clé vide donnerait une signature valide et sans valeur : mieux
        # vaut refuser que signer avec rien.
        raise JsltError("hmacsha256 attend une clé secrète non vide")
    return hmac.new(
        stringify(key).encode("utf-8"), stringify(token).encode("utf-8"), hashlib.sha256
    ).hexdigest()


# --- URL, HTML, hexadécimal ---------------------------------------------------

_QUOTE_MODES = {"all": "", "path": "/"}


@jslt_function(
    "urlencode",
    description="Encode une valeur pour une URL (mode path pour conserver les barres obliques)",
    description_en="Encodes a value for a URL (path mode to keep the slashes)",
)
def execute_urlencode(ctx: Any, token: Any = None, mode: Any = None) -> Any:
    name = (stringify(mode) or "all").strip().lower()
    if name not in _QUOTE_MODES:
        raise JsltError(
            f"mode d'encodage d'URL inconnu : {mode!r} (attendu : {', '.join(_QUOTE_MODES)})"
        )
    if token is None:
        return None
    return quote(stringify(token), safe=_QUOTE_MODES[name])


@jslt_function("urldecode", description="Décode une valeur venue d'une URL (%20, %C3%A9…)", description_en="Decodes a value coming from a URL (%20, %C3%A9…)")
def execute_urldecode(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return unquote(stringify(token))


@jslt_function("htmlescape", description="Échappe les caractères qui ont un sens en HTML (< > & \" ')", description_en="Escapes the characters that mean something in HTML (< > & \" ')")
def execute_htmlescape(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return html.escape(stringify(token), quote=True)


@jslt_function("htmlunescape", description="Remplace les entités HTML (&amp;, &lt;…) par leurs caractères", description_en="Replaces HTML entities (&amp;, &lt;…) with their characters")
def execute_htmlunescape(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return html.unescape(stringify(token))


@jslt_function("hexencode", description="Écrit les octets UTF-8 d'une valeur en hexadécimal", description_en="Writes the UTF-8 bytes of a value in hexadecimal")
def execute_hexencode(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    return stringify(token).encode("utf-8").hex()


@jslt_function("hexdecode", description="Relit un texte hexadécimal en chaîne UTF-8", description_en="Reads hexadecimal text back into a UTF-8 string")
def execute_hexdecode(ctx: Any, token: Any = None) -> Any:
    if token is None:
        return None
    try:
        return bytes.fromhex(stringify(token)).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise JsltError(f"hexadécimal illisible : {token!r}") from exc
