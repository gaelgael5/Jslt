"""Plugin jslt : recherche Elasticsearch (``esconnect`` / ``essearch``).

Deux fonctions de template, dans l'esprit du couple ``connectsql`` / ``readsql`` :

* ``esconnect(hosts, api_key, username, password, verify_certs)`` → descripteur de
  connexion (à stocker dans une variable) ;
* ``essearch(connection, index, query, size)`` → liste des documents trouvés
  (le ``_source`` de chaque hit).

Client : `elasticsearch` (client officiel). Importé **paresseusement** pour que la
découverte/introspection du plugin ne force pas l'import du client.

Découvert automatiquement par ``jslt`` via l'entry point ``urban_json.functions``.
"""

from __future__ import annotations

from typing import Any

__version__ = "0.1.1"

__all__ = ["execute_esconnect", "execute_essearch", "register"]


def _build_client(connection: dict) -> Any:
    """Construit le client Elasticsearch depuis un descripteur. Point d'injection (tests)."""
    from elasticsearch import Elasticsearch

    kwargs: dict[str, Any] = {"hosts": connection.get("hosts")}
    if connection.get("api_key"):
        kwargs["api_key"] = connection["api_key"]
    if connection.get("basic_auth"):
        kwargs["basic_auth"] = tuple(connection["basic_auth"])
    if "verify_certs" in connection:
        kwargs["verify_certs"] = connection["verify_certs"]
    return Elasticsearch(**kwargs)


def execute_esconnect(
    ctx: Any,
    hosts: Any = None,
    api_key: str | None = None,
    username: str | None = None,
    password: str | None = None,
    verify_certs: bool = True,
) -> dict:
    """Crée un descripteur de connexion Elasticsearch (port esprit ``connectsql``).

    Args:
        hosts: URL (ou liste d'URL) du/des nœud(s) Elasticsearch.
        api_key: clé d'API (optionnelle).
        username / password: authentification basique (optionnelle).
        verify_certs: vérifie les certificats TLS (défaut ``True``).

    Returns:
        Un descripteur à passer à :func:`execute_essearch`.
    """
    if not hosts:
        raise ValueError("esconnect: hosts est requis")
    descriptor: dict[str, Any] = {"hosts": hosts, "verify_certs": verify_certs}
    if api_key:
        descriptor["api_key"] = api_key
    if username is not None and password is not None:
        descriptor["basic_auth"] = [username, password]
    return descriptor


def execute_essearch(
    ctx: Any,
    connection: Any = None,
    index: str | None = None,
    query: Any = None,
    size: int | None = None,
) -> list:
    """Exécute une recherche et renvoie les documents (``_source`` des hits).

    Args:
        connection: descripteur issu de :func:`execute_esconnect`.
        index: index (ou motif d'index) à interroger.
        query: clause de requête (DSL Elasticsearch) ; ``match_all`` si absente.
        size: nombre maximum de résultats (défaut du serveur si absent).

    Returns:
        La liste des ``_source`` des documents trouvés.
    """
    if not isinstance(connection, dict) or "hosts" not in connection:
        raise ValueError("essearch: connection doit être le descripteur de esconnect")
    if not index:
        raise ValueError("essearch: index est requis")

    search_kwargs: dict[str, Any] = {"index": index, "query": query or {"match_all": {}}}
    if size is not None:
        search_kwargs["size"] = size

    client = _build_client(connection)
    response = client.search(**search_kwargs)
    hits = response["hits"]["hits"]
    return [hit.get("_source") for hit in hits]


def register(registry: Any) -> None:
    """Enregistre les fonctions du plugin dans un registre jslt (entry point)."""
    registry.register(
        "esconnect",
        execute_esconnect,
        description="Crée un descripteur de connexion Elasticsearch.",
    )
    registry.register(
        "essearch",
        execute_essearch,
        description="Recherche Elasticsearch -> liste des documents (_source des hits).",
    )
