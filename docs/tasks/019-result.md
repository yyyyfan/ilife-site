# 019 结果：图片全部迁到 Cloudflare R2

完成时间：2026-10-22 23:40（北京时间 / JST 2026-10-23 00:40）。由 Grok Bot 直接实施（基础设施变更，用户明确要求，并确认了重写历史与强制推送）。

## R2
- 桶：`ilife-images`（位置 ENAM，Standard）。Public Development URL 已开启：`https://pub-12b0e8cdf6994377a377f1b1909e1ea9.r2.dev/`
- 账号下没有 Cloudflare 托管的域名，所以没有绑自定义域名。Cloudflare 文档说明 r2.dev "is rate-limited and should only be used for development purposes"（超限返回 429）；以后有域名时可绑到桶上，只需改 `db/export.py` 的 `IMG_BASE` 并重新导出部署。
- 对象：4048 个，851,782,258 字节（3693 jpg + 355 webp），键 = 原路径 `img/<文件名>`，按原字节上传，Content-Type 按扩展名。
- 上传方式：Cloudflare 连接器没有创建 API 令牌的权限，连接器的出网 fetch 也被限制，单次请求体上限 4 MB。因此临时部署了一个带 R2 绑定、用随机密钥保护的 Worker `ilife-r2-upload-tmp`，从工作机按原字节 PUT 进桶（写入时由 R2 校验 MD5）。上传完立即删除了该 Worker，密钥文件也已删除。为此账号新建了 workers.dev 子域 `yyyyfan.workers.dev`（Cloudflare 首次打开 Workers 页面也会自动建），现在上面没有任何 Worker。
- 核对：
  1. 连接器列出桶内全部对象，与本地清单逐个比对键、字节数、MD5（etag）、Content-Type：4048/4048 一致，无缺失、无多余。
  2. 从公开 r2.dev 地址全量下载 4048 个对象，核对 HTTP 200、Content-Type、字节数与 MD5：0 个问题。

## 代码与数据
- `db/export.py`：唯一配置 `IMG_BASE`；导出时 `images.local` 和以 `img/` 开头的 `images.url`（5 条早期分格图）拼成 R2 完整地址；"图片存在"检查改为核对 `db/r2_manifest.json`，并新增 `url` 为站内图时的检查。数据库内容未改（`local` 仍存对象键）。
- 新增 `db/r2_manifest.json`（4048 条：键 → [字节数, md5, Content-Type]）和 `db/r2_images.py`（add / upload-cmd / verify）。
- `db/cf_upload.py` 跳过 `img/` 与图片扩展名；`_headers` 删掉 `/img/*`；`.gitignore` 忽略 `img/` 和图片扩展名。
- 导出 JSON 里 5706 处站内图片地址全部指向 R2 且都在清单中；`python3 db/export.py --check` 全部一致；新版本 `f676d8a2`。
- 本地 `python3 -m http.server` 用无头 Chrome 打开首页、成员、成员详情、公演、公演详情（l=700）、歌曲、图库、时期：图片全部来自 r2.dev 且 HTTP 200，无破图、无脚本错误，本地服务器没有收到 `/img/` 请求。

## Git 历史重写
- 备份（都在 `/workspace/ilife-export/`，不在仓库里）：`ilife-site-pre-r2-mirror.git`（`git clone --mirror`，旧的 9 个分支，含 e61b6bc）、原有的 `ilife-site-full-history.bundle`（已校验 complete history）、`refs-before-rewrite.txt` / `remote-refs-before-rewrite.txt` / `remote-refs-after-rewrite.txt`、旧 worktree 中未跟踪文件的打包 `worktree-untracked-leftovers.tar`。原 `img/` 目录移到 `img-pre-r2/`。
- `git filter-repo --invert-paths --path img/ --path-regex '(?i)\.(jpe?g|png|webp|gif|avif|heic|bmp|tiff?|ico)$'`，作用于全部 9 个分支（远端没有标签，也没有只在远端的分支、PR 或 fork）。历史中所有图片都在 `img/` 下（4056 个路径），其他文件未动：每个分支重写后的文件树 = 旧文件树去掉 `img/`（逐分支比对一致）。提交数 141 → 142（多出的是 019 的提交），没有提交被丢弃。
- 重写后全部历史中图片路径数 = 0。本地 `.git` 886.96 MiB → 5.53 MiB。
- 强制推送 9 个分支（旧 → 新）：
  - main e61b6bc → 99c0d0b（019 提交；其父提交 09e82a5 即原 e61b6bc）
  - agy/012-lives-2022 6260d06 → 0cd4637
  - agy/013-lives-cards 578a02f → f790cf7
  - agy/016-all-images 839e6a7 → 5600d2a
  - agy/017-images-2020-2023 44e029c → 3e45a3b
  - agy/018-lives-2020-2022-official-sources 395bf4e → ffe7066
  - codex/013-lives-cards 484d592 → 6e83b2b
  - codex/014-venue-2027-images 57cfd9f → 44fd0bd
  - codex/015-lives-2023-2026 bcefdc4 → d850367
- 旧的 worktree（ilife-site-agy012/013/016/017/018、codex014/015、ilife-016-acc）已用 `git worktree remove --force` 删除并 prune（未跟踪文件先打包备份）。
- 之前文档和聊天里出现的旧提交号（如 395bf4e、44e029c、e61b6bc）在新历史里都不存在了；旧克隆要重新 clone，不能 pull。

## 部署
- Cloudflare Pages 部署 `55bab748-605f-4cfc-a23b-1f4adce593cd`：103 个文件，不含任何图片。
- 两站 `data/version.json` = `f676d8a2`；GitHub Pages 已按 99c0d0b 构建。
- 线上用无头 Chrome 打开首页、成员详情、公演详情（l=700）、歌曲、图库（两站都查）：图片全部来自 r2.dev，HTTP 200，无破图、无脚本错误。
- 旧图片地址：`https://yyyyfan.github.io/ilife-site/img/...` 返回 404；`https://ilife-site.pages.dev/img/...` 返回 200 但内容是首页 HTML（Pages 没有 404.html 时的默认回退），不再是图片。

## 遗留
- GitHub 的 `size` 字段和服务端旧对象要等 GitHub 自己回收；旧提交在被回收前仍可能按完整 SHA 直接访问。要立即彻底清除，需要仓库所有者联系 GitHub Support 请求 GC。
- Google Drive 上 `ilife-site-export-e61b6bc/ilife-site` 是旧快照（含图片、旧历史），保留作备份；如要与新仓库一致，需重新导出。
- r2.dev 限速：正式使用建议以后绑自定义域名（见上）。

## 后续：自定义域名（任务 021，2026-10-23）

域名 `ilifefan.dpdns.org` 已托管到 Cloudflare；R2 桶 `ilife-images` 自定义域名 `img.ilifefan.dpdns.org` 已启用。`IMG_BASE` 已切到该域名（见 `docs/tasks/021-result.md` / HANDOFF 第 6 节）。r2.dev 公开访问**保持开启**作备用/开发。

