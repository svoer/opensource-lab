"""Fabrique les documents fictifs du banc « La journée » et leurs corrigés (graine fixe, rien de réel).

Usage : python3 fabriquer.py      → dossiers/NN-*/ (ce que Pi reçoit) et corriges/NN-*.json (jamais envoyés à Pi)
Toutes les personnes, adresses, sociétés et montants sont inventés.
"""
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOS, COR = ROOT / "dossiers", ROOT / "corriges"
rng = random.Random(2611)


def put(rel, text):
    p = DOS / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")


def key(name, data):
    COR.mkdir(exist_ok=True)
    (COR / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# 01 · Les mails : 30 messages, 3 vraiment urgents, 4 fausses urgences publicitaires ------------------------------
urgents = [
    ("ecole", "Mme Lefort, école Jean-Macé", "Sortie au musée : autorisation à rendre DEMAIN",
     "Bonjour,\n\nPetit rappel : la sortie de la classe de CM1 au musée des Confluences a lieu jeudi. Il nous manque "
     "toujours l'autorisation parentale signée de Léo. Elle doit être dans son cartable demain mardi au plus tard, "
     "sinon il ne pourra pas partir avec la classe et restera dans une autre classe ce jour-là.\n\nMerci,\nMme Lefort"),
    ("banque", "Banque Rivière, service clients", "Prélèvement rejeté sur votre compte",
     "Madame, Monsieur,\n\nLe prélèvement de 64,90 € de votre fournisseur d'électricité a été rejeté le 22/11 faute de "
     "provision suffisante. Sans régularisation de votre part sous 48 heures, des frais de rejet de 20 € seront "
     "appliqués et le fournisseur sera informé de l'incident.\n\nVous pouvez approvisionner votre compte depuis "
     "l'application.\n\nBanque Rivière"),
    ("mutuelle", "Mutuelle Horizon", "Pièce manquante pour votre remboursement dentaire",
     "Bonjour,\n\nPour traiter votre demande de remboursement dentaire de 380 €, il nous manque la facture détaillée "
     "du cabinet. Merci de nous l'envoyer avant vendredi 27/11 : passé ce délai, le dossier sera clôturé et il "
     "faudra refaire une demande complète.\n\nCordialement,\nMutuelle Horizon"),
]
faux = [
    ("UrbanShoes", "URGENT : -60 % seulement aujourd'hui !!!", "Dernière chance, nos baskets à -60 % jusqu'à minuit. Ne ratez pas ça !"),
    ("VoyagesMalins", "Action requise : votre séjour vous attend", "Votre séjour de rêve à Lisbonne n'attend plus que vous. Réservez avant dimanche."),
    ("Streamix", "Votre compte va expirer ?!", "Découvrez notre offre Premium : 3 mois offerts si vous passez à l'offre annuelle."),
    ("Bricoplus", "DERNIER RAPPEL avant la fin des soldes", "Perceuses, scies et visseuses : jusqu'à -40 % ce week-end."),
]
normaux = [
    ("Julie Martin", "Repas de samedi", "Coucou ! On fait toujours le repas samedi ? J'apporte le dessert. Bises"),
    ("Club de tennis", "Planning des cours de décembre", "Bonjour à tous, vous trouverez ci-joint le planning des cours de décembre."),
    ("Marc (voisin)", "Colis", "Salut, j'ai récupéré un colis à ton nom vendredi, passe le chercher quand tu veux."),
    ("La Poste", "Votre colis a été livré", "Votre colis n° 6A123 a été remis en point relais."),
    ("Mairie de Lyon 7e", "Lettre d'information de novembre", "Travaux rue de Marseille, marché de Noël, inscriptions sur les listes électorales."),
    ("Papa", "Photos des vacances", "Je t'envoie les photos de cet été, il y en a de très belles de la plage."),
    ("Ciné Lumière", "Programme de la semaine", "Cette semaine : trois avant-premières et une soirée courts-métrages."),
    ("Atelier vélo", "Votre vélo est prêt", "Bonjour, la révision de votre vélo est terminée, vous pouvez venir le chercher aux heures d'ouverture."),
    ("Sophie (travail)", "Pot de départ de Karim", "On organise le pot de départ de Karim le 4 décembre, tu participes à la cagnotte ?"),
    ("Assurance Habitat+", "Votre attestation 2027", "Votre attestation d'assurance habitation 2027 est disponible dans votre espace."),
    ("Bibliothèque", "Retour de prêt", "Le livre « Le Petit Prince » est à rendre avant le 12 décembre."),
    ("Doctolib-like", "Rappel de rendez-vous", "Rappel : rendez-vous chez le Dr Benali le 9 décembre à 18 h 30."),
    ("Thomas", "Match dimanche", "Tu viens au match dimanche ? Il reste une place dans la voiture."),
    ("Opérateur Tel", "Votre facture de novembre", "Votre facture de 29,99 € sera prélevée le 5 décembre."),
    ("Association des parents", "Vente de gâteaux", "Vente de gâteaux le 11 décembre à la sortie de l'école, toutes les contributions sont bienvenues."),
    ("Covoit'", "Votre trajet est confirmé", "Votre trajet Lyon → Grenoble du 13 décembre est confirmé."),
    ("Mamie", "Noël", "Est-ce que vous venez tous pour Noël cette année ? Dis-moi vite pour que je m'organise."),
    ("Jardin partagé", "Réunion mensuelle", "La prochaine réunion du jardin partagé aura lieu le 2 décembre à 19 h."),
    ("Supermarché Frais", "Vos bons de réduction", "Vos 3 bons de réduction de la semaine sont disponibles."),
    ("Newsletter Tech", "Les actus de la semaine", "Nouveaux processeurs, une IA qui code, et nos tests de casques audio."),
    ("Karim", "Merci !", "Merci pour le coup de main pour le déménagement, je te dois une pizza."),
    ("Salle de sport", "Nouveaux horaires", "À partir de décembre, la salle ouvre à 6 h 30 en semaine."),
    ("Trésor public (info)", "Votre avis est disponible", "Votre avis de taxe foncière est disponible dans votre espace. Aucune action requise, il a déjà été payé."),
]
mails = []
for who, subj, body in normaux:
    mails.append(("normal", who, subj, body))
for who, subj, body in faux:
    mails.append(("faux", who, subj, body))
for tag, who, subj, body in urgents:
    mails.append((tag, who, subj, body))
rng.shuffle(mails)
lines, ids = ["# Boîte de réception · lundi 23 novembre 2026, 8 h", ""], {}
for i, (tag, who, subj, body) in enumerate(mails, 1):
    ids.setdefault(tag, []).append(i)
    lines += [f"## Mail {i:02}", f"De : {who}", f"Objet : {subj}", "", body, ""]
put("01-mails/boite.md", "\n".join(lines))
key("01-mails", {"urgents": {k: ids[k][0] for k in ("ecole", "banque", "mutuelle")}, "plus_urgent": ids["ecole"][0],
                 "fausses_urgences": ids["faux"], "a_ne_pas_classer_urgent": ids["faux"] + ids["normal"],
                 "regle": "Le plus urgent est l'école (échéance demain mardi). Les 4 publicités « urgentes » ne sont pas urgentes."})

# 02 · Le bail : 22 articles, la réponse est dans les articles 9, 11 et 17 -------------------------------------------
art = {
    1: ("Désignation des parties", "Le présent contrat est conclu entre Mme Claire Dumas, demeurant 12 rue des Tanneurs, 69002 Lyon, ci-après « le bailleur », et M. Sébastien Exemple, ci-après « le locataire ». Les parties déclarent avoir la capacité de contracter."),
    2: ("Objet du contrat", "Le bailleur loue au locataire, qui l'accepte, le logement décrit à l'article 3, à usage exclusif d'habitation principale. Le locataire ne pourra exercer aucune activité commerciale dans les lieux."),
    3: ("Désignation du logement", "Appartement de type T3 de 64 m² situé au 3e étage avec ascenseur du 41 rue Garibaldi, 69007 Lyon, comprenant une entrée, un séjour, deux chambres, une cuisine équipée, une salle d'eau et un WC séparé, ainsi qu'une cave n° 14. Le logement est situé en zone d'urbanisation continue de plus de 50 000 habitants où il existe un déséquilibre marqué entre l'offre et la demande de logements, dite « zone tendue », au sens de l'article 17 de la loi du 6 juillet 1989."),
    4: ("Date de prise d'effet et durée", "Le contrat prend effet le 1er septembre 2025 pour une durée de trois ans. À défaut de congé donné dans les conditions de l'article 9, il est reconduit tacitement pour la même durée."),
    5: ("Loyer", "Le loyer mensuel hors charges est fixé à 780 € (sept cent quatre-vingts euros). Il est payable d'avance, le 5 de chaque mois au plus tard, par virement sur le compte indiqué par le bailleur."),
    6: ("Charges récupérables", "Le locataire verse chaque mois une provision sur charges de 70 €, régularisée une fois par an sur présentation des justificatifs : eau froide, entretien des parties communes, ascenseur, taxe d'enlèvement des ordures ménagères."),
    7: ("Révision du loyer", "Le loyer est révisé chaque année à la date anniversaire du contrat, selon la variation de l'indice de référence des loyers publié par l'INSEE, la référence étant l'indice du deuxième trimestre."),
    8: ("Dépôt de garantie", "À la signature, le locataire verse un dépôt de garantie de 780 €, correspondant à un mois de loyer hors charges. Ce dépôt ne porte pas intérêt et ne peut en aucun cas être imputé par le locataire sur le dernier mois de loyer."),
    9: ("Congé donné par le locataire", "9.1. Le locataire peut donner congé à tout moment, par lettre recommandée avec accusé de réception, acte d'huissier ou remise en main propre contre émargement. 9.2. Le délai de préavis est de trois mois. Par exception, il est réduit à un mois lorsque le logement est situé dans une zone tendue telle que définie à l'article 3, ce qui est le cas du présent logement. 9.3. Le délai de préavis court à compter du jour de la réception de la lettre par le bailleur. 9.4. Pendant le préavis, le locataire reste redevable du loyer et des charges."),
    10: ("Congé donné par le bailleur", "Le bailleur peut donner congé pour la fin du bail, avec un préavis de six mois, pour reprendre le logement, le vendre ou pour un motif légitime et sérieux."),
    11: ("Restitution du dépôt de garantie", "Le dépôt de garantie est restitué dans un délai d'un mois à compter de la remise des clés lorsque l'état des lieux de sortie est conforme à l'état des lieux d'entrée, et de deux mois dans le cas contraire, déduction faite des sommes dûment justifiées restant dues au bailleur."),
    12: ("État des lieux", "Un état des lieux contradictoire est établi à l'entrée et à la sortie du locataire. Il est annexé au présent contrat."),
    13: ("Obligations du locataire", "Le locataire s'engage à payer le loyer et les charges aux termes convenus, à user paisiblement des lieux, à répondre des dégradations survenues pendant la location, à prendre à sa charge l'entretien courant et les menues réparations, et à s'assurer contre les risques locatifs."),
    14: ("Obligations du bailleur", "Le bailleur s'engage à délivrer un logement décent, à assurer au locataire la jouissance paisible du logement, à entretenir les locaux en état de servir à l'usage prévu et à faire les réparations autres que locatives."),
    15: ("Assurance", "Le locataire justifie chaque année d'une assurance couvrant les risques locatifs. À défaut, le bailleur pourra souscrire une assurance pour le compte du locataire et en récupérer le montant."),
    16: ("Travaux", "Le locataire ne peut transformer les lieux sans l'accord écrit du bailleur. Les aménagements légers (peinture, étagères) sont autorisés à condition de remettre les lieux en état à la sortie s'ils ne sont pas de couleur neutre."),
    17: ("Frais de remise en location", "Les frais liés à la remise en location du logement après le départ du locataire (annonces, visites, rédaction du nouveau bail) sont intégralement à la charge du bailleur. Aucune somme ne pourra être réclamée à ce titre au locataire sortant."),
    18: ("Animaux", "La détention d'un animal familier est autorisée, sous réserve qu'il ne cause ni dégât ni trouble de voisinage."),
    19: ("Sous-location", "Le locataire ne peut sous-louer tout ou partie du logement sans l'accord écrit du bailleur, y compris pour de courtes durées."),
    20: ("Clause résolutoire", "Le contrat sera résilié de plein droit deux mois après un commandement de payer demeuré infructueux, en cas de défaut de paiement du loyer, des charges ou du dépôt de garantie."),
    21: ("Solidarité", "En cas de pluralité de locataires, ceux-ci sont tenus solidairement des obligations du présent bail."),
    22: ("Élection de domicile", "Pour l'exécution du présent contrat, le bailleur fait élection de domicile à son adresse et le locataire dans les lieux loués."),
}
annexe = ("Annexe : règlement de copropriété (extraits). Les parties communes doivent rester libres de tout encombrement. "
          "Les vélos sont rangés dans le local prévu à cet effet. Le tri des déchets est obligatoire. Les travaux bruyants "
          "sont autorisés en semaine de 8 h à 19 h et le samedi de 9 h à 12 h. ")
doc = ["# Contrat de location · logement vide", "", "Soumis à la loi n° 89-462 du 6 juillet 1989.", ""]
for n, (t, x) in art.items():
    doc += [f"## Article {n} · {t}", "", x, "",
            "Les stipulations du présent article s'appliquent sans préjudice des dispositions légales et réglementaires d'ordre public, "
            "qui prévalent en cas de contradiction. Toute modification fera l'objet d'un avenant écrit signé des deux parties.", ""]
doc += ["## Annexes", "", annexe * 6, "", "Fait à Lyon, le 25 août 2025, en deux exemplaires originaux."]
put("02-contrat/bail.md", "\n".join(doc))
key("02-contrat", {"preavis": "1 mois (article 9.2, zone tendue, article 3) et non 3 mois",
                   "envoi_lettre": "pour partir le 31 janvier 2027, la lettre doit être reçue par le bailleur au plus tard le 31 décembre 2026 (article 9.3)",
                   "cout_depart": "loyer + charges pendant le préavis : 780 + 70 = 850 € ; aucun frais de remise en location (article 17)",
                   "depot": "780 € rendus sous 1 mois si l'état des lieux est conforme, 2 mois sinon (article 11)",
                   "pieges": ["dire 3 mois de préavis", "réclamer des frais de relocation", "imputer le dépôt sur le dernier loyer (interdit, article 8)"]})

# 03 · Les repas : pas de document, la correction recalcule le total et cherche les fruits à coque --------------------
key("03-repas", {"budget_max": 80, "personnes": 4, "jours": 7, "interdits": ["noix", "noisette", "amande", "cajou", "pécan", "pecan",
                 "pistache", "macadamia", "praliné", "pralin", "frangipane", "nougat", "pignon"],
                 "controle": "total recalculé depuis la liste de courses ≤ 80 € ; aucun fruit à coque ; 7 dîners différents"})

# 04 · La réunion : 6 décisions avec un responsable et une date, 1 idée rejetée -------------------------------------------
gens = ["Nadia", "Paul", "Inès", "Hugo", "Claire"]
bavard = [
    "Oui, je suis d'accord, enfin dans l'ensemble.", "Attends, je retrouve le document, une seconde.",
    "Ça me fait penser à ce qu'on avait vu en septembre.", "On en avait déjà parlé, non ?", "Je ne sais pas trop, honnêtement.",
    "Quelqu'un a le lien vers le tableau ?", "Pardon, ma connexion a coupé, tu peux répéter ?", "C'est noté.",
    "Il faudrait demander à la compta, mais bon.", "Je vois ce que tu veux dire.", "Bon, on avance ?", "Ah oui, c'est vrai.",
    "Je trouve que c'est une bonne idée sur le principe.", "On peut en reparler la semaine prochaine si besoin.",
    "J'ai eu le client au téléphone hier, il était plutôt content.", "Le café de la machine est encore en panne, au fait.",
    "Ça dépend du budget, comme toujours.", "Je prends des notes, continuez.", "Est-ce qu'on a des chiffres là-dessus ?",
    "Moi ça me va.", "Pour info, je serai en congé la semaine du 21.", "On l'avait testé l'an dernier, ça n'avait pas pris.",
]
decisions = [
    ("Paul", "Bon, on tranche : on passe la newsletter à un envoi par mois au lieu de deux. Paul, tu t'en occupes, c'est effectif dès décembre.",
     "Newsletter mensuelle au lieu de bimensuelle", "Paul", "dès décembre"),
    ("Nadia", "Décision prise pour le salon de Lyon : on y va, avec un stand de 9 m². Inès réserve le stand avant le 15 décembre.",
     "Participation au salon de Lyon, stand de 9 m²", "Inès", "avant le 15 décembre"),
    ("Hugo", "OK pour moi, je mets à jour la page tarifs du site avec les nouveaux prix d'ici vendredi.",
     "Mise à jour de la page tarifs avec les nouveaux prix", "Hugo", "vendredi"),
    ("Nadia", "On valide le recrutement d'un alternant pour janvier. Claire, tu publies l'annonce cette semaine.",
     "Recrutement d'un alternant pour janvier", "Claire", "cette semaine"),
    ("Claire", "Pour le client Bertin, on accepte le délai supplémentaire de deux semaines, je lui confirme par mail demain.",
     "Délai de deux semaines accordé au client Bertin", "Claire", "demain"),
    ("Nadia", "Dernier point : la réunion d'équipe passe au mardi 9 h à partir de janvier. Nadia envoie la nouvelle invitation.",
     "Réunion d'équipe déplacée au mardi 9 h dès janvier", "Nadia", "à partir de janvier"),
]
rejet = ("Hugo", "Et si on lançait une appli mobile cette année ?", "Nadia",
         "Non, on n'a ni le budget ni le temps, on abandonne l'idée de l'appli pour cette année.")
tr, minute, dpos = ["# Transcription · réunion d'équipe du lundi 23 novembre 2026, 14 h", "",
                    "Transcription automatique, non relue. Participants : " + ", ".join(gens) + ".", ""], 0, [18, 46, 75, 104, 132, 158]
lignes = []
for i in range(190):
    lignes.append((rng.choice(gens), rng.choice(bavard)))
for pos, d in zip(dpos, decisions):
    lignes.insert(pos, (d[0], d[1]))
lignes.insert(90, (rejet[0], rejet[1]))
lignes.insert(92, (rejet[2], rejet[3]))
for i, (who, txt) in enumerate(lignes):
    tr.append(f"[{14 + (i * 10) // 600:02}:{(i * 10 // 60) % 60:02}:{(i * 10) % 60:02}] {who} : {txt}")
put("04-reunion/transcription.md", "\n".join(tr))
key("04-reunion", {"decisions": [{"quoi": d[2], "qui": d[3], "quand": d[4]} for d in decisions],
                   "piege": "L'appli mobile a été proposée puis abandonnée : elle ne doit pas apparaître comme décision."})

# 05 · Les comptes : relevé de 3 mois, catégories connues, totaux au centime ---------------------------------------
cats = {
    "Courses": [("CARREFOUR MARKET LYON7", 38, 96), ("LIDL GERLAND", 22, 61), ("BOULANGERIE DU PARC", 4, 12), ("MARCHE JEAN MACE", 15, 34)],
    "Logement": [("LOYER DUMAS VIREMENT", 850, 850), ("EDF ELECTRICITE", 64.9, 64.9), ("ASSURANCE HABITAT PLUS", 18.4, 18.4)],
    "Transport": [("TCL ABONNEMENT", 74.1, 74.1), ("TOTALENERGIES STATION", 42, 68), ("SNCF CONNECT", 29, 87)],
    "Abonnements": [("STREAMIX", 13.49, 13.49), ("OPERATEUR TEL", 29.99, 29.99), ("SALLE DE SPORT FITLY", 34.9, 34.9)],
    "Loisirs": [("CINE LUMIERE", 9.5, 24), ("RESTAURANT LE BOUCHON", 28, 74), ("LIBRAIRIE PASSAGES", 12, 39), ("FNAC LYON", 19, 89)],
    "Santé": [("PHARMACIE GARIBALDI", 6, 31), ("DR BENALI CONSULTATION", 30, 30)],
}
fixes = {"LOYER DUMAS VIREMENT": 3, "EDF ELECTRICITE": 4, "ASSURANCE HABITAT PLUS": 2, "TCL ABONNEMENT": 1, "STREAMIX": 6,
         "OPERATEUR TEL": 5, "SALLE DE SPORT FITLY": 2, "DR BENALI CONSULTATION": None}
rows, tot = [], {}
for mois in (9, 10, 11):
    m = f"2026-{mois:02}"
    rows.append((date(2026, mois, 1), "SALAIRE ATELIER NORD", 2480.00, "Revenus"))
    for cat, shops in cats.items():
        for shop, lo, hi in shops:
            if shop in fixes:
                if fixes[shop] is None and mois != 10:
                    continue
                rows.append((date(2026, mois, fixes[shop] or 18), shop, -round(lo, 2), cat))
                continue
            n = {"Courses": 5, "Transport": 2, "Loisirs": 2, "Santé": 1}.get(cat, 1)
            for _ in range(n):
                rows.append((date(2026, mois, rng.randint(2, 28)), shop, -round(rng.uniform(lo, hi), 2), cat))
rows.sort()
for d, lib, mt, cat in rows:
    k = (d.strftime("%Y-%m"), cat)
    tot[k] = round(tot.get(k, 0) + mt, 2)
p = DOS / "05-comptes" / "releve.csv"
p.parent.mkdir(parents=True, exist_ok=True)
with p.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["date", "libelle", "montant"])
    for d, lib, mt, cat in rows:
        w.writerow([d.strftime("%d/%m/%Y"), lib, f"{mt:.2f}".replace(".", ",")])
