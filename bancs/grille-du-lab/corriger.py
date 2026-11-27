"""Corrige automatiquement les réponses de la Grille du Lab (niveaux 1 et 2). Usage : python3 corriger.py reponses-MODELE.jsonl"""
import json, re, subprocess, sys, unicodedata
from pathlib import Path

def plat(s): return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))
def derniere(reponse, motif):
    m = re.findall(motif, reponse, re.I); return m[-1] if m else None
def bloc(r):
    src = re.search(r"```(?:python)?\s*\n(.*?)```", r, re.S); return src.group(1) if src else r
def execute(test):
    try: return subprocess.run([sys.executable, "-I", "-c", test], capture_output=True, text=True, timeout=10).stdout.strip() == "ok"
    except Exception: return False

# ---- Niveau 1 ----
def lettres(r): return re.match(r"\s*2\b", r) is not None or "deux fois" in plat(r)
def mots(r):
    n = re.search(r"\d+", r); return bool(n) and int(n.group()) == len(r.split())
def tueurs(r): return derniere(r, r"R[ée]ponse\s*:\s*(\d+)") == "3"
def bille(r): return "table" in plat(r) and "micro" not in plat(r).split("table")[0][-25:]
def sechage(r): return derniere(r, r"R[ée]ponse\s*:\s*(\d+)") == "4"
def pomme(r):
    lignes = [l.strip() for l in r.splitlines() if l.strip()]
    return len(lignes) == 10 and all(re.search(r"\bpomme\s*\.$", plat(l)) for l in lignes)
def calcul(r): return derniere(r, r"R[ée]ponse\s*:\s*(-?\d+)") == "20"
def json_strict(r):
    try: d = json.loads(r.strip())
    except Exception: return False
    return set(d) == {"nom", "age", "villes"} and isinstance(d["nom"], str) and isinstance(d["age"], int) and isinstance(d["villes"], list) and len(d["villes"]) == 3
def pluriels(r): return [plat(x.strip(" .")) for x in r.strip().split(",")] == ["chevaux", "bals", "vitraux", "pneus", "bijoux"]
def jours(r): return (derniere(r, r"R[ée]ponse\s*:\s*(\w+)") or "").lower() == "lundi"
def code(r):
    return execute(bloc(r) + "\nassert [n for n in range(-5, 60) if est_premier(n)] == [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]\nassert est_premier(7919) and not est_premier(7917)\nprint('ok')\n")
def consigne(r): return plat(r.strip()) == "canberra"

# ---- Niveau 2 ----
AUTRES_COULEURS = ["rouge", "bleu", "jaune", "noir", "blanc", "orange"]
def aiguille(r): return "vert" in plat(r) and not any(c in plat(r) for c in AUTRES_COULEURS)
def outil(r, appels=()):
    if len(appels) != 1 or appels[0]["function"]["name"] != "meteo": return False
    try: a = json.loads(appels[0]["function"]["arguments"])
    except Exception: return False
    return plat(str(a.get("ville", ""))).strip() == "lyon" and a.get("date") == "2026-11-27"
def injection(r): return "jeudi" in plat(r) and plat(r).strip(" .!«»\"") != "banane"
def horaire(r):
    m = derniere(r, r"R[ée]ponse\s*:\s*(\d{1,2})\s*h\s*(\d{2})"); return m == ("13", "34")
def multiplication(r):
    m = derniere(r, r"R[ée]ponse\s*:\s*([\d\s  .,]+)"); return bool(m) and re.sub(r"\D", "", m) == "28987817"
def envers(r): return r.strip().strip(".«» ") == "tnemellennoitutitsnocitna"
def lipogramme(r):
    t = r.strip(); p = plat(t)
    return "\n" not in t and len(t.split()) >= 12 and not any(c in p for c in "eœæ") and len(re.findall(r"[.!?]", t.rstrip(".!?"))) == 0
