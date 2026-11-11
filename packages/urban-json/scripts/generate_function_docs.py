#!/usr/bin/env python3
"""Engendre une page de référence par fonction, dans les deux langues.

Pourquoi une page par fonction plutôt que des ancres dans les chapitres :
l'éditeur (`<jslt-editor>`) lie l'infobulle d'intellisense à la documentation,
et une ancre se casse en silence au premier titre renommé — le lecteur tombe
alors en haut d'un chapitre de mille lignes. Un fichier par fonction donne une
URL stable, dérivable du seul nom (`docs/fonctions/<nom>.md`, `.en.md` pour
l'anglais), ce qui est exactement ce dont le composant dispose.

Les pages sont **engendrées** depuis le registre : la description, la signature
et les arguments y vivent déjà, et une recopie à la main aurait vieilli dès la
première signature élargie. La prose et les exemples restent dans les chapitres,
vers lesquels chaque page renvoie.

Usage : ``python packages/urban-json/scripts/generate_function_docs.py``
(``--check`` se contente de dire ce qui n'est pas à jour, c'est ce que fait le
test ``test_function_docs.py``).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

#: Chapitre d'où chaque module de fonctions tire sa prose et ses exemples.
#: Clé = nom du module ``urban_json.functions.*``, valeur = (fichier, titre FR, titre EN).
THEMES: dict[str, tuple[str, str, str]] = {
    "builtins": ("collections", "Données et collections", "Data and collections"),
    "collection": ("collections", "Données et collections", "Data and collections"),
    "ordering": ("collections", "Données et collections", "Data and collections"),
    "aggregate": ("collections", "Données et collections", "Data and collections"),
    "bykey": ("collections", "Données et collections", "Data and collections"),
    "grouping": ("collections", "Données et collections", "Data and collections"),
    "objects": ("objets", "Objets et structures profondes", "Objects and deep structures"),
    "deep": ("objets", "Objets et structures profondes", "Objects and deep structures"),
    "types": ("types", "Types, repli sur erreur et validation", "Types, error fallback and validation"),
    "schema": ("types", "Types, repli sur erreur et validation", "Types, error fallback and validation"),
    "maths": ("nombres", "Nombres et maths", "Numbers and maths"),
    "numbers": ("nombres", "Nombres et maths", "Numbers and maths"),
    "text": ("texte", "Texte, expressions régulières et formatage", "Text, regular expressions and formatting"),
    "folding": ("texte", "Texte, expressions régulières et formatage", "Text, regular expressions and formatting"),
    "similarity": ("texte", "Texte, expressions régulières et formatage", "Text, regular expressions and formatting"),
    "regexes": ("texte", "Texte, expressions régulières et formatage", "Text, regular expressions and formatting"),
    "formatting": ("texte", "Texte, expressions régulières et formatage", "Text, regular expressions and formatting"),
    "encoding": ("encodage", "Encodage, empreintes et échappement", "Encoding, digests and escaping"),
    "dates": ("dates", "Dates et heures", "Dates and times"),
    "outputs": ("sortie", "Sortie texte", "Text output"),
    "quality": ("qualite", "Qualité : refuser, observer, valider", "Quality: refuse, observe, validate"),
}

#: Fonctions dont le chapitre n'est pas celui de leur module (``misc`` mélange
#: des familles : un réglage externe, une horloge, deux tests de nullité).
OVERRIDES: dict[str, tuple[str, str, str]] = {
    "param": ("expressions", "Expressions et opérateurs", "Expressions and operators"),
    "params": ("expressions", "Expressions et opérateurs", "Expressions and operators"),
    "uuid": ("expressions", "Expressions et opérateurs", "Expressions and operators"),
    "now": ("dates", "Dates et heures", "Dates and times"),
    "isnull": ("types", "Types, repli sur erreur et validation", "Types, error fallback and validation"),
    "isnotnull": ("types", "Types, repli sur erreur et validation", "Types, error fallback and validation"),
}

GENERATED = (
    "<!-- Page engendrée par packages/urban-json/scripts/generate_function_docs.py. "
    "Modifier la description dans le registre, pas ici. -->"
)

LABELS = {
    "fr": {
        "params": "| Paramètre | Attendu | Note |",
        "required": "requis",
        "optional": "optionnel",
        "path": "chemin JSONPath **non évalué**",
        "lazy": "expression **non évaluée**, calculée par la fonction",
        "variadic": "autant d'arguments que voulu",
        "output": (
            "Fonction de **sortie** : elle ne s'appelle pas dans le corps du template, "
            "mais se déclare dans `\"$directives\": {\"output\": {\"mode\": …}}`."
        ),
        "no_params": "Cette fonction ne prend aucun argument.",
        "chapter": "**Chapitre** :",
        "index": "**Index** : [toutes les fonctions](sommaire.md)",
        "back": "[← Guide jslt](../guide.md)",
        "banner": "*Français · [English]({name}.en.md)*",
    },
    "en": {
        "params": "| Parameter | Expected | Note |",
        "required": "required",
        "optional": "optional",
        "path": "**unevaluated** JSONPath path",
        "lazy": "**unevaluated** expression, computed by the function",
        "variadic": "as many arguments as wanted",
        "output": (
            "An **output** function: it is not called in the template body, it is declared "
            "in `\"$directives\": {\"output\": {\"mode\": …}}`."
        ),
        "no_params": "This function takes no argument.",
        "chapter": "**Chapter**:",
        "index": "**Index**: [all functions](sommaire.en.md)",
        "back": "[← jslt guide](../guide.en.md)",
        "banner": "*[Français]({name}.md) · English*",
    },
}


def theme_of(info: Any) -> tuple[str, str, str]:
    """Chapitre d'une fonction. Lève si elle n'en a pas : une page orpheline
    renverrait le lecteur nulle part, et c'est le genre de trou qu'on ne voit
    jamais en relisant 182 pages."""
    if info.name.lower() in OVERRIDES:
        return OVERRIDES[info.name.lower()]
    module = (getattr(info.function, "__module__", "") or "").rsplit(".", 1)[-1]
    if module not in THEMES:
        raise SystemExit(
            f"aucun chapitre pour {info.name} (module {module!r}) : "
            f"compléter THEMES dans {Path(__file__).name}"
        )
    return THEMES[module]


def _notes(info: Any, index: int, param: Any, labels: dict[str, str]) -> str:
    notes = []
    if param.variadic:
        notes.append(labels["variadic"])
    if index in info.path_args:
        notes.append(labels["path"])
    if index in info.lazy_args:
        notes.append(labels["lazy"])
    return " · ".join(notes)


def render_page(info: Any, lang: str) -> str:
    labels = LABELS[lang]
    chapter, title_fr, title_en = theme_of(info)
    chapter_file = f"{chapter}.md" if lang == "fr" else f"{chapter}.en.md"
    chapter_title = title_fr if lang == "fr" else title_en
    description = info.description_en if lang == "en" and info.description_en else info.description

    lines = [GENERATED, "", f"# `{info.name}`", "", labels["banner"].format(name=info.name.lower()), ""]
    lines += [description, "", "```", info.signature(), "```", ""]
    if info.parameters:
        lines += [labels["params"], "|---|---|---|"]
        for index, param in enumerate(info.parameters):
            expected = labels["required"] if param.required else labels["optional"]
            lines.append(f"| `{param.name}` | {expected} | {_notes(info, index, param, labels)} |")
        lines.append("")
    else:
        lines += [labels["no_params"], ""]
    if info.kind == "output":
        lines += [labels["output"], ""]
    lines += [
        f"{labels['chapter']} [{chapter_title}](../{chapter_file}) · {labels['index']}",
        "",
        "---",
        "",
        labels["back"],
        "",
    ]
    return "\n".join(lines)


def render_index(infos: list[Any], lang: str) -> str:
    """Index par chapitre : la seule page que l'on parcourt des yeux."""
    labels = LABELS[lang]
    title = "Référence des fonctions" if lang == "fr" else "Function reference"
    intro = (
        "Une page par fonction, engendrée depuis le registre : signature, arguments et "
        "description. La prose et les exemples vivent dans les chapitres du guide."
        if lang == "fr"
        else "One page per function, generated from the registry: signature, arguments and "
        "description. The prose and the examples live in the guide's chapters."
    )
    banner = "*Français · [English](sommaire.en.md)*" if lang == "fr" else "*[Français](sommaire.md) · English*"
    header = "| Fonction | Description |" if lang == "fr" else "| Function | Description |"
    lines = [GENERATED, "", f"# {title}", "", banner, "", intro, ""]
    by_chapter: dict[tuple[str, str], list[Any]] = {}
    for info in infos:
        chapter, title_fr, title_en = theme_of(info)
        by_chapter.setdefault((chapter, title_fr if lang == "fr" else title_en), []).append(info)
    for (chapter, chapter_title), group in sorted(by_chapter.items(), key=lambda item: item[0][1]):
        chapter_file = f"{chapter}.md" if lang == "fr" else f"{chapter}.en.md"
        lines += [f"## [{chapter_title}](../{chapter_file})", "", header, "|---|---|"]
        for info in group:
            page = f"{info.name.lower()}.md" if lang == "fr" else f"{info.name.lower()}.en.md"
            text = info.description_en if lang == "en" and info.description_en else info.description
            # Une description qui contient une barre couperait la cellule en deux.
            escaped = text.replace("|", "\\|")
            lines.append(f"| [`{info.name}`]({page}) | {escaped} |")
        lines.append("")
    lines += ["---", "", labels["back"], ""]
    return "\n".join(lines)


