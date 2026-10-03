# 更新日志

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-10-04

首个发布版本。

### 新增
- **五步流程**：采集 → 摄取 → 量化 → 蒸馏 → 生成，产出一个可运行的数字生命体 Skill
- **八条不可变内核**：完全代入 / 数据即我 / 语料是缩影 / 自我学习 / 认知模型优先 / 保留棱角与禁忌 / 等等推演总则
- **多源摄取**：WeFlow 的 **txt** 与 chatlab **jsonl**、Codex/Claude 会话、通用文本笔记
- **认知模型层**：人格五层之前先写"思考协议"，让人格能回答语料里没有的问题
- **多人物管理**：`list_lives.py` 列出全部数字生命体；触发词可多选组合
- **完整命令面**：`/create-life` `/list-lives` `/{slug}` `/{slug}-persona` `/{slug}-self` `/update-life` `/correct-life` `/life-rollback` `/delete-life`
- **版本管理**：备份 / 回滚 / 列表；快照里的 `SKILL.md` 自动存为 `.archived`，避免技能列表重复注册
- **合规与隐私**：`preflight.py` 发布前自检（凭据 / 第三方身份 / 超长引用，支持 `--strict` 与行内豁免）、`THIRD_PARTY_NOTICES.md`、`docs/PRIVACY.md`

### 第三方工具
- 支持 **WeFlow** 导出的 txt / jsonl；**不随仓库分发**其安装包（体积超 GitHub 限制 + CC BY-NC-SA 4.0）
- 提供 `tools/third-party/get-weflow.ps1|.sh`：默认只打印链接，`-Download` 才下载，三级回退，校验 SHA256，不自动安装

### 已知边界
- 语音内容：多数导出只留文字，语音转写缺失会降低还原度
- 语料里的第三方隐私需使用者自行清理（见 `docs/PRIVACY.md`）
