# Épisode 1 · Une journée avec une IA locale (Inkling 2 Mini, RTX 3060 12 Go)

Est-ce qu'une IA qui tourne chez soi, sur une carte graphique de 12 Go, peut aider toute une journée ? Huit tâches de tous les jours, sans un seul appel au cloud.

## Réglages

Strata 0.2.21 · Inkling 2 Mini SQ-10 · cache K8V4 · contexte 128K · 4 requêtes parallèles · PC Linux, i9-10900F, 64 Go de RAM, RTX 3060 12 Go. Agent : Pi 1.5.0 avec 5 skills (voir [bancs/la-journee/pi-lab](../../bancs/la-journee/pi-lab/)).

## Résultats

| Heure | Épreuve | Verdict | Temps de travail |
| --- | --- | --- | --- |
| 8 h | Les mails | réussi | 29 s |
| 9 h | Le bail | réussi | 47 s |
| 12 h | Les repas | à reprendre (total faux) | 63 s |
| 14 h | La réunion | réussi | 32 s |
| 15 h | Les comptes | à reprendre (essence rangée dans le logement) | 2 min 38 |
| 17 h | Les devoirs | réussi | 36 s |
| 18 h | Le Tetris Game Boy | réussi, un seul prompt | 3 min 46 |
| 21 h | Le vrai bug | réussi, test caché vert | 49 s |

**6 réussies sur 8, 2 à reprendre, 0 ratée.** Détail et justification de chaque note : [RESULTATS-inkling.md](RESULTATS-inkling.md).

- Grille du Lab : **22 sur 24** (réponses brutes dans [grille/](grille/)).
- Débit : 50,8 tok/s seul ; à 4 en même temps, 92,4 tok/s au total, soit 23,3 tok/s par personne.

## Ce qu'il y a ici

- [reponses/](reponses/) : ce qu'Inkling a rendu, épreuve par épreuve. Le Tetris se joue en ouvrant [reponses/07-tetris/index.html](reponses/07-tetris/index.html) dans un navigateur.
- [grille/](grille/) : ses réponses à la grille du Lab, avec les notes.