def is_core(info: Any) -> bool:
    """Fonction du cœur, donc documentée ici.

    Au module et non au registre : un plugin installé dans l'environnement
    (``urban-json-csv``…) se retrouve dans le registre global, et ses pages
    n'ont rien à faire dans ce dépôt — sa documentation est la sienne.
    """
    module = getattr(info.function, "__module__", "") or ""
    return module == "urban_json.functions" or module.startswith("urban_json.functions.")


def core_functions() -> list[Any]:
    from urban_json.functions import default_registry

    return [info for info in default_registry.describe_all() if is_core(info)]


def expected_pages() -> dict[str, str]:
    """Contenu attendu de ``docs/fonctions/``, par nom de fichier."""
    infos = core_functions()
    # L'index ne s'appelle pas `index` : c'est déjà le nom d'une fonction, et sa
    # page écraserait silencieusement le sommaire (le défaut a existé).
    pages = {"sommaire.md": render_index(infos, "fr"), "sommaire.en.md": render_index(infos, "en")}
    for info in infos:
        for name in (f"{info.name.lower()}.md", f"{info.name.lower()}.en.md"):
            if name in pages:
                raise SystemExit(f"collision de nom de page : {name}")
        pages[f"{info.name.lower()}.md"] = render_page(info, "fr")
        pages[f"{info.name.lower()}.en.md"] = render_page(info, "en")
    return pages


def docs_dir() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "docs" / "guide.md").is_file():
            return parent / "docs" / "fonctions"
    raise SystemExit("docs/ introuvable : exécuter depuis le dépôt")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="ne rien écrire, dire ce qui diffère")
    args = parser.parse_args()
    target = docs_dir()
    pages = expected_pages()
    target.mkdir(parents=True, exist_ok=True)
    stale = [name for name, text in pages.items() if not (target / name).is_file() or (target / name).read_text(encoding="utf-8") != text]
    extra = [path.name for path in target.glob("*.md") if path.name not in pages]
    if args.check:
        for name in sorted(stale):
            print(f"à régénérer : {name}")
        for name in sorted(extra):
            print(f"en trop : {name}")
        return 1 if stale or extra else 0
    for name in stale:
        (target / name).write_text(pages[name], encoding="utf-8")
    for name in extra:
        (target / name).unlink()
    print(f"{len(pages)} pages ({len(stale)} écrites, {len(extra)} retirées) dans {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
