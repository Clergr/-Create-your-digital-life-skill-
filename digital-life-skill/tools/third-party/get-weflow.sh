#!/usr/bin/env bash
# 按需下载 WeFlow 安装包（默认只打印信息，不下载任何东西）。
# 三级回退：官方 Releases → 镜像 Releases → 打印链接后停止。
# 下载后打印 SHA256，不安装、不执行。
set -euo pipefail

MIRROR_REPO="${MIRROR_REPO:-}"
OUT_DIR="${OUT_DIR:-$(cd "$(dirname "$0")" && pwd)/third_party}"
UPSTREAM="hicccc77/WeFlow"
DO_DOWNLOAD=0
[ "${1:-}" = "--download" ] && DO_DOWNLOAD=1

cat <<EOF

WeFlow —— 微信聊天记录导出工具（第三方软件，本仓库不分发源码）
  官网      : https://weflow.top
  上游仓库  : https://github.com/$UPSTREAM
  文档站    : https://doc.weflow.top
  作者/版权 : cc (GitHub: hicccc77) © 2026
  许可证    : CC BY-NC-SA 4.0（署名 · 非商业 · 相同方式共享）
              https://creativecommons.org/licenses/by-nc-sa/4.0/
  声明      : 与上游作者无隶属关系；商业使用请自行联系上游作者。

EOF

if [ "$DO_DOWNLOAD" -eq 0 ]; then
  echo "（当前为「只看不下载」模式。要真正下载，请加 --download）"
  echo "  官方渠道：https://github.com/$UPSTREAM/releases"
  echo "  官网入口：https://weflow.top"
  [ -n "$MIRROR_REPO" ] && echo "  镜像渠道：https://github.com/$MIRROR_REPO/releases"
  echo
  echo "  用法示例：MIRROR_REPO=<维护者>/digital-life-skill $0 --download"
  exit 0
fi

fetch_assets() {
  local repo="$1"
  [ -z "$repo" ] && return 0
  curl -fsSL -H 'User-Agent: digital-life-skill' \
    "https://api.github.com/repos/$repo/releases?per_page=20" 2>/dev/null \
    | grep -o '"browser_download_url": *"[^"]*"' | sed 's/.*"\(http[^"]*\)"/\1/' || true
}

urls="$(fetch_assets "$UPSTREAM")"
urls="$urls
$(fetch_assets "$MIRROR_REPO")"
url="$(printf '%s\n' "$urls" | grep -Ei '\.(exe|dmg|zip|AppImage|deb)$' | head -n1 || true)"

if [ -z "$url" ]; then
  echo "没有找到可自动下载的安装包（上游当前没有任何 Release）。"
  echo "请手动下载："
  echo "    https://weflow.top"
  echo "    https://github.com/$UPSTREAM"
  [ -n "$MIRROR_REPO" ] && echo "    https://github.com/$MIRROR_REPO/releases"
  exit 1
fi

mkdir -p "$OUT_DIR"
dest="$OUT_DIR/$(basename "$url")"
echo "  下载中 → $dest"
curl -fL --progress-bar -H 'User-Agent: digital-life-skill' -o "$dest" "$url"

echo
echo "下载完成（未安装、未执行）："
echo "  文件   : $dest"
echo -n "  SHA256 : "; sha256sum "$dest" | cut -d' ' -f1
echo
echo "  提醒：该目录已被 .gitignore 排除；遵守上游 CC BY-NC-SA 4.0。"
echo "        再分发给他人时必须保留署名：WeFlow / 作者 cc (hicccc77) /"
echo "        https://github.com/hicccc77/WeFlow / CC BY-NC-SA 4.0 / 非商业用途。"
echo "        完整文本见 THIRD_PARTY_NOTICES.md"
