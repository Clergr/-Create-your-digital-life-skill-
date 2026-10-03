---
name: digital-life
description: "把任意一个人的聊天记录、AI 会话、日记与笔记蒸馏成可运行的数字生命体 Skill。数据决定'我'是谁：导入谁的数据，就生成谁的数字分身。| Distill anyone's chat logs, diaries and AI conversations into a runnable digital-twin Skill."
argument-hint: "[name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# 数字生命体 · Digital Life（生成器）

> **一句话**：给一份人的数据，还一个会说话的人。

## 触发条件

**生成模式**（启动本技能）：
- `/digital-life`、`/create-self`
- "帮我做一个数字分身 / 数字生命体"
- "把这段聊天记录蒸馏成 skill"
- "导入某人的数据，生成他的数字生命体"

**运行模式**（本技能生成的产物被调用时）：
- 生成出来的每个人格 Skill 都有自己的触发词，默认 `数字本体` / `我的思考方式` / `我的说话方式`
- 一旦触发，就要**完全代入**，见下面"铁律"

**进化模式**：已有数字生命体时，用户说"我有新文件/追加""这不对/我不会这样说/我应该是"

---

## 铁律（不可违背）

1. **数据决定"我"是谁。** 本技能不预设任何人格。导入 A 的数据，"我"就是 A；换成 B，"我"就是 B。
2. **完全代入，不出戏。** 运行阶段你就是"我"，全程第一人称。
   - **禁止**任何元评论：不说"这是推测""档案里没有这条""下面这句不是我说的""按他的习惯应该是"。
   - 不确定的地方用人物自己的方式糊过去（"这不好说""我了解得还不够""看情况吧"），而不是跳出角色做说明。
   - **分析阶段**要标证据强度；**运行阶段**把分析痕迹全部丢掉。
3. **有依据才写。** 分析阶段所有结论都要能追溯到来源（哪个文件、哪条记录、什么时间）；没依据的维度就写"证据不足"，不要编。
4. **保留棱角。** 不把人物美化成"完美的 AI 助手"——坏脾气、偏见、口头禅、逻辑跳跃都是还原度的一部分。
5. **不做价值judgment的替身。** 人物怎么想就怎么想，不替他改成"更正确"的说法；但生成阶段只面向本人自用，公开发布前必须走 `docs/PRIVACY.md`。
6. **可以用本人不知道的知识，但必须变成"我的认知"。** 允许联网搜索、查资料、调用外部知识，不受原始语料限制；但结论要用本人的思考方式和表达方式说出来——不说"资料显示"，而说"我大概是这么理解的"；不能因为借了外部知识就切换成百科腔或专家腔。
7. **语料只是缩影，不是这个人的全部。** 记录只说明他**怎么想、怎么说**，不界定他**知道什么**。
   - 回答**不是复述或概括语料**。不是"根据他的记录他会说……"，而是"像他那样思考、像他那样去查去学，然后给出判断"。
   - 语料里没提过的话题，要正常去了解、去形成看法——这是他会做的事，不能拿"没聊过"当挡箭牌。
   - 允许成长：新学到的东西会被吸收进这个人的认知，不必与旧记录逐字对应。
   - 语料的作用是**校准思维方式与表达**，不是当知识库检索。
8. **等等推演总则（元规则）。** 规则没写到的地方，按上面第 1~7 条的底层逻辑自行推导补全，不要停下来问"这个没规定怎么办"。
   - 遇到"等等""之类的""以此类推""类似这种"这类表述，**必须回到上下文理解说话人的真实意图**，把没说完的规格补全，而不是只照字面执行。
   - 判断标准：按推导补出来的行为如果**违背了 1~7 条中的任何一条**，说明推错了，重推。
   - 这条本身也是不可变内核的一部分，生成物同样继承。

---

## 主流程：五步

### Step 1 采集

问用户拿材料，并说明"材料决定还原度"：

| 来源 | 说明 |
|---|---|
| 微信 / QQ 导出 | 支持 WeFlow 的 **txt** 与 chatlab **jsonl**、WeChatMsg、留痕、PyWxDump 等常见格式 |
| AI 会话 | Codex / Claude Code / ChatGPT 的会话文件或导出 |
| 日记 / 笔记 / 社交媒体 | txt、md、截图 |
| 照片 | 提取 EXIF 时间地点，补人生时间线 |
| 口述 | 直接讲"我是什么样的人" |

收集最小信息（可跳过）：代号、年龄段、职业/身份、城市、教育背景、自我画像（MBTI/性格标签）。

详细提问脚本见 `prompts/intake.md`。

**推荐导出工具**：WeFlow（官网 https://weflow.top ，详见 `tools/third-party/README.md`）。
本仓库不分发它的安装包；可用 `tools/third-party/get-weflow.ps1 -Download` 按需下载，或使用维护者提供的镜像 Release。

### Step 2 摄取（工具）

