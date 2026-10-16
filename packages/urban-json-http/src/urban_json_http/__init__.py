"""Plugin jslt : appels HTTP depuis les templates (``http`` / ``httpget``).

Le moteur .NET n'offre qu'un GET minimal (``loadhttpgetJson``). Ce plugin le
remplace par une formalisation **déclarative** de l'appel, suivant la convention
Fetch / ``RequestInit`` (le vocabulaire HTTP-en-JSON standard) :

* ``http(request)`` — ``request`` est un objet
  ``{method, url, headers, query, body, timeout}`` ; renvoie un objet réponse
  ``{status, headers, body}`` (``body`` = JSON parsé si la réponse est du JSON,
  sinon le texte brut).
* ``httpget(url, headers)`` — convenance GET renvoyant directement le ``body``.

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

__version__ = "0.0.1"

__all__ = ["execute_http", "execute_httpget", "register"]

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
