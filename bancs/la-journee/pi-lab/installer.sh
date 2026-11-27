#!/bin/sh
# Installe la configuration Pi du banc « La journée » dans ~/pi-lab, avec ses 5 skills, sur la machine où tourne le modèle.
# Usage : sh installer.sh [URL_API] [ID_MODELE]   (par défaut http://127.0.0.1:8080/v1 et inkling-2-mini-sq-10)
# Prérequis : Pi installé (commande `pi`), et les skills verification-before-completion, systematic-debugging,
# efficient-testing et frontend-design présents dans ~/.pi/agent/skills.
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
API="${1:-http://127.0.0.1:8080/v1}"; MODELE="${2:-inkling-2-mini-sq-10}"
L="${PI_LAB:-$HOME/pi-lab}"
mkdir -p "$L/skills"
cp -R "$HERE/skills/verifier-page" "$L/skills/"
for s in verification-before-completion systematic-debugging efficient-testing frontend-design; do
  if [ -d "$HOME/.pi/agent/skills/$s" ]; then
    rm -rf "$L/skills/$s"; cp -R "$HOME/.pi/agent/skills/$s" "$L/skills/"
    sed -i.bak "/^disable-model-invocation:/d" "$L/skills/$s/SKILL.md" && rm -f "$L/skills/$s/SKILL.md.bak"
  else
    echo "skill absent, ignoré : $s"
  fi
done
rm -f "$L/skills/systematic-debugging/"test-*.md "$L/skills/systematic-debugging/CREATION-LOG.md"
cat > "$L/models.json" <<J
{"providers":{"local":{"baseUrl":"$API","api":"openai-completions","apiKey":"local","compat":{"supportsDeveloperRole":false,"supportsReasoningEffort":false},"models":[{"id":"$MODELE","name":"$MODELE (local)","reasoning":true,"input":["text"],"contextWindow":131072,"maxTokens":16384,"cost":{"input":0,"output":0,"cacheRead":0,"cacheWrite":0}}]}}}
J
echo "{\"defaultProvider\":\"local\",\"defaultModel\":\"$MODELE\",\"quietStartup\":true}" > "$L/settings.json"
ls "$L/skills"
