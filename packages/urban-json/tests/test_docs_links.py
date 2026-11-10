"""Les liens entre documents du guide ne doivent pas pendre dans le vide.

Le guide est découpé en une dizaine de documents thématiques, doublés en
anglais : les renvois croisés y sont nombreux et un titre renommé casse une
ancre sans que rien ne le signale. Un lecteur, lui, tombe sur le haut d'une page
au lieu de la section promise — défaut silencieux, donc défaut durable.
"""

from __future__ import annotations

import re

from _docs import DOCS

# Liens markdown hors blocs de code (un exemple jslt peut contenir des crochets).
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_HEADING_RE = re.compile(r"^#{1,6} (.*)$", re.MULTILINE)
_SLUG_DROP = re.compile(r"[^\w\s-]", re.UNICODE)


def _slug(text: str) -> str:
    """Ancre GitHub : minuscules, ponctuation retirée, espaces en tirets."""
    return _SLUG_DROP.sub("", text.strip().lower()).replace(" ", "-")


def _anchors(markdown: str) -> set[str]:
    return {_slug(title) for title in _HEADING_RE.findall(markdown)}


def _body(path) -> str:
    return _FENCE_RE.sub("", path.read_text(encoding="utf-8"))


def test_every_document_has_its_translation() -> None:
    # Convention du projet : français canonique, anglais côte à côte.
    french = {p.name for p in DOCS.glob("*.md") if not p.name.endswith(".en.md")}
    english = {p.name for p in DOCS.glob("*.en.md")}
    missing = {name for name in french if f"{name[:-3]}.en.md" not in english}
    assert not missing, f"documents sans version anglaise : {sorted(missing)}"


def test_documents_links_resolve() -> None:
    dangling: list[str] = []
    for path in sorted(DOCS.glob("*.md")):
        for link in _LINK_RE.findall(_body(path)):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            target, _, anchor = link.partition("#")
            page = path if not target else (path.parent / target).resolve()
            if not page.is_file():
                dangling.append(f"{path.name} -> {link} (fichier absent)")
                continue
            if anchor and anchor not in _anchors(page.read_text(encoding="utf-8")):
                dangling.append(f"{path.name} -> {link} (ancre absente)")
    assert not dangling, "liens cassés dans docs/ :\n  " + "\n  ".join(dangling)
