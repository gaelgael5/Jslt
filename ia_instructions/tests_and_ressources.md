# Ressources de test attribuées

Mémoire des ressources mises à disposition de ce workspace (`urban-json`) : on
ajoute à chaque attribution, on retire quand la ressource est reprise. Les règles
d'usage sont dans le standard des machines de test, pas ici.

## Machines de test

| Alias SSH | Nom d'hôte réel | Adresses | Usage | Depuis |
|---|---|---|---|---|
| `test1` | `host-test-37` | mesh 100.74.9.236 (rebond `devflow-jump` 100.74.13.151) | Playground urban-json : clone `~/urban-json` (branche `dev`), `./dev-deploy.sh`, port 8095 | 2026-10-31 |

Notes sur `test1` :

- **L'alias a été recyclé** : il désignait `host-test-36` (mesh 100.74.129.165)
  jusqu'au 2026-10-22 ; depuis le 2026-10-31 il pointe `host-test-37`, une autre
  machine, sans clone ni stack urban-json au départ. Vérifier le nom d'hôte réel
  avant tout déploiement reste la seule façon de ne pas se tromper de cible.
- Machine **partagée** avec d'autres stacks (miles, miles-enrolement,
  miles-environnement, tutor, tutor-mobile, photoreader) : le port 8080 y est
  pris par `miles-frontend`, d'où `PLAYGROUND_PORT=8095` dans le `.env` de
  l'instance (posé au premier déploiement par `PLAYGROUND_PORT=8095 ./dev-deploy.sh`).
- Services standard présents : `browserless-chromium` (port 3000, API
  `POST /function`, TOKEN vide — pas de jeton à passer), collecteurs
  `devpod-alloy-agent` / `devpod-alloy-metrics`.
- **Provisionnement incomplet à l'arrivée** : `/etc/git/` était absent, donc le
  durcissement `harden-git-http.sh` (étape A.10e, HTTP/1.1 forcé vers github.com)
  n'avait pas été appliqué — et `git` y est en 2.39.5, la version qui échoue par
  intermittence en HTTP/2 sur le `POST git-upload-pack`. Posé à la main au niveau
  système (`/etc/git/http2-github.inc` inclus depuis `/etc/gitconfig`) avant de
  cloner ; à rejouer si la machine est reconstruite, et à signaler côté image de
  machine de test plutôt qu'à contourner dans `dev-deploy.sh`.
- Accès par rebond `devflow-jump` matérialisé par le portail dans
  `~/.ssh/config` (bloc `portal test-vm test1`) : il disparaît si la machine
  n'est plus partagée avec ce workspace.

## Services exposés à l'annuaire

| Service | Cible | URL publique |
|---|---|---|
| `urban-json-urban-json` | 100.74.9.236:8095 | `https://svc-urban-json-urban-json.yoops.org/` (derrière la session du portail `dev.yoops.org`) |
