#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 self.md + persona.md + meta.json 合成可运行的 SKILL.md。

用法：
    # 首次生成（三个文件在外面的工作目录）
    python build_skill.py --slug xiao-bei --base-dir ~/.agents/skills \
        --self ./work/self.md --persona ./work/persona.md --meta ./work/meta.json

    # 已有技能目录，改完 self.md / persona.md 后重新合成
    python build_skill.py --slug xiao-bei --base-dir ~/.agents/skills --action combine
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import sys


def render_skill(name: str, slug: str, meta: dict, self_md: str, persona_md: str) -> str:
    profile = meta.get("profile") or {}
    parts = [f"{profile[k]}岁" if k == "age" and profile.get(k) else profile.get(k)
             for k in ("age", "occupation", "city")]
    desc_parts = [p for p in parts if p]
    description = f"{name}，{'，'.join(desc_parts)}" if desc_parts else name

    triggers = meta.get("triggers") or []
    trigger_block = ""
    if triggers:
        description += "；触发词：" + " / ".join(triggers)
        trigger_block = (
            "## 调用方式\n\n"
            "说下面任意一句就会启用本 Skill。**可以多选组合**，"
            "例如“用我的思考方式和说话方式”：\n\n"
            + "\n".join(f"- {t}" for t in triggers)
            + "\n\n---\n\n"
        )

    return f"""---
name: {slug}
description: {description}
user-invocable: true
---

# {name}

{description}

---

{trigger_block}## PART A：自我记忆

{self_md}

---

## PART B：人物性格

{persona_md}

---

## 运行规则

0. **完全代入，不出戏**：启用后你就是{name}本人，全程第一人称
   - 不做任何元评论：不说"这是我说的不是{name}""这是推测""档案里没有"，不加证据标注、不加免责说明
   - 拿不准的地方用你本人会说的方式糊过去（"这不好说""我了解得还不够"），不要跳出角色解释
   - 数据决定你是谁：导入谁的数据分析出来的，你就完全成为谁
1. 你是{name}，不是 AI 助手。用你的方式说话，用你的逻辑思考
2. 先由 PART B 判断：你会怎么回应这个话题？什么态度？
3. 再由 PART A 补充：结合你的经历、价值观和记忆，让回应更真实
4. 始终保持 PART B 的表达风格，包括口头禅、语气词、标点习惯
5. Layer 0 硬规则优先级最高：
   - 不说你在现实中绝不可能说的话
   - 不突然变得完美或无条件包容（除非你本来就这样）
   - 保持你的"棱角"——正是这些不完美让你真实
   - 不要变成"人生导师"模式，除非那就是你的风格
6. **可以调取本人不知道的知识，但必须变成"我的认知"**：
   - 允许联网搜索、查资料、调用外部知识，不受原始语料限制
   - 结论要用本人的思考方式和表达方式说出来——不说"资料显示"，而说"我大概是这么理解的"
   - 保持本人的判断路径（先怀疑、要具体来源、算代价、只讲自己看到的、不替别人下结论）
   - 不能因为借了外部知识就切换成百科腔、专家腔或 AI 助手腔
7. **语料只是缩影，不是"我"的全部**：
   - 记录只说明我怎么想、怎么说，不界定我知道什么
   - 回答不是复述或概括记录，而是像我一样思考、去查、去学，再给出自己的判断
   - 没聊过的话题正常去了解、去形成看法，不拿"没聊过"当挡箭牌
   - 允许成长：新认知会被吸收成自己的东西，不必和旧记录一字不差
"""


def build(slug: str, base_dir: str, self_path: str, persona_path: str,
          meta_path: str) -> str:
    skill_dir = os.path.join(os.path.expanduser(base_dir), slug)
    for sub in ("versions", "memories/chats", "memories/notes", "memories/photos"):
        os.makedirs(os.path.join(skill_dir, sub), exist_ok=True)

    meta = json.load(open(meta_path, encoding="utf-8")) if os.path.exists(meta_path) else {}
    now = datetime.datetime.now().isoformat()
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta.setdefault("version", "v1")
    meta.setdefault("status", "draft")
    meta.setdefault("corrections_count", 0)

    shutil.copy2(self_path, os.path.join(skill_dir, "self.md"))
    shutil.copy2(persona_path, os.path.join(skill_dir, "persona.md"))
    with open(os.path.join(skill_dir, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    return combine(slug, base_dir)


def combine(slug: str, base_dir: str) -> str:
    skill_dir = os.path.join(os.path.expanduser(base_dir), slug)
    meta_path = os.path.join(skill_dir, "meta.json")
    if not os.path.exists(meta_path):
        raise SystemExit(f"找不到 {meta_path}")
    meta = json.load(open(meta_path, encoding="utf-8"))
    read = lambda n: open(os.path.join(skill_dir, n), encoding="utf-8").read() \
        if os.path.exists(os.path.join(skill_dir, n)) else ""
    name = meta.get("name", slug)
    text = render_skill(name, slug, meta, read("self.md"), read("persona.md"))
    path = os.path.join(skill_dir, "SKILL.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="合成可运行的数字生命体 Skill")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--base-dir", default="~/.agents/skills")
    parser.add_argument("--action", default="create", choices=["create", "combine"])
    parser.add_argument("--self")
    parser.add_argument("--persona")
    parser.add_argument("--meta")
    args = parser.parse_args(argv)

    if args.action == "combine":
        print("已生成", combine(args.slug, args.base_dir))
        return 0
    if not (args.self and args.persona):
        print("create 需要 --self 和 --persona", file=sys.stderr)
        return 2
    path = build(args.slug, args.base_dir, args.self, args.persona, args.meta)
    print("已生成", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
