"""Plugin jslt : lecture en base de données SQL (``connectsql`` / ``readsql``).

Port de ``Bb.Jslt.Services.Sql.ServicesSql`` (.NET), déjà un assembly séparé côté
.NET. Deux fonctions de template :

* ``connectsql(client, connection)`` → descripteur de connexion
  ``{"client": ..., "connection": ...}`` (à stocker dans une variable) ;
* ``readsql(connection, sql)`` → exécute la requête et renvoie un tableau de
  lignes ; chaque ligne est un objet ``{"$_line": n, <colonnes...>}`` (noms de
  colonnes assainis, comme en .NET).

Le .NET s'appuie sur ``DbProviderFactory`` (clé ``client``). Le portage utilise un
**registre de clients DB-API 2.0** : ``sqlite`` est fourni (stdlib, sans
dépendance). D'autres SGBD s'ajoutent via :func:`register_client` ou en extras
(PostgreSQL, MySQL…).

Sécurité : ``readsql`` exécute la requête SQL **telle quelle**. Ne construis pas la
requête par concaténation de données non fiables (risque d'injection) ; le contenu
de ``sql`` est sous la responsabilité de l'auteur du template.

Découvert automatiquement par ``jslt`` via l'entry point ``urban_json.functions``.
"""

from __future__ import annotations

import sqlite3
import unicodedata
from collections.abc import Callable
from typing import Any

__version__ = "0.1.0"

__all__ = ["execute_connectsql", "execute_readsql", "register", "register_client"]

#: Connexion DB-API 2.0 : une callable ``(connection_string) -> connection``.
DbConnector = Callable[[str], Any]

#: Registre des clients SQL (clé insensible à la casse) -> connecteur DB-API.
_CLIENTS: dict[str, DbConnector] = {}


def register_client(name: str, connector: DbConnector) -> None:
    """Enregistre un client SQL (ex. ``register_client("postgresql", psycopg.connect)``).

    ``connector`` reçoit la chaîne de connexion et renvoie une connexion DB-API 2.0.
    """
    _CLIENTS[name.lower()] = connector


# Client intégré : SQLite (stdlib). Alias usuels, dont la forme « .NET-like ».
register_client("sqlite", sqlite3.connect)
register_client("sqlite3", sqlite3.connect)
register_client("system.data.sqlite", sqlite3.connect)


def _sanitize(name: str) -> str:
    """Assainit un nom de colonne (même logique que urban-json-csv / ``ServiceCsv.GetLabel``)."""
    decomposed = unicodedata.normalize("NFKD", name)
    out: list[str] = []
    for char in decomposed:
        if unicodedata.combining(char):
            continue
        if char.isascii() and char.isalnum():
            out.append(char)
        elif char in (" ", "'", '"'):
            out.append("_")
    label = "".join(out)
    while "___" in label:
        label = label.replace("___", "_")
    return label.replace("__", "_")


def execute_connectsql(
    ctx: Any, client: str | None = None, connection: str | None = None
) -> dict:
    """Crée un descripteur de connexion SQL (port de ``connectsql``).

    Args:
        client: clé du client SQL (``sqlite``, ou un client enregistré).
        connection: chaîne de connexion (pour SQLite : chemin du fichier ``.db``).

    Returns:
        Un descripteur ``{"client": client, "connection": connection}`` à passer à
        :func:`execute_readsql` (typiquement via une variable de template).
    """
    if not client:
        raise ValueError("connectsql: client est requis")
    if client.lower() not in _CLIENTS:
        raise ValueError(
            f"connectsql: client '{client}' inconnu. Clients disponibles : "
            f"{', '.join(sorted(_CLIENTS))}"
        )
    return {"client": client, "connection": connection}


def execute_readsql(ctx: Any, connection: Any = None, sql: str | None = None) -> list:
    """Exécute une requête SQL et renvoie les lignes (port de ``readsql``).

    Args:
        connection: descripteur issu de :func:`execute_connectsql`.
        sql: requête SQL à exécuter.

    Returns:
        La liste des lignes, chacune ``{"$_line": n, <colonne>: <valeur>, ...}``.
    """
    if not isinstance(connection, dict) or "client" not in connection:
        raise ValueError("readsql: connection doit être le descripteur de connectsql")
    if not sql:
        raise ValueError("readsql: sql est requis")

    client = connection["client"]
    connector = _CLIENTS.get(str(client).lower())
    if connector is None:
        raise ValueError(f"readsql: client '{client}' inconnu")

    conn = connector(connection.get("connection"))
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        if cursor.description is None:  # requête sans jeu de résultats
            return []
        columns = [_sanitize(col[0]) for col in cursor.description]
        rows: list[dict] = []
        for line, record in enumerate(cursor.fetchall(), start=1):
            obj: dict[str, Any] = {"$_line": line}
            for name, value in zip(columns, record):
                obj[name] = value
            rows.append(obj)
        return rows
    finally:
        conn.close()


def register(registry: Any) -> None:
    """Enregistre les fonctions du plugin dans un registre jslt (entry point)."""
    registry.register(
        "connectsql",
        execute_connectsql,
        description="Crée un descripteur de connexion SQL (client + chaîne de connexion).",
    )
    registry.register(
        "readsql",
        execute_readsql,
        description="Exécute une requête SQL et renvoie les lignes (tableau d'objets).",
    )
