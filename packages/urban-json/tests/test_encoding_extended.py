"""Empreintes, URL, HTML, hexadécimal — sujet « encodage et empreintes ».

Le moteur savait faire base64, crc32, sha256 et sha512 ; il manquait de quoi
écrire une URL, échapper du HTML, ou signer un message (HMAC).
"""

from __future__ import annotations

import pytest

from urban_json import JsltTemplate
from urban_json.errors import JsltError


def run(template: str, source=None):
    return JsltTemplate.parse(template).transform(source)


def test_md5_et_sha1():
    source = {"t": "abc"}
    assert run('{ "a": md5($.t), "b": sha1($.t) }', source) == {
        "a": "900150983cd24fb0d6963f7d28e17f72",
        "b": "a9993e364706816aba3e25717850c26c9cd0d89d",
    }


def test_hmacsha256():
    # Vecteur de test RFC 4231 (clé « key », message « The quick brown fox... »).
    source = {"m": "The quick brown fox jumps over the lazy dog", "k": "key"}
    assert run('{ "r": hmacsha256($.m, $.k) }', source) == {
        "r": "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"
    }


def test_hmacsha256_sans_clef_leve():
    with pytest.raises(JsltError, match="clé"):
        run('{ "r": hmacsha256($.m, $.k) }', {"m": "x"})


def test_urlencode_et_urldecode():
    source = {"t": "a b/c?d=é"}
    encoded = run('{ "r": urlencode($.t) }', source)["r"]
    assert encoded == "a%20b%2Fc%3Fd%3D%C3%A9"
    assert run('{ "r": urldecode($.t) }', {"t": encoded}) == {"r": "a b/c?d=é"}


def test_urlencode_garde_le_chemin_sur_demande():
    assert run('{ "r": urlencode($.t, "path") }', {"t": "a b/c"}) == {"r": "a%20b/c"}


def test_urlencode_mode_inconnu_leve():
    with pytest.raises(JsltError, match="mode"):
        run('{ "r": urlencode($.t, "zzz") }', {"t": "a"})


def test_htmlescape_et_htmlunescape():
    source = {"t": '<a href="x">p & q</a>'}
    escaped = run('{ "r": htmlescape($.t) }', source)["r"]
    assert escaped == "&lt;a href=&quot;x&quot;&gt;p &amp; q&lt;/a&gt;"
    assert run('{ "r": htmlunescape($.t) }', {"t": escaped}) == {"r": source["t"]}


def test_hexencode_et_hexdecode():
    assert run('{ "r": hexencode($.t) }', {"t": "abc"}) == {"r": "616263"}
    assert run('{ "r": hexdecode($.t) }', {"t": "616263"}) == {"r": "abc"}


def test_hexdecode_invalide_leve():
    with pytest.raises(JsltError, match="hexadécimal"):
        run('{ "r": hexdecode($.t) }', {"t": "zz"})


@pytest.mark.parametrize(
    "call",
    ["md5($.t)", "sha1($.t)", "urlencode($.t)", "urldecode($.t)", "htmlescape($.t)",
     "htmlunescape($.t)", "hexencode($.t)", "hexdecode($.t)", "hmacsha256($.t, $.k)"],
)
def test_null_reste_null(call):
    assert run('{ "r": ' + call + ' }', {"k": "k"}) == {"r": None}


def test_empreinte_d_un_objet_passe_par_son_json():
    # Même convention que sha256 : un objet est haché via son JSON compact.
    source = {"o": {"a": 1}}
    assert run('{ "r": md5($.o) }', source) == {"r": run('{ "r": md5($.t) }', {"t": '{"a":1}'})["r"]}


def test_exemple_complet_url_signee():
    template = (
        '{ "url": concat(["https://x/?q=", urlencode($.q)]), '
        '"signature": hmacsha256($.q, $.secret) -> substring(0, 16) }'
    )
    result = run(template, {"q": "a b", "secret": "s3cr3t"})
    assert result["url"] == "https://x/?q=a%20b"
    assert len(result["signature"]) == 16
