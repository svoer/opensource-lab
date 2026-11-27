"""Banc OpenSource Lab · requêtes simultanées et contexte long.

Usage :
  python3 -u bench2.py http://HOTE:8080 short            # 5 lots à 1, 2 et 4 clients, prompts courts
  python3 -u bench2.py http://HOTE:8080 ctx CLIENTS MOTS # un lot de CLIENTS prompts longs de MOTS mots chacun
  python3 -u bench2.py http://HOTE:8080 ctx CLIENTS MOTS SEED

Chaque ligne JSON décrit un lot. Les débits comptent tous les tokens générés, raisonnement compris.
"""
import concurrent.futures
import json
import random
import sys
import threading
import time
import urllib.error
import urllib.request

base, mode = sys.argv[1:3]
MODEL = "inkling-2-mini-sq-10"
WORDS = ("harbor willow cedar lantern blue green stone valley river field hill light horse garden "
         "silver amber maple forest cloud meadow").split()


def run_group(count, repeat, words=0, label=None):
    barrier = threading.Barrier(count)

    def request(index):
        rng = random.Random(730000 + repeat * 101 + index * 7 + words)
        key = str(rng.randrange(100000, 999999))
        if words:
            blocks = []
            for i in range(words // 10):
                if i == words // 20:
                    blocks.append(f" The audit key is {key}. ")
                blocks.append(" ".join(rng.choices(WORDS, k=10)))
            prompt = f"Read these records. {chr(10).join(blocks)}\nWhat is the audit key? Return only its six digits."
        else:
            prompt = (f"Begin with AUDIT{key}, then write a detailed numbered technical checklist "
                      "for a local AI video studio, at least 30 substantial items.")
        payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                   "stream": True, "stream_options": {"include_usage": True}, "temperature": 0,
                   "max_tokens": 256 if words else 192}
        req = urllib.request.Request(base + "/v1/chat/completions", json.dumps(payload).encode(),
                                     {"Content-Type": "application/json"})
        barrier.wait()
        start = time.monotonic()
        first_any = first = last = None
        output = ""
        usage, timings = {}, {}
        try:
            with urllib.request.urlopen(req, timeout=1800) as stream:
                for line in stream:
                    if not line.startswith(b"data: "):
                        continue
                    item = line[6:].strip()
                    if item == b"[DONE]":
                        break
                    event = json.loads(item)
                    usage = event.get("usage") or usage
                    timings = event.get("timings") or timings
                    if event.get("error"):
                        raise RuntimeError(event["error"])
                    for choice in event.get("choices", []):
                        delta = choice.get("delta", {})
                        if delta.get("content") or delta.get("reasoning_content"):
                            first_any = first_any or time.monotonic()
                        chunk = delta.get("content") or ""
                        if chunk:
                            last = time.monotonic()
                            first = first or last
                            output += chunk
            seconds = time.monotonic() - start
            generated = usage.get("completion_tokens", 0)
            return dict(id=index, ttft_any=round(first_any - start, 3) if first_any else None,
                        ttft=round(first - start, 3) if first else None,
                        seconds=round(seconds, 3), usage=usage, timings=timings,
                        client_tps=round(generated / seconds, 2) if seconds else None,
                        key=key, answer=output[:100], correct=key in output)
        except urllib.error.HTTPError as exc:
            return dict(id=index, error=str(exc), detail=exc.read(2048).decode(errors="replace"),
                        seconds=round(time.monotonic() - start, 3))
        except Exception as exc:  # noqa: BLE001 - le banc consigne toute erreur
            return dict(id=index, error=str(exc), seconds=round(time.monotonic() - start, 3))

    with concurrent.futures.ThreadPoolExecutor(max_workers=count) as pool:
        rows = list(pool.map(request, range(count)))
    tokens = sum(row.get("usage", {}).get("completion_tokens", 0) for row in rows)
    prompt_tokens = sum(row.get("usage", {}).get("prompt_tokens", 0) for row in rows)
    total = max(row["seconds"] for row in rows)
    print(json.dumps(dict(mode=label or mode, count=count, repeat=repeat, words=words, seconds=round(total, 3),
                          aggregate_tps=round(tokens / total, 2), prompt_tokens=prompt_tokens,
                          requests=rows)), flush=True)


if mode == "ctx":
    clients, words = int(sys.argv[3]), int(sys.argv[4])
    run_group(clients, int(sys.argv[5]) if len(sys.argv) > 5 else 50, words)
else:
    for repeat in range(5):
        for count in ((1, 2, 4) if repeat % 2 == 0 else (4, 2, 1)):
            run_group(count, repeat)
