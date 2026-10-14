#!/usr/bin/env bash
#
# Régénère le parser Python depuis les grammaires ANTLR (grammar/*.g4).
#
# La sortie (src/jslt/_antlr/) est versionnée afin que la librairie fonctionne
# sans l'outil ANTLR : seule l'évolution de la grammaire nécessite de relancer
# ce script.
#
# Prérequis :
#   - Java (pour l'outil ANTLR)
#   - Le jar complet ANTLR, par défaut tools/antlr-<version>-complete.jar
#     (non versionné ; ce script le télécharge si absent)
#   - Le runtime Python correspondant : pip install antlr4-python3-runtime==<version>
#
set -euo pipefail

ANTLR_VERSION="${ANTLR_VERSION:-4.13.2}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JAR="${ANTLR_JAR:-$ROOT/tools/antlr-${ANTLR_VERSION}-complete.jar}"
GRAMMAR_DIR="$ROOT/grammar"
OUT_DIR="$ROOT/src/jslt/_antlr"

if [[ ! -f "$JAR" ]]; then
    echo "ANTLR jar introuvable ($JAR) — téléchargement depuis Maven Central…"
    mkdir -p "$(dirname "$JAR")"
    curl -fsSL -o "$JAR" \
        "https://repo1.maven.org/maven2/org/antlr/antlr4/${ANTLR_VERSION}/antlr4-${ANTLR_VERSION}-complete.jar"
fi

echo "Génération du parser Python (ANTLR ${ANTLR_VERSION}) → $OUT_DIR"
mkdir -p "$OUT_DIR"

# Le lexer et le parser doivent être générés ensemble : JsltParser référence
# tokenVocab=JsltLexer.
java -jar "$JAR" \
    -Dlanguage=Python3 \
    -visitor \
    -o "$OUT_DIR" \
    -Xexact-output-dir \
    "$GRAMMAR_DIR/JsltLexer.g4" \
    "$GRAMMAR_DIR/JsltParser.g4"

# Rend le dossier généré importable.
touch "$OUT_DIR/__init__.py"

echo "Terminé. Fichiers générés :"
ls -1 "$OUT_DIR"
