#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布前自检：扫凭据、扫第三方身份、扫超长引用、扫被忽略目录。

用法：
    python tools/preflight.py --root .

退出码 0 = 可以发布；1 = 发现问题，先修再发。
"""

from __future__ import annotations

import argparse
import os
import re
import sys

CHECKS = [
    ("凭据", re.compile(r"密码|passwd|password|token|secret|api[_-]?key|sk-[A-Za-z0-9]{8,}")),
    ("手机号", re.compile(r"1[3-9]\d{9}")),
    ("邮箱", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|cn|net)")),
    ("微信 id", re.compile(r"wxid_[A-Za-z0-9]+")),
    ("身份证", re.compile(r"\b\d{17}[\dXx]\b")),
    ("银行卡", re.compile(r"\b\d{16,19}\b")),
]

FORBIDDEN_DIRS = ("corpus", "exports", "work", "versions")
SKIP_EXT = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".pdf"}

# 本仓库自己的说明文档里必然出现"密码""wxid_xxxx"这类示例词，默认跳过；
# 用 --strict 可以连它们一起扫（发布自己的数据时建议加 --strict）。
DEFAULT_SKIP = {
    "README.md",
    "SKILL.md",
    "docs/PRIVACY.md",
    "docs/LESSONS.md",
    "docs/METHOD.md",
    "prompts/analyzer.md",
    "tools/preflight.py",
}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="发布前自检")
    parser.add_argument("--root", default=".")
    parser.add_argument("--max-line", type=int, default=400, help="超过这个长度的行会报警（疑似整段搬运）")
    parser.add_argument("--strict", action="store_true", help="连本仓库说明文档一起扫")
    args = parser.parse_args(argv)

    problems = []
    for base, dirs, files in os.walk(args.root):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        rel_base = os.path.relpath(base, args.root)
        for name in files:
            if os.path.splitext(name)[1].lower() in SKIP_EXT:
                continue
            path = os.path.join(base, name)
            rel = os.path.normpath(os.path.join(rel_base, name))
            if not args.strict and rel.replace("\\", "/") in DEFAULT_SKIP:
                continue
            if name.endswith(".py") or name in ("LICENSE",):
                continue
            try:
                lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                # 行内豁免：文档里必须示范"密码"这类词的场合，加 preflight:ignore 标记
                if "preflight:ignore" in line:
                    continue
                for label, rx in CHECKS:
                    if rx.search(line):
                        problems.append(f"[{label}] {rel}:{i}  {line.strip()[:90]}")
                if len(line) > args.max_line:
                    problems.append(f"[超长行 {len(line)} 字，疑似整段搬运] {rel}:{i}")

    for bad in FORBIDDEN_DIRS:
        p = os.path.join(args.root, bad)
        if os.path.isdir(p) and any(os.scandir(p)):
            problems.append(f"[不该提交的目录有内容] {bad}/  —— 请确认已在 .gitignore 中排除并清空")

    if not problems:
        print("✅ 自检通过：未发现凭据、第三方身份或整段搬运的痕迹")
        return 0

    print("⚠️  自检发现以下问题，发布前请逐条确认：\n")
    for p in problems[:80]:
        print("  " + p)
    if len(problems) > 80:
        print(f"  ...（共 {len(problems)} 条）")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
