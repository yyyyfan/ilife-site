# 019 图片全部迁到 Cloudflare R2，仓库与 Pages 不再含图片

## 目标
用户要求（2026-10-22）：所有图片统一放 Cloudflare R2；GitHub 仓库（包括全部 Git 历史）和 Cloudflare Pages 都不再放任何图片文件；网站（含本地开发）一律从 R2 公开地址读图。这样本地只需代码和数据，部署 Pages 只传代码与 JSON，不会把线上图片冲掉，仓库也不再因图片历史膨胀。

## 范围
- Cloudflare：新建 R2 桶 `ilife-images`，开启 Public Development URL（r2.dev）。账号下没有自有域名，暂不绑自定义域名。
- 上传：`img/` 下全部 4048 个文件按原字节上传（不转码、不裁剪），对象键 = 原相对路径（`img/xxx.jpg`），Content-Type 按扩展名（jpg→image/jpeg，webp→image/webp）。
- 代码：
  - `db/export.py`：新增唯一配置常量 `IMG_BASE`（R2 公开地址前缀）；导出 JSON 时把 `images.local`（以及以 `img/` 开头的 `images.url`）拼成完整地址；"图片文件存在"检查改为核对 `db/r2_manifest.json`。数据库里 `local` 仍存对象键，不改数据。
  - 新增 `db/r2_manifest.json`（R2 对象清单：键 → [字节数, md5, Content-Type]）和 `db/r2_images.py`（add / upload-cmd / verify）。
  - `db/cf_upload.py`：部署时跳过 `img/` 目录和所有图片扩展名。
  - `_headers`：删除已无用的 `/img/*` 规则。
  - `.gitignore`：忽略 `img/` 与图片扩展名（`img/` 只作上传前本地暂存）。
  - `app.js` 不用改（本来就读 `i.local||i.url`）。
- Git：从所有分支的全部历史中删除 `img/`（历史中只有图片在这个目录），强制推送全部分支。
- 文档：`docs/HANDOFF.md`、`db/README.md`、`AGENTS.md` 更新图片存储说明。
- 不做：不改任何数据内容；不改图片；不绑自定义域名（账号下暂无域名）。

## 数据来源
无新增事实数据；图片字节来自仓库 `img/`（e61b6bc）。

## 验收标准
- [x] R2 对象数 = 4048，总字节 = 851,782,258，每个对象字节数、MD5（etag）、Content-Type 与本地一致（连接器逐个比对 + 公开地址全量下载比对）
- [x] `python3 db/export.py --check` 全部一致；JSON 中所有站内图片地址都以 `IMG_BASE` 开头且在清单中
- [x] 本地 `python3 -m http.server` 打开首页/成员/成员详情/公演/公演详情/歌曲/图库/时期，图片全部来自 R2 且 HTTP 200，无破图、无脚本错误，本地服务器没有任何 `/img/` 请求
- [x] 重写历史前完整备份（`git clone --mirror` + 原有 bundle）
- [x] 全部分支历史中没有图片文件；强制推送后远端分支与本地一致
- [x] 部署 Pages 不含图片；两站 `version.json` 为新版本；线上页面图片来自 R2 且 200

## 状态
已完成（结果见 `019-result.md`）。
