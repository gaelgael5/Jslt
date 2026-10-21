"""Plugin jslt : lecture de fichiers XML (``loadxml``).

Le moteur .NET n'expose pas de fonction de template ``loadxml`` mais convertit
XML ↔ JSON via le ``XmlNodeConverter`` (conventions Newtonsoft). Ce plugin porte
ces **mêmes conventions** sous forme d'une fonction ``loadxml`` :

* un élément devient un objet ;
* un attribut devient une propriété préfixée par ``@`` ;
* le texte d'un élément (s'il a aussi des attributs/enfants) va dans ``#text`` ;
  un élément qui n'a que du texte prend directement cette valeur (chaîne) ;
* des éléments frères de même nom deviennent un tableau ;
* l'élément racine est enveloppé : ``<root>…</root>`` → ``{"root": {…}}``.

Les valeurs restent des **chaînes** (comme Newtonsoft : pas de coercition de type).

Sécurité : le XML est analysé avec ``defusedxml`` (entités externes et expansion
d'entités désactivées — protection XXE / « billion laughs »).

Découvert automatiquement par ``jslt`` via l'entry point ``urban_json.functions``.
"""

from __future__ import annotations

from typing import Any

from defusedxml.ElementTree import parse as _parse

__version__ = "0.1.0"

__all__ = ["execute_loadxml", "register"]

# Clés spéciales, fidèles au XmlNodeConverter (.NET/Newtonsoft).
_TEXT_KEY = "#text"
_ATTR_PREFIX = "@"


def _local_name(tag: str, strip_namespaces: bool) -> str:
    """Nom local d'une balise/attribut ``{uri}local`` -> ``local`` (si demandé)."""
    if strip_namespaces and tag.startswith("{"):
        return tag.rsplit("}", 1)[-1]
    return tag


def _element_to_obj(
    element: Any, attribute_prefix: str, text_key: str, strip_namespaces: bool
) -> Any:
    """Convertit un élément ElementTree en structure JSON (conventions Newtonsoft)."""
    children = list(element)
    attributes = element.attrib
    text = (element.text or "").strip()

    # Feuille sans attribut ni enfant : la valeur texte directe (ou None si vide).
    if not children and not attributes:
        return text if text else None

    obj: dict[str, Any] = {}

    for name, value in attributes.items():
        obj[attribute_prefix + _local_name(name, strip_namespaces)] = value

    # Regroupe les enfants par nom : les frères homonymes forment un tableau.
    groups: dict[str, list[Any]] = {}
    order: list[str] = []
    for child in children:
        key = _local_name(child.tag, strip_namespaces)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(_element_to_obj(child, attribute_prefix, text_key, strip_namespaces))
    for key in order:
        values = groups[key]
        obj[key] = values[0] if len(values) == 1 else values

    if text:
        obj[text_key] = text

    return obj


def execute_loadxml(
    ctx: Any,
    source_path: str | None = None,
    attribute_prefix: str = _ATTR_PREFIX,
    text_key: str = _TEXT_KEY,
    strip_namespaces: bool = True,
) -> dict:
    """Lit un fichier XML et le convertit en JSON (conventions Newtonsoft).

    Args:
        source_path: chemin du fichier XML (absolu ou relatif au répertoire courant).
        attribute_prefix: préfixe des propriétés issues d'attributs (défaut ``@``).
        text_key: clé portant le texte d'un élément mixte (défaut ``#text``).
        strip_namespaces: réduit ``{uri}local`` au nom local (défaut ``True``).

    Returns:
        Un objet ``{nom_racine: contenu}`` reflétant l'arbre XML.
    """
    if not source_path:
        raise ValueError("loadxml: source_path est requis")

    tree = _parse(source_path)
    root = tree.getroot()
    return {
        _local_name(root.tag, strip_namespaces): _element_to_obj(
            root, attribute_prefix, text_key, strip_namespaces
        )
    }


def register(registry: Any) -> None:
    """Enregistre les fonctions du plugin dans un registre jslt (entry point)."""
    registry.register(
        "loadxml",
        execute_loadxml,
        description="Lit un fichier XML et le convertit en JSON (conventions Newtonsoft).",
    )
