#!/usr/bin/env bash
# 用法：./deploy.sh [提交说明] [Cloudflare 上传令牌文件]
#  1) 由 db/ilife.sqlite 导出 data/*.json（完整性检查失败则中止）
#  2) git commit + push（GitHub Pages 自动发布）
#  3) 若给出令牌文件：上传缺失文件到 Cloudflare Pages，并生成 db/cf_deploy.js
#     令牌须通过 Cloudflare 连接器获取（GET /accounts/{id}/pages/projects/ilife-site/upload-token），
#     最后一步“创建部署”也须用连接器 execute 运行生成的 db/cf_deploy.js —— 这两步无法在脚本内完成。
set -euo pipefail
cd "$(dirname "$0")"
MSG="${1:-Update data}"; TOKEN="${2:-}"
python3 db/export.py
git add -A
if git diff --cached --quiet; then echo "无改动，跳过提交"; else git commit -qm "$MSG"; fi
git push -q && echo "GitHub 已推送：$(git rev-parse --short HEAD)"
if [ -n "$TOKEN" ]; then
  SITE_ROOT="$PWD" MANIFEST="$PWD/db/cf_manifest.json" python3 db/cf_upload.py "$TOKEN"
  python3 - <<'PY'
s=open('db/cf_deploy.template.js').read().replace('__MANIFEST__',open('db/cf_manifest.json').read())
open('db/cf_deploy.js','w').write(s)
PY
  echo "已生成 db/cf_deploy.js：请用 Cloudflare 连接器 execute 运行它以创建部署。"
else
  echo "未提供令牌文件，跳过 Cloudflare。"
fi
