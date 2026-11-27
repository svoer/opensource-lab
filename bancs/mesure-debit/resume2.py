"""Résume un fichier de mesures bench2.py : débit total, débit par client, délais."""
import json, statistics as st, sys
from collections import defaultdict
from pathlib import Path

def med(v):
    v = [x for x in v if x is not None]
    return f"{st.median(v):.2f} [{min(v):.2f}–{max(v):.2f}]" if v else "—"
for name in sys.argv[1:]:
    groups = defaultdict(list)
    for line in Path(name).read_text().splitlines():
        if line.strip(): 
            run = json.loads(line); groups[(run["count"], run["words"])].append(run)
    for (count, words), runs in sorted(groups.items()):
        reqs = [r for run in runs for r in run["requests"]]
        ok = [r for r in reqs if r.get("correct") and not r.get("error")]
        print(f"{Path(name).name} clients={count} mots={words} lots={len(runs)} valides={len(ok)}/{len(reqs)}")
        print("  débit total tok/s      ", med([run["aggregate_tps"] for run in runs]))
        print("  débit par client tok/s ", med([r["client_tps"] for r in ok]))
        print("  génération seule tok/s ", med([r["timings"]["predicted_per_second"] for r in ok if r.get("timings")]))
        print("  lecture prompt tok/s   ", med([r["timings"]["prompt_per_second"] for r in ok if r.get("timings")]))
        print("  1er token (tout) s     ", med([r["ttft_any"] for r in ok if r.get("ttft_any")]))
        print("  1er texte visible s    ", med([r["ttft"] for r in ok if r.get("ttft")]))
        print("  fin du lot s           ", med([run["seconds"] for run in runs]))
        print("  tokens entrée/requête  ", med([r["usage"]["prompt_tokens"] for r in ok]),
              "| sortie", med([r["usage"]["completion_tokens"] for r in ok]),
              "| cache", med([r["usage"].get("prompt_tokens_details", {}).get("cached_tokens", 0) for r in ok]))
        for r in reqs:
            if r not in ok: print("  ÉCHEC:", {k: r.get(k) for k in ("id", "error", "detail", "answer", "seconds", "usage")})
