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

    def test_remise_exactement_10_articles(self):
        self.assertEqual(total_ligne_ht(4.20, 10), Decimal("37.80"))


if __name__ == "__main__":
    unittest.main()
