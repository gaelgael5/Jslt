"""Plugin jslt : appels HTTP depuis les templates (``http`` / ``httpget``).

Le moteur .NET n'offre qu'un GET minimal (``loadhttpgetJson``). Ce plugin le
remplace par une formalisation **déclarative** de l'appel, suivant la convention
Fetch / ``RequestInit`` (le vocabulaire HTTP-en-JSON standard) :

* ``http(request)`` — ``request`` est un objet
  ``{method, url, headers, query, body, timeout}`` ; renvoie un objet réponse
  ``{status, headers, body}`` (``body`` = JSON parsé si la réponse est du JSON,
  sinon le texte brut).
* ``httpget(url, headers)`` — convenance GET renvoyant directement le ``body``.
* ``loadhttpgetjson(root_path, method_name)`` — compatibilité avec le GET .NET,
  pour les templates existants.

Client HTTP : `httpx`. Le corps (``body``) est envoyé en JSON si c'est un objet ou
un tableau, sinon tel quel.

Sécurité : ``http`` réalise de **vraies requêtes réseau** vers l'URL fournie.
Attention aux URL issues de données non fiables (SSRF). Un ``timeout`` par défaut
(30 s) est appliqué et surchargeable par requête.

Découvert automatiquement par ``jslt`` via l'entry point ``urban_json.functions``.
"""

from __future__ import annotations

from typing import Any

import httpx

__version__ = "0.2.1"

__all__ = ["execute_http", "execute_httpget", "execute_loadhttpgetjson", "register"]

#: Timeout par défaut (secondes) si la requête n'en précise pas.
DEFAULT_TIMEOUT = 30.0


def _build_client(timeout: float) -> httpx.Client:
    """Fabrique le client HTTP. Point d'injection pour les tests (transport mocké)."""
    return httpx.Client(timeout=timeout)


def _parse_body(response: httpx.Response) -> Any:
    """Corps de réponse : JSON parsé si le content-type est JSON, sinon texte."""
    content_type = response.headers.get("content-type", "")
    if "json" in content_type.lower():
        try:
            return response.json()
        except ValueError:
            return response.text
    return response.text


def execute_http(ctx: Any, request: Any = None) -> dict:
    """Effectue un appel HTTP décrit par un objet Fetch/``RequestInit``.

    Args:
        request: objet ``{method, url, headers, query, body, timeout}``.
            ``method`` défaut ``GET`` ; ``headers``/``query`` sont des objets ;
            ``body`` est envoyé en JSON si objet/tableau, sinon tel quel.

    Returns:
        ``{"status": int, "headers": {...}, "body": <json|texte>}``.
    """
    if not isinstance(request, dict):
        # ValueError (et non TypeError) : contrat « mauvais argument » uniforme.
        raise ValueError("http: request doit être un objet {method, url, ...}")  # noqa: TRY004
    url = request.get("url")
    if not url:
        raise ValueError("http: 'url' est requis")

    method = str(request.get("method") or "GET").upper()
    headers = {str(k): str(v) for k, v in (request.get("headers") or {}).items()}
    params = request.get("query") or {}
    body = request.get("body")
    timeout = request.get("timeout", DEFAULT_TIMEOUT)

    kwargs: dict[str, Any] = {"headers": headers, "params": params}
    if isinstance(body, (dict, list)):
        kwargs["json"] = body
    elif body is not None:
        kwargs["content"] = body if isinstance(body, (str, bytes)) else str(body)

    with _build_client(timeout) as client:
        response = client.request(method, url, **kwargs)

    return {
        "status": response.status_code,
        "headers": dict(response.headers),
        "body": _parse_body(response),
    }


def execute_httpget(ctx: Any, url: str | None = None, headers: Any = None) -> Any:
    """GET de convenance : renvoie directement le corps (port « amélioré » du .NET)."""
    response = execute_http(ctx, {"method": "GET", "url": url, "headers": headers or {}})
    return response["body"]


def execute_loadhttpgetjson(ctx: Any, root_path: Any = None, method_name: Any = None) -> Any:
    """Compatibilité .NET (``loadhttpgetJson``) : GET de ``root_path`` + ``method_name``.

    Comme le .NET (``HttpClient.BaseAddress`` + chemin relatif, ``Accept:
    application/json``) : la réponse est lue en JSON quel que soit son
    content-type ; échec HTTP ou corps non JSON -> ``null`` (le .NET émettait un
    avertissement) ; hôte injoignable ou délai dépassé -> ``JsltError`` (le .NET
    levait). Pour un appel complet, préférer ``http`` / ``httpget``.
    """
    from urllib.parse import urljoin

    from urban_json import JsltError

    if not root_path:
        raise JsltError("loadhttpgetjson : l'URL de base (root_path) est requise")
    url = urljoin(str(root_path), str(method_name or ""))
    try:
        with _build_client(DEFAULT_TIMEOUT) as client:
            response = client.get(url, headers={"Accept": "application/json"})
    except httpx.TransportError as exc:
        # Hôte injoignable, délai dépassé… : le .NET levait aussi (seuls un statut
        # d'erreur et un corps non JSON donnent null) ; ici, une erreur lisible.
        raise JsltError(f"loadhttpgetjson : appel impossible vers {url!r} ({exc})") from exc
    if not response.is_success:
        return None
    try:
        return response.json()
    except ValueError:
        return None


def register(registry: Any) -> None:
    """Enregistre les fonctions du plugin dans un registre jslt (entry point)."""
    registry.register(
        "http",
        execute_http,
        description="Appel HTTP (objet Fetch {method,url,headers,query,body}) -> {status,headers,body}.",
    )
    registry.register(
        "httpget",
        execute_httpget,
        description="GET HTTP renvoyant directement le corps (JSON parsé ou texte).",
    )
    registry.register(
        "loadhttpgetjson",
        execute_loadhttpgetjson,
        description="GET JSON sur une URL de base + un chemin (compatibilité .NET) ; null en cas d'échec.",
    )
