"""Petit outil de facturation de l'atelier : total d'une commande, remise par quantité, TVA."""
from decimal import Decimal, ROUND_HALF_UP

TVA = Decimal("0.20")
SEUIL_REMISE = 10          # remise de 10 % à partir de 10 articles identiques
TAUX_REMISE = Decimal("0.10")


def arrondi(x):
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def total_ligne_ht(prix_unitaire, quantite):
    """Total HT d'une ligne, remise comprise."""
    total = Decimal(str(prix_unitaire)) * quantite
    if quantite > SEUIL_REMISE:
        total -= total * TAUX_REMISE
    return arrondi(total)


def total_commande(lignes):
    """lignes : liste de (prix_unitaire, quantite). Renvoie (ht, tva, ttc)."""
    ht = sum((total_ligne_ht(p, q) for p, q in lignes), Decimal("0"))
    tva = arrondi(ht * TVA)
    return ht, tva, ht + tva


if __name__ == "__main__":
    import sys
    lignes = [(float(a.split("x")[1]), int(a.split("x")[0])) for a in sys.argv[1:]]
    ht, tva, ttc = total_commande(lignes)
    print(f"HT {ht} €  TVA {tva} €  TTC {ttc} €")