out = {}
for (m, c), v in sorted(tot.items()):
    out.setdefault(m, {})[c] = v
key("05-comptes", {"lignes": len(rows), "totaux_par_mois_et_categorie": out,
                   "depenses_par_mois": {m: round(sum(v for c, v in d.items() if c != "Revenus"), 2) for m, d in out.items()},
                   "categories": list(cats) + ["Revenus"]})

# 06 · Les devoirs ----------------------------------------------------------------------------------------------------
key("06-devoirs", {"prix_solde": 204.00, "prix_final": 224.40, "prix_moins_5": 228.00, "meme_prix": False,
                   "explication": "240 × 0,85 = 204 ; 204 × 1,10 = 224,40 ; 240 × 0,95 = 228 : ce n'est pas pareil, car les 10 % s'appliquent à un prix déjà baissé."})

# 07 · Le Tetris : pas de document, correction à l'écran (jouable, pièces, lignes, score, niveau, style) --------------
key("07-tetris", {"criteres": ["la page s'ouvre sans erreur", "7 pièces qui tombent", "rotation et déplacements au clavier",
                               "les lignes pleines disparaissent", "score, lignes et niveau affichés", "la vitesse augmente avec le niveau",
                               "fin de partie et recommencer", "palette 4 tons vert Game Boy, look 2026 soigné"]})