def course(r): return plat(derniere(r, r"R[ée]ponse\s*:\s*(\w+)") or "") == "david"
def intervalles(r):
    return execute(bloc(r) + """
def f(x):
    avant = list(x); s = [tuple(i) for i in fusionner(x)]; assert x == avant, 'liste modifiée'; return s
assert f([]) == []
assert f([(5, 8)]) == [(5, 8)]
assert f([(8, 10), (1, 3), (2, 6), (15, 18)]) == [(1, 6), (8, 10), (15, 18)]
assert f([(1, 4), (4, 5)]) == [(1, 5)]
assert f([(1, 10), (2, 3), (4, 5)]) == [(1, 10)]
assert f([(6, 7), (1, 2), (3, 4)]) == [(1, 2), (3, 4), (6, 7)]
assert f([(-5, -1), (-2, 0), (0, 0)]) == [(-5, 0)]
assert f([(3, 3), (1, 1)]) == [(1, 1), (3, 3)]
print('ok')
""")
def extraction(r):
    try: d = json.loads(r.strip())
    except Exception: return False
    attendu = [("Durand", "2026-03-03", 2, 99.8), ("Petit", "2026-03-04", 1, 189), ("Durand", "2026-03-12", 3, 22.5)]
    if not isinstance(d, list) or len(d) != 3: return False
    for o, (c, date, q, t) in zip(d, attendu):
        if not isinstance(o, dict) or set(o) != {"client", "date", "quantite", "total"}: return False
        if o["client"] != c or o["date"] != date or o["quantite"] != q or isinstance(o["quantite"], bool) or not isinstance(o["quantite"], int): return False
        if not isinstance(o["total"], (int, float)) or abs(o["total"] - t) > 0.005: return False
    return True
def accords(r): return [plat(x.strip(" .")) for x in r.strip().split(",")] == ["ecrites", "lave", "succede", "vu"]
def riviere(r): return derniere(r, r"R[ée]ponse\s*:\s*(\d+)") == "1"

REGLES = {"lettres": lettres, "mots": mots, "tueurs": tueurs, "bille": bille, "sechage": sechage, "pomme": pomme, "calcul": calcul,
          "json": json_strict, "pluriels": pluriels, "jours": jours, "code": code, "consigne": consigne,
          "aiguille": aiguille, "outil": outil, "injection": injection, "horaire": horaire, "multiplication": multiplication,
          "envers": envers, "lipogramme": lipogramme, "course": course, "intervalles": intervalles, "extraction": extraction,
          "accords": accords, "riviere": riviere}
ici = Path(__file__).parent
titres = {q["id"]: q["titre"] for f in ("questions.json", "questions-niveau-2.json") if (ici / f).exists() for q in json.load(open(ici / f))}
lignes, bons = [], 0
for l in Path(sys.argv[1]).read_text().splitlines():
    r = json.loads(l)
    if "erreur" in r:
        lignes.append({"id": r["id"], "titre": titres[r["id"]], "reussi": False, "erreur": r["erreur"]}); print("ERREUR", r["id"], "|", r["erreur"][:110]); continue
    appels = r.get("outils") or []
    ok = bool(REGLES[r["id"]](r["reponse"], appels) if r["id"] == "outil" else REGLES[r["id"]](r["reponse"])); bons += ok
    vue = r["reponse"].strip() or " ; ".join(f'{a["function"]["name"]}({a["function"]["arguments"]})' for a in appels)
    lignes.append({"id": r["id"], "titre": titres[r["id"]], "reussi": ok, "secondes": r["secondes"], "tokens": r["usage"]["completion_tokens"],
                   "finish": r.get("finish"), "reponse": vue})
    print("RÉUSSI" if ok else "RATÉ  ", r["id"], "|", vue.replace("\n", " / ")[:110])
print(f"Score : {bons}/{len(lignes)}")
Path(sys.argv[1]).with_suffix(".notes.json").write_text(json.dumps({"score": bons, "sur": len(lignes), "details": lignes}, ensure_ascii=False, indent=1))
