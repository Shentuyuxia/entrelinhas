#!/usr/bin/env python3
"""Rebuild marginalia/index.json from the day files marginalia/YYYY-MM-DD.json."""
import datetime, glob, json, os, sys

root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "marginalia")
days = []
for f in sorted(glob.glob(os.path.join(root, "20[0-9][0-9]-[0-9][0-9]-[0-9][0-9].json")), reverse=True):
    with open(f, encoding="utf-8") as fh:
        d = json.load(fh)
    items = [{"i": i, "lang": it.get("lang"), "title": it.get("title"), "kind": it.get("kind"),
              "level": it.get("level"), "hour": it.get("hour")} for i, it in enumerate(d.get("items", []))]
    days.append({"date": d.get("date") or os.path.basename(f)[:10], "items": items})
with open(os.path.join(root, "index.json"), "w", encoding="utf-8") as fh:
    json.dump({"updated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "days": days},
              fh, ensure_ascii=False, indent=1)
print(f"index.json: {len(days)} days, {sum(len(d['items']) for d in days)} items")
