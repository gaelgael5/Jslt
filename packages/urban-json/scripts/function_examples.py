"""Un exemple exécuté par fonction, inlined dans sa page de référence.

Pourquoi ici et pas dans les chapitres : un exemple de chapitre enseigne un
*usage* et mêle souvent trois fonctions (`selectmany(sort(…), …)`) ; la page de
référence, elle, doit montrer **une** fonction, au plus court. Les deux ont leur
place, et ce fichier porte la seconde.

Pourquoi des données et pas du texte écrit dans les pages : chaque exemple est
rejoué par la suite du guide (`tests/_docs.py` balaie aussi `docs/fonctions/`),
donc par les **deux** moteurs — interprété et compilé. Un exemple faux fait
rougir la suite au lieu d'égarer le lecteur.

Forme d'un exemple :

    {"template": …, "source": …, "output": …}      exécuté (triplet du guide)
    {"template": …, "source": …, "render": …}      sortie texte : `render()`,
                                                   donc montré sans être rejoué

Les clés des documents sont **courtes et neutres** : le même exemple sert les
deux langues, le code n'ayant pas à être traduit.
"""

from __future__ import annotations

#: name -> liste d'exemples (un seul, sauf quand deux usages se répondent).
EXAMPLES: dict[str, list[dict[str, str]]] = {
    # --- maths ----------------------------------------------------------------
    "abs": [{"template": '{ "r": abs($.n) }', "source": '{ "n": -3.5 }', "output": '{ "r": 3.5 }'}],
    "acos": [{"template": '{ "r": acos($.n) }', "source": '{ "n": 1 }', "output": '{ "r": 0.0 }'}],
    "acosh": [{"template": '{ "r": acosh($.n) }', "source": '{ "n": 1 }', "output": '{ "r": 0.0 }'}],
    "asin": [{"template": '{ "r": asin($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "asinh": [{"template": '{ "r": asinh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "atan": [{"template": '{ "r": atan($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "atan2": [{"template": '{ "r": atan2($.y, $.x) }', "source": '{ "y": 0, "x": 1 }', "output": '{ "r": 0.0 }'}],
    "atanh": [{"template": '{ "r": atanh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "ceil": [
        {
            "template": '{ "entier": ceil($.n), "deux_decimales": ceil($.n, 2) }',
            "source": '{ "n": 2.341 }',
            "output": '{ "entier": 3.0, "deux_decimales": 2.35 }',
        }
    ],
    "cos": [{"template": '{ "r": cos($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 1.0 }'}],
    "cosh": [{"template": '{ "r": cosh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 1.0 }'}],
    "e": [{"template": '{ "r": round(e(), 3) }', "source": "{}", "output": '{ "r": 2.718 }'}],
    "exp": [{"template": '{ "r": round(exp($.n), 3) }', "source": '{ "n": 1 }', "output": '{ "r": 2.718 }'}],
    "floor": [
        {
            "template": '{ "entier": floor($.n), "deux_decimales": floor($.n, 2) }',
            "source": '{ "n": 2.349 }',
            "output": '{ "entier": 2.0, "deux_decimales": 2.34 }',
        }
    ],
    "logarithm": [{"template": '{ "r": logarithm($.n) }', "source": '{ "n": 1 }', "output": '{ "r": 0.0 }'}],
    "logarithm10": [{"template": '{ "r": logarithm10($.n) }', "source": '{ "n": 1000 }', "output": '{ "r": 3.0 }'}],
    "logarithm2": [{"template": '{ "r": logarithm2($.n) }', "source": '{ "n": 8 }', "output": '{ "r": 3.0 }'}],
    "max": [
        {
            "template": '{ "deux": max($.a, $.b), "du_tableau": max($.l) }',
            "source": '{ "a": 2, "b": 9, "l": [3, 11, 7] }',
            "output": '{ "deux": 9.0, "du_tableau": 11 }',
        }
    ],
    "min": [
        {
            "template": '{ "deux": min($.a, $.b), "du_tableau": min($.l) }',
            "source": '{ "a": 2, "b": 9, "l": [3, 11, 7] }',
            "output": '{ "deux": 2.0, "du_tableau": 3 }',
        }
    ],
    "pi": [{"template": '{ "r": round(pi(), 4) }', "source": "{}", "output": '{ "r": 3.1416 }'}],
    "pow": [{"template": '{ "r": pow($.b, $.e) }', "source": '{ "b": 2, "e": 10 }', "output": '{ "r": 1024.0 }'}],
    "round": [
        {
            "template": '{ "pair": round($.a), "deux_decimales": round($.b, 2) }',
            "source": '{ "a": 2.5, "b": 1.2345 }',
            "output": '{ "pair": 2.0, "deux_decimales": 1.23 }',
        }
    ],
    "sin": [{"template": '{ "r": sin($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "sinh": [{"template": '{ "r": sinh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "sqrt": [{"template": '{ "r": sqrt($.n) }', "source": '{ "n": 9 }', "output": '{ "r": 3.0 }'}],
    "tan": [{"template": '{ "r": tan($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "tanh": [{"template": '{ "r": tanh($.n) }', "source": '{ "n": 0 }', "output": '{ "r": 0.0 }'}],
    "truncate": [
        {
            "template": '{ "vers_zero": truncate($.n), "deux_decimales": truncate($.n, 2) }',
            "source": '{ "n": -2.789 }',
            "output": '{ "vers_zero": -2.0, "deux_decimales": -2.78 }',
        }
    ],
    # --- nombres ---------------------------------------------------------------
    "clamp": [
        {
            "template": '{ "r": clamp($.n, 0, 100) }',
            "source": '{ "n": 142 }',
            "output": '{ "r": 100 }',
        }
    ],
    "frombase": [{"template": '{ "r": frombase($.t, 2) }', "source": '{ "t": "1011" }', "output": '{ "r": 11 }'}],
    "fromhex": [{"template": '{ "r": fromhex($.t) }', "source": '{ "t": "0xff" }', "output": '{ "r": 255 }'}],
    "gcd": [{"template": '{ "r": gcd($.a, $.b) }', "source": '{ "a": 84, "b": 36 }', "output": '{ "r": 12 }'}],
    "isfinite": [
        {
            "template": '{ "nombre": isfinite($.n), "texte": isfinite($.t) }',
            "source": '{ "n": 3, "t": "3" }',
            "output": '{ "nombre": true, "texte": false }',
        }
    ],
    "isnan": [
        {
            "template": '{ "r": isnan($.n) }',
            "source": '{ "n": 3 }',
            "output": '{ "r": false }',
        }
    ],
    "log": [{"template": '{ "r": log($.n, 10) }', "source": '{ "n": 1000 }', "output": '{ "r": 3.0 }'}],
    "parsenumber": [
        {
            "template": '{ "r": parsenumber($.t, "fr-FR") }',
            "source": '{ "t": "1 234,56" }',
            "output": '{ "r": 1234.56 }',
        }
    ],
    "shiftleft": [{"template": '{ "r": shiftleft($.n, 3) }', "source": '{ "n": 1 }', "output": '{ "r": 8 }'}],
    "shiftright": [{"template": '{ "r": shiftright($.n, 3) }', "source": '{ "n": 64 }', "output": '{ "r": 8 }'}],
    "sign": [
        {
            "template": '{ "negatif": sign($.a), "zero": sign($.b), "positif": sign($.c) }',
            "source": '{ "a": -4, "b": 0, "c": 7 }',
            "output": '{ "negatif": -1, "zero": 0, "positif": 1 }',
        }
    ],
    "tobase": [
        {
            "template": '{ "binaire": tobase($.n, 2), "sur_huit": tobase($.n, 2, 8) }',
            "source": '{ "n": 11 }',
            "output": '{ "binaire": "1011", "sur_huit": "00001011" }',
        }
    ],
    "tohex": [
        {
            "template": '{ "r": tohex($.n), "sur_quatre": tohex($.n, 4) }',
            "source": '{ "n": 255 }',
            "output": '{ "r": "ff", "sur_quatre": "00ff" }',
        }
    ],
    # --- texte -----------------------------------------------------------------
    "endswith": [
        {
            "template": '{ "r": endswith($.t, ".json") }',
            "source": '{ "t": "contrat.json" }',
            "output": '{ "r": true }',
        }
    ],
    "indexof": [
        {
            "template": '{ "texte": indexof($.t, "o"), "tableau": indexof($.l, "b") }',
            "source": '{ "t": "bonjour", "l": ["a", "b", "c"] }',
            "output": '{ "texte": 1, "tableau": 1 }',
        }
    ],
    "lastindexof": [
        {
            "template": '{ "r": lastindexof($.t, "o") }',
            "source": '{ "t": "bonjour" }',
            "output": '{ "r": 4 }',
        }
    ],
    "lower": [{"template": '{ "r": lower($.t) }', "source": '{ "t": "ACME SA" }', "output": '{ "r": "acme sa" }'}],
    "padleft": [
        {
            "template": '{ "r": padleft($.t, 6, "0") }',
            "source": '{ "t": "42" }',
            "output": '{ "r": "000042" }',
        }
    ],
    "padright": [
        {
            "template": '{ "r": padright($.t, 6, ".") }',
            "source": '{ "t": "42" }',
            "output": '{ "r": "42...." }',
        }
    ],
    "repeat": [{"template": '{ "r": repeat($.t, 3) }', "source": '{ "t": "ab" }', "output": '{ "r": "ababab" }'}],
    "replace": [
        {
            "template": '{ "r": replace($.t, "-", "/") }',
            "source": '{ "t": "2026-11-11" }',
            "output": '{ "r": "2026/11/11" }',
        }
    ],
    "shorten": [
        {
            "template": '{ "r": shorten($.t, 12) }',
            "source": '{ "t": "Facture annuelle 2026" }',
            "output": '{ "r": "Facture…" }',
        }
    ],
    "split": [
        {
            "template": '{ "r": split($.t, ";") }',
            "source": '{ "t": "a;b;c" }',
            "output": '{ "r": ["a", "b", "c"] }',
        }
    ],
    "splitstring": [
        {
            "template": '{ "r": splitstring($.t, " - ") }',
            "source": '{ "t": "a - b - c" }',
            "output": '{ "r": ["a", "b", "c"] }',
        }
    ],
    "startswith": [
        {
            "template": '{ "r": startswith($.t, "FR") }',
            "source": '{ "t": "FR7630006000011234567890189" }',
            "output": '{ "r": true }',
        }
    ],
    "stringcontains": [
        {
            "template": '{ "r": stringcontains($.t, "@") }',
            "source": '{ "t": "ana@exemple.fr" }',
            "output": '{ "r": true }',
        }
    ],
    "stringlenght": [
        {
            "template": '{ "r": stringlenght($.t) }',
            "source": '{ "t": "bonjour" }',
            "output": '{ "r": 7 }',
        }
    ],
    "substring": [
        {
            "template": '{ "debut": substring($.t, 0, 3), "depuis_la_fin": substring($.t, -2) }',
            "source": '{ "t": "bonjour" }',
            "output": '{ "debut": "bon", "depuis_la_fin": "ur" }',
        }
    ],
    "titlecase": [
        {
            "template": '{ "r": titlecase($.t) }',
            "source": '{ "t": "ana de la tour" }',
            "output": '{ "r": "Ana De La Tour" }',
        }
    ],
    "trim": [
        {
            "template": '{ "espaces": trim($.a), "caracteres": trim($.b, "*") }',
            "source": '{ "a": "  ok  ", "b": "**ok**" }',
            "output": '{ "espaces": "ok", "caracteres": "ok" }',
        }
    ],
    "trimend": [{"template": '{ "r": trimend($.t) }', "source": '{ "t": "ok   " }', "output": '{ "r": "ok" }'}],
    "trimstart": [{"template": '{ "r": trimstart($.t) }', "source": '{ "t": "   ok" }', "output": '{ "r": "ok" }'}],
    "upper": [{"template": '{ "r": upper($.t) }', "source": '{ "t": "acme" }', "output": '{ "r": "ACME" }'}],
    # --- pliage Unicode et proximité -------------------------------------------
    "deaccent": [
        {
            "template": '{ "r": deaccent($.t) }',
            "source": '{ "t": "Évêché" }',
            "output": '{ "r": "Eveche" }',
        }
    ],
    "foldtext": [
        {
            "template": '{ "r": foldtext($.t) }',
            "source": '{ "t": "Évêché" }',
            "output": '{ "r": "eveche" }',
        }
    ],
    "normalize": [
        {
            "template": '{ "r": stringlenght(normalize($.t, "C")) }',
            "source": '{ "t": "e\u0301" }',
            "output": '{ "r": 1 }',
        }
    ],
    "slugify": [
        {
            "template": '{ "r": slugify($.t) }',
            "source": '{ "t": "Évêché de Lyon" }',
            "output": '{ "r": "eveche-de-lyon" }',
        }
    ],
    "levenshtein": [
        {
            "template": '{ "r": levenshtein($.a, $.b) }',
            "source": '{ "a": "chat", "b": "chats" }',
            "output": '{ "r": 1 }',
        }
    ],
    "similarity": [
        {
            "template": '{ "r": round(similarity($.a, $.b), 2) }',
            "source": '{ "a": "Durand", "b": "Durrand" }',
            "output": '{ "r": 0.86 }',
        }
    ],
    # --- expressions régulières -------------------------------------------------
    "regexismatch": [
        {
            "template": '{ "r": regexismatch($.t, "^[A-Z]{2}[0-9]+$") }',
            "source": '{ "t": "FR123" }',
            "output": '{ "r": true }',
        }
    ],
    "regexmatches": [
        {
            "template": '{ "r": regexmatches($.t, "[0-9]+") }',
            "source": '{ "t": "a1 b22 c333" }',
            "output": '{ "r": ["1", "22", "333"] }',
        }
    ],
    "regexreplace": [
        {
            "template": '{ "r": regexreplace($.t, "(\\\\d{4})-(\\\\d{2})", "$2/$1") }',
            "source": '{ "t": "2026-11" }',
            "output": '{ "r": "11/2026" }',
        }
    ],
    "splitregex": [
        {
            "template": '{ "r": splitregex($.t, "\\\\s*;\\\\s*") }',
            "source": '{ "t": "a ; b;c" }',
            "output": '{ "r": ["a", "b", "c"] }',
        }
    ],
    # --- encodage et empreintes --------------------------------------------------
    "crc32": [{"template": '{ "r": crc32($.t) }', "source": '{ "t": "abc" }', "output": '{ "r": 891568578 }'}],
    "frombase64": [
        {
            "template": '{ "r": frombase64($.t) }',
            "source": '{ "t": "Ym9uam91cg==" }',
            "output": '{ "r": "bonjour" }',
        }
    ],
    "hexdecode": [
        {
            "template": '{ "r": hexdecode($.t) }',
            "source": '{ "t": "616263" }',
            "output": '{ "r": "abc" }',
        }
    ],
    "hexencode": [{"template": '{ "r": hexencode($.t) }', "source": '{ "t": "abc" }', "output": '{ "r": "616263" }'}],
    "hmacsha256": [
        {
            "template": '{ "r": hmacsha256($.t, $.cle) }',
            "source": '{ "t": "message", "cle": "secret" }',
            "output": '{ "r": "8b5f48702995c1598c573db1e21866a9b825d4a794d169d7060a03605796360b" }',
        }
    ],
    "htmlescape": [
        {
            "template": '{ "r": htmlescape($.t) }',
            "source": '{ "t": "<b>ok</b>" }',
            "output": '{ "r": "&lt;b&gt;ok&lt;/b&gt;" }',
        }
    ],
    "htmlunescape": [
        {
            "template": '{ "r": htmlunescape($.t) }',
            "source": '{ "t": "&lt;b&gt;ok&lt;/b&gt;" }',
            "output": '{ "r": "<b>ok</b>" }',
        }
    ],
    "md5": [
        {
            "template": '{ "r": md5($.t) }',
            "source": '{ "t": "abc" }',
            "output": '{ "r": "900150983cd24fb0d6963f7d28e17f72" }',
        }
    ],
    "sha1": [
        {
            "template": '{ "r": sha1($.t) }',
            "source": '{ "t": "abc" }',
            "output": '{ "r": "a9993e364706816aba3e25717850c26c9cd0d89d" }',
        }
    ],
    "sha256": [
        {
            "template": '{ "r": sha256($.t) }',
            "source": '{ "t": "abc" }',
            "output": '{ "r": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" }',
        }
    ],
    "sha512": [
        {
            "template": '{ "r": stringlenght(sha512($.t)) }',
            "source": '{ "t": "abc" }',
            "output": '{ "r": 128 }',
        }
    ],
    "tobase64": [
        {
            "template": '{ "r": tobase64($.t) }',
            "source": '{ "t": "bonjour" }',
            "output": '{ "r": "Ym9uam91cg==" }',
        }
    ],
    "urldecode": [
        {
            "template": '{ "r": urldecode($.t) }',
            "source": '{ "t": "caf%C3%A9%20noir" }',
            "output": '{ "r": "café noir" }',
        }
    ],
    "urlencode": [
        {
            "template": '{ "r": urlencode($.t) }',
            "source": '{ "t": "café noir" }',
            "output": '{ "r": "caf%C3%A9%20noir" }',
        }
    ],
    # --- collections ------------------------------------------------------------
    "any": [
        {
            "template": '{ "pleine": any($.l), "vide": any($.v) }',
            "source": '{ "l": [1], "v": [] }',
            "output": '{ "pleine": true, "vide": false }',
        }
    ],
    "chunk": [
        {
            "template": '{ "r": chunk($.l, 2) }',
            "source": '{ "l": [1, 2, 3, 4, 5] }',
            "output": '{ "r": [[1, 2], [3, 4], [5]] }',
        }
    ],
    "concat": [
        {
            "template": '{ "colle": concat($.l), "joint": concat($.l, "-") }',
            "source": '{ "l": ["a", "b", "c"] }',
            "output": '{ "colle": "abc", "joint": "a-b-c" }',
        }
    ],
    "contains": [
        {
            "template": '{ "r": contains($.l, "b") }',
            "source": '{ "l": ["a", "b"] }',
            "output": '{ "r": true }',
        }
    ],
    "difference": [
        {
            "template": '{ "r": difference($.a, $.b) }',
            "source": '{ "a": [1, 2, 3], "b": [2] }',
            "output": '{ "r": [1, 3] }',
        }
    ],
    "distinct": [
        {
            "template": '{ "r": distinct($.l, $.*) }',
            "source": '{ "l": [1, 2, 2, 3] }',
            "output": '{ "r": [1, 2, 3] }',
        }
    ],
    "distinctby": [
        {
            "template": '{ "r": distinctby($.l, $.ville) }',
            "source": '{ "l": [{ "id": 1, "ville": "Lyon" }, { "id": 2, "ville": "Lyon" }, { "id": 3, "ville": "Brest" }] }',
            "output": '{ "r": [{ "id": 1, "ville": "Lyon" }, { "id": 3, "ville": "Brest" }] }',
        }
    ],
    "flatten": [
        {
            "template": '{ "a_fond": flatten($.l), "un_niveau": flatten($.l, 1) }',
            "source": '{ "l": [1, [2, [3]]] }',
            "output": '{ "a_fond": [1, 2, 3], "un_niveau": [1, 2, [3]] }',
        }
    ],
    "intersect": [
        {
            "template": '{ "r": intersect($.a, $.b) }',
            "source": '{ "a": [1, 2, 3], "b": [3, 1] }',
            "output": '{ "r": [1, 3] }',
        }
    ],
    "limit": [
        {
            "template": '{ "r": limit($.l, 2) }',
            "source": '{ "l": [1, 2, 3, 4] }',
            "output": '{ "r": [1, 2] }',
        }
    ],
    "partition": [
        {
            "template": '{ "r": partition($.l, $.actif) }',
            "source": '{ "l": [{ "n": "a", "actif": true }, { "n": "b", "actif": false }] }',
            "output": '{ "r": { "true": [{ "n": "a", "actif": true }], "false": [{ "n": "b", "actif": false }] } }',
        }
    ],
    "select": [
        {
            "template": '{ "r": select($.d, $.client.nom) }',
            "source": '{ "d": { "client": { "nom": "Ana" } } }',
            "output": '{ "r": "Ana" }',
        }
    ],
    "selectany": [
        {
            "template": '{ "r": selectany($.d, $.client.nom) }',
            "source": '{ "d": { "client": { "nom": "Ana" } } }',
            "output": '{ "r": true }',
        }
    ],
    "selectmany": [
        {
            "template": '{ "r": selectmany($.l, $.*.id) }',
            "source": '{ "l": [{ "id": 1 }, { "id": 2 }] }',
            "output": '{ "r": [1, 2] }',
        }
    ],
    "skip": [
        {
            "template": '{ "r": skip($.l, 2) }',
            "source": '{ "l": [1, 2, 3, 4] }',
            "output": '{ "r": [3, 4] }',
        }
    ],
    "union": [
        {
            "template": '{ "r": union($.l) }',
            "source": '{ "l": [[1, 2], [3]] }',
            "output": '{ "r": [1, 2, 3] }',
        }
    ],
    "unzip": [
        {
            "template": '{ "r": unzip($.l) }',
            "source": '{ "l": [[1, "a"], [2, "b"]] }',
            "output": '{ "r": [[1, 2], ["a", "b"]] }',
        }
    ],
    "window": [
        {
            "template": '{ "r": window($.l, 2) }',
            "source": '{ "l": [1, 2, 3] }',
            "output": '{ "r": [[1, 2], [2, 3]] }',
        }
    ],
    "zip": [
        {
            "template": '{ "r": zip($.a, $.b) }',
            "source": '{ "a": [1, 2], "b": ["x", "y"] }',
            "output": '{ "r": [[1, "x"], [2, "y"]] }',
        }
    ],
    # --- tri et ordre -------------------------------------------------------------
    "first": [{"template": '{ "r": first($.l) }', "source": '{ "l": [3, 1] }', "output": '{ "r": 3 }'}],
    "last": [{"template": '{ "r": last($.l) }', "source": '{ "l": [3, 1] }', "output": '{ "r": 1 }'}],
    "reverse": [
        {
            "template": '{ "tableau": reverse($.l), "texte": reverse($.t) }',
            "source": '{ "l": [1, 2, 3], "t": "abc" }',
            "output": '{ "tableau": [3, 2, 1], "texte": "cba" }',
        }
    ],
    "sort": [
        {
            "template": '{ "par_prix": selectmany(sort($.l, $.prix), $.*.id) }',
            "source": '{ "l": [{ "id": 1, "prix": 30 }, { "id": 2, "prix": 10 }] }',
            "output": '{ "par_prix": [2, 1] }',
        },
        {
            "template": '{ "ville_puis_prix_decroissant": selectmany(sort($.l, [$.ville, $.prix], [false, true]), $.*.id) }',
            "source": '{ "l": [{ "id": 1, "ville": "Lyon", "prix": 10 }, { "id": 2, "ville": "Lyon", "prix": 30 }, { "id": 3, "ville": "Brest", "prix": 5 }] }',
            "output": '{ "ville_puis_prix_decroissant": [3, 2, 1] }',
        },
    ],
    # --- agrégats et statistiques ---------------------------------------------------
    "avg": [{"template": '{ "r": avg($.n) }', "source": '{ "n": [1, 2, 6] }', "output": '{ "r": 3.0 }'}],
    "count": [
        {
            "template": '{ "tableau": count($.l), "objet": count($.o), "texte": count($.t) }',
            "source": '{ "l": [1, 2], "o": { "a": 1 }, "t": "abc" }',
            "output": '{ "tableau": 2, "objet": 1, "texte": 3 }',
        }
    ],
    "median": [{"template": '{ "r": median($.n) }', "source": '{ "n": [1, 9, 2] }', "output": '{ "r": 2 }'}],
    "mode": [
        {
            "template": '{ "r": mode($.l) }',
            "source": '{ "l": ["a", "b", "a"] }',
            "output": '{ "r": "a" }',
        }
    ],
    "percentile": [
        {
            "template": '{ "p90": percentile($.n, 90) }',
            "source": '{ "n": [1, 2, 3, 4, 5] }',
            "output": '{ "p90": 4.6 }',
        }
    ],
    "product": [{"template": '{ "r": product($.n) }', "source": '{ "n": [2, 3, 4] }', "output": '{ "r": 24 }'}],
    "stddev": [
        {
            "template": '{ "population": stddev($.n), "echantillon": round(stddev($.n, true), 3) }',
            "source": '{ "n": [2, 4, 4, 4, 5, 5, 7, 9] }',
            "output": '{ "population": 2.0, "echantillon": 2.138 }',
        }
    ],
    "sum": [{"template": '{ "r": sum($.n) }', "source": '{ "n": [1, 2, 3] }', "output": '{ "r": 6 }'}],
    "variance": [
        {
            "template": '{ "r": variance($.n) }',
            "source": '{ "n": [2, 4, 4, 4, 5, 5, 7, 9] }',
            "output": '{ "r": 4.0 }',
        }
    ],
    # --- agrégation par clef calculée ------------------------------------------------
    "avgby": [
        {
            "template": '{ "r": avgby($.l, $.ville, $.m) }',
            "source": '{ "l": [{ "ville": "Lyon", "m": 10 }, { "ville": "Lyon", "m": 20 }, { "ville": "Brest", "m": 7 }] }',
            "output": '{ "r": { "Lyon": 15.0, "Brest": 7.0 } }',
        }
    ],
    "countby": [
        {
            "template": '{ "r": countby($.l, $.ville) }',
            "source": '{ "l": [{ "ville": "Lyon" }, { "ville": "Lyon" }, { "ville": "Brest" }] }',
            "output": '{ "r": { "Lyon": 2, "Brest": 1 } }',
        }
    ],
    "groupby": [
        {
            "template": '{ "plat": groupby($.l, $.ville) }',
            "source": '{ "l": [{ "id": 1, "ville": "Lyon" }, { "id": 2, "ville": "Brest" }] }',
            "output": '{ "plat": { "Lyon": [{ "id": 1, "ville": "Lyon" }], "Brest": [{ "id": 2, "ville": "Brest" }] } }',
        },
        {
            "template": '{ "imbrique": groupby($.l, [$.pays, $.ville], true) }',
            "source": '{ "l": [{ "id": 1, "pays": "FR", "ville": "Lyon" }] }',
            "output": '{ "imbrique": { "FR": { "Lyon": [{ "id": 1, "pays": "FR", "ville": "Lyon" }] } } }',
        },
    ],
    "sumby": [
        {
            "template": '{ "r": sumby($.l, $.ville, $.m) }',
            "source": '{ "l": [{ "ville": "Lyon", "m": 10 }, { "ville": "Lyon", "m": 5 }, { "ville": "Brest", "m": 7 }] }',
            "output": '{ "r": { "Lyon": 15, "Brest": 7 } }',
        }
    ],
    # --- regroupement et jointure ------------------------------------------------------
    "group": [
        {
            "template": '{ "r": group($.p, ["$.ville"]) }',
            "source": '{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }',
            "output": '{ "r": [{ "Label": "Lyon", "Items": [{ "nom": "Ana", "ville": "Lyon" }] }] }',
        }
    ],
    "join": [
        {
            "template": '{ "r": join($.c, $.id, false, [{ "Name": "commandes", "Key": "$.client", "Source": $.o }]) }',
            "source": '{ "c": [{ "id": 1, "nom": "Ana" }], "o": [{ "client": 1, "total": 12 }] }',
            "output": '{ "r": [{ "id": 1, "nom": "Ana", "commandes": [{ "total": 12 }] }] }',
        }
    ],
    "createindex": [
        {
            "template": '{ "i:": createindex($.p, "", "$.nom"), "ana": index(i:, "Ana") }',
            "source": '{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }',
            "output": '{ "ana": { "nom": "Ana", "ville": "Lyon" } }',
        }
    ],
    "index": [
        {
            "template": '{ "i:": createindex($.p, "", "$.nom"), "ana": index(i:, "Ana") }',
            "source": '{ "p": [{ "nom": "Ana", "ville": "Lyon" }] }',
            "output": '{ "ana": { "nom": "Ana", "ville": "Lyon" } }',
        }
    ],
    # --- types et repli ----------------------------------------------------------------
    "convert": [
        {
            "template": '{ "entier": convert($.t, "integer"), "texte": convert($.n, "string") }',
            "source": '{ "t": "42", "n": 7 }',
            "output": '{ "entier": 42, "texte": "7" }',
        }
    ],
    "isarray": [
        {
            "template": '{ "tableau": isarray($.l), "objet": isarray($.o) }',
            "source": '{ "l": [], "o": {} }',
            "output": '{ "tableau": true, "objet": false }',
        }
    ],
    "isboolean": [
        {
            "template": '{ "r": isboolean($.b), "nombre": isboolean($.n) }',
            "source": '{ "b": false, "n": 0 }',
            "output": '{ "r": true, "nombre": false }',
        }
    ],
    "isnotnull": [
        {
            "template": '{ "presente": isnotnull($.a), "absente": isnotnull($.z) }',
            "source": '{ "a": 0 }',
            "output": '{ "presente": true, "absente": false }',
        }
    ],
    "isnull": [
        {
            "template": '{ "absente": isnull($.z), "vide": isnull($.t) }',
            "source": '{ "t": "" }',
            "output": '{ "absente": true, "vide": false }',
        }
    ],
    "isnumber": [
        {
            "template": '{ "nombre": isnumber($.n), "booleen": isnumber($.b) }',
            "source": '{ "n": 3, "b": true }',
            "output": '{ "nombre": true, "booleen": false }',
        }
    ],
    "isobject": [
        {
            "template": '{ "objet": isobject($.o), "tableau": isobject($.l) }',
            "source": '{ "o": {}, "l": [] }',
            "output": '{ "objet": true, "tableau": false }',
        }
    ],
    "isstring": [
        {
            "template": '{ "texte": isstring($.t), "nombre": isstring($.n) }',
            "source": '{ "t": "a", "n": 1 }',
            "output": '{ "texte": true, "nombre": false }',
        }
    ],
    "parsejson": [
        {
            "template": '{ "r": select(parsejson($.t), $.ville) }',
            "source": '{ "t": "{\\"ville\\": \\"Lyon\\"}" }',
            "output": '{ "r": "Lyon" }',
        }
    ],
    "trydefault": [
        {
            "template": '{ "r": trydefault($.a / $.b, "division impossible") }',
            "source": '{ "a": 1, "b": 0 }',
            "output": '{ "r": "division impossible" }',
        }
    ],
    "typeof": [
        {
            "template": '{ "texte": typeof($.t), "tableau": typeof($.l), "absent": typeof($.z) }',
            "source": '{ "t": "a", "l": [] }',
            "output": '{ "texte": "string", "tableau": "array", "absent": "null" }',
        }
    ],
    # --- objets ---------------------------------------------------------------------
    "entries": [
        {
            "template": '{ "r": entries($.o) }',
            "source": '{ "o": { "a": 1, "b": 2 } }',
            "output": '{ "r": [{ "key": "a", "value": 1 }, { "key": "b", "value": 2 }] }',
        }
    ],
    "fromentries": [
        {
            "template": '{ "r": fromentries($.l) }',
            "source": '{ "l": [{ "key": "a", "value": 1 }] }',
            "output": '{ "r": { "a": 1 } }',
        }
    ],
    "has": [
        {
            "template": '{ "presente": has($.o, "a"), "absente": has($.o, "z") }',
            "source": '{ "o": { "a": null } }',
            "output": '{ "presente": true, "absente": false }',
        }
    ],
    "keys": [{"template": '{ "r": keys($.o) }', "source": '{ "o": { "a": 1, "b": 2 } }', "output": '{ "r": ["a", "b"] }'}],
    "merge": [
        {
            "template": '{ "r": merge($.a, $.b) }',
            "source": '{ "a": { "x": 1, "y": 2 }, "b": { "y": 9 } }',
            "output": '{ "r": { "x": 1, "y": 9 } }',
        }
    ],
    "omit": [
        {
            "template": '{ "r": omit($.o, ["secret"]) }',
            "source": '{ "o": { "nom": "Ana", "secret": "x" } }',
            "output": '{ "r": { "nom": "Ana" } }',
        }
    ],
    "pick": [
        {
            "template": '{ "r": pick($.o, ["nom", "ville"]) }',
            "source": '{ "o": { "nom": "Ana", "ville": "Lyon", "secret": "x" } }',
            "output": '{ "r": { "nom": "Ana", "ville": "Lyon" } }',
        }
    ],
    "renamekeys": [
        {
            "template": '{ "r": renamekeys($.o, { "nom": "name" }) }',
            "source": '{ "o": { "nom": "Ana", "ville": "Lyon" } }',
            "output": '{ "r": { "name": "Ana", "ville": "Lyon" } }',
        }
    ],
    "values": [{"template": '{ "r": values($.o) }', "source": '{ "o": { "a": 1, "b": 2 } }', "output": '{ "r": [1, 2] }'}],
    # --- structures profondes ----------------------------------------------------------
    "flattenobject": [
        {
            "template": '{ "r": flattenobject($.o) }',
            "source": '{ "o": { "client": { "nom": "Ana" } } }',
            "output": '{ "r": { "client.nom": "Ana" } }',
        }
    ],
    "prune": [
        {
            "template": '{ "nulls": prune($.o), "vides_aussi": prune($.o, "empty") }',
            "source": '{ "o": { "a": 1, "b": null, "c": "" } }',
            "output": '{ "nulls": { "a": 1, "c": "" }, "vides_aussi": { "a": 1 } }',
        }
    ],
    "setpath": [
        {
            "template": '{ "r": setpath($.o, "client.ville", "Lyon") }',
            "source": '{ "o": { "client": { "nom": "Ana" } } }',
            "output": '{ "r": { "client": { "nom": "Ana", "ville": "Lyon" } } }',
        }
    ],
    "unflatten": [
        {
            "template": '{ "r": unflatten($.o) }',
            "source": '{ "o": { "client.nom": "Ana" } }',
            "output": '{ "r": { "client": { "nom": "Ana" } } }',
        }
    ],
    "unsetpath": [
        {
            "template": '{ "r": unsetpath($.o, "client.secret") }',
            "source": '{ "o": { "client": { "nom": "Ana", "secret": "x" } } }',
            "output": '{ "r": { "client": { "nom": "Ana" } } }',
        }
    ],
    "walk": [
        {
            "template": '{ "r": walk($.o, when(isstring($)) { "True": upper($), "default": $ }) }',
            "source": '{ "o": { "a": "x", "b": { "c": "y" } } }',
            "output": '{ "r": { "a": "X", "b": { "c": "Y" } } }',
        }
    ],
    # --- dates --------------------------------------------------------------------------
    "dateadd": [
        {
            "template": '{ "r": dateadd($.d, "month", 2) }',
            "source": '{ "d": "2026-01-31T00:00:00" }',
            "output": '{ "r": "2026-03-31T00:00:00" }',
        }
    ],
    "datediff": [
        {
            "template": '{ "jours": datediff($.a, $.b, "day") }',
            "source": '{ "a": "2026-11-01T00:00:00", "b": "2026-11-11T00:00:00" }',
            "output": '{ "jours": 10 }',
        }
    ],
    "dateduration": [
        {
            "template": '{ "r": dateduration($.a, $.b) }',
            "source": '{ "a": "2026-01-01T00:00:00", "b": "2027-03-02T04:05:06" }',
            "output": '{ "r": { "negative": false, "years": 1, "months": 2, "days": 1, "hours": 4, "minutes": 5, "seconds": 6 } }',
        }
    ],
    "dateendof": [
        {
            "template": '{ "r": dateendof($.d, "month") }',
            "source": '{ "d": "2026-02-10T12:00:00" }',
            "output": '{ "r": "2026-02-28T23:59:59.999999" }',
        }
    ],
    "datepart": [
        {
            "template": '{ "annee": datepart($.d, "year"), "jour_semaine": datepart($.d, "dayofweek") }',
            "source": '{ "d": "2026-11-11T09:30:00" }',
            "output": '{ "annee": 2026, "jour_semaine": 3 }',
        }
    ],
    "datestartof": [
        {
            "template": '{ "r": datestartof($.d, "week") }',
            "source": '{ "d": "2026-11-11T09:30:00" }',
            "output": '{ "r": "2026-11-09T00:00:00" }',
        }
    ],
    "datesub": [
        {
            "template": '{ "r": datesub($.d, "day", 1) }',
            "source": '{ "d": "2026-03-01T00:00:00" }',
            "output": '{ "r": "2026-02-28T00:00:00" }',
        }
    ],
    "datezone": [
        {
            "template": '{ "r": datezone($.d, "Europe/Paris") }',
            "source": '{ "d": "2026-11-11T09:30:00" }',
            "output": '{ "r": "2026-11-11T09:30:00+01:00" }',
        }
    ],
    "now": [
        {
            "template": '{ "r": datepart(now(), "year") >= 2026 }',
            "source": "{}",
            "output": '{ "r": true }',
        }
    ],
    "parsedate": [
        {
            "template": '{ "culture": parsedate($.a, "fr-FR"), "masque": parsedate($.b, "", "dd/MM/yyyy") }',
            "source": '{ "a": "11/11/2026", "b": "11/11/2026" }',
            "output": '{ "culture": "2026-11-11T00:00:00", "masque": "2026-11-11T00:00:00" }',
        }
    ],
    "today": [
        {
            "template": '{ "r": datepart(today(), "hour") }',
            "source": "{}",
            "output": '{ "r": 0 }',
        }
    ],
    # --- formatage -----------------------------------------------------------------------
    "format": [
        {
            "template": '{ "nombre": format($.n, "N2", "fr-FR"), "pourcent": format($.p, "P0", "fr-FR") }',
            "source": '{ "n": 1234.5, "p": 0.25 }',
            "output": '{ "nombre": "1 234,50", "pourcent": "25 %" }',
        },
        {
            "template": '{ "date": format($.d, "dd/MM/yyyy"), "long": format($.d, "dddd d MMMM yyyy", "fr-FR") }',
            "source": '{ "d": "2026-11-11T09:30:00" }',
            "output": '{ "date": "11/11/2026", "long": "mercredi 11 novembre 2026" }',
        },
    ],
    # --- schéma --------------------------------------------------------------------------
    "schema": [
        {
            "template": '{ "r": schema($.o) }',
            "source": '{ "o": { "nom": "Ana" } }',
            "output": '{ "r": { "$schema": "http://json-schema.org/draft-04/schema#", "type": "object", "properties": { "nom": { "type": "string" } } } }',
        }
    ],
    "schemaerrors": [
        {
            "template": '{ "r": schemaerrors($.o, $.s) }',
            "source": '{ "o": { "age": "vieux" }, "s": { "type": "object", "properties": { "age": { "type": "integer" } } } }',
            "output": '{ "r": ["$.age : attendu un entier, reçu une chaîne"] }',
        }
    ],
    "schemaisvalid": [
        {
            "template": '{ "r": schemaisvalid($.o, $.s) }',
            "source": '{ "o": { "age": 42 }, "s": { "type": "object", "properties": { "age": { "type": "integer" } } } }',
            "output": '{ "r": true }',
        }
    ],
    # --- qualité et diagnostic --------------------------------------------------------------
    "isemail": [
        {
            "template": '{ "r": isemail($.t) }',
            "source": '{ "t": "ana@exemple.fr" }',
            "output": '{ "r": true }',
        }
    ],
    "isiban": [
        {
            "template": '{ "r": isiban($.t) }',
            "source": '{ "t": "FR7630006000011234567890189" }',
            "output": '{ "r": true }',
        }
    ],
    "isurl": [
        {
            "template": '{ "r": isurl($.t) }',
            "source": '{ "t": "https://exemple.fr/a" }',
            "output": '{ "r": true }',
        }
    ],
    "isuuid": [
        {
            "template": '{ "r": isuuid(uuid()) }',
            "source": "{}",
            "output": '{ "r": true }',
        }
    ],
    "require": [
        {
            "template": '{ "r": require($.n, "le montant est obligatoire") }',
            "source": '{ "n": 0 }',
            "output": '{ "r": 0 }',
        }
    ],
    "requirethat": [
        {
            "template": '{ "r": trydefault(requirethat($.n > 100, "montant trop faible"), "refusé") }',
            "source": '{ "n": 10 }',
            "output": '{ "r": "refusé" }',
        }
    ],
    "trace": [
        {
            "template": '{ "r": trace($.n, "montant") }',
            "source": '{ "n": 42 }',
            "output": '{ "r": 42 }',
        }
    ],
    "traces": [
        {
            "template": '{ "r": trace($.n, "montant"), "journal": traces() }',
            "source": '{ "n": 42 }',
            "output": '{ "r": 42, "journal": [{ "label": "montant", "value": 42 }] }',
        }
    ],
    # --- divers ----------------------------------------------------------------------------
    "param": [
        {
            "template": '{ "r": param("lot", "defaut") }',
            "source": "{}",
            "output": '{ "r": "defaut" }',
        }
    ],
    "params": [
        {
            "template": '{ "r": params() }',
            "source": "{}",
            "output": '{ "r": {} }',
        }
    ],
    "uuid": [
        {
            "template": '{ "r": stringlenght(uuid()) }',
            "source": "{}",
            "output": '{ "r": 36 }',
        }
    ],
    # --- sortie texte ---------------------------------------------------------------------
    # Ces cinq-là ne s'appellent pas dans le corps du template : le triplet montre
    # ce que rend `transform()` (la directive n'y paraît jamais), et `render` le
    # texte produit — vérifié lui aussi par la suite.
    "to_block": [
        {
            "template": '{ "$directives": { "output": { "filter": $.lignes, "mode": to_block() } }, "lignes": $.l[*] }',
            "source": '{ "l": [{ "id": 1 }, { "id": 2 }] }',
            "output": '{ "lignes": [{ "id": 1 }, { "id": 2 }] }',
            "render": '{"id":1}\n{"id":2}\n',
        }
    ],
    "to_csv": [
        {
            "template": '{ "$directives": { "output": { "filter": $.lignes, "mode": to_csv() } }, "lignes": [ { "$source": $.clients, "id": $.id, "ville": $.adr.ville } ] }',
            "source": '{ "clients": [{ "id": 1, "adr": { "ville": "Lyon" } }] }',
            "output": '{ "lignes": [{ "id": 1, "ville": "Lyon" }] }',
            "render": "id;ville\r\n1;Lyon\r\n",
        }
    ],
    "to_json": [
        {
            "template": '{ "$directives": { "output": { "mode": to_json(true) } }, "ville": $.v }',
            "source": '{ "v": "Lyon" }',
            "output": '{ "ville": "Lyon" }',
            "render": '{\n  "ville": "Lyon"\n}\n',
        }
    ],
    "to_xml": [
        {
            "template": '{ "$directives": { "output": { "filter": $.client, "mode": to_xml("client") } }, "client": { "@id": $.id, "ville": $.v } }',
            "source": '{ "id": 1, "v": "Lyon" }',
            "output": '{ "client": { "@id": 1, "ville": "Lyon" } }',
            "render": '<?xml version="1.0" encoding="utf-8"?>\n<client id="1"><ville>Lyon</ville></client>\n',
        }
    ],
    "to_yaml": [
        {
            "template": '{ "$directives": { "output": { "filter": $.client, "mode": to_yaml() } }, "client": { "id": $.id, "ville": $.v } }',
            "source": '{ "id": 1, "v": "Lyon" }',
            "output": '{ "client": { "id": 1, "ville": "Lyon" } }',
            "render": "id: 1\nville: Lyon\n",
        }
    ],
}
