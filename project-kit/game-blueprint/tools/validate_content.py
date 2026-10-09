#!/usr/bin/env python3
"""Validate a mygame content tree (stdlib only).

Usage: python validate_content.py <content_dir> [--check-files]
Exit code 0 = no errors (warnings allowed), 1 = errors.
"""
import json
import re
import sys
from pathlib import Path

RANKS = {"-", "D", "C", "B", "A"}
FACTIONS = {"player", "enemy", "ally", "neutral"}
TRIGGERS = {"turn_start", "unit_defeated", "hp_below", "after_battle", "before_battle",
            "all_enemies_defeated", "faction_remaining", "area_enter", "persuade",
            "opening", "deploy", "ending", "delay"}
FIELDS = {
    "pilots": {"id", "name_key", "portrait", "spirits", "stats"},
    "units": {"id", "name_key", "sprite", "hp", "en", "armor", "terrain", "weapons"},
    "weapons": {"id", "name_key", "power", "melee", "range", "en_cost"},
    "spirits": {"id", "name_key", "sp_cost", "until", "effect"},
}
PLACEHOLDER = re.compile(r"\{[A-Za-z]+[A-Za-z0-9:]*\}")


def load(path, errors):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        errors.append(f"{path}: cannot read JSON ({e})")
        return None


def validate(root, check_files=False):
    root = Path(root)
    errors, warnings = [], []
    ids = {}

    def err(m):
        errors.append(m)

    # --- records
    for kind, allowed in FIELDS.items():
        p = root / "data" / f"{kind}.json"
        if not p.exists():
            err(f"{p}: missing")
            continue
        doc = load(p, errors)
        if doc is None:
            continue
        if doc.get("schema") != f"mygame.{kind}.v1":
            err(f"{p}: bad schema {doc.get('schema')!r}")
        for r in doc.get("records", []):
            rid = r.get("id", "?")
            for k in set(r) - allowed:
                err(f"{rid}: unknown field {k!r}")
            for k in allowed - set(r):
                err(f"{rid}: missing field {k!r}")
            if rid in ids:
                err(f"duplicate id {rid}")
            ids[rid] = kind
    recs = {}
    for kind in FIELDS:
        doc = load(root / "data" / f"{kind}.json", []) or {}
        recs[kind] = {r["id"]: r for r in doc.get("records", []) if "id" in r}

    for u in recs["units"].values():
        for w in u.get("weapons", []):
            if w not in recs["weapons"]:
                err(f"{u['id']}: unknown weapon {w}")
        for t, rk in u.get("terrain", {}).items():
            if rk not in RANKS:
                err(f"{u['id']}: bad terrain rank {rk!r} for {t}")
    for p in recs["pilots"].values():
        for s in p.get("spirits", []):
            if s not in recs["spirits"]:
                err(f"{p['id']}: unknown spirit {s}")

    # --- upgrade rules
    ur = load(root / "data" / "rules" / "upgrade-rules.json", errors)
    if ur:
        if not 5 <= ur.get("cap", 0) <= 15:
            err("upgrade-rules: cap must be 5..15")
        if len(ur.get("curve", [])) != 15:
            err("upgrade-rules: curve must have 15 entries")
        pr = ur.get("price", [])
        if len(pr) != 15 or not all(1 <= x <= 99998 for x in pr):
            err("upgrade-rules: price needs 15 values in 1..99998")

    # --- art manifest
    art = (load(root / "art" / "manifest.json", errors) or {}).get("assets", {})
    for kind, field in (("pilots", "portrait"), ("units", "sprite")):
        for r in recs[kind].values():
            if r.get(field) not in art:
                err(f"{r['id']}: {field} {r.get(field)!r} not in art manifest")
    if check_files:
        for k, a in art.items():
            if not (root / a["file"]).exists():
                err(f"art {k}: file missing {a['file']}")

    # --- locales
    locales = {}
    for f in sorted((root / "locales").glob("*.json")):
        d = load(f, errors)
        if d:
            locales[d.get("locale", f.stem)] = d
    keys_needed = {r["name_key"] for k in FIELDS for r in recs[k].values() if "name_key" in r}

    # --- scenes / campaign
    camp = load(root / "campaign.json", errors) or {}
    stages = camp.get("stages", {})
    if camp.get("start") not in stages:
        err("campaign: start not in stages")
    keys_needed.add(camp.get("name_key", ""))
    graph = {}
    dlg_refs = set()
    for sid, st in stages.items():
        sc = load(root / st["file"], errors)
        if not sc:
            continue
        if sc.get("id") != sid:
            err(f"{st['file']}: id {sc.get('id')} != stage {sid}")
        keys_needed.add(sc.get("title_key", ""))
        for d in sc.get("deployments", []):
            if d.get("template") not in recs["units"]:
                err(f"{sid}: deployment unit {d.get('template')} unknown")
            if d.get("pilot") not in recs["pilots"]:
                err(f"{sid}: deployment pilot {d.get('pilot')} unknown")
            if d.get("faction") not in FACTIONS:
                err(f"{sid}: bad faction {d.get('faction')}")
        graph[sid] = set()
        terminal = False
        for ev in sc.get("events", []):
            if ev.get("trigger", {}).get("type") not in TRIGGERS:
                err(f"{sid}/{ev.get('id')}: bad trigger")
            for c in ev.get("commands", []):
                if c.get("op") == "next_scene":
                    graph[sid].add(c.get("scene"))
                    if c.get("scene") not in stages:
                        err(f"{sid}: next_scene {c.get('scene')} not in campaign")
                elif c.get("op") in ("ending", "game_over"):
                    terminal = True
                elif c.get("op") == "dialogue":
                    dlg_refs.add(c.get("ref"))
        if not graph[sid] and not terminal:
            warnings.append(f"{sid}: dead end (no next_scene/ending)")
    seen, todo = set(), [camp.get("start")]
    while todo:
        s = todo.pop()
        if s in seen or s not in graph:
            continue
        seen.add(s)
        todo.extend(graph[s])
    for s in set(stages) - seen:
        warnings.append(f"{s}: unreachable from start")

    # --- locale keys
    src = next((d for d in locales.values() if d.get("locale") == d.get("source_locale")), None)
    for loc, d in locales.items():
        for k in keys_needed - {""}:
            if k not in d.get("names", {}):
                (errors if d is src else warnings).append(f"locale {loc}: missing key {k}")

    # --- dialogue refs
    declared = set()
    for f in (root / "dialogue").glob("*/story/*.txt"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("@"):
                declared.add(line[1:].split()[0])
    if (root / "dialogue").exists():
        for r in dlg_refs - declared:
            err(f"dialogue ref {r} not found in any dialogue file")
    return errors, warnings


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    errors, warnings = validate(argv[0], "--check-files" in argv)
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
