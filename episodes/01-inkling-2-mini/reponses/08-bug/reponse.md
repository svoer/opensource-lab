# Réponse

**Cause :** la remise de 10 % ne s'appliquait qu'à partir de 11 articles (`quantite > SEUIL_REMISE`) au lieu de 10 (`>=`), donc 10 carnets à 4,20 € n'étaient pas remisés.

**Changement :** dans `projet/facture.py`, condition corrigée en `quantite >= SEUIL_REMISE` ; test ajouté dans `projet/test_facture.py` (`test_remise_exactement_10_articles`, 4,20 € × 10 → 37,80 € HT). Tous les tests passent (4/4).

**Réponse à la cliente :** « Bonjour Mme Roux, nous avons corrigé la remise : à partir de 10 articles identiques, 10 % sont désormais appliqués. Votre commande de 10 carnets à 4,20 € s'affiche donc à 37,80 € HT (TVA 7,56 €, TTC 45,36 €). »
