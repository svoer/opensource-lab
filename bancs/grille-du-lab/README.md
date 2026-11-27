# La grille du Lab · vingt-quatre questions fixes, en deux niveaux

Les mêmes questions pour chaque modèle, en français, température 0, une réponse par question. La correction est automatique : pas d'appréciation à la main.

| N° | Épreuve | Ce qu'elle vérifie | Bonne réponse |
| ---: | --- | --- | --- |
| 1 | Compter les lettres | Attention au caractère près | 2 « r » dans « framboisier » |
| 2 | Compter ses propres mots | Se relire | Le nombre annoncé égale le nombre de mots de la phrase |
| 3 | Les tueurs dans la pièce | Raisonnement | 3 |
| 4 | La bille et le verre | Physique de bon sens | Sur la table |
| 5 | Les chemises au soleil | Piège de proportionnalité | 4 heures |
| 6 | Dix phrases, un dernier mot | Contrainte de forme tenue dix fois | Dix lignes finissant par « pomme. » |
| 7 | Priorité des opérations | Calcul | 20 |
| 8 | JSON strict | Suivre un format | Objet valide, trois clés, rien autour |
| 9 | Pluriels irréguliers | Français | chevaux, bals, vitraux, pneus, bijoux |
| 10 | Les jours de la semaine | Logique temporelle | lundi |
| 11 | Fonction Python | Code exécuté contre des assertions | `est_premier` juste de −5 à 59, plus 7919 et 7917 |
| 12 | Un seul mot | Obéir à une consigne courte | Canberra, et rien d'autre |

[Énoncés exacts](questions.json) · [Passage](passer.py) · [Correction](corriger.py)

## Niveau 2 · douze questions plus dures (ajoutées le 25 novembre 2026)

Le niveau 1 ne départageait rien (12 sur 12). Le niveau 2 garde les mêmes règles : français, température 0, correction automatique.

| N° | Épreuve | Ce qu'elle vérifie | Bonne réponse |
| ---: | --- | --- | --- |
| 13 | Deux notes dans un long journal | Retrouver et relier deux faits dans 20 000 tokens, avec six leurres | Le tiroir vert |
| 14 | Appeler le bon outil | Choisir entre deux outils et calculer une date | `meteo(ville="Lyon", date="2026-11-27")`, un seul appel |
| 15 | L'ordre caché dans le courriel | Résister à une instruction glissée dans un texte à résumer | Un résumé qui cite jeudi, pas « BANANE » |
| 16 | Calcul d'horaire en trois étapes | Calcul en base 60 | 13 h 34 |
| 17 | Grande multiplication | 4789 × 6053 sans outil | 28 987 817 |
| 18 | Le mot à l'envers | Travail lettre par lettre sur 25 lettres | tnemellennoitutitsnocitna |
| 19 | Une phrase sans la lettre e | Contrainte d'écriture tenue sur douze mots | Une phrase, douze mots au moins, aucun e |
| 20 | L'ordre d'arrivée | Logique à quatre contraintes | David |
| 21 | Fusionner des intervalles | Code exécuté contre huit assertions (ordre, contact, liste intacte) | `fusionner` juste |
| 22 | Extraire des commandes en JSON | Dates relatives, virgule décimale, totaux | Trois objets exacts |
| 23 | Accords du participe passé | Français difficile | écrites, lavé, succédé, vu |
| 24 | La rivière sans piège | Ne pas réciter l'énigme classique | 1 |

[Énoncés exacts](questions-niveau-2.json) · [Générateur, graine fixe](construire-niveau-2.py)

## Inkling 2 Mini SQ-10 · 25 novembre 2026

**12 sur 12.** [Réponses brutes](../../episodes/01-inkling-2-mini/grille/reponses-inkling-sq10.jsonl) · [Notes](../../episodes/01-inkling-2-mini/grille/reponses-inkling-sq10.notes.json)

- Les dix phrases « pomme » respectent la règle mais se ressemblent presque toutes (« … se termine par une pomme. »). La grille ne note pas la variété.
- Les durées enregistrées ne valent pas mesure de vitesse : le serveur traitait d'autres requêtes en même temps.
- **Ce niveau est trop facile pour ce modèle.** Un 12 sur 12 ne départage rien : d'où le niveau 2 ci-dessus.

## Inkling 2 Mini SQ-10 · niveau 2 · 25 novembre 2026

**10 sur 12**, soit **22 sur 24** sur l'ensemble. [Réponses brutes](../../episodes/01-inkling-2-mini/grille/reponses-niveau-2-inkling-sq10.jsonl) · [Notes](../../episodes/01-inkling-2-mini/grille/reponses-niveau-2-inkling-sq10.notes.json)

- **Raté · la phrase sans « e ».** Le raisonnement tourne en boucle (« tous no e » répété) et la génération s'arrête après 426 tokens sans aucune réponse.
- **Raté · les accords.** « écrites, lavées, succédés, vue » : une forme juste sur quatre. Le raisonnement penchait vers « lavé » quand le service l'a interrompu.
- **Le service coupe la réflexion à 2 064 tokens** puis force la réponse (« I have thought about this long enough »). Le mot à l'envers a été réussi juste à cette limite, les accords ont été ratés à cette limite. C'est le modèle tel qu'il est servi par ce profil Strata, pas le modèle dans l'absolu.
- Le journal long fait 20 284 tokens : lu et répondu en 27 secondes.
- Un seul passage à température 0. Pas de moyenne sur plusieurs tirages.

## Rejouer

```sh
scp passer.py questions.json TON_SERVEUR:/tmp/ && ssh TON_SERVEUR 'cd /tmp && python3 -u passer.py' > reponses-MODELE.jsonl
python3 corriger.py reponses-MODELE.jsonl
scp passer.py questions-niveau-2.json TON_SERVEUR:/tmp/ && ssh TON_SERVEUR 'cd /tmp && python3 -u passer.py questions-niveau-2.json' > reponses-niveau-2-MODELE.jsonl
python3 corriger.py reponses-niveau-2-MODELE.jsonl
```

La fonction Python renvoyée par le modèle est exécutée sur le Mac, dans un interpréteur isolé (`-I`), dix secondes au plus.
