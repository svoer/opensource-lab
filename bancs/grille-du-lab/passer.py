"""Grille du Lab : fait passer les questions une par une au modèle servi par Strata (température 0).
S'exécute sur le serveur :
  scp passer.py questions.json TON_SERVEUR:/tmp/ && ssh TON_SERVEUR 'cd /tmp && python3 -u passer.py' > reponses.jsonl
  scp passer.py questions-niveau-2.json TON_SERVEUR:/tmp/ && ssh TON_SERVEUR 'cd /tmp && python3 -u passer.py questions-niveau-2.json' > reponses-niveau-2.jsonl
"""
import json, sys, time, urllib.request
args = sys.argv[1:]
FICHIER = next((a for a in args if a.endswith(".json")), "questions.json")
BASE = next((a for a in args if a.startswith("http")), "http://127.0.0.1:8080")
for item in json.load(open(FICHIER)):
    messages = ([{"role": "system", "content": item["systeme"]}] if item.get("systeme") else []) + [{"role": "user", "content": item["q"]}]
    payload = {"model": "inkling-2-mini-sq-10", "messages": messages, "temperature": 0, "max_tokens": 8000 if "niveau-2" in FICHIER else 3000}
    if item.get("outils"):
        payload["tools"] = item["outils"]
    req = urllib.request.Request(BASE + "/v1/chat/completions", json.dumps(payload).encode(), {"Content-Type": "application/json"})
    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            out = json.load(r)
    except Exception as e:  # une question qui plante ne doit pas faire perdre les autres
        detail = e.read().decode(errors="replace")[:500] if hasattr(e, "read") else ""
        print(json.dumps({"id": item["id"], "erreur": f"{e} {detail}"}, ensure_ascii=False), flush=True)
        continue
    msg = out["choices"][0]["message"]
    print(json.dumps({"id": item["id"], "secondes": round(time.monotonic() - start, 2), "usage": out.get("usage"),
                      "finish": out["choices"][0].get("finish_reason"), "raisonnement": msg.get("reasoning_content", ""),
                      "reponse": msg.get("content") or "", "outils": msg.get("tool_calls") or []}, ensure_ascii=False), flush=True)
