#!/usr/bin/env bash
set -euo pipefail
# 用法：./deploy.sh [提交说明] [Cloudflare 上传令牌文件]
#  1) 由 db/ilife.sqlite 导出 data/*.json（完整性检查失败则中止）
#  2) git commit + push（GitHub Pages 自动发布）
#  3) 若给出令牌文件：上传缺失文件到 Cloudflare Pages，并生成 db/cf_deploy.js
#     令牌须通过 Cloudflare 连接器获取（GET /accounts/{id}/pages/projects/ilife-site/upload-token），
#     最后一步“创建部署”也须用连接器 execute 运行生成的 db/cf_deploy.js —— 这两步无法在脚本内完成。

cd "$(dirname "$0")"

cleanup() {
  local exit_code=$?
  if [ $exit_code -ne 0 ]; then
    rm -f db/cf_deploy.js db/cf_deploy.js.tmp
  fi
}
trap cleanup EXIT

MSG="${1:-Update data}"; TOKEN="${2:-}"

# 若指定了令牌文件，提前校验文件是否存在
if [ -n "$TOKEN" ] && [ ! -f "$TOKEN" ]; then
  echo "错误：令牌文件不存在：$TOKEN" >&2
  exit 1
fi

python3 db/export.py

# 提交并推送到 GitHub
git add -A
# 严防令牌文件被意外暂存提交（若令牌文件位于仓库目录下）
if [ -n "$TOKEN" ]; then
  git reset -q HEAD -- "$TOKEN" 2>/dev/null || true
fi

if git diff --cached --quiet; then
  echo "无改动，跳过提交"
else
  git commit -qm "$MSG"
fi
git push -q && echo "GitHub 已推送：$(git rev-parse --short HEAD)"

if [ -n "$TOKEN" ]; then
  # 先清理旧的产物，避免失败时残留
  rm -f db/cf_deploy.js db/cf_deploy.js.tmp db/cf_manifest.json

  SITE_ROOT="$PWD" MANIFEST="$PWD/db/cf_manifest.json" python3 db/cf_upload.py "$TOKEN"

  python3 - <<'PY'
import os
template = open('db/cf_deploy.template.js', encoding='utf-8').read()
manifest = open('db/cf_manifest.json', encoding='utf-8').read()
content = template.replace('__MANIFEST__', manifest)
with open('db/cf_deploy.js.tmp', 'w', encoding='utf-8') as f:
    f.write(content)
os.replace('db/cf_deploy.js.tmp', 'db/cf_deploy.js')
PY

  echo "已生成 db/cf_deploy.js：请用 Cloudflare 连接器 execute 运行它以创建部署。"
  echo "提示：令牌使用完毕，请及时删除本地令牌文件（如 rm -f \"$TOKEN\"）以避免凭据泄露。"
else
  echo "未提供令牌文件，跳过 Cloudflare。"
fi
