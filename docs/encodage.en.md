# Encoding, digests and escaping — jslt guide

*[Français](encodage.md) · English*

[← jslt guide](guide.en.md) · the examples on this page are **run by the test
suite** (`tests/test_guide_examples.py`) as *template → input → output* triples.

---

These functions work on the **string representation** of the value: a scalar is
converted to text, an object or array to compact JSON. `null` yields `null`.

| Function | Purpose |
|---|---|
| `tobase64(v)` / `frombase64(t)` | Base64 of UTF-8 text |
| `hexencode(v)` / `hexdecode(t)` | UTF-8 bytes as hexadecimal |
| `urlencode(v, mode)` / `urldecode(t)` | URL encoding (`mode` = `all` or `path`) |
| `htmlescape(v)` / `htmlunescape(t)` | `<`, `>`, `&`, `"`, `'` |
| `crc32(v)` | checksum, unsigned integer |
| `sha256(v)`, `sha512(v)` | digests, lowercase hexadecimal |
| `md5(v)`, `sha1(v)` | **identity** digests (see below) |
| `hmacsha256(v, key)` | **signature** with a secret |

**`md5` and `sha1` sign nothing.** They are broken for that purpose. They are
here for identity only: a deduplication key, a stable file name, comparison with
an existing system that mandates them.

**To sign, use `hmacsha256`.** Concatenating a secret and a message before a
`sha256` — what people write when HMAC is missing — is exposed to length
extension. The function was missing, so templates were doing the wrong
construction. An empty key is **refused**: it would produce a valid, worthless
signature.

```jslt
{
  "digest": sha256($.message),
  "signature": hmacsha256($.message, $.secret)
}
```

```json
{ "message": "The quick brown fox jumps over the lazy dog", "secret": "key" }
```

```json
{
  "digest": "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
  "signature": "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"
}
```

**URLs.** `urlencode` escapes everything by default, including `/`. The `path`
mode keeps them, so you can encode a path segment without breaking the path.

```jslt
{
  "all": urlencode($.t),
  "path": urlencode($.t, "path"),
  "back": urlencode($.t) -> urldecode()
}
```

```json
{ "t": "folder a/file é.txt" }
```

```json
{
  "all": "folder%20a%2Ffile%20%C3%A9.txt",
  "path": "folder%20a/file%20%C3%A9.txt",
  "back": "folder a/file é.txt"
}
```

**HTML.** `htmlescape` also escapes quotes (single and double), which makes it
safe inside an attribute value and not only in text.

```jslt
{ "safe": htmlescape($.t) }
```

```json
{ "t": "<a href=\"x\">p & q</a>" }
```

```json
{ "safe": "&lt;a href=&quot;x&quot;&gt;p &amp; q&lt;/a&gt;" }
```

**Digest of an object.** The value goes through its compact JSON, keys in
document order: two objects with the same keys written in a different order do
**not** share a digest. For a stable digest, sort the keys first (for example
with `entries` + `sort` + `fromentries`).

---

**See also**: [Text](texte.en.md) to cut and fold a string, [Types](types.en.md)
to read encoded JSON.

---

[← jslt guide](guide.en.md)
