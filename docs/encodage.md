# Encodage, empreintes et échappement — guide jslt

*Français · [English](encodage.en.md)*

[← Guide jslt](guide.md) · les exemples de cette page sont **exécutés par la
suite de tests** (`tests/test_guide_examples.py`), sous la forme de triplets
*template → entrée → sortie*.

---

Ces fonctions opèrent sur la **représentation chaîne** de la valeur : un
scalaire est converti en texte, un objet ou un tableau en JSON compact. `null`
donne `null`.

| Fonction | Rôle |
|---|---|
| `tobase64(v)` / `frombase64(t)` | Base64 d'un texte UTF-8 |
| `hexencode(v)` / `hexdecode(t)` | octets UTF-8 en hexadécimal |
| `urlencode(v, mode)` / `urldecode(t)` | encodage pour URL (`mode` = `all` ou `path`) |
| `htmlescape(v)` / `htmlunescape(t)` | `<`, `>`, `&`, `"`, `'` |
| `crc32(v)` | somme de contrôle, entier non signé |
| `sha256(v)`, `sha512(v)` | empreintes, hexadécimal minuscule |
| `md5(v)`, `sha1(v)` | empreintes **d'identité** (voir ci-dessous) |
| `hmacsha256(v, clé)` | **signature** avec un secret |

**`md5` et `sha1` ne signent rien.** Ils sont cassés pour cet usage. Ils ne sont
là que pour l'identité : clé de déduplication, nom de fichier stable,
comparaison avec un système existant qui les impose.

**Pour signer, c'est `hmacsha256`.** Concaténer un secret et un message avant un
`sha256` — ce qu'on écrit faute de HMAC — expose à l'extension de longueur. La
fonction manquait, donc les templates faisaient le mauvais montage. Une clé vide
est **refusée** : elle produirait une signature valide et sans valeur.

```jslt
{
  "empreinte": sha256($.message),
  "signature": hmacsha256($.message, $.secret)
}
```

```json
{ "message": "The quick brown fox jumps over the lazy dog", "secret": "key" }
```

```json
{
  "empreinte": "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
  "signature": "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"
}
```

**URL.** `urlencode` échappe tout par défaut, y compris les `/`. Le mode `path`
les conserve, pour encoder un segment de chemin sans casser le chemin.

```jslt
{
  "tout": urlencode($.t),
  "chemin": urlencode($.t, "path"),
  "retour": urlencode($.t) -> urldecode()
}
```

```json
{ "t": "dossier a/fichier é.txt" }
```

```json
{
  "tout": "dossier%20a%2Ffichier%20%C3%A9.txt",
  "chemin": "dossier%20a/fichier%20%C3%A9.txt",
  "retour": "dossier a/fichier é.txt"
}
```

**HTML.** `htmlescape` échappe aussi les guillemets (simples et doubles), ce qui
le rend sûr dans une valeur d'attribut et pas seulement dans du texte.

```jslt
{ "sur": htmlescape($.t) }
```

```json
{ "t": "<a href=\"x\">p & q</a>" }
```

```json
{ "sur": "&lt;a href=&quot;x&quot;&gt;p &amp; q&lt;/a&gt;" }
```

**Empreinte d'un objet.** La valeur passe par son JSON compact, clés dans
l'ordre du document : deux objets aux mêmes clés écrites dans un ordre différent
n'ont donc **pas** la même empreinte. Pour une empreinte stable, trier les clés
en amont (par exemple via `entries` + `sort` + `fromentries`).

---

**Voir aussi** : [Texte](texte.md) pour découper et plier une chaîne,
[Types](types.md) pour lire du JSON encodé.

---

[← Guide jslt](guide.md)
