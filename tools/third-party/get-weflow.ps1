<#
.SYNOPSIS
    按需下载 WeFlow 安装包（默认只打印信息，不下载任何东西）。

.DESCRIPTION
    三级回退：
      ① 官方渠道  github.com/hicccc77/WeFlow 的 Releases（当前为空，会自动跳过）
      ② 镜像渠道  本仓库自己的 Release 附件（用 -MirrorRepo 指定）
      ③ 都拿不到  打印链接清单后停止，绝不猜测地址
    下载后打印 SHA256 供核对，**不安装、不执行**下载到的文件。

.EXAMPLE
    .\get-weflow.ps1
        只打印官网、上游仓库、推荐版本与许可提示。

.EXAMPLE
    .\get-weflow.ps1 -Download -MirrorRepo "yourname/digital-life-skill"
        从镜像 Release 下载安装包到 .\third_party\（该目录已被 .gitignore 排除）。
#>

[CmdletBinding()]
param(
    [switch]$Download,
    [string]$OutDir = '',
    [string]$MirrorRepo = '',
    [string]$Version = '4.5.1',
    [string]$AssetPattern = 'WeFlow*.exe'
)

$ErrorActionPreference = 'Stop'

# $PSScriptRoot 在参数默认值里取不到，这里补算一次
if ([string]::IsNullOrEmpty($OutDir)) {
    $scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
    $OutDir = Join-Path $scriptDir 'third_party'
}

$Upstream = 'hicccc77/WeFlow'

function Write-Info {
    Write-Host ''
    Write-Host 'WeFlow —— 微信聊天记录导出工具（第三方软件，本仓库不分发源码）' -ForegroundColor Cyan
    Write-Host "  官网      : https://weflow.top"
    Write-Host "  上游仓库  : https://github.com/$Upstream"
    Write-Host "  文档站    : https://doc.weflow.top"
    Write-Host "  推荐版本  : $Version (x64, Windows)"
    Write-Host '  作者/版权 : cc (GitHub: hicccc77) © 2026'
    Write-Host '  许可证    : CC BY-NC-SA 4.0（署名 · 非商业 · 相同方式共享）'
    Write-Host '              https://creativecommons.org/licenses/by-nc-sa/4.0/'
    Write-Host '  声明      : 本仓库与 WeFlow 作者无隶属关系，不为其提供担保；'
    Write-Host '              分发属非商业性质，商业使用请自行联系上游作者。'
    Write-Host ''
}

function Get-ReleaseAssets {
    param([string]$Repo)
    if ([string]::IsNullOrWhiteSpace($Repo)) { return @() }
    $url = "https://api.github.com/repos/$Repo/releases?per_page=20"
    try {
        $rels = Invoke-RestMethod -Uri $url -Headers @{ 'User-Agent' = 'digital-life-skill' } -TimeoutSec 30
    } catch {
        Write-Host "  · 读取 $Repo 的 Release 失败：$($_.Exception.Message)" -ForegroundColor DarkYellow
        return @()
    }
    $out = @()
    foreach ($r in $rels) {
        foreach ($a in $r.assets) {
            $out += [pscustomobject]@{ Repo = $Repo; Tag = $r.tag_name; Name = $a.name; Url = $a.browser_download_url; Size = $a.size }
        }
    }
    return $out
}

Write-Info

if (-not $Download) {
    Write-Host '（当前为「只看不下载」模式。要真正下载，请加 -Download 参数）' -ForegroundColor Green
    Write-Host '  官方渠道：https://github.com/hicccc77/WeFlow/releases'
    Write-Host '  官网入口：https://weflow.top'
    if ($MirrorRepo) { Write-Host "  镜像渠道：https://github.com/$MirrorRepo/releases" }
    Write-Host ''
    Write-Host '  用法示例： .\get-weflow.ps1 -Download -MirrorRepo "<维护者>/digital-life-skill"' -ForegroundColor DarkGray
    exit 0
}

Write-Host '开始按三级回退查找安装包……' -ForegroundColor Cyan

$candidates = @()
$candidates += Get-ReleaseAssets -Repo $Upstream | Where-Object { $_.Name -like $AssetPattern -or $_.Name -like '*.exe' }
if ($MirrorRepo) {
    $candidates += Get-ReleaseAssets -Repo $MirrorRepo | Where-Object { $_.Name -like $AssetPattern -or $_.Name -like '*.exe' }
}

if (-not $candidates) {
    Write-Host ''
    Write-Host '没有找到可自动下载的安装包（上游当前没有任何 Release）。' -ForegroundColor Yellow
    Write-Host '请手动下载，链接如下：' -ForegroundColor Yellow
    Write-Host '    https://weflow.top'
    Write-Host "    https://github.com/$Upstream"
    if ($MirrorRepo) { Write-Host "    https://github.com/$MirrorRepo/releases" } else { Write-Host '    （提示：加 -MirrorRepo "<维护者>/digital-life-skill" 可启用镜像渠道）' }
    Write-Host '下载后放到本目录的 third_party\ 下即可，工具不会自动执行它。'
    exit 1
}

$pick = $candidates | Sort-Object Size -Descending | Select-Object -First 1
Write-Host ("  命中：{0}  ←  {1} ({2} @ {3:N1} MB)" -f $pick.Name, $pick.Repo, $pick.Tag, ($pick.Size / 1MB)) -ForegroundColor Green

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$dest = Join-Path $OutDir $pick.Name
Write-Host "  下载中 → $dest"
Invoke-WebRequest -Uri $pick.Url -OutFile $dest -Headers @{ 'User-Agent' = 'digital-life-skill' } -TimeoutSec 1800

$hash = (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash
$len = (Get-Item -LiteralPath $dest).Length
Write-Host ''
Write-Host '下载完成（未安装、未执行）：' -ForegroundColor Green
Write-Host "  文件      : $dest"
Write-Host ("  大小      : {0:N1} MB" -f ($len / 1MB))
Write-Host "  SHA256    : $hash"
Write-Host ''
Write-Host '  提醒：该目录已被 .gitignore 排除，不会被提交到仓库。'
Write-Host '        安装与运行由你自己双击完成。'
Write-Host '        若你要把安装包再分发给别人，必须同时保留以下署名：'
Write-Host '          名称 WeFlow | 作者 cc (GitHub: hicccc77) | 仓库 https://github.com/hicccc77/WeFlow'
Write-Host '          版本 4.5.1 | 许可 CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/'
Write-Host '          本分发为非商业用途，与上游作者无隶属关系'
Write-Host '        完整署名文本见 THIRD_PARTY_NOTICES.md'
exit 0
