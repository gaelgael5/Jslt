"""Tests du composant jslt-editor (côté Python : assets + catalogue + montage)."""

from __future__ import annotations

from urban_json import FunctionRegistry

import urban_json_editor


def test_assets_present() -> None:
    directory = urban_json_editor.assets_dir()
    assert directory.is_dir()
    for name in urban_json_editor.ASSET_FILES:
        assert (directory / name).is_file()


def test_js_defines_custom_element() -> None:
    js = (urban_json_editor.assets_dir() / "jslt-editor.js").read_text(encoding="utf-8")
    assert 'customElements.define("jslt-editor"' in js


def test_hints_are_opt_in_and_overridable() -> None:
    """Les messages de diagnostic ne parlent que si l'hôte les demande.

    Un composant qui se met soudain à parler dans tous les projets qui
    l'utilisent serait une rupture : l'attribut `hints` est donc requis, et les
    textes sont surchargeables par code (le composant ne porte aucun i18n).
    """
    js = (urban_json_editor.assets_dir() / "jslt-editor.js").read_text(encoding="utf-8")
    assert 'hasAttribute("hints")' in js
    assert "setMessages(messages)" in js
    assert "this._hints = false;" in js  # silence par défaut
    paths = (urban_json_editor.assets_dir() / "jslt-paths.js").read_text(encoding="utf-8")
    assert "export const DEFAULT_HINT_MESSAGES" in paths
    css = (urban_json_editor.assets_dir() / "jslt-editor.css").read_text(encoding="utf-8")
    assert ".jslt-hint" in css


def test_catalog_default_registry() -> None:
    cat = urban_json_editor.catalog()
    names = {entry["name"] for entry in cat}
    assert "sum" in names and "distinct" in names
    # Chaque entrée porte de quoi alimenter l'intellisense.
    sample = next(e for e in cat if e["name"] == "distinct")
    assert "signature" in sample and "parameters" in sample


def test_catalog_custom_registry() -> None:
    reg = FunctionRegistry()
    reg.register("double", lambda ctx, x=None: x * 2, description="Double")
    cat = urban_json_editor.catalog(reg)
    assert [e["name"] for e in cat] == ["double"]


def test_mount_on_starlette(tmp_path) -> None:
    starlette = __import__("starlette.applications", fromlist=["Starlette"])
    app = starlette.Starlette()
    urban_json_editor.mount(app, "/jslt-editor")
    # Une route montée porte le chemin demandé.
    assert any(getattr(r, "path", "").startswith("/jslt-editor") for r in app.routes)
