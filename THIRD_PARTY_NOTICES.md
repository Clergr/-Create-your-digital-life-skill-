# 第三方组件与出处声明 / Third-Party Notices

本仓库（`digital-life-skill`）自身以 **MIT** 许可发布。
以下第三方组件**不包含在本仓库中**，仅在文档与脚本里被引用；各自的权利与许可归其作者所有。

---

## 1. WeFlow（推荐使用的微信聊天记录导出工具）

| 项 | 内容 |
|---|---|
| 名称 | WeFlow |
| 作者 / 版权 | cc（GitHub: **hicccc77**）© 2026 |
| 上游仓库 | https://github.com/hicccc77/WeFlow |
| 官网 | https://weflow.top |
| 文档站 | https://doc.weflow.top |
| 本仓库测试版本 | 4.5.1 (x64, Windows) |
| 许可证 | **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International** |
| 许可证全文 | https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode |
| 在本仓库中的用途 | **仅作为推荐的外部导出工具被引用**；本仓库不分发其源码或二进制 |

### 为什么不分发

1. 安装包 169.8 MB，超过 GitHub 单文件 100 MB 硬上限（zip 压缩后 169.5 MB，仍超限）
2. 上游为 CC BY-NC-SA 4.0：允许非商业分享，但**要求署名、标明许可，并保持相同方式共享**

### 再分发时必须保留的署名文本

如果你把 WeFlow 安装包或构建产物再分发给他人（例如挂到本仓库的 GitHub Release 附件），请连同下面这段一起发布：

> 本文件为 WeFlow（作者 cc / GitHub: hicccc77，官网 https://weflow.top ，仓库 https://github.com/hicccc77/WeFlow ）的安装包，版本 4.5.1。
> 采用 Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International 许可（https://creativecommons.org/licenses/by-nc-sa/4.0/ ）。
> 本项目与 WeFlow 作者无隶属关系，不为其提供担保；本分发为非商业用途。

### 使用限制提醒

- **非商业**：CC BY-NC-SA 的 NC 条款禁止商业性使用；商业场景请自行联系上游作者取得授权
- **相同方式共享**：若你对 WeFlow 做了修改再分发，修改后的作品必须以同样的 CC BY-NC-SA 4.0 许可发布
- **无担保**：上游与本仓库均不提供任何担保

---

## 2. 方法论与结构上的参考来源

本仓库的设计参考了以下开源项目与规范。**未逐字复制其代码**；此处署名出于尊重与来源透明。

| 来源 | 作者 | 许可 | 参考了什么 |
|---|---|---|---|
| [yourself-skill](https://github.com/notdog1998/yourself-skill) | notdog1998 | MIT | "问答 + 导入聊天记录 → 生成人格 Skill" 的产品形态与流程骨架 |
| [AgentSkills](https://agentskills.io) | 社区规范 | — | `SKILL.md` + `prompts/` + `tools/` 的技能组织约定 |
| [colleague-skill](https://github.com/titanwings/colleague-skill) | titanwings | 见其仓库 | "双层架构（记忆 + 人格）" 的原始思路（经 yourself-skill 转述） |

---

## 3. 本仓库不含任何真实个人数据

- `examples/` 下的示例为**完全虚构**的人物
- 所有真实素材（聊天记录、AI 会话、日记、照片）只应存在于使用者本机
- `.gitignore` 已排除 `corpus/`、`lives/`、`exports/`、`work/`、`versions/`、`third_party/`、`*.wechat_exp_config.json`

---

## 4. 引用规范（对本仓库自身）

转载、改编或以本仓库为基础发布时，请保留：

1. 仓库名与链接
2. MIT 许可声明（见 `LICENSE`）
3. 本文件 `THIRD_PARTY_NOTICES.md`（若你同时分发了 WeFlow，则其中第 1 节的署名文本为必需项）
