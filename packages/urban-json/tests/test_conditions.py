"""La conditionnelle en position d'expression — sujet 1.

Le moteur n'avait que `when`, un aiguillage sur une **valeur** : une condition
composée devait être calculée puis aiguillée sur son texte. Ce qui se joue ici,
c'est surtout la **paresse** des branches : une conditionnelle dont les deux
branches sont évaluées ne protège de rien, et c'est tout l'usage qu'on en
attend.
"""

from __future__ import annotations

from urban_json import JsltTemplate


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


def test_ifelse_rend_la_branche_vraie() -> None:
    assert run('{ "r": ifelse($.n > 10, "grand", "petit") }', {"n": 42}) == {"r": "grand"}


def test_ifelse_rend_la_branche_fausse() -> None:
    assert run('{ "r": ifelse($.n > 10, "grand", "petit") }', {"n": 2}) == {"r": "petit"}


def test_ifelse_accepte_une_condition_composee() -> None:
    """Le manque qui motivait la fonction : `when` n'aiguille que sur une valeur."""
    template = '{ "r": ifelse($.n > 10 && $.actif, "ok", "non") }'
    assert run(template, {"n": 42, "actif": True}) == {"r": "ok"}
    assert run(template, {"n": 42, "actif": False}) == {"r": "non"}


def test_ifelse_n_evalue_pas_la_branche_ecartee() -> None:
    """Sans paresse, la division par zéro partirait avant la condition."""
    assert run('{ "r": ifelse($.d == 0, 0, 100 / $.d) }', {"d": 0}) == {"r": 0}
    assert run('{ "r": ifelse($.d == 0, 0, 100 / $.d) }', {"d": 4}) == {"r": 25}


def test_ifelse_n_evalue_pas_la_branche_ecartee_par_le_chemin_compile() -> None:
    """Les deux moteurs partagent le mécanisme d'arguments paresseux ; une
    divergence ici passerait inaperçue jusqu'à ce qu'un intégrateur appelle
    `build()` sur un template qui se protégeait d'une donnée fautive."""
    template = JsltTemplate.parse('{ "r": ifelse($.d == 0, 0, 100 / $.d) }').build()
    assert template.transform({"d": 0}) == {"r": 0}


def test_ifelse_lit_la_condition_comme_filter() -> None:
    """`null`, `0` et `""` sont faux — la lecture de `filter`/`every`, pas celle,
    stricte, de `requirethat`."""
    source = {"vide": "", "zero": 0, "texte": "oui"}
    assert run('{ "a": ifelse($.absent, 1, 0), "b": ifelse($.vide, 1, 0) }', source) == {"a": 0, "b": 0}
    assert run('{ "a": ifelse($.zero, 1, 0), "b": ifelse($.texte, 1, 0) }', source) == {"a": 0, "b": 1}


def test_ifelse_sans_branche_rend_null() -> None:
    """Comme un `when` sans `default`."""
    assert run('{ "r": ifelse($.n > 10, "grand") }', {"n": 2}) == {"r": None}


def test_ifelse_s_imbrique_pour_plus_de_deux_cas() -> None:
    template = '{ "r": ifelse($.n < 0, "négatif", ifelse($.n == 0, "nul", "positif")) }'
    assert [run(template, {"n": n})["r"] for n in (-1, 0, 1)] == ["négatif", "nul", "positif"]


def test_ifelse_rend_un_conteneur() -> None:
    """Une branche est une expression quelconque, pas seulement un scalaire."""
    assert run('{ "r": ifelse($.ok, [1, 2], {}) }', {"ok": True}) == {"r": [1, 2]}
