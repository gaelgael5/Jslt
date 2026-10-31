# urban-json-html

*Français · [English](https://github.com/gaelgael5/Jslt/blob/main/packages/urban-json-html/README.en.md)*

Plugin [urban-json](https://github.com/gaelgael5/Jslt) : **HTML vers JSON** dans les
templates, via `loadhtml(chemin_ou_url)` (port de `ServiceHtml`, .NET). Aucune
dépendance : `html.parser` de la bibliothèque standard.

```bash
pip install urban-json-html
```

Forme produite (celle du .NET, HtmlAgilityPack) :

```json
{ "#id": "#document", "content": { "#id": "p", "class": "x", "content": "#text: Bonjour" } }
```

- élément → `{"#id": balise, attributs…, "content": enfant | [enfants]}` ;
- texte → `"#text: …"` (blancs seuls ignorés, entités conservées) ;
- commentaire et `<!DOCTYPE>` → `"#comment: …"`.

`loadhtml` accepte un fichier (chemin ou URI `file://`) ou une URL `http(s)://`
(délai de 30 s). Attention aux URL issues de données non fiables (SSRF).