# 08 · Le vrai bug : un petit outil de facturation en Python, un bug signalé par une cliente ----------------------
put("08-bug/projet/facture.py", '''
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
''')
put("08-bug/projet/test_facture.py", '''
import unittest
from decimal import Decimal
from facture import total_ligne_ht, total_commande


class TestFacture(unittest.TestCase):
    def test_sans_remise(self):
        self.assertEqual(total_ligne_ht(12.50, 3), Decimal("37.50"))

    def test_remise_au_dela_du_seuil(self):
        self.assertEqual(total_ligne_ht(5, 12), Decimal("54.00"))

    def test_commande(self):
        self.assertEqual(total_commande([(12.50, 3), (5, 12)]), (Decimal("91.50"), Decimal("18.30"), Decimal("109.80")))


if __name__ == "__main__":
    unittest.main()
''')
put("08-bug/projet/README.md", '''
# Facturation de l'atelier

`python3 facture.py 10x4.20 2x15` affiche le total d'une commande (10 articles à 4,20 €, 2 à 15 €).
Règle commerciale : **remise de 10 % à partir de 10 articles identiques** sur une même ligne.
Tests : `python3 -m unittest`.
''')
put("08-bug/signalement.md", '''
Mail de Mme Roux, cliente : « Bonjour, j'ai commandé exactement 10 carnets à 4,20 € et votre facture affiche 42,00 € HT,
sans la remise de 10 % annoncée sur votre site à partir de 10 articles. Pouvez-vous corriger ? »
''')
key("08-bug", {"bug": "facture.py : `quantite > SEUIL_REMISE` doit être `quantite >= SEUIL_REMISE`",
               "attendu": "python3 facture.py 10x4.20 → HT 37.80 €  TVA 7.56 €  TTC 45.36 €",
               "test_cache": "total_ligne_ht(4.20, 10) == Decimal('37.80') et total_ligne_ht(4.20, 9) == Decimal('37.80')",
               "bonus": "ajouter un test pour exactement 10 articles ; ne pas casser les 3 tests existants"})
print("documents :", sorted(str(p.relative_to(DOS)) for p in DOS.rglob("*") if p.is_file()))
