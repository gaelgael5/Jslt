#!/usr/bin/env bash
# Déploie le playground urban-json sur une machine de test (branche dev).
#
# Usage (depuis le clone du dépôt sur la machine) :
#   ./dev-deploy.sh                 # déploiement normal
#   ./dev-deploy.sh --no-detach     # CI / débogage : sans le filet anti-raccrochage
#   ./dev-deploy.sh --exposer-seulement
#                                   # stack déjà en place : santé + déclaration seules
#
# Déclaration à l'annuaire du portail (dernière étape utile, après la santé) :
# active seulement si PORTAL_TOKEN est dans l'environnement — code TOTP
# « <login>:<code> » obtenu par l'outil MCP `totp_code`, valable 30 s, jamais
# écrit dans .env ni dans le journal. Comme il expire bien avant la fin d'un
# build, on enchaîne en pratique : ./dev-deploy.sh, puis un code frais et
# ./dev-deploy.sh --exposer-seulement.
#
# Prérequis : git, docker (+ plugin compose v2), curl, et l'accès réseau au dépôt
# GitHub — le script se met à jour depuis origin/dev avant tout, il n'existe pas
# de mode « déployer ce qui est déjà là ».
#
# Pas de base de données dans cette stack : aucune migration à jouer.
set -euo pipefail

BRANCH="dev"
SERVICE="playground"
STEPS=9
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$REPO_DIR/deploy-logs"
PRUNE_STAMP="$LOG_DIR/.last-prune"
cd "$REPO_DIR"

DETACH=1
EXPOSE_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --no-detach) DETACH=0 ;;
    --exposer-seulement) EXPOSE_ONLY=1 ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "Option inconnue : $arg" >&2; exit 2 ;;
  esac
done

# --- 0. Survivre à la perte de la session -----------------------------------
# Le script arrête la stack : si le terminal tombe (mobile, session web) entre
# l'arrêt et la relance, SIGHUP le tuerait et laisserait la stack à terre. On
# ignore donc HUP et on journalise tout dans un fichier, avec `tee -p` qui
# continue d'écrire le fichier même quand le terminal a disparu.
mkdir -p "$LOG_DIR"
if [[ "$DETACH" == 1 && -z "${DEV_DEPLOY_LOGGING:-}" ]]; then
  export DEV_DEPLOY_LOGGING=1
  export DEV_DEPLOY_LOG="$LOG_DIR/deploy-$(date +%Y%m%d-%H%M%S).log"
  trap '' HUP PIPE
  exec > >(tee -a -p "$DEV_DEPLOY_LOG") 2>&1
  echo "Journal du déploiement : $DEV_DEPLOY_LOG"
fi

step() { echo; echo "=== [$1/$STEPS] $2"; }
die()  { echo "ERREUR : $*" >&2; exit 1; }

# --- 1. Prérequis --------------------------------------------------------------
step 1 "Prérequis"
command -v git  >/dev/null || die "git introuvable — sudo apt-get install -y git"
command -v curl >/dev/null || die "curl introuvable — sudo apt-get install -y curl"
command -v docker >/dev/null || die "docker introuvable — https://docs.docker.com/engine/install/"
docker compose version >/dev/null 2>&1 \
  || die "plugin docker compose v2 introuvable — sudo apt-get install -y docker-compose-plugin"
docker info >/dev/null 2>&1 \
  || die "le démon docker ne répond pas, ou droits insuffisants — sudo usermod -aG docker \$USER (puis reconnexion)"
echo "OK : $(docker compose version --short) / $(git --version)"

# --- 2. Mise à jour depuis le dépôt, puis ré-exécution ---------------------------
# Sans ré-exécution, on déploierait le code neuf avec un script, un compose et un
# Dockerfile périmés. DEV_DEPLOY_REEXEC évite de boucler.
step 2 "Mise à jour depuis origin/$BRANCH"
if [[ -z "${DEV_DEPLOY_REEXEC:-}" ]]; then
  [[ -z "$(git status --porcelain --untracked-files=no)" ]] \
    || die "modifications locales sur la machine (git status) : aucune retouche à la main n'est admise, tout passe par le dépôt"
  before="$(git rev-parse HEAD)"
  git fetch --prune origin "$BRANCH"
  git checkout -q "$BRANCH"
  git merge --ff-only -q "origin/$BRANCH" \
    || die "la branche locale a divergé d'origin/$BRANCH — reclone la branche dev"
  after="$(git rev-parse HEAD)"
  if [[ "$before" != "$after" ]]; then
    echo "Mis à jour ${before:0:7} -> ${after:0:7} : relance avec la version récupérée"
    export DEV_DEPLOY_REEXEC=1
    exec "$REPO_DIR/dev-deploy.sh" "$@"
  fi
fi
echo "Déploiement de $(git log -1 --format='%h %s')"

