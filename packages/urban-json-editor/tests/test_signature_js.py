"""Aide à la signature : la suite node, lancée depuis pytest.

Même dispositif que `test_paths_js.py` : la logique qui décide *quel appel* et
*quel paramètre* est pure, donc éprouvée sous node ; ce qui relève du DOM est
vérifié ici sur la source du composant, faute de navigateur dans la boucle.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

import urban_json_editor

TESTS_DIR = Path(__file__).resolve().parent


def editor_source() -> str:
    return (urban_json_editor.assets_dir() / "jslt-editor.js").read_text(encoding="utf-8")


def test_component_imports_signature_module() -> None:
    assert "jslt-signature.js" in urban_json_editor.ASSET_FILES
    assert './jslt-signature.js"' in editor_source()


def test_signature_follows_the_caret_not_only_the_typing() -> None:
    """Clic et flèches déplacent le caret sans produire d'`input`.

    Sans ces écoutes, revenir dans les parenthèses d'un appel déjà écrit
    laisserait l'aide fermée — c'est le geste de qui corrige un argument.
    """
    js = editor_source()
    assert 'addEventListener("click", () => this._maybeOpenSig())' in js
    assert 'addEventListener("keyup"' in js
    assert 'e.key.startsWith("Arrow")' in js


def test_signature_marks_the_parameter_being_typed() -> None:
    js = editor_source()
    assert "signatureSegments(fn, context.argIndex)" in js
    assert 'jslt-sig-param${seg.active ? " active" : ""}' in js
    css = (urban_json_editor.assets_dir() / "jslt-editor.css").read_text(encoding="utf-8")
    assert ".jslt-sig-param.active" in css
    assert "font-weight: 700" in css


def test_signature_links_to_the_documentation_in_a_new_tab() -> None:
    js = editor_source()
    assert "docUrlFor(fn, lang, this.getAttribute(\"docs-base\"))" in js
    assert 'target="_blank"' in js and 'rel="noopener noreferrer"' in js


def test_clicking_the_tooltip_does_not_blur_the_editor() -> None:
    """Le flou referme la boîte après 120 ms : le clic n'atteindrait jamais le lien."""
    js = editor_source()
    assert 'this._sigEl.addEventListener("mousedown", (e) => e.preventDefault());' in js


def test_signature_and_completion_list_can_be_open_together() -> None:
    """Saisir un argument ouvre la liste des chemins — et c'est précisément là
    qu'on veut savoir quel paramètre on remplit. L'aide se pose donc au-dessus
    de la ligne, la liste en dessous."""
    js = editor_source()
    assert "this._positionBox(this._sigEl, context.open, true);" in js
    assert "const lifted = top - lineHeight - el.offsetHeight;" in js
    assert "if (this._ac.open) return this._closeSig();" not in js


@pytest.mark.skipif(shutil.which("node") is None, reason="node absent")
def test_signature_suite_passes() -> None:
    node = shutil.which("node")
    assert node is not None
    # Binaire résolu par shutil.which, arguments fixes : pas d'entrée externe.
    proc = subprocess.run(
        [node, "--test", str(TESTS_DIR / "signature.test.mjs")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_box_that_sets_display_can_still_be_hidden() -> None:
    """`display: flex` sur la boîte l'emportait sur le `[hidden]` du navigateur.

    Spécificité : `jslt-editor .jslt-sig` (0,1,1) bat le `[hidden] {display:none}`
    de la feuille de l'agent, donc une fois affichée, l'aide ne se refermait
    **jamais** — le JS la masquait pourtant, et c'est ce qui rend le défaut
    difficile à voir depuis le code. Toute boîte qui pose `display` doit donc
    poser aussi sa règle `[hidden]`.
    """
    css = (urban_json_editor.assets_dir() / "jslt-editor.css").read_text(encoding="utf-8")
    rules = re.findall(r"([^{}]+)\{([^{}]*)\}", css)
    boxes = {".jslt-ac", ".jslt-sig", ".jslt-hint"}
    sets_display = {
        box
        for selector, body in rules
        for box in boxes
        if selector.strip().endswith(box) and "display:" in body
    }
    hidden = {
        box
        for selector, body in rules
        for box in boxes
        if f"{box}[hidden]" in selector and "display: none" in body
    }
    assert sets_display <= hidden, (
        "boîtes qui posent `display` sans règle `[hidden]`, donc impossibles à "
        f"masquer : {sorted(sets_display - hidden)}"
    )
