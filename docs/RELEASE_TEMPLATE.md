# GitHub Release 发布说明模板

> 用途：把 WeFlow 安装包作为镜像附件发布时，**直接复制下面内容**，确保署名与许可合规。
> 发布前记得：附件不要包含 `*.wechat_exp_config.json`（内含微信数据库解密密钥）。

---

## 复制以下内容

**Tag**：`weflow-4.5.1`

**Release title**：`WeFlow 4.5.1 安装包（镜像备份，非官方分发）`

**Release notes**：

```markdown
本附件为 **WeFlow 4.5.1 (x64, Windows)** 安装包的镜像备份，方便使用者获取。

## 出处与署名（必要）

- 名称：WeFlow
- 作者 / 版权：cc（GitHub: hicccc77）© 2026
- 上游仓库：https://github.com/hicccc77/WeFlow
- 官网：https://weflow.top
- 文档站：https://doc.weflow.top
- 许可证：Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
  https://creativecommons.org/licenses/by-nc-sa/4.0/

## 声明

- 本项目与 WeFlow 作者**没有隶属关系**，不为其提供担保、不支持、不承担任何责任
- 本分发为**非商业用途**；商业使用请自行联系上游作者取得授权
- 若你对 WeFlow 做了修改再分发，修改后的作品必须以同样的 CC BY-NC-SA 4.0 许可发布
- 安装包的完整性与安全性请自行校验；本仓库只做镜像，不对二进制内容做任何改动

## 校验

下载后请核对 SHA256：

    （发布时填上 sha256，例如）
    WeFlow-4.5.1-x64-Setup.exe  <SHA256>

## 使用

1. 下载并自行安装（本仓库不提供自动安装）
2. 用 WeFlow 导出微信聊天记录为 **txt**
3. 交给 digital-life-skill：

       python tools/ingest.py --source wechat-txt --input "<导出目录>" --me "我" --out ./corpus

安全提醒：WeFlow 生成的 `.wechat_exp_config.json` 含微信数据库解密密钥，请勿提交到任何仓库。
```

---

## 上传步骤（网页）

1. 打开仓库页面 → 右侧 **Releases** → **Draft a new release**
2. **Choose a tag** 填 `weflow-4.5.1`（新标签，选 "Create new tag"）
3. 标题与说明按上面的模板填
4. 把 `WeFlow-4.5.1-x64-Setup.exe` 拖进附件区
5. **Publish release**

发布后，下载脚本就能自动命中镜像：

```powershell
.\tools\third-party\get-weflow.ps1 -Download -MirrorRepo "<你的用户名>/digital-life-skill"
```
