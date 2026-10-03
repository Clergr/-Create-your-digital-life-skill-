#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把原始材料抽成"只有我说话"的语料。

用法：
    # 微信导出（WeFlow / chatlab jsonl）
    python ingest.py --source wechat --input ./exports/texts --me wxid_xxx --out ./corpus

    # WeFlow 的 txt 导出（每个会话一个「私聊_某某.txt」）
    python ingest.py --source wechat-txt --input ./exports/txt --me 我 --out ./corpus

    # AI 会话导出（Codex / Claude Code / DeepSeek / 通用 jsonl）
    python ingest.py --source ai --input ./exports/ai --out ./corpus

    # 纯文本 / Markdown
    python ingest.py --source files --input ./exports/notes --out ./corpus --pattern "*.md"

    # 去重（同一会话里完全相同的发言只留一条）
    python ingest.py --source dedup --input ./corpus/mine.txt

产物：
    <out>/mine.txt     本人发言，格式 [时间][会话] 内容
    <out>/others.txt   他人发言（微信来源才有，用于"他人评价"分析）
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import sys

# 机器注入的噪声（不是本人说的话），按前缀过滤
NOISE_PREFIX = (
    "<",
    "The following is the Codex agent history",
    ">>> TRANSCRIPT",
    "APPROVAL REQUEST",
    "Reviewed Codex session id",
    "Caveat:",
)


def ts(value) -> str:
    try:
        return datetime.datetime.fromtimestamp(float(value)).strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return "?"


def noisy(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return True
    return any(text.startswith(p) for p in NOISE_PREFIX)


# ---------------------------------------------------------------- 微信
def from_wechat(root: str, me: str, out: str) -> tuple[int, int]:
    mine, others = [], []
    files = glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True)
    for path in sorted(files):
        chat = re.sub(r"^(私聊|群聊)_", "", os.path.splitext(os.path.basename(path))[0])
        members, rows = {}, []
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("_type") == "member":
                members[obj.get("platformId")] = obj.get("accountName")
            elif obj.get("_type") == "message":
                rows.append(obj)
        if not rows:
            continue
        for msg in rows:
            body = (msg.get("content") or "").strip()
            if not body:
                continue
            when = ts(msg.get("timestamp"))
            if msg.get("sender") == me:
                mine.append(f"[{when}][{chat}] {body}")
            else:
                who = members.get(msg.get("sender"), msg.get("accountName") or "?")
                others.append(f"[{when}][{chat}][{who}] {body}")
    write(out, "mine.txt", mine)
    write(out, "others.txt", others)
    return len(mine), len(others)


# ---------------------------------------------------------------- AI 会话
TXT_TS = re.compile(r"(\d{4}[-/.]\d{2}[-/.]\d{2} \d{2}:\d{2}:\d{2})")
TXT_SENDER = re.compile(r"""["'“”](.*?)["'“”]""")


def parse_weflow_txt(path: str) -> list:
    """解析 WeFlow 的 txt 导出。

    格式：
        2023-01-01 12:00:00 "我"
        你好！

        2023-01-01 12:01:00 "张三"
        [图片]
    时间戳支持 - / . 三种分隔符；发送者带引号（无引号也兼容）；
    正文持续到下一个时间戳行或空行为止。
    """
    items, cur = [], None
    for raw in open(path, encoding="utf-8", errors="replace"):
        line = raw.rstrip("\n")
        m = TXT_TS.search(line)
        if m:
            if cur:
                items.append(cur)
            after = line[m.end():]
            sm = TXT_SENDER.search(after)
            cur = {"ts": m.group(1), "sender": (sm.group(1) if sm else after.strip()), "lines": []}
        elif cur is not None:
            if not line.strip():
                if cur["lines"]:
                    items.append(cur)
                    cur = None
            else:
                cur["lines"].append(line)
    if cur:
        items.append(cur)
    return [(i["ts"], i["sender"], "\n".join(i["lines"]).strip()) for i in items]


def from_wechat_txt(root: str, me: str, out: str) -> tuple:
    mine, others = [], []
    for path in sorted(glob.glob(os.path.join(root, "**", "*.txt"), recursive=True)):
        base = os.path.splitext(os.path.basename(path))[0]
        chat = base.split("_", 1)[-1] if base.startswith(("私聊_", "群聊_")) else base
        for ts, sender, body in parse_weflow_txt(path):
            if not body:
                continue
            who = sender.strip().strip('"').strip("“”")
            if who == me:
                mine.append(f"[{ts}][{chat}] {body}")
            else:
                others.append(f"[{ts}][{chat}][{who}] {body}")
    write(out, "mine.txt", mine)
    write(out, "others.txt", others)
    return len(mine), len(others)


