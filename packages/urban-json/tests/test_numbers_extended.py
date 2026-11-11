"""Arrondis dirigés, logarithme à base, bases arbitraires — catégorie « nombres ».

`floor` existait sans `ceil` (l'asymétrie la plus visible du lot), aucun arrondi
dirigé n'avait de précision, et `logarithm` était fixé à la base e.
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


# --- arrondis dirigés ---------------------------------------------------------


def test_ceil():
    assert run('{ "a": ceil($.a), "b": ceil($.b) }', {"a": 2.1, "b": -2.1}) == {
        "a": 3.0, "b": -2.0
    }


def test_ceil_et_floor_sont_symetriques():
    source = {"v": 2.5}
    assert run('{ "c": ceil($.v), "f": floor($.v) }', source) == {"c": 3.0, "f": 2.0}


@pytest.mark.parametrize(
    "fn, expected", [("ceil", 1.24), ("floor", 1.23), ("truncate", 1.23)]
)
def test_precision_des_arrondis_diriges(fn, expected):
    assert run('{ "r": ' + fn + "($.v, 2) }", {"v": 1.2345}) == {"r": expected}


def test_precision_sur_un_negatif():
    # Troncature vers zéro, plancher vers le bas : les deux diffèrent ici.
    source = {"v": -1.2345}
    assert run('{ "t": truncate($.v, 2), "f": floor($.v, 2) }', source) == {
        "t": -1.23, "f": -1.24
    }


def test_arrondis_sans_precision_inchanges():
    source = {"v": -2.7}
    assert run('{ "f": floor($.v), "t": truncate($.v) }', source) == {"f": -3.0, "t": -2.0}


# --- logarithme à base --------------------------------------------------------


def test_log_a_base():
    assert run('{ "a": log($.v, 2), "b": log($.v, 10) }', {"v": 1000}) == {
        "a": 9.965784284662087, "b": 3.0
    }


def test_log_base_invalide_leve():
    for base in (0, 1, -2):
        with pytest.raises(JsltError, match="base"):
            run('{ "r": log($.v, ' + str(base) + ") }", {"v": 10})


def test_log_d_une_valeur_non_positive_leve():
    with pytest.raises(JsltError, match="logarithme"):
        run('{ "r": log($.v, 10) }', {"v": 0})


# --- isnan / isfinite ---------------------------------------------------------


def test_isfinite_et_isnan_sur_un_nombre_ordinaire():
    assert run('{ "f": isfinite($.v), "n": isnan($.v) }', {"v": 1.5}) == {
        "f": True, "n": False
    }


def test_isfinite_detecte_un_debordement():
    # Un calcul peut produire l'infini là où JSON ne sait pas l'écrire.
    template = '{ "f": isfinite($.v * $.v), "n": isnan($.v * $.v) }'
    assert run(template, {"v": 1e308}) == {"f": False, "n": False}


def test_predicats_sur_une_non_valeur_sont_faux():
    template = '{ "f": isfinite($.t), "n": isnan($.t) }'
    assert run(template, {"t": "abc"}) == {"f": False, "n": False}
    assert run(template, {}) == {"f": False, "n": False}


# --- bases arbitraires --------------------------------------------------------


@pytest.mark.parametrize(
    "value, base, expected",
    [(255, 16, "ff"), (255, 2, "11111111"), (255, 36, "73"), (10, 8, "12"), (-5, 2, "-101")],
)
def test_tobase(value, base, expected):
    template = '{ "r": tobase($.v, ' + str(base) + ") }"
    assert run(template, {"v": value}) == {"r": expected}


@pytest.mark.parametrize(
    "text, base, expected", [("ff", 16, 255), ("11111111", 2, 255), ("73", 36, 255)]
)
def test_frombase(text, base, expected):
    template = '{ "r": frombase($.t, ' + str(base) + ") }"
    assert run(template, {"t": text}) == {"r": expected}


def test_tobase_largeur_minimale():
    assert run('{ "r": tobase($.v, 2, 8) }', {"v": 5}) == {"r": "00000101"}


@pytest.mark.parametrize("base", [1, 0, 37, -2])
def test_base_hors_bornes_leve(base):
    with pytest.raises(JsltError, match="base"):
        run('{ "r": tobase($.v, ' + str(base) + ") }", {"v": 5})


def test_frombase_texte_invalide_leve():
    with pytest.raises(JsltError, match="base 2"):
        run('{ "r": frombase($.t, 2) }', {"t": "129"})


def test_tobase_et_tohex_concordent():
    source = {"v": 48879}
    assert run('{ "a": tobase($.v, 16), "b": tohex($.v) }', source) == {
        "a": "beef", "b": "beef"
    }


@pytest.mark.parametrize("call", ["ceil($.v)", "ceil($.v, 2)", "tobase($.v, 16)", "log($.v, 2)"])
def test_convention_numerique_null(call):
    assert run('{ "r": ' + call + ' }', {}) == {"r": None}
    assert run('{ "r": ' + call + ' }', {"v": "x"}) == {"r": None}
