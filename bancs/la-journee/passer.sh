#!/bin/sh
# Passe les épreuves de « La journée » avec l'agent Pi, une à la fois, sur la machine où tourne ton modèle.
# Usage : sh passer.sh [01-mails 02-contrat …]   (après sh pi-lab/installer.sh ; sans argument : les 8 épreuves)
# Mêmes options que dans la vidéo : config isolée ~/pi-lab, 5 skills, outils read,bash,edit,write, sans extensions ni MCP.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LIST=${*:-$(cd "$HERE/epreuves" && ls *.md | sed 's/\.md$//')}
PI_LAB="${PI_LAB:-$HOME/pi-lab}"; SK="$PI_LAB/skills"
SKILLS=""; for s in verification-before-completion systematic-debugging efficient-testing frontend-design verifier-page; do
  [ -d "$SK/$s" ] && SKILLS="$SKILLS --skill $SK/$s"; done
for e in $LIST; do
  R="$HERE/resultats/$e"; rm -rf "$R"; mkdir -p "$R/fichiers"
  [ -d "$HERE/dossiers/$e" ] && cp -R "$HERE/dossiers/$e/." "$R/fichiers/"
  debut=$(date +%s)
  (cd "$R/fichiers" && PI_CODING_AGENT_DIR="$PI_LAB" PI_OFFLINE=1 pi --no-extensions --no-mcp $SKILLS --no-context-files \
     --no-prompt-templates --tools read,bash,edit,write "$(cat "$HERE/epreuves/$e.md")") > "$R/pi.log" 2>&1
  echo "$(( $(date +%s) - debut ))" > "$R/duree-s.txt"
  echo "$e : $(cat "$R/duree-s.txt") s ; fichiers : $(ls "$R/fichiers" | tr '\n' ' ')"
done
echo "Fini. Contrôles automatiques : python3 noter.py ; puis compare chaque reponse.md à corriges/."