# --- 3. Configuration : compléter .env sans écraser l'existant --------------------
step 3 "Configuration (.env)"
touch .env
env_get() { grep "^$1=" .env | tail -1 | cut -d= -f2-; }
env_default() { grep -q "^$1=" .env || echo "$1=$2" >> .env; }
# Isolation sur VM partagée : nom de stack et port paramétrés, jamais en dur.
env_default COMPOSE_PROJECT_NAME urban-json
env_default PLAYGROUND_PORT 8080
# Cible de la déclaration à l'annuaire (le jeton, lui, n'est jamais ici).
env_default EXPOSE_PORTAL_URL https://dev.yoops.org
env_default EXPOSE_WORKSPACE urban-json
PORT="$(env_get PLAYGROUND_PORT)"
STACK="$(env_get COMPOSE_PROJECT_NAME)"
export COMPOSE_PROJECT_NAME="$STACK"
echo "Stack : $STACK — port publié : $PORT"

if [[ "$EXPOSE_ONLY" == 1 ]]; then
  echo "--exposer-seulement : étapes 4 à 6 sautées (stack supposée en place)"
else

# --- 4. Construction --------------------------------------------------------------
# Construire ici, depuis la copie fraîche du dépôt, est la vraie validation de
# l'image : jamais d'image réutilisée d'ailleurs.
step 4 "Construction de l'image"
docker compose build --pull

# --- 5. Arrêt (orphelins compris) puis contrôle du port ---------------------------
# Le port se sonde APRÈS l'arrêt : avant, on prendrait notre propre conteneur
# pour un conflit.
step 5 "Arrêt de la stack et contrôle du port"
docker compose down --remove-orphans
if (exec 3<>"/dev/tcp/127.0.0.1/$PORT") 2>/dev/null; then
  die "le port $PORT est occupé par un autre service après l'arrêt de la stack — change PLAYGROUND_PORT dans .env (diagnostic : sudo ss -ltnp 'sport = :$PORT')"
fi
echo "Port $PORT libre"

# --- 6. Lancement, attente d'un conteneur réellement en marche --------------------
step 6 "Lancement"
docker compose up -d
for _ in $(seq 1 30); do
  state="$(docker compose ps --format '{{.State}}' "$SERVICE" 2>/dev/null || true)"
  [[ "$state" == "running" ]] && break
  sleep 2
done
[[ "${state:-}" == "running" ]] \
  || die "le conteneur $SERVICE n'est pas en marche (état : ${state:-absent}) — docker compose logs $SERVICE"
echo "Conteneur $SERVICE en marche"
fi

# --- 7. Contrôle de santé, plafonné, sur le port réellement publié ----------------
step 7 "Contrôle de santé (http://127.0.0.1:$PORT/healthz)"
ok=0
for _ in $(seq 1 45); do
  if curl -fsS --max-time 2 "http://127.0.0.1:$PORT/healthz" | grep -q '"ok"'; then ok=1; break; fi
  sleep 2
done
[[ "$ok" == 1 ]] || die "pas de réponse saine en 90 s — docker compose logs --tail=100 $SERVICE"
echo "Service sain : http://$(hostname -f 2>/dev/null || hostname):$PORT/"

# --- 8. Déclaration à l'annuaire du portail (best-effort) ---------------------------
# Après la santé : on ne publie pas une stack qui ne répond pas. Nom du service =
# nom de la stack, pour que le lien de la machine retrouve l'exposition. Voie
# --me : enregistrée sous le workspace de l'appelant authentifié par son TOTP.
step 8 "Déclaration à l'annuaire"
if [[ -n "${PORTAL_TOKEN:-}" ]]; then
  TARGET_HOST="$(hostname -I 2>/dev/null | awk '{print $1}')"
  bash "$REPO_DIR/scripts/declarer-exposition.sh" --me \
    --portal "$(env_get EXPOSE_PORTAL_URL)" \
    --workspace "$(env_get EXPOSE_WORKSPACE)" \
    --service "$STACK" \
    --target-host "$TARGET_HOST" \
    --target-port "$PORT" \
    --host "$(hostname)"
else
  echo "PORTAL_TOKEN absent : pas de déclaration (relancer avec un code TOTP et --exposer-seulement)"
fi

# --- 9. Purge disque hebdomadaire (ne fait jamais échouer le déploiement) ---------
# Chaque build laisse des couches détaggées que rien ne récupère. Portée limitée
# au cache de build et aux images détaggées ; jamais les volumes ni les images de
# base. Témoin horodaté : au plus une fois par semaine.
step 9 "Purge disque (hebdomadaire)"
if [[ "$EXPOSE_ONLY" == 1 ]]; then
  echo "--exposer-seulement : pas de purge"
elif [[ ! -f "$PRUNE_STAMP" ]] || [[ -n "$(find "$PRUNE_STAMP" -mtime +6 2>/dev/null)" ]]; then
  {
    echo "Avant : $(df -h / | awk 'NR==2{print $4}') libres"
    docker builder prune -f --filter until=168h
    docker image prune -f
    echo "Après : $(df -h / | awk 'NR==2{print $4}') libres"
    touch "$PRUNE_STAMP"
  } || echo "AVERTISSEMENT : purge en échec (déploiement non affecté)"
else
  echo "Dernière purge il y a moins d'une semaine : rien à faire"
fi

echo
echo "Déploiement terminé."
