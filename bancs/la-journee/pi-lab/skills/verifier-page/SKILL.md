---
name: verifier-page
description: Use after writing or editing any HTML page with JavaScript, before saying it works. Checks every inline and local script for syntax errors with node.
---

# Vérifier une page web

Avant de dire qu'une page marche, lance :

    node ~/pi-lab/skills/verifier-page/check.mjs CHEMIN/index.html

- `OK` : aucun script ne contient d'erreur de syntaxe.
- Sinon, le script fautif et la ligne sont affichés : corrige, puis relance jusqu'à `OK`.

Ce contrôle ne voit pas les erreurs qui n'arrivent qu'à l'exécution (variable `const` réassignée, élément introuvable). Relis donc aussi les variables modifiées dans la boucle principale : une variable réassignée doit être déclarée avec `let`.
