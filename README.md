# OPENSOURCE LAB

Les fichiers de la chaîne YouTube **[OPENSOURCE LAB](https://www.youtube.com/@opensource-lab)** : logiciels libres, IA locale et auto-hébergement, installés chez soi, expliqués et testés pour de vrai.

Tout ce qui sert dans les vidéos est ici, en libre accès : scripts d'installation, réglages, fichiers de test, bancs de mesure et résultats bruts. Le but est que tu puisses refaire chaque test chez toi et comparer.

## Organisation du dépôt

| Dossier | Contenu |
| --- | --- |
| [bancs/](bancs/) | Les bancs de test réutilisables d'une vidéo à l'autre |
| [episodes/](episodes/) | Un dossier par vidéo : fichiers, réglages et résultats bruts |

## Les bancs de test (communs à toutes les vidéos)


| Banc | Ce qu'il mesure |
| --- | --- |
| [La journée](bancs/la-journee/) | 8 tâches de tous les jours, des mails au vrai bug, passées par l'agent Pi, avec des corrigés préparés à l'avance |
| [La grille du Lab](bancs/grille-du-lab/) | 24 questions sur 2 niveaux, les mêmes pour chaque modèle |
| [La mesure de débit](bancs/mesure-debit/) | tokens par seconde à 1, 2 et 4 personnes en même temps |

Chaque banc se passe sur la machine où tourne ton modèle, derrière une API compatible OpenAI (Strata, llama.cpp, LM Studio…). Tous les documents de test sont inventés.

## Les vidéos

| # | Vidéo | Fichiers | Sujet et machine | Résultat |
| --- | --- | --- | --- | --- |
| 1 | [Inkling 2 Mini en local : test complet sur RTX 3060](https://youtu.be/LWlXptHarPE) | [episodes/01-inkling-2-mini](episodes/01-inkling-2-mini/) | Inkling 2 Mini SQ-10 sur RTX 3060 12 Go | 6 épreuves sur 8, 22/24 à la grille, 23 tok/s chacun à 4 |

Chaque dossier de vidéo garde les réponses brutes du modèle, pour comparer avec les tiennes.
