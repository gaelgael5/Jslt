"""Exemples prêts à charger dans le playground.

Chaque exemple est un triplet ``{name, template, source}`` couvrant une
construction du langage. Ils n'utilisent que des fonctions du **cœur** (cohérent
avec le bac à sable du playground). Un test vérifie qu'ils transforment tous sans
erreur — ils servent donc aussi d'exemples de conformité.
"""

from __future__ import annotations

EXAMPLES: list[dict[str, str]] = [
    {
        "name": "Champs & calcul",
        "template": '{\n  "name": $.user.name,\n  "year": $.user.age + 1\n}',
        "source": '{ "user": { "name": "Alice", "age": 30 } }',
    },
    {
        "name": "Descente récursive",
        "template": '{ "ids": $..id }',
        "source": '{ "a": { "id": 1 }, "b": { "nested": { "id": 2 } }, "c": { "id": 3 } }',
    },
    {
        "name": "Variables & projection",
        "template": '{ "u:": $.user, "nom": u:$.name, "ville": u:$.city }',
        "source": '{ "user": { "name": "Bob", "city": "Lyon" } }',
    },
    {
        "name": "Coalescence (valeur par défaut)",
        "template": '{ "ville": $.user.city ?? "inconnue" }',
        "source": '{ "user": { "name": "Z" } }',
    },
    {
        "name": "Fonctions",
        "template": '{ "total": sum($.n), "maj": upper($.s) }',
        "source": '{ "n": [1, 2, 3], "s": "hi" }',
    },
    {
        "name": "Expressions régulières",
        "template": '{\n  "valide": regexismatch($.mail, "^[\\\\w.]+@[\\\\w.]+\\\\.[a-z]+$"),\n  "nombres": regexmatches($.s, "\\\\d+")\n}',
        "source": '{ "mail": "bob@ex.fr", "s": "lot 12, ref 345" }',
    },
    {
        "name": "when / switch",
        "template": '{ "statut": when($.code) { "200": "ok", "404": "introuvable", "default": "autre" } }',
        "source": '{ "code": 404 }',
    },
    {
        "name": "Boucle + filtre",
        "template": '[ { "$source": $.items[?(@.ok == true)], "v": $.n } ]',
        "source": '{ "items": [ { "n": 1, "ok": true }, { "n": 2, "ok": false }, { "n": 3, "ok": true } ] }',
    },
    {
        "name": "Cast #integer",
        "template": '{ "i": $.s #integer }',
        "source": '{ "s": "42" }',
    },
]


def examples() -> list[dict[str, str]]:
    """Liste des exemples du playground."""
    return EXAMPLES
