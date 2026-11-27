# Mesure de débit · 1, 2 et 4 personnes en même temps

Combien de tokens par seconde chacun reçoit quand plusieurs personnes utilisent le modèle à la fois.

```bash
python3 -u bench2.py http://HOTE:8080 short > mesures.jsonl     # 5 lots à 1, 2 et 4 clients, prompts courts
python3 -u bench2.py http://HOTE:8080 ctx 1 MOTS >> mesures.jsonl  # un prompt long de MOTS mots (contexte long)
python3 resume2.py mesures.jsonl                                  # débit total, débit par client, délais
```

Les débits comptent tous les tokens générés, raisonnement compris. Résultats de chaque modèle : dans son dossier d'épisode.
