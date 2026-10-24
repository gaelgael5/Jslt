"""Complétion des chemins : la suite node, lancée depuis pytest.

La logique vit en JS (elle tourne dans le navigateur) mais elle est pure, donc
éprouvée sous node — et rattachée ici pour qu'un `pytest packages/...` ne la
laisse pas hors de la boucle de vérification.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

import urban_json_editor

TESTS_DIR = Path(__file__).resolve().parent


def test_component_imports_paths_module() -> None:
    """Le module de chemins doit être livré ET importé par le composant."""
    assert "jslt-paths.js" in urban_json_editor.ASSET_FILES
    js = (urban_json_editor.assets_dir() / "jslt-editor.js").read_text(encoding="utf-8")
    assert './jslt-paths.js"' in js


@pytest.mark.skipif(shutil.which("node") is None, reason="node absent")
def test_paths_suite_passes() -> None:
    node = shutil.which("node")
    assert node is not None
    # Binaire résolu par shutil.which, arguments fixes : pas d’entrée externe.
    proc = subprocess.run(
        [node, "--test", str(TESTS_DIR / "paths.test.mjs")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
