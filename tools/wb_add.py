#!/usr/bin/env python3
"""Add word-bank entries and validate the word lists in data/.

Usage:
  python3 tools/wb_add.py LANG LEVEL new_rows.json   # append rows, skipping words already anywhere in LANG
  python3 tools/wb_add.py --check                     # validate all files and print counts

Row formats (8 fields, all strings):
  pt: [word with article, pos, zh, en, fr, example, example_zh, example_en]
  fr: [word with article, pos, zh, en, de, example, example_zh, example_en]
  de: [word with article, pos, plural or "", zh, en, example, example_zh, example_en]
  en: [word, pos, IPA, zh, English definition, de, example, example_zh]
pos: pt/de/fr nouns use gender m / f / n (pl for plural-only); en nouns use "noun" · v · adj · adv · prep · conj · pron · num · interj · phr · expr
"""
import json, sys, os, re
D = os.path.join(os.path.dirname(__file__), "..", "data")
LV = ["A1", "A2", "B1", "B2", "C1", "C2", "UG"]
TARGET = {"A1": 600, "A2": 600, "B1": 1000, "B2": 1500, "C1": 1500, "C2": 1500, "UG": 800}
# UG = Umgangssprache (German only): everyday spoken phrases, idioms and reactions; pos "expr", plural field ""
def lvs(l): return LV if l == "de" else LV[:-1]

def path(l, lv): return os.path.join(D, f"{l}-{lv}.json")
def load(l, lv):
    p = path(l, lv)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
def save(l, lv, rows):
    json.dump(rows, open(path(l, lv), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
def key(w): return re.sub(r"\s+", " ", w.strip().lower())

def bad(l, r):
    if not isinstance(r, list) or len(r) != 8 or not all(isinstance(x, str) for x in r): return "needs 8 strings"
    need = [0, 1, 3, 4, 5, 6] if l != "en" else [0, 1, 3, 4, 6, 7]
    if any(not r[i].strip() for i in need): return "empty field"
    if l in ("pt", "de", "fr") and not re.search(r"[一-鿿]", r[3 if l == "de" else 2]): return "zh missing"
    return None

def check():
    ok = True
    for l in ("pt", "de", "en", "fr"):
        seen = {}; counts = []
        for lv in lvs(l):
            rows = load(l, lv); counts.append(f"{lv} {len(rows)}/{TARGET[lv]}")
            for r in rows:
                e = bad(l, r)
                if e: ok = False; print(f"  {l}-{lv}: {e}: {r[:2]}")
                k = key(r[0])
                if k in seen: ok = False; print(f"  duplicate {l}: {r[0]} ({seen[k]} and {lv})")
                seen[k] = lv
        print(l, " · ".join(counts), "· total", len(seen))
    return ok

if __name__ == "__main__":
    if sys.argv[1:2] == ["--check"]:
        sys.exit(0 if check() else 1)
    l, lv, f = sys.argv[1], sys.argv[2], sys.argv[3]
    assert l in ("pt", "de", "en", "fr") and lv in lvs(l)
    new = json.load(open(f, encoding="utf-8"))
    have = {key(r[0]) for x in lvs(l) for r in load(l, x)}
    rows = load(l, lv); added = skipped = 0
    for r in new:
        e = bad(l, r)
        if e or key(r[0]) in have: skipped += 1; print("  skip:", r[0] if isinstance(r, list) and r else r, e or "duplicate"); continue
        rows.append(r); have.add(key(r[0])); added += 1
    save(l, lv, rows)
    print(f"{l}-{lv}: +{added} (skipped {skipped}) → {len(rows)}")
