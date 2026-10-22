#!/usr/bin/env bash
# Déploie le playground urban-json sur une machine de test (branche dev).
#
# Usage (depuis le clone du dépôt sur la machine) :
#   ./dev-deploy.sh                 # déploiement normal
#   ./dev-deploy.sh --no-detach     # CI / débogage : sans le filet anti-raccrochage
#
# Prérequis : git, docker (+ plugin compose v2), curl, et l'accès réseau au dépôt
# GitHub — le script se met à jour depuis origin/dev avant tout, il n'existe pas
# de mode « déployer ce qui est déjà là ».
#
# Pas de base de données dans cette stack : aucune migration à jouer.
set -euo pipefail

BRANCH="dev"
SERVICE="playground"
STEPS=8
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$REPO_DIR/deploy-logs"
PRUNE_STAMP="$LOG_DIR/.last-prune"
cd "$REPO_DIR"

DETACH=1
for arg in "$@"; do
  case "$arg" in
    --no-detach) DETACH=0 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
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
grep -q '^PLAYGROUND_PORT=' .env || echo "PLAYGROUND_PORT=8080" >> .env
PORT="$(grep '^PLAYGROUND_PORT=' .env | tail -1 | cut -d= -f2)"
echo "Port publié : $PORT"

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

# --- 7. Contrôle de santé, plafonné, sur le port réellement publié ----------------
step 7 "Contrôle de santé (http://127.0.0.1:$PORT/healthz)"
ok=0
for _ in $(seq 1 45); do
  if curl -fsS --max-time 2 "http://127.0.0.1:$PORT/healthz" | grep -q '"ok"'; then ok=1; break; fi
  sleep 2
done
[[ "$ok" == 1 ]] || die "pas de réponse saine en 90 s — docker compose logs --tail=100 $SERVICE"
echo "Service sain : http://$(hostname -f 2>/dev/null || hostname):$PORT/"

# --- 8. Purge disque hebdomadaire (ne fait jamais échouer le déploiement) ---------
# Chaque build laisse des couches détaggées que rien ne récupère. Portée limitée
# au cache de build et aux images détaggées ; jamais les volumes ni les images de
# base. Témoin horodaté : au plus une fois par semaine.
step 8 "Purge disque (hebdomadaire)"
if [[ ! -f "$PRUNE_STAMP" ]] || [[ -n "$(find "$PRUNE_STAMP" -mtime +6 2>/dev/null)" ]]; then
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
