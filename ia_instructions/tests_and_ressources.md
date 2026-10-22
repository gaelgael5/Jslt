# Ressources de test attribuées

Mémoire des ressources mises à disposition de ce workspace (`urban-json`) : on
ajoute à chaque attribution, on retire quand la ressource est reprise. Les règles
d'usage sont dans le standard des machines de test, pas ici.

## Machines de test

| Alias SSH | Nom d'hôte réel | Adresses | Usage | Depuis |
|---|---|---|---|---|
| `test1` | `host-test-36` | LAN 192.168.10.203 · mesh 100.74.129.165 | Playground urban-json : clone `~/urban-json` (branche `dev`), `./dev-deploy.sh`, port 8095 | 2026-10-22 |

Notes sur `test1` :

- Machine **partagée** avec d'autres stacks (miles, harpocrate, tutor,
  photoreader) : le port 8080 y est pris, d'où `PLAYGROUND_PORT=8095` dans le
  `.env` de l'instance.
- Services standard présents : `browserless-chromium` (port 3000, API
  `POST /function`), collecteurs `devpod-alloy-agent` / `devpod-alloy-metrics`.
- Accès par rebond `devflow-jump` matérialisé par le portail dans
  `~/.ssh/config` (bloc `portal test-vm test1`) : il disparaît si la machine
  n'est plus partagée avec ce workspace.

## Services exposés à l'annuaire

| Service | Cible | URL publique |
|---|---|---|
| `urban-json-urban-json` | 100.74.129.165:8095 | `https://svc-urban-json-urban-json.dev.yoops.org/` |
