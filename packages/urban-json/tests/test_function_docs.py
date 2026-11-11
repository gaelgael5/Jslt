"""Les pages de référence par fonction, et le lien que l'éditeur y pose.

L'infobulle d'intellisense de `<jslt-editor>` renvoie vers `docs/fonctions/<nom>`
dans la langue du lecteur. Trois choses doivent donc tenir ensemble, et aucune
ne se voit à la lecture : la page existe dans les deux langues, son contenu suit
le registre (elle est engendrée), et le catalogue pointe là où elle est.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from _docs import DOCS, NO_DOCS
from urban_json.functions import default_registry

pytestmark = pytest.mark.skipif(DOCS is None, reason=NO_DOCS)

GENERATOR = Path(__file__).resolve().parents[1] / "scripts" / "generate_function_docs.py"


def load_generator():
    """Le générateur est un script du dépôt, pas un module du paquet : il n'entre
    pas dans la distribution, et ces tests sautent alors avec les autres."""
    if not GENERATOR.is_file():
        pytest.skip("script de génération absent (exécution hors dépôt)")
    spec = importlib.util.spec_from_file_location("_generate_function_docs", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def pages_dir() -> Path:
    assert DOCS is not None
    return DOCS / "fonctions"


def core_names() -> list[str]:
    """Seules les fonctions du cœur : les plugins installés dans l'environnement
    de test (csv, xml, files…) sont documentés chez eux."""
    return [info.name for info in load_generator().core_functions()]


def test_every_function_has_its_two_pages() -> None:
    missing = []
    for name in core_names():
        for page in (f"{name.lower()}.md", f"{name.lower()}.en.md"):
            if not (pages_dir() / page).is_file():
                missing.append(page)
    assert not missing, f"pages absentes : {sorted(missing)}"


def test_pages_are_up_to_date_with_the_registry() -> None:
    """Engendrées, donc jamais « presque à jour ».

    Sans ce test, une signature élargie laisserait une page qui décrit l'ancienne
    — et c'est elle que lit l'utilisateur venu de l'éditeur.
    """
    expected = load_generator().expected_pages()
    stale = [
        name
        for name, text in expected.items()
        if not (pages_dir() / name).is_file()
        or (pages_dir() / name).read_text(encoding="utf-8") != text
    ]
    extra = [path.name for path in pages_dir().glob("*.md") if path.name not in expected]
    assert not stale and not extra, (
        "docs/fonctions/ n'est plus à jour : relancer "
        "`python packages/urban-json/scripts/generate_function_docs.py`\n"
        f"  à régénérer : {sorted(stale)}\n  en trop : {sorted(extra)}"
    )


def test_catalog_points_at_an_existing_page() -> None:
    # C'est ce champ que l'éditeur transforme en URL : un `doc` qui ne désigne
    # rien donnerait un lien mort dans l'infobulle.
    assert DOCS is not None
    core = {name.lower() for name in core_names()}
    for entry in default_registry.catalog():
        if entry["name"].lower() not in core:
            # Un plugin n'a pas de page ici : pas de `doc`, donc pas de lien.
            continue
        assert entry["doc"] == f"fonctions/{entry['name'].lower()}", entry["name"]
        assert (DOCS / f"{entry['doc']}.md").is_file()
        assert (DOCS / f"{entry['doc']}.en.md").is_file()


def test_every_function_is_described_in_both_languages() -> None:
    # La page anglaise n'a pas d'autre source que le registre.
    untranslated = [i.name for i in load_generator().core_functions() if not i.description_en]
    assert not untranslated, f"sans description anglaise : {untranslated}"


def test_every_function_has_a_chapter() -> None:
    """Chaque page renvoie vers la prose et les exemples de son chapitre.

    Le générateur lève sur une fonction sans chapitre ; ce test le dit ici, où on
    le lit, plutôt qu'au prochain `git` de celui qui ajoute un module.
    """
    generator = load_generator()
    for info in generator.core_functions():
        chapter, title_fr, title_en = generator.theme_of(info)
        assert DOCS is not None
        assert (DOCS / f"{chapter}.md").is_file(), (info.name, chapter)
        assert title_fr and title_en


def test_every_function_has_an_example() -> None:
    """Une page sans exemple n'aide pas : la signature seule ne dit ni ce qu'on
    met dedans, ni ce qui en sort. Les triplets eux-mêmes sont rejoués par la
    suite du guide, qui balaie `docs/fonctions/`."""
    examples = load_generator().EXAMPLES
    missing = [name for name in core_names() if name.lower() not in examples]
    assert not missing, f"fonctions sans exemple : {sorted(missing)}"


def test_output_examples_render_what_the_page_shows() -> None:
    """Les cinq fonctions de sortie ne s'appellent pas dans le corps du
    template : leur texte produit n'est pas un triplet, donc rien ne le
    vérifierait — sauf ici, en rejouant `render()`."""
    from urban_json import JsltTemplate

    checked = 0
    for name, items in load_generator().EXAMPLES.items():
        for example in items:
            if "render" not in example:
                continue
            template = JsltTemplate.parse(example["template"])
            assert template.render(json.loads(example["source"])) == example["render"], name
            checked += 1
    assert checked == 5, f"{checked} sorties vérifiées, 5 attendues"


def test_the_index_is_not_shadowed_by_a_function() -> None:
    # `index` est une fonction : son sommaire s'appelle donc `sommaire`.
    assert (pages_dir() / "sommaire.md").is_file()
    assert "index" in default_registry
