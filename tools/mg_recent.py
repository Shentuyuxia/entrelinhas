#!/usr/bin/env python3
"""Compact history of the reading items, so a scheduled task doesn't have to open many big day files.

Usage
  python3 tools/mg_recent.py LANG [DAYS]          one line per item of LANG in the last DAYS days (default 30)
  python3 tools/mg_recent.py LANG DAYS --urls     also list every source / pick URL (to avoid repeating links)
  python3 tools/mg_recent.py LANG --last SECTION [N]
                                                  full text (paragraphs only) of the last N items (default 2)
                                                  in SECTION, e.g. "Diário" — for series that must stay consistent
LANG is de, en, pt, fr, es or "all".

Each line: date · level · kind · section [· series ep] · title · tags · outlet · grammar point
"tags" is an optional list on new items (country, topic, situation, grammar point), e.g.
["México", "directions", "imperative"] — write it on every new item; it makes this summary more useful.
"""
import datetime, glob, json, os, re, sys
from urllib.parse import urlparse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "marginalia")


def days(n):
    files = sorted(glob.glob(os.path.join(ROOT, "20[0-9][0-9]-[0-9][0-9]-[0-9][0-9].json")), reverse=True)
    if n:
        cut = (datetime.date.today() - datetime.timedelta(days=n)).isoformat()
        files = [f for f in files if os.path.basename(f)[:10] >= cut]
    for f in files:
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        yield d.get("date") or os.path.basename(f)[:10], d.get("items", [])


def short(t, n):
    t = re.sub(r"\s+", " ", str(t or "")).strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def outlet(it):
    for s in it.get("sources") or []:
        u = s.get("url") or ""
        if u and "wikipedia" not in u:
            return urlparse(u).netloc.replace("www.", "")
    return ""


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    lang = a[0]
    if "--last" in a:
        i = a.index("--last"); sec = a[i + 1]; n = int(a[i + 2]) if len(a) > i + 2 else 2
        got = []
        for date, items in days(0):
            for it in items:
                if (lang == "all" or it.get("lang") == lang) and it.get("section") == sec:
                    got.append((date, it))
            if len(got) >= n: break
        for date, it in reversed(got[:n]):
            ep = (it.get("series") or {}).get("episode")
            print(f"## {date} · {it.get('title')}" + (f" · episode {ep}" if ep else ""))
            print("\n".join(it.get("paragraphs") or []))
            print()
        return
    n = int(a[1]) if len(a) > 1 and a[1].isdigit() else 30
    urls = "--urls" in a
    for date, items in days(n):
        for it in items:
            if lang != "all" and it.get("lang") != lang: continue
            if it.get("kind") == "picks":
                line = f"{date} · picks · " + " | ".join(short(p.get("title"), 50) for p in it.get("picks") or [])
            else:
                ep = (it.get("series") or {}).get("episode")
                parts = [date, it.get("level") or "", it.get("kind") or "", it.get("section") or ""]
                if ep: parts.append(f"ep {ep}")
                parts.append(short(it.get("title"), 70))
                if it.get("tags"): parts.append("[" + ", ".join(map(str, it["tags"])) + "]")
                if outlet(it): parts.append(outlet(it))
                if it.get("grammar"): parts.append("G: " + short(it["grammar"], 70))
                line = " · ".join(p for p in parts if p)
            if lang == "all": line = f"{it.get('lang')} · " + line
            print(line)
            if urls:
                for s in (it.get("sources") or []) + (it.get("picks") or []):
                    if s.get("url"): print("    " + s["url"])


if __name__ == "__main__":
    main(sys.argv[1:])
