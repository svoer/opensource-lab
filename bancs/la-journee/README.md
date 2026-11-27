# Banc « La journée » · une journée avec une IA locale (27 novembre 2026)

Sur YouTube, on voit surtout des IA locales faire de la 3D ou des démos de pointe. Ce banc teste plutôt ce que des gens normaux font tous les jours, en montant jusqu'au développeur. Inspiré de Build & Mind (une mission comme fil rouge), Luke's Dev Lab (tests vivants, agent sur un vrai projet, carte PASS), Matthew Berman (réponse connue d'avance), Bijan Bowen (un prompt, une correction permise), Tina Huang (verdict par profil).

| Heure | Épreuve | Pour qui | Prompt | Correction |
| --- | --- | --- | --- | --- |
| 8 h | Les mails | Tout le monde | [01-mails](epreuves/01-mails.md) | 3 urgents cachés parmi 30, 4 fausses urgences publicitaires |
| 9 h | Le contrat | Tout le monde | [02-contrat](epreuves/02-contrat.md) | préavis 1 mois (zone tendue), lettre avant le 31/12, 850 €, dépôt 780 € sous 1 mois |
| 12 h | Les repas | Tout le monde | [03-repas](epreuves/03-repas.md) | total ≤ 80 € recalculé, aucun fruit à coque |
| 14 h | La réunion | Au boulot | [04-reunion](epreuves/04-reunion.md) | 6 décisions cachées, 1 idée abandonnée à ne pas lister |
| 15 h | Les comptes | Au boulot | [05-comptes](epreuves/05-comptes.md) | totaux par catégorie et par mois au centime |
| 17 h | Les devoirs | Parents | [06-devoirs](epreuves/06-devoirs.md) | 204 €, 224,40 €, 228 € : pas le même prix |
| 18 h | Le Tetris Game Boy | Bricoleurs | [07-tetris](epreuves/07-tetris.md) | jouable à l'écran, palette 4 verts, une correction permise |
| 21 h | Le vrai bug | Développeurs | [08-bug](epreuves/08-bug.md) | `>` au lieu de `>=` ; test caché ; tests du projet verts |

## Comment on passe le banc

- **Agent** : Pi 1.5.0 sur Strata, Inkling 2 Mini SQ-10 en local, configuration isolée `~/pi-lab` installée par [pi-lab/installer.sh](pi-lab/installer.sh), outils read, bash, edit, write, sans extension ni MCP.
- **Skills (les mêmes pour tous les modèles)** : verification-before-completion, systematic-debugging, efficient-testing, frontend-design (copiés de `~/.pi/agent/skills`, auto-invocation réactivée) et [verifier-page](pi-lab/skills/verifier-page/SKILL.md) (contrôle de syntaxe des scripts d'une page, écrit pour le banc).
- **Documents** : tous fictifs, fabriqués par [fabriquer.py](fabriquer.py) (graine fixe) dans `dossiers/`. Les corrigés sont dans `corriges/`, jamais envoyés à Pi.
- **Passage** : `sh passer.sh [épreuves]` sur la machine où tourne le modèle. Une épreuve à la fois ; ce que Pi écrit atterrit dans `resultats/*/fichiers/`, son journal dans `resultats/*/pi.log`, la durée dans `resultats/*/duree-s.txt`.
- **Notation** : `python3 noter.py` pour les contrôles chiffrés et la durée réelle, puis relecture de chaque `reponse.md` à côté du corrigé. Carte identique : réussi, à reprendre, raté, avec le temps d'attente réel.
