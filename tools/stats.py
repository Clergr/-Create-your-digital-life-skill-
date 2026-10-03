#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对本人语料做量化统计——这些数字是后面写人格时的硬证据。

用法：
    python stats.py --input ./corpus/mine.txt --out ./corpus/stats.md
"""

from __future__ import annotations

import argparse
import collections
import datetime
import os
import re


def parse(line: str):
    m = re.match(r"^\[([^\]]+)\]\[([^\]]+)\]\s*(.*)$", line)
    if m:
        return m.group(1), m.group(2), m.group(3)
    return "?", "?", line


def hour_of(stamp: str) -> int | None:
    m = re.search(r"(\d{2}):(\d{2})", stamp)
    return int(m.group(1)) if m else None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="本人语料量化统计")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default=None)
    parser.add_argument("--top-ngram", type=int, default=40)
    parser.add_argument("--longest", type=int, default=12)
    args = parser.parse_args(argv)

    rows = [parse(l.rstrip("\n")) for l in open(args.input, encoding="utf-8", errors="replace") if l.strip()]
    texts = [r[2] for r in rows]
    out = ["# 语料量化统计\n", f"- 消息总数：{len(texts)}"]

    lens = sorted(len(t) for t in texts) or [0]
    out += [
        f"- 平均 {sum(lens)/len(lens):.1f} 字，中位 {lens[len(lens)//2]} 字，最长 {lens[-1]} 字",
        f"- ≤6 字的短消息：{sum(1 for l in lens if l <= 6)/len(lens)*100:.0f}%",
        f"- 含换行的长段落：{sum(1 for t in texts if chr(10) in t)} 条",
        "",
        "## 时段分布",
    ]
    hours = collections.Counter(h for h in (hour_of(r[0]) for r in rows) if h is not None)
    top = max(hours.values()) if hours else 1
    for h in range(24):
        n = hours.get(h, 0)
        out.append(f"  {h:02d}时 {n:5d} {'#' * int(n / top * 50)}")

    out += ["", "## 标点与语气"]
    for label, pat in [("句号 。", "。"), ("感叹号 ！", "！"), ("问号 ？", "？"),
                       ("波浪号 ~", "~"), ("省略号 ...", "..."), ("逗号 ，", "，"),
                       ("hh/哈哈哈", r"[hHｈ]{2,}|哈{2,}")]:
        n = sum(1 for t in texts if re.search(pat, t))
        out.append(f"- 含「{label}」：{n} 条（{n/max(1,len(texts))*100:.1f}%）")

    out += ["", "## 表情与 emoji"]
    bracket = collections.Counter()
    for t in texts:
        bracket.update(re.findall(r"\[[^\]]{1,8}\]", t))
    for k, v in bracket.most_common(20):
        out.append(f"  {k} × {v}")
    emoji = collections.Counter(ch for t in texts for ch in t if ord(ch) > 0x1F000)
    if emoji:
        out.append("  原生 emoji：" + " ".join(f"{k}×{v}" for k, v in emoji.most_common(15)))

    out += ["", "## 高频短语（2-6 字，出现 ≥8 次）"]
    ng = collections.Counter()
    for t in texts:
        clean = re.sub(r"\[[^\]]*\]|\s+", "", t)
        for n in range(2, 7):
            for i in range(len(clean) - n + 1):
                ng[clean[i:i + n]] += 1
    shown = 0
    for k, v in ng.most_common(600):
        if v < 8 or shown >= args.top_ngram:
            break
        if any(ng.get(k[:i], 0) == v or ng.get(k[i:], 0) == v for i in range(1, len(k))):
            continue
        out.append(f"  {k} × {v}")
        shown += 1

    out += ["", f"## 最长的 {args.longest} 条消息（看思维方式）"]
    for stamp, chat, body in sorted(rows, key=lambda r: -len(r[2]))[:args.longest]:
        out.append(f"\n--- [{stamp}][{chat}] ({len(body)} 字)\n{body[:2000]}")

    text = "\n".join(out)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        open(args.out, "w", encoding="utf-8").write(text)
        print(f"已写入 {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