def _texts_from_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(item.get("text") or item.get("content") or "")
        return "\n".join(p for p in parts if p)
    return ""


def _iter_jsonl(path: str):
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _user_texts(obj) -> list[str]:
    """从一条记录里抽出'本人说的话'。兼容 Codex / Claude Code / 通用格式。"""
    found = []
    # Codex rollout
    if obj.get("type") == "response_item":
        payload = obj.get("payload") or {}
        if payload.get("type") == "message" and payload.get("role") == "user":
            found.append(_texts_from_content(payload.get("content")))
    # Claude Code / 通用
    if obj.get("type") == "user" and not obj.get("isMeta"):
        found.append(_texts_from_content((obj.get("message") or {}).get("content")))
    # DeepSeek 风格
    if str(obj.get("role", "")).upper() == "USER":
        text = obj.get("content") or ""
        if not text:
            for frag in obj.get("fragments") or []:
                if isinstance(frag, dict):
                    text += (frag.get("content") or "")
        found.append(text)
    return [f for f in found if f and f.strip()]


def from_ai(root: str, out: str) -> tuple[int, int]:
    mine = []
    for path in sorted(glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True)):
        src = os.path.basename(path)
        for obj in _iter_jsonl(path):
            for text in _user_texts(obj):
                if noisy(text):
                    continue
                when = ts(obj.get("timestamp") or obj.get("inserted_at") or 0)
                mine.append(f"[{when}][{src}] {text.strip()}")
    write(out, "mine_ai.txt", mine)
    return len(mine), 0


def from_files(root: str, out: str, pattern: str) -> tuple[int, int]:
    mine = []
    for path in sorted(glob.glob(os.path.join(root, "**", pattern), recursive=True)):
        name = os.path.basename(path)
        try:
            body = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        mine.append(f"[?][{name}] {body.strip()}")
    write(out, "mine_files.txt", mine)
    return len(mine), 0


# ---------------------------------------------------------------- 去重
def dedup(path: str) -> tuple[int, int]:
    entries, seen, kept = [], set(), []
    for raw in open(path, encoding="utf-8", errors="replace"):
        line = raw.rstrip("\n")
        m = re.match(r"^(\[[^\]]+\]\[[^\]]+\])\s*(.*)$", line)
        if m:
            entries.append([m.group(1), m.group(2)])
        elif entries:
            entries[-1][1] += " / " + line.strip()
    for pre, body in entries:
        key = (pre.split("][", 1)[1], body.strip())
        if key in seen:
            continue
        seen.add(key)
        kept.append(f"{pre} {body}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(kept))
    return len(entries), len(kept)


# ---------------------------------------------------------------- helpers
def write(out_dir: str, name: str, lines: list[str]) -> None:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"  {path}  ({len(lines)} 条)")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="把原始材料抽成本人语料")
    parser.add_argument("--source", required=True,
                        choices=["wechat", "wechat-txt", "ai", "files", "dedup"])
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="./corpus")
    parser.add_argument("--me", help="本人的账号 id / 昵称（微信来源必填）")
    parser.add_argument("--pattern", default="*.txt", help="files 来源的文件匹配")
    args = parser.parse_args(argv)

    if args.source == "wechat-txt":
        if not args.me:
            print("txt 来源需要 --me（本人显示名，例如 \"我\"）", file=sys.stderr)
            return 2
        a, b = from_wechat_txt(args.input, args.me, args.out)
        print(f"完成：本人 {a} 条，他人 {b} 条")
    elif args.source == "wechat":
        if not args.me:
            print("微信来源需要 --me（本人的 wxid 或昵称）", file=sys.stderr)
            return 2
        a, b = from_wechat(args.input, args.me, args.out)
        print(f"完成：本人 {a} 条，他人 {b} 条")
    elif args.source == "ai":
        a, _ = from_ai(args.input, args.out)
        print(f"完成：本人 {a} 条")
    elif args.source == "files":
        a, _ = from_files(args.input, args.out, args.pattern)
        print(f"完成：{a} 个文件")
    else:
        before, after = dedup(args.input)
        print(f"去重：{before} → {after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
