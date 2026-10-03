# 第三方素材导出工具

本目录**不包含任何第三方软件的安装包**，只提供说明与按需下载脚本。

---

## WeFlow（推荐用于导出微信聊天记录）

| 项 | 内容 |
|---|---|
| 用途 | 把本地微信聊天记录导出成 txt / jsonl，供本技能摄取 |
| 官网 | https://weflow.top |
| 上游仓库 | https://github.com/hicccc77/WeFlow |
| 文档站 | https://doc.weflow.top |
| 本技能测试版本 | 4.5.1 (x64, Windows) |
| 许可证 | **CC BY-NC-SA 4.0**（署名 · 非商业 · 相同方式共享） |

### 为什么本仓库不直接附带安装包

1. **体积**：安装包 169.8 MB，超过 GitHub 单文件 100 MB 硬上限；zip 压缩后 169.5 MB（压缩率 0.2%），仍然超限。
2. **许可证**：WeFlow 使用 CC BY-NC-SA 4.0 —— 允许非商业分享，但要求**保留署名**并**标明许可**。因此本仓库把它作为**独立附件**分发，不混入本仓库代码。
3. **时效**：官方更新后，链接随手可得，仓库不必跟着变大。

### 当前获取 installable 版本的现实情况（2026-10 核实）

- 官网 weflow.top 的「立即下载」按钮实际是读取**上游 GitHub Releases** 的接口（`api.github.com/repos/hicccc77/WeFlow/releases`）
- 上游 **Release 数量为 0**，仓库里只有 TypeScript 源码（需要自行构建才能运行）
- 因此**官网当前无法直接下到可运行的安装包**

### 三条获取路径（按推荐顺序）

**① 本仓库维护者提供的镜像（最省事）**

维护者把测试过的 4.5.1 安装包上传到本仓库的 GitHub Release 附件，用户一条命令即可下载：

```powershell
.\tools\third-party\get-weflow.ps1 -Download -MirrorRepo "<维护者>/digital-life-skill"
```

**② 官网 / 上游渠道（官方更新后优先）**

打开 https://weflow.top 或 https://github.com/hicccc77/WeFlow/releases 自行下载。

**③ 自行从源码构建**

需要 Node.js 环境，适合开发者，普通用户不推荐。

### 用 WeFlow 导出素材

1. 安装并打开 WeFlow
2. 选择要导出的聊天 / 群，导出为 **txt**（推荐）或 jsonl
3. 把导出的文件夹交给本技能：

```bash
# txt 导出（每个会话一个「私聊_某某.txt」）
python tools/ingest.py --source wechat-txt --input "D:\导出的文件夹" --me "我" --out ./corpus

# jsonl 导出（chatlab 格式）——把尖括号里换成你自己的实际值
python tools/ingest.py --source wechat --input "D:\导出的文件夹" --me "<你的 wxid>" --out ./corpus
```

### ⚠️ 安全提醒

WeFlow 生成的 `.wechat_exp_config.json` 里含**微信数据库解密密钥**。

- 与导出的聊天记录放在同一目录时，**永远不要提交到任何仓库**
- 本仓库 `.gitignore` 已排除 `*.wechat_exp_config.json` 与 `third_party/`

### 许可与合规

- 本仓库与 WeFlow 作者**没有隶属关系**，不为其提供担保
- 本仓库对 WeFlow 的分发属**非商业性质**；如需商业使用，请自行联系上游作者确认
- 转载 / 再分发时请保留：项目名、作者、原仓库链接、CC BY-NC-SA 4.0 许可声明
- 完整的第三方声明与可复制的署名文本见仓库根目录 [`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md)
- 发布镜像附件时，发布说明请直接套用 [`docs/RELEASE_TEMPLATE.md`](../../docs/RELEASE_TEMPLATE.md)
