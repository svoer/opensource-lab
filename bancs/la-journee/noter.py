"""Contrôles automatiques du banc « La journée » : ce qu'un script peut vérifier sans débat.

Usage : python3 noter.py          → affiche, épreuve par épreuve, les contrôles chiffrés et la durée réelle de Pi
Le jugement final (réussi / à reprendre / raté) se fait en relisant reponse.md à côté du corrigé (corriges/).
"""
import csv
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RES, COR = ROOT / "resultats", ROOT / "corriges"


def lire(e, f="reponse.md"):
    p = RES / e / "fichiers" / f
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def sans_accent(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def session(e):
    """Durée réelle de travail et tokens, d'après la session Pi (horodatages et usage des messages)."""
    p = RES / e / "session.jsonl"
    if not p.exists() or not p.read_text().strip():
        return "session absente"
    stamps, out, inp = [], 0, 0
    for line in p.read_text().splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        ts = ev.get("timestamp") or (ev.get("message") or {}).get("timestamp")
        if isinstance(ts, str):
            stamps.append(datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp())
        elif isinstance(ts, (int, float)):
            stamps.append(ts / 1000 if ts > 1e11 else ts)
        u = (ev.get("message") or {}).get("usage") or {}
        out += u.get("output", 0) or 0
        inp += u.get("input", 0) or 0
    d = max(stamps) - min(stamps) if len(stamps) > 1 else 0
    return f"{d:.0f} s de travail, {out} tokens écrits, {inp} lus"


def c01():
    k, t = json.loads((COR / "01-mails.json").read_text()), lire("01-mails")
    nums = [int(n) for n in re.findall(r"[Mm]ail\s*(?:n°\s*)?0?(\d{1,2})", t)]
    vus = {nom: n in nums for nom, n in k["urgents"].items()}
    faux = [n for n in k["fausses_urgences"] if n in nums[:6]]
    return f"urgents cités {vus} ; fausses urgences parmi les 6 premiers cités : {faux or 'aucune'} ; premier cité : mail {nums[0] if nums else '?'} (attendu {k['plus_urgent']})"


def c02():
    t = sans_accent(lire("02-contrat"))
    return (f"1 mois cité : {'1 mois' in t or 'un mois' in t} ; « 3 mois » cité : {'3 mois' in t or 'trois mois' in t} ; "
            f"31 décembre : {'31 decembre' in t or '31/12' in t} ; 850 € : {'850' in t} ; 780 € : {'780' in t} ; "
            f"article 17 : {'17' in t} ; frais de relocation réclamés : {'frais de relocation' in t and 'aucun' not in t}")


def c03():
    k, t = json.loads((COR / "03-repas.json").read_text()), lire("03-repas")
    tn = sans_accent(t)
    interdits = [w for w in k["interdits"] if re.search(r"\b" + sans_accent(w), tn)]
    prix = []
    for line in t.splitlines():
        if line.startswith("|") and not re.search(r"total", line, re.I):
            cells = [c.strip() for c in line.strip("|").split("|")]
            m = re.search(r"(\d+[,.]\d{1,2})\s*€?\s*$", cells[-1]) if cells else None
            if m:
                prix.append(Decimal(m.group(1).replace(",", ".")))
    annonce = re.findall(r"total[^\n\d]*(\d+[,.]\d{2})", t, re.I)
    return f"somme recalculée des lignes : {sum(prix)} € ({len(prix)} lignes) ; total annoncé : {annonce[-1] if annonce else '?'} ; fruits à coque cités : {interdits or 'aucun'}"


def c04():
    k, t = json.loads((COR / "04-reunion.json").read_text()), sans_accent(lire("04-reunion"))
    reperes = ["newsletter", "salon", "tarif", "alternant", "bertin", "mardi"]
    trouve = [r for r in reperes if r in t]
    appli = "appli" in t or "application mobile" in t
    return f"décisions retrouvées : {len(trouve)}/6 {trouve} ; appli mobile mentionnée : {appli} (doit être absente ou marquée abandonnée)"


def c05():
    k = json.loads((COR / "05-comptes.json").read_text())
    p = RES / "05-comptes" / "fichiers" / "categories.csv"
    if not p.exists():
        return "categories.csv absent"
    rows = list(csv.reader(p.open(encoding="utf-8"), delimiter=";" if ";" in p.read_text()[:200] else ","))
    head = [sans_accent(h) for h in rows[0]]
    try:
        i_d, i_m, i_c = head.index("date"), head.index("montant"), head.index("categorie")
    except ValueError:
        return f"colonnes inattendues : {rows[0]}"
    tot = {}
    for r in rows[1:]:
        if len(r) <= max(i_d, i_m, i_c):
            continue
        d, m = r[i_d], Decimal(r[i_m].replace(",", ".").replace(" ", ""))
        mois = f"{d[6:10]}-{d[3:5]}" if "/" in d else d[:7]
        tot[(mois, r[i_c].strip())] = tot.get((mois, r[i_c].strip()), Decimal(0)) + m
    justes, faux = 0, []
    for mois, cats in k["totaux_par_mois_et_categorie"].items():
        for c, v in cats.items():
            if tot.get((mois, c), Decimal(0)) == Decimal(str(v)).quantize(Decimal("0.01")):
                justes += 1
            else:
                faux.append(f"{mois} {c} : {tot.get((mois, c))} au lieu de {v}")
    n = sum(len(c) for c in k["totaux_par_mois_et_categorie"].values())
    t = lire("05-comptes")
    dep = {m: str(v).replace(".", ",") in t or str(v) in t for m, v in k["depenses_par_mois"].items()}
    g = (RES / "05-comptes" / "fichiers" / "graphique.html").exists()
    return f"classement : {justes}/{n} totaux justes au centime ; {len(rows) - 1}/{k['lignes']} lignes ; dépenses mensuelles justes dans reponse.md : {dep} ; graphique : {g}" + (f" ; écarts : {faux[:4]}" if faux else "")


def c06():
    t = lire("06-devoirs")
    return f"204 : {'204' in t} ; 224,40 : {'224,40' in t or '224.40' in t or '224,4 ' in t} ; 228 : {'228' in t} ; « pas le même » : {bool(re.search(r'(pas|n.est pas) le m[eê]me', t, re.I))}"


def c07():
    p = RES / "07-tetris" / "fichiers" / "index.html"
    if not p.exists():
        return "index.html absent"
    h = p.read_text(encoding="utf-8", errors="replace")
    pal = [c for c in ("#0f380f", "#306230", "#8bac0f", "#9bbc0f") if c in h.lower()]
    r = subprocess.run(["node", str(ROOT / "pi-lab/skills/verifier-page/check.mjs"), str(p)], capture_output=True, text=True)
    return f"{len(h.splitlines())} lignes ; syntaxe : {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[:80]} ; palette Game Boy : {len(pal)}/4 ; à jouer à l'écran pour juger"


def c08():
    d = RES / "08-bug" / "fichiers" / "projet"
    if not d.exists():
        return "projet absent"
    cache = ("import sys; sys.path.insert(0, '.'); from decimal import Decimal; from facture import total_ligne_ht, total_commande;"
             "assert total_ligne_ht(4.20, 10) == Decimal('37.80'); assert total_ligne_ht(12.50, 3) == Decimal('37.50');"
             "assert total_ligne_ht(5, 12) == Decimal('54.00'); assert total_ligne_ht(4.20, 9) == Decimal('37.80'); print('test caché OK')")
    a = subprocess.run([sys.executable, "-c", cache], cwd=d, capture_output=True, text=True)
    b = subprocess.run([sys.executable, "-m", "unittest"], cwd=d, capture_output=True, text=True)
    n = re.search(r"Ran (\d+) test", b.stderr)
    return f"{(a.stdout or a.stderr).strip().splitlines()[-1]} ; tests du projet : {n.group(1) if n else '?'} lancés, {'OK' if b.returncode == 0 else 'ÉCHEC'}"


for e, f in [("01-mails", c01), ("02-contrat", c02), ("03-repas", c03), ("04-reunion", c04), ("05-comptes", c05),
             ("06-devoirs", c06), ("07-tetris", c07), ("08-bug", c08)]:
    if (RES / e).exists():
        try:
            print(f"{e:11} · {session(e)}\n            {f()}")
        except Exception as x:  # un contrôle qui casse ne doit pas cacher les autres
            print(f"{e:11} · contrôle impossible : {x}")
