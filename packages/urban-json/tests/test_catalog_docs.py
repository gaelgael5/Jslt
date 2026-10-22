"""Le catalogue (aide de l'éditeur, playground) doit documenter chaque fonction :
une description lisible par un utilisateur de template, pas un renvoi au code .NET."""

from __future__ import annotations

import pytest

from urban_json import default_registry

CATALOG = default_registry.catalog()


@pytest.mark.parametrize("entry", CATALOG, ids=[e["name"] for e in CATALOG])
def test_chaque_fonction_a_une_description_utile(entry) -> None:
    description = (entry["description"] or "").strip()
    assert len(description) >= 15, f"{entry['name']} : description absente ou trop courte"
    assert "``" not in description, f"{entry['name']} : balisage RST dans la description"
    assert "port de" not in description.lower(), f"{entry['name']} : renvoi au .NET au lieu d'une description"
