#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""版本备份 / 回滚 / 列表。

注意：备份时会把 SKILL.md 存成 SKILL.md.archived。
原因：运行时（Codex / Claude Code）会递归扫描技能目录，任何叫 SKILL.md 的文件都会被注册成一个技能，
版本快照里的 SKILL.md 会让技能列表里出现一堆重名条目。

用法：
    python version_manager.py --action backup   --slug xiao-bei --base-dir ~/.agents/skills
    python version_manager.py --action list     --slug xiao-bei --base-dir ~/.agents/skills
    python version_manager.py --action rollback --slug xiao-bei --base-dir ~/.agents/skills --version v3
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import sys

FILES = ("self.md", "persona.md", "meta.json")


def _dirs(slug: str, base_dir: str):
    skill_dir = os.path.join(os.path.expanduser(base_dir), slug)
    return skill_dir, os.path.join(skill_dir, "versions")


def backup(slug: str, base_dir: str) -> str:
    skill_dir, versions = _dirs(slug, base_dir)
    meta_path = os.path.join(skill_dir, "meta.json")
    if not os.path.exists(meta_path):
        raise SystemExit(f"找不到 {meta_path}")
    version = json.load(open(meta_path, encoding="utf-8")).get("version", "v0")
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = os.path.join(versions, f"{version}_{stamp}")
    os.makedirs(target, exist_ok=True)
    for name in FILES:
        src = os.path.join(skill_dir, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(target, name))
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if os.path.exists(skill_md):
        shutil.copy2(skill_md, os.path.join(target, "SKILL.md.archived"))
    print(f"已备份到 {target}")
    return target


def rollback(slug: str, base_dir: str, version: str) -> None:
    skill_dir, versions = _dirs(slug, base_dir)
    target = None
    for name in sorted(os.listdir(versions)):
        if name.startswith(version):
            target = os.path.join(versions, name)
    if not target:
        raise SystemExit(f"找不到版本 {version}")
    for name in FILES:
        src = os.path.join(target, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(skill_dir, name))
    archived = os.path.join(target, "SKILL.md.archived")
    if os.path.exists(archived):
        shutil.copy2(archived, os.path.join(skill_dir, "SKILL.md"))
        print("已连 SKILL.md 一起还原")
    else:
        print("已还原 self/persona/meta；请重跑 build_skill.py --action combine 重新合成 SKILL.md")
    print(f"已回滚到 {os.path.basename(target)}")


def listing(slug: str, base_dir: str) -> None:
    _, versions = _dirs(slug, base_dir)
    if not os.path.isdir(versions):
        print("还没有版本快照")
        return
    for name in sorted(os.listdir(versions)):
        path = os.path.join(versions, name)
        if not os.path.isdir(path):
            continue
        meta = os.path.join(path, "meta.json")
        info = json.load(open(meta, encoding="utf-8")) if os.path.exists(meta) else {}
        print(f"  {name}  版本={info.get('version','?')}  修正次数={info.get('corrections_count','?')}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="数字生命体版本管理")
    parser.add_argument("--action", required=True, choices=["backup", "rollback", "list"])
    parser.add_argument("--slug", required=True)
    parser.add_argument("--base-dir", default="~/.agents/skills")
    parser.add_argument("--version")
    args = parser.parse_args(argv)

    if args.action == "backup":
        backup(args.slug, args.base_dir)
    elif args.action == "list":
        listing(args.slug, args.base_dir)
    else:
        if not args.version:
            print("rollback 需要 --version", file=sys.stderr)
            return 2
        rollback(args.slug, args.base_dir, args.version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
