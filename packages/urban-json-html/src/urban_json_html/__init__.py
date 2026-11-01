"""Plugin urban-json : conversion HTML vers JSON (``loadhtml``).

Port de ``ServiceHtml`` / ``HtmlToJson`` (.NET, HtmlAgilityPack) avec le
``html.parser`` de la bibliothèque standard, sans dépendance. Forme produite,
identique au .NET :

* élément -> ``{"#id": balise, <attributs>…, "content": enfant | [enfants]}``
  (``content`` absent sans enfant, valeur seule pour un enfant unique) ;
* texte -> ``"#text: <texte brut>"``, ignoré s'il n'est fait que de blancs ;
* commentaire et ``<!DOCTYPE>`` -> ``"#comment: <!-- … -->"`` (HtmlAgilityPack
  range la déclaration DOCTYPE parmi les commentaires) ;
* racine -> ``{"#id": "#document", …}``.

Comme HtmlAgilityPack, le texte garde ses entités telles quelles (``&amp;``) et
la casse d'origine des balises est conservée. Écarts : les noms d'attributs sont
mis en minuscules et leurs valeurs décodées (``html.parser`` le fait toujours) ;
un chemin relatif est accepté (le .NET exigeait un chemin absolu ou une URI).

Découvert automatiquement via l'entry point ``urban_json.functions``.
"""

from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import unquote, urlparse

from urban_json import JsltError

__version__ = "0.1.1"

__all__ = ["execute_loadhtml", "html_to_json", "register"]

#: Délai maximal (secondes) pour charger une page distante.
DEFAULT_TIMEOUT = 30.0

# Éléments HTML sans contenu ni balise fermante.
_VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr",
}
_TAG_NAME = re.compile(r"<\s*([^\s/>]+)")


class _Node:
    __slots__ = ("attrs", "children", "name")

    def __init__(self, name: str, attrs: list[tuple[str, str | None]]) -> None:
        self.name = name
        self.attrs = attrs
        self.children: list[Any] = []


class _TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = _Node("#document", [])
        self.stack = [self.root]

    def _append(self, item: Any) -> None:
        self.stack[-1].children.append(item)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        raw = self.get_starttag_text() or ""
        match = _TAG_NAME.match(raw)
        node = _Node(match.group(1) if match else tag, attrs)
        self._append(node)
        if tag not in _VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        raw = self.get_starttag_text() or ""
        match = _TAG_NAME.match(raw)
        self._append(_Node(match.group(1) if match else tag, attrs))

    def handle_endtag(self, tag: str) -> None:
        # Ferme jusqu'à la balise ouverte correspondante ; une fermante orpheline est ignorée.
        for depth in range(len(self.stack) - 1, 0, -1):
            if self.stack[depth].name.lower() == tag:
                del self.stack[depth:]
                return

    def handle_data(self, data: str) -> None:
        self._append(("#text", data))

    def handle_entityref(self, name: str) -> None:
        self._append(("#text", f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self._append(("#text", f"&#{name};"))

    def handle_comment(self, data: str) -> None:
        self._append(("#comment", f"<!--{data}-->"))

    def handle_decl(self, decl: str) -> None:
        self._append(("#comment", f"<!{decl}>"))


def _merge_text(children: list[Any]) -> list[Any]:
    """Recolle les morceaux de texte consécutifs (le parseur coupe sur les entités)."""
    merged: list[Any] = []
    for child in children:
        if isinstance(child, tuple) and child[0] == "#text" and merged and isinstance(merged[-1], tuple) \
                and merged[-1][0] == "#text":
            merged[-1] = ("#text", merged[-1][1] + child[1])
        else:
            merged.append(child)
    return merged


def _to_json(item: Any) -> Any:
    if isinstance(item, tuple):
        kind, text = item
        return f"{kind}: {text}" if text.strip() else None
    result: dict[str, Any] = {"#id": item.name}
    for name, value in item.attrs:
        result.setdefault(name, value if value is not None else "")
    children = [c for c in (_to_json(child) for child in _merge_text(item.children)) if c is not None]
    if len(children) == 1:
        result["content"] = children[0]
    elif children:
        result["content"] = children
    return result


def html_to_json(payload: str) -> dict:
    """Convertit un texte HTML en JSON (forme ``HtmlToJson`` du .NET)."""
    builder = _TreeBuilder()
    builder.feed(payload)
    builder.close()
    return _to_json(builder.root)


def _fetch_url(url: str) -> str:
    """Charge une page distante. Point d'injection pour les tests."""
    from urllib.request import Request, urlopen

    request = Request(url, headers={"User-Agent": "urban-json-html"})
    with urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def execute_loadhtml(ctx: Any, path: Any = None) -> dict:
    if not path:
        raise JsltError("loadhtml : le chemin ou l'URL de la page est requis")
    location = str(path)
    parsed = urlparse(location)
    if parsed.scheme in ("http", "https"):
        return html_to_json(_fetch_url(location))
    file_path = unquote(parsed.path) if parsed.scheme == "file" else location
    if not os.path.isfile(file_path):
        raise JsltError(f"loadhtml : page HTML introuvable {file_path!r}")
    with open(file_path, encoding="utf-8-sig", errors="replace") as handle:
        return html_to_json(handle.read())


def register(registry: Any) -> None:
    """Enregistre ``loadhtml``."""
    registry.register(
        "loadhtml",
        execute_loadhtml,
        description="Charge une page HTML (fichier ou URL http/https) et la convertit en JSON {#id, attributs, content}",
    )
