# OPENSOURCE LAB · Le Lab

Les fichiers de la chaîne YouTube **OPENSOURCE LAB** : des IA qui tournent chez soi, testées sur du vrai matériel, avec tout ce qu'il faut pour refaire les tests chez toi.

## Les bancs de test (communs à tous les épisodes)

| Banc | Ce qu'il mesure |
| --- | --- |
| [La journée](bancs/la-journee/) | 8 tâches de tous les jours, des mails au vrai bug, passées par l'agent Pi, avec des corrigés préparés à l'avance |
| [La grille du Lab](bancs/grille-du-lab/) | 24 questions sur 2 niveaux, les mêmes pour chaque modèle |
| [La mesure de débit](bancs/mesure-debit/) | tokens par seconde à 1, 2 et 4 personnes en même temps |

Chaque banc se passe sur la machine où tourne ton modèle, derrière une API compatible OpenAI (Strata, llama.cpp, LM Studio…). Tous les documents de test sont inventés.

## Les épisodes

| # | Épisode | Modèle et machine | Résultat |
| --- | --- | --- | --- |
| 1 | [Une journée avec une IA locale](episodes/01-inkling-2-mini/) | Inkling 2 Mini SQ-10 sur RTX 3060 12 Go | 6 épreuves sur 8, 22/24 à la grille, 23 tok/s chacun à 4 |

Chaque dossier d'épisode garde les réponses brutes du modèle, pour comparer avec les tiennes.
