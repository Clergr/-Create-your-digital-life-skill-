#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出所有已生成的数字生命体。

用法：
    python list_lives.py                      # 自动探测技能目录
    python list_lives.py --base-dir ~/.agents/skills
    python list_lives.py --json
"""

from __future__ import annotations

import argparse
import json
import os

CANDIDATES = ("~/.agents/skills", "~/.claude/skills", "~/.codex/skills")


def find_lives(base_dir: str):
    out = []
    root = os.path.expanduser(base_dir)
    if not os.path.isdir(root):
        return out
    for slug in sorted(os.listdir(root)):
        skill_dir = os.path.join(root, slug)
        meta_path = os.path.join(skill_dir, "meta.json")
        if not os.path.isfile(meta_path):
            continue
        try:
            meta = json.load(open(meta_path, encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        profile = meta.get("profile") or {}
        out.append({
            "slug": slug,
            "name": meta.get("name", slug),
            "version": meta.get("version", "?"),
            "status": meta.get("status", "?"),
            "corrections": meta.get("corrections_count", 0),
            "updated_at": (meta.get("updated_at") or "?")[:10],
            "triggers": meta.get("triggers") or [],
            "summary": " · ".join(p for p in (profile.get("occupation"), profile.get("city")) if p),
            "path": skill_dir,
        })
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="列出所有数字生命体")
    parser.add_argument("--base-dir", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    dirs = [args.base_dir] if args.base_dir else \
        [c for c in CANDIDATES if os.path.isdir(os.path.expanduser(c))]
    lives = []
    for d in dirs:
        lives += find_lives(d)

    if args.json:
        print(json.dumps(lives, ensure_ascii=False, indent=2))
        return 0
    if not lives:
        print("还没有任何数字生命体。说「帮我做一个数字生命体」开始。")
        return 0

    print(f"共 {len(lives)} 个数字生命体：\n")
    for it in lives:
        print(f"  {it['name']}（{it['slug']}）  {it['version']} · {it['status']}")
        if it["summary"]:
            print(f"    {it['summary']}")
        if it["triggers"]:
            print("    触发词：" + " / ".join(it["triggers"]))
        print(f"    修正 {it['corrections']} 次 · 更新于 {it['updated_at']}")
        print(f"    {it['path']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
