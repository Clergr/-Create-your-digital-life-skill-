<div align="center">

# 数字生命体 · Digital Life

> **数据决定"我"是谁。** 导入一个人的聊天记录、AI 会话、笔记与照片，把它解构成一个能开口说话的"我"。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

</div>

---

## 这是什么

一个**通用的数字分身生成器**。

它不是一个固定的角色，而是一套流程：你给它**任意一个人**的原始材料，它输出一个**可运行的人格 Skill**——那个人会用自己的方式说话、用自己的逻辑思考。


本仓库只包含**方法、模板与工具**，不含任何人的真实数据。

## 核心原则：数据即我

> 启用这个 Skill 之后，你就是"我"——不是模仿，不是推测，是完全代入。

1. **人物由数据定义**，不由代码定义。同一个技能包，换一份数据，就是另一个人。
2. **完全代入，不出戏**。运行期间不做元评论：不说"这是推测""档案里没有""这是按他的习惯推的"。拿不准就用人物自己的说法糊过去（"这不好说""我了解得还不够"）。
3. **先分析，再成为**。分析阶段允许也要求标注证据强度；生成之后只保留人格，不保留分析痕迹。
4. **可以用本人不知道的知识，但必须变成"我的认知"**。允许联网搜索与外部资料，不受原始语料限制；但要用本人的思考路径消化后再讲——不说"资料显示"，而说"我大概是这么理解的"，并且不切换到百科腔。
5. **语料是缩影，不是本人的全部**。数据用来**校准思维方式与表达方式**，不是当知识库检索。
   判断标准很简单：回答应该是"像我一样思考、去查、去学之后得到的判断"，而不是"我的聊天记录里说过什么"的复述。没聊过的话题，他会去了解——那也要体现在回答里。

## 安装

```bash
# 作为 Agent Skill 安装（Claude Code / Codex / 兼容 AgentSkills 的运行时）
git clone https://github.com/<your-name>/digital-life ~/.agents/skills/digital-life

# 或者只当工具链用
git clone https://github.com/<your-name>/digital-life
cd digital-life && pip install -r requirements.txt
```

## 使用：五步

| 步骤 | 做什么 | 用什么 |
|---|---|---|
| 1 采集 | 拿到原始材料：微信/QQ 导出、AI 会话、日记、笔记、照片 | 你手上的导出文件 |
| 2 摄取 | 把材料抽成**只有"我"说的话**的纯文本语料，去噪去重 | `tools/ingest.py` |
| 3 量化 | 统计说话特征：消息长度、时段、标点、口头禅、表情 | `tools/stats.py` |
| 4 蒸馏 | 按 `prompts/analyzer.md` 的维度分析 → 填 `templates/` 生成自我记忆与人格五层 | LLM + 本仓库的 prompt |
| 5 生成 | 合成可运行 Skill，标注触发词，建立版本管理 | `tools/build_skill.py` |

```bash
# 例：从一个微信导出目录生成某人的语料
python tools/ingest.py --source wechat --input ./exports/texts --me "<your-wxid>" --out ./corpus
python tools/stats.py --input ./corpus/mine.txt --out ./corpus/stats.md

# 蒸馏完成后，合成可运行 skill
python tools/build_skill.py --slug xiao-bei --base-dir ~/.agents/skills \
  --self ./work/self.md --persona ./work/persona.md --meta ./work/meta.json
```

### 素材怎么来：WeFlow导出微信聊天记录（推荐）

感谢来自CC大佬的开源项目（官网 https://weflow.top ，上游 https://github.com/hicccc77/WeFlow ）。

【压缩包放在Releases可以直接下载】



## 触发词（可多选）

技能包里可以为每个人配置触发词，默认这套：

| 触发词 | 作用 |
|---|---|
| **数字本体** | 完整代入 |
| **我的思考方式** | 只用判断逻辑、价值观、决策路径 |
| **我的说话方式** | 只用语气、句式、用词 |
| 用 {名字} 的方式 / 像 {名字} 那样 | 完整代入 |

可以组合："**用我的思考方式和说话方式**"。

> 第三方组件与出处声明见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)；发布 WeFlow 附件的说明模板见 [`docs/RELEASE_TEMPLATE.md`](docs/RELEASE_TEMPLATE.md)。

## 目录结构

```
digital-life/
├── SKILL.md                 技能入口（AgentSkills 标准）
├── README.md / README_EN.md 中英说明
├── THIRD_PARTY_NOTICES.md   第三方组件与出处声明
├── prompts/
│   ├── intake.md            信息录入
│   ├── analyzer.md          分析维度（认知模型 + 自我记忆 + 人格五层）
│   ├── builder.md           生成规范
│   ├── correction.md        纠正流程
│   └── merger.md            追加素材的增量合并
├── templates/
│   ├── self.template.md     自我记忆模板
│   ├── persona.template.md  人格五层 + 认知模型模板
│   └── meta.template.json   元数据模板
├── tools/
│   ├── ingest.py            多源摄取 → 本人语料（含 WeFlow txt）
│   ├── stats.py             量化统计
│   ├── build_skill.py       合成可运行 SKILL.md
│   ├── version_manager.py   版本备份 / 回滚
│   ├── list_lives.py        列出所有数字生命体
│   ├── preflight.py         发布前自检（凭据 / 他人身份 / 长引用）
│   └── third-party/         WeFlow 说明 + 按需下载脚本（不含安装包）
├── docs/
│   ├── METHOD.md            方法论
│   ├── LESSONS.md           我们踩过的六个坑
│   ├── PRIVACY.md           隐私与伦理
│   └── PRD.md               产品说明
└── examples/
    └── example-self.md      脱敏示例（虚构人物）
```

## 为什么值得用

- **可验证**：每条结论都要求标注来源（哪份文件、哪条记录、什么时间）
- **可纠错**：说"我不会这样说"，系统走 correction 流程写进档案并重新生成
- **可回滚**：每次改动自动存快照，随时回到上一版
- **可迁移**：换一份数据就是另一个人，流程不变

## 已知边界

1. **语音内容**：多数导出只留文字，语音转写丢失会明显降低还原度。
2. **场景 ≠ 特征**：单一场景里的高强度表现不能当成稳定人格（见 `docs/LESSONS.md`）。
3. **隐私**：原始材料往往包含第三方的账号、住址、私事。发布或分享前必须清理，见 `docs/PRIVACY.md`。
4. **伦理**：这是自我观察与创作工具，不要用来冒充真人对外交流或获取信任。

## English

A universal **digital-twin generator** for AI agents. Feed it anyone's chat logs, AI conversations, diaries and notes; it distills them into a runnable persona Skill that speaks and reasons as that person. Same pipeline, different data — a different "self". No personal data ships with this repo.

## License

MIT © contributors