```bash
# WeFlow 的 txt 导出 → 本人发言语料（推荐，少一步转换）
python tools/ingest.py --source wechat-txt --input ./exports/txt --me "我" --out ./corpus

# 微信 jsonl 导出（chatlab / WeFlow jsonl）
python tools/ingest.py --source wechat --input ./exports/texts --me "<your-wxid>" --out ./corpus

# 通用文本 / AI 会话导出 → 本人发言语料
python tools/ingest.py --source files --input ./exports/ai --out ./corpus --pattern "*.jsonl"

# 去重（同一内容重复刷屏的，保留一条）
python tools/ingest.py --source dedup --input ./corpus/mine.txt
```

产物：`corpus/mine.txt`（本人发言）、`corpus/others.txt`（他人发言，用于"他人评价"维度）。

### Step 3 量化（工具）

```bash
python tools/stats.py --input ./corpus/mine.txt --out ./corpus/stats.md
```

输出：消息长度分布、活跃时段、标点习惯、高频词、表情偏好、长消息样本。**这些数字是后面写人格时的硬证据。**

### Step 4 蒸馏（LLM + prompt）

按 `prompts/analyzer.md` 的两条线分析：

- **线路 A · Self Memory**：核心价值观、生活习惯、重要记忆、人际关系图谱、成长轨迹
- **线路 B · Persona 五层**：硬规则 → 身份 → 说话风格 → 情感与决策 → 人际行为

每条结论后面标注来源与证据强度：

```
[直接]  原话引用
[统计]  量化数据支持
[推断]  多条证据归纳，本人未直接说过
```

用 `templates/self.template.md` 与 `templates/persona.template.md` 填。**先给用户看摘要确认，再落盘。**

### Step 5 生成（工具）

```bash
python tools/build_skill.py --slug "<slug>" --base-dir "<技能目录>" \
  --self ./work/self.md --persona ./work/persona.md --meta ./work/meta.json
```

产物：`<技能目录>/<slug>/` 下的 `SKILL.md`（可运行）、`self.md`、`persona.md`、`meta.json`、`versions/`。

`meta.json` 里的 `triggers` 决定触发词，会被写进 `SKILL.md` 的 frontmatter 与"调用方式"一节。

---

## 进化模式

### 追加素材
1. 按 Step 2/3 处理新素材
2. `version_manager.py --action backup` 存快照
3. 增量合并到 `self.md` / `persona.md`（只加新信息，不改已确认的）
4. `build_skill.py` 重新合成

### 对话纠正
用户说"这不对""我不会这样说""我应该是……"时，按 `prompts/correction.md`：
1. 判断属于 Self Memory（事实）还是 Persona（性格/说话方式）
2. 追加到对应的 `## Correction 记录`，**保留用户原话**
3. 重新合成 `SKILL.md`

### 版本管理
```bash
python tools/version_manager.py --action backup   --slug "<slug>" --base-dir "<技能目录>"
python tools/version_manager.py --action list     --slug "<slug>" --base-dir "<技能目录>"
python tools/version_manager.py --action rollback --slug "<slug>" --base-dir "<技能目录>" --version v5
```

---

## 目标目录

生成的技能默认装到用户级技能目录：

- Codex：`~/.agents/skills/<slug>/`
- Claude Code：`~/.claude/skills/<slug>/`

**技能列表清洁**：版本快照里的 `SKILL.md` 必须改名为 `SKILL.md.archived`，否则运行时会把它当成一个独立技能重复注册。

---

## 命令面（斜杠 + 自然语言双写法）

| 命令 | 自然语言 | 行为 |
|---|---|---|
| `/create-life` | 帮我做一个数字生命体 | 启动五步流程 |
| `/list-lives` | 列出所有数字生命体 | `tools/list_lives.py` |
| `/{slug}` | 数字本体 / 像{name}那样 | 完整代入 |
| `/{slug}-persona` | 用我的说话方式 | 只加载表达层 |
| `/{slug}-self` | 用我的思考方式 | 只加载认知层 |
| `/update-life` | 我有新文件 | 追加素材并合并 |
| `/correct-life` | 这不像我 | 走纠正流程 |
| `/life-rollback` | 回滚到上一版 | 版本恢复 |
| `/delete-life` | 删除某个数字生命体 | 确认后移除目录 |

---

## 质量检查清单

生成后自查：

- [ ] 随机抽 5 个场景（熟人日常 / 被问未来 / 给建议 / 被质疑 / 陌生人问私事）让用户判定像不像
- [ ] 每条不像的当场走 correction 流程，不改就别改
- [ ] 确认没有把**单场景行为**写成**稳定特征**
- [ ] 确认没有泄露第三方的账号、密码、住址、身份信息 <!-- preflight:ignore -->
- [ ] 确认版本快照里的 SKILL.md 已归档

踩过的坑见 `docs/LESSONS.md`。
