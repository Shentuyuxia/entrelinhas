#!/usr/bin/env python3
"""Build the offline Portuguese dictionary dict/pt/ from Wiktionary data (wiktextract / kaikki.org).

Usage:
  python3 tools/build_ptdict.py kaikki-portuguese.jsonl[.gz]   # one JSON object per line (lang_code "pt")

Normally run on GitHub (.github/workflows/build-ptdict.yml), which downloads the data from kaikki.org first.

Output (CC BY-SA 4.0, like Wiktionary itself – see dict/pt/LICENSE.md):
  dict/pt/NNN.json   512 shards; word -> list of entries; shard = FNV-1a hash of the word (see ptHash in index.html)
  dict/pt/meta.json  counts, source, build date

One entry = [pos, senses, ipa, gender]
  senses: list of [gloss]            ordinary meaning (English, from English Wiktionary)
          or      [code, lemma]      inflected form, e.g. ["1.s.pret.ind", "falar"]; the app turns the code into words
          or      [gloss, lemma]     other "… of LEMMA" senses whose tags have no code (gloss kept as text)
  ipa:    Brazilian pronunciation if given, else the first IPA
  gender: "m", "f", "mf" or ""
"""
import gzip, json, os, re, sys, time, unicodedata
from collections import defaultdict

SHARDS = 512
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "dict", "pt")
MAX_POS, MAX_SENSES, MAX_GLOSS = 3, 4, 160

# grammatical tags → short codes (order = order of display)
TAGS = [("first-person", "1"), ("second-person", "2"), ("third-person", "3"),
        ("singular", "s"), ("plural", "p"),
        ("masculine", "m"), ("feminine", "f"),
        ("present", "pres"), ("preterite", "pret"), ("imperfect", "impf"), ("pluperfect", "plup"),
        ("future", "fut"), ("conditional", "cond"), ("past", "past"),
        ("indicative", "ind"), ("subjunctive", "subj"), ("imperative", "imp"),
        ("affirmative", "aff"), ("negative", "neg"),
        ("infinitive", "inf"), ("personal", "pers"), ("impersonal", "impers"),
        ("gerund", "ger"), ("participle", "ptcp"),
        ("diminutive", "dim"), ("augmentative", "aug"), ("superlative", "sup"), ("comparative", "comp")]
TAG_CODE = dict(TAGS)
IGNORE_TAGS = {"form-of", "inflection-of", "multiword-construction", "with-enclitic", "Brazil", "Portugal",
               "error-unknown-tag", "combined-form", "masculine-usually"}
SKIP_SENSE_TAGS = {"obsolete", "archaic", "rare", "dated", "misspelling", "nonstandard"}
POS_KEEP = None  # keep every part of speech


def fnv(s):  # FNV-1a 32-bit over UTF-16 code units – same as ptHash() in index.html
    h = 0x811C9DC5
    b = s.encode("utf-16-le")
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8)
        h = (h * 16777619) & 0xFFFFFFFF
    return h % SHARDS


def clean(t):
    t = re.sub(r"\s+", " ", str(t or "")).strip()
    return t if len(t) <= MAX_GLOSS else t[: MAX_GLOSS - 1].rstrip() + "…"


def ipa_of(e):
    ipas = [(s.get("ipa"), s.get("tags") or []) for s in e.get("sounds") or [] if s.get("ipa")]
    for ipa, tags in ipas:
        if any(t in ("Brazil", "Brazilian-Portuguese", "São-Paulo", "Rio-de-Janeiro") for t in tags):
            return ipa
    return ipas[0][0] if ipas else ""


def gender_of(e):
    tags = set(e.get("tags") or [])
    for f in e.get("head_templates") or []:
        exp = f.get("expansion") or ""
        if re.search(r"\bm\b", exp): tags.add("masculine")
        if re.search(r"\bf\b", exp): tags.add("feminine")
    m, f = "masculine" in tags, "feminine" in tags
    return "mf" if m and f else "m" if m else "f" if f else ""


def form_code(tags):
    tags = [t for t in tags if t not in IGNORE_TAGS]
    if not tags or any(t not in TAG_CODE for t in tags):
        return None
    order = {t: i for i, (t, _) in enumerate(TAGS)}
    return ".".join(TAG_CODE[t] for t in sorted(set(tags), key=order.get))


def senses_of(e):
    out, plain = [], []
    for s in e.get("senses") or []:
        tags = set(s.get("tags") or [])
        fo = s.get("form_of") or s.get("alt_of")
        gl = clean((s.get("glosses") or [""])[0])
        if fo and fo[0].get("word"):
            lemma = fo[0]["word"]
            code = form_code(s.get("tags") or []) if s.get("form_of") else None
            out.append([code, lemma] if code else [gl or ("form of " + lemma), lemma])
        elif gl:
            (plain if tags & SKIP_SENSE_TAGS else out).append([("Portugal: " if "Portugal" in tags else "") + gl])
    if not out: out = plain  # only rare/archaic senses: keep them
    seen, res = set(), []
    for x in out:
        k = tuple(x)
        if k not in seen: seen.add(k); res.append(x)
    return res[:MAX_SENSES]


def open_any(path):
    return gzip.open(path, "rt", encoding="utf-8") if path.endswith(".gz") else open(path, encoding="utf-8")


def main(src):
    words = defaultdict(list)
    n_in = n_pt = 0
    t0 = time.time()
    with open_any(src) as fh:
        for line in fh:
            n_in += 1
            try: e = json.loads(line)
            except ValueError: continue
            if e.get("lang_code") != "pt" or not e.get("word"): continue
            ss = senses_of(e)
            if not ss: continue
            n_pt += 1
            w = unicodedata.normalize("NFC", e["word"])
            if len(words[w]) < MAX_POS:
                words[w].append([e.get("pos") or "", ss, ipa_of(e), gender_of(e)])
            if n_in % 200000 == 0: print(f"  {n_in} lines, {len(words)} words, {time.time()-t0:.0f}s", flush=True)
    shards = defaultdict(dict)
    for w, es in words.items(): shards[fnv(w)][w] = es
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if re.fullmatch(r"\d{3}\.json", f): os.remove(os.path.join(OUT, f))
    size = 0
    for k in range(SHARDS):
        p = os.path.join(OUT, f"{k:03d}.json")
        with open(p, "w", encoding="utf-8") as fh: json.dump(shards.get(k, {}), fh, ensure_ascii=False, separators=(",", ":"))
        size += os.path.getsize(p)
    forms = sum(1 for es in words.values() if all(len(s) == 2 for e in es for s in e[1]))
    meta = {"words": len(words), "inflected_only": forms, "entries": n_pt, "shards": SHARDS, "bytes": size,
            "source": "English Wiktionary via wiktextract / kaikki.org", "license": "CC BY-SA 4.0",
            "built": time.strftime("%Y-%m-%d")}
    with open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8") as fh: json.dump(meta, fh, ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
