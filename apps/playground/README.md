# jslt playground

Petite application web de **test/démo** pour `jslt` : on saisit un template jslt
(éditeur avec **coloration syntaxique + intellisense** via le composant
[`jslt-editor`](../../packages/jslt-editor/)) et un document JSON source, et on voit
le résultat transformé par le **vrai moteur** côté serveur (FastAPI).

Ce n'est pas une distribution publiée — c'est une application du dépôt.

Fonctionnalités : éditeur avec coloration + intellisense, **bibliothèque
d'exemples**, **transformation automatique** (debounce, désactivable), **partage
par URL** (l'état est encodé dans le lien), **panneau de référence** des fonctions
disponibles (filtrable).

## Lancer en local

```bash
pip install -e "apps/playground[dev]"      # tire jslt, jslt-editor, fastapi, uvicorn
uvicorn jslt_playground.app:app --reload
# puis http://127.0.0.1:8000
```

## Sécurité

Le playground n'exécute que les **fonctions du cœur**. Les plugins d'E-S (CSV, XML,
SQL, HTTP, Elasticsearch) ne sont **pas** chargés : un template arbitraire ne peut
donc ni lire les fichiers du serveur, ni émettre de requêtes (SSRF), ni exécuter de
SQL. Techniquement, un registre isolé (copie du registre cœur, sans plugins) est
passé à chaque `transform`.

L'application n'est pas durcie pour un hébergement public (pas de limite de débit,
pas de timeout d'exécution) ; pour un déploiement exposé, ajouter ces garde-fous.

## Endpoints

| Méthode | Chemin | Rôle |
|---|---|---|
| `POST` | `/api/transform` | `{template, source}` → `{result}` ou `{error}` |
| `GET` | `/api/functions` | catalogue des fonctions (cœur) pour l'intellisense |
| `GET` | `/api/examples` | exemples prêts à charger (template + source) |
| `GET` | `/jslt-editor/*` | assets du composant d'édition |
| `GET` | `/` | la page du playground |

## Licence

Apache-2.0.
