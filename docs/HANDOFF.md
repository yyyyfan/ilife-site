# iLiFE! 应援资料库 · 项目交接说明（HANDOFF）

> 写于 2026-10-22（JST/北京时间同日）。交给新的 AI / 协作者继续维护时，**先读本文件，再读根目录 `AGENTS.md` 和 `db/README.md`**。
> 本文不含任何令牌、密钥或密码，只说明去哪里、怎样获取。

## 1. 项目是什么
- 偶像团体 **iLiFE!**（アイライフ，运营 HEROINES / imaginate）的**非官方粉丝资料库**：成员、在籍时间轴、时期阵容、歌曲与打歌服、全部公演、会场、日历、图库。
- 页面文案为简体中文，成员名、歌名、公演名保持日文原文。
- 线上地址：
  - GitHub Pages：<https://yyyyfan.github.io/ilife-site/>（push 到 `main` 自动发布）
  - Cloudflare Pages：<https://ilife-site.pages.dev>（项目名 `ilife-site`，**手动直传部署**，不连 Git）
- GitHub 仓库：<https://github.com/yyyyfan/ilife-site>（owner `yyyyfan`，默认分支 `main`）。
- 交接时线上版本：`data/version.json` = `45ebf2c3`（两站一致）。019（图片迁 R2）之后的版本见 `docs/tasks/019-result.md`，以两站 `data/version.json` 为准。
- **图片不在仓库里**：全部图片在 Cloudflare R2 桶 `ilife-images`，公开地址前缀 `https://img.ilifefan.dpdns.org/`（R2 自定义域名，见第 6 节）。

## 2. 技术栈
- 纯静态站：8 个很小的 HTML 壳 + 一个 `app.js`（原生 JS，无框架、无构建）+ `style.css`。数据由前端 `fetch('data/*.json?v=版本')` 读取。
- 数据源：SQLite 数据库 `db/ilife.sqlite`（唯一真源）→ `db/export.py`（Python 3 标准库）导出 `data/*.json`。
- 部署脚本：`deploy.sh`（bash）+ `db/cf_upload.py`（需 `pip install blake3 requests`）+ `db/cf_deploy.template.js`（生成的部署脚本在 Cloudflare 连接器里执行）。
- 图片处理：Pillow（转 webp、读宽高）。图片存储：Cloudflare R2（`db/r2_images.py` 维护清单 `db/r2_manifest.json`）。
- 本地预览：仓库根目录 `python3 -m http.server 8000`，打开 <http://localhost:8000/>。

## 3. 目录结构
```
ilife-site/
├─ AGENTS.md              协作规范与硬性规则（执行方必读）
├─ index/members/songs/lives/venues/calendar/eras/gallery.html   页面壳（data-page 区分页面）
├─ app.js                 全部前端逻辑（导航、各页渲染、灯箱、网格）
├─ style.css              样式（偶像应援风 + 成员应援色）
├─ _headers               Cloudflare Pages 缓存头（作为部署表单字段上传）
├─ .nojekyll              让 GitHub Pages 不走 Jekyll
├─ data/                  由 db/export.py 生成的 JSON（不要手改）
│   members / eras / timeline / lives / songs / images .json, version.json
├─ img/                   （不入库）新图上传 R2 前的本地暂存目录，已在 .gitignore
├─ db/
│   ├─ ilife.sqlite        数据库（唯一真源）
│   ├─ schema.sql          表结构
│   ├─ export.py           校验 + 导出 JSON + 更新 HTML 资源版本号
│   ├─ check_sources.py    抓取校验非 X 外部出处 / 会场容量出处
│   ├─ cf_upload.py        Cloudflare Pages 资产上传（自动跳过 img/ 与所有图片文件）
│   ├─ r2_manifest.json    R2 图片对象清单：键 → [字节数, md5, Content-Type]（export 用它校验图片存在）
│   ├─ r2_images.py        R2 图片工具：add 记入清单 / upload-cmd 打印 wrangler 上传命令 / verify 核对公开地址
│   ├─ cf_deploy.template.js  创建部署的连接器脚本模板
│   ├─ import_from_json.py 一次性迁移脚本（已执行，勿重跑）
│   └─ README.md           数据库与发布说明
├─ docs/
│   ├─ HANDOFF.md          本文件
│   └─ tasks/              任务单 001–018、结果(-result)、验收(-acceptance)、审计脚本(015-audit/016-audit/audit)
├─ member-audit.md, photo-audit.md   早期成员与照片核对记录
└─ deploy.sh              一键导出+推送+Cloudflare 上传
```
`.gitignore` 忽略 `db/cf_manifest.json`、`db/cf_deploy.js`、`__pycache__/`（部署临时产物），以及 `img/` 和 jpg/jpeg/png/webp/gif/avif/heic（图片一律不进 Git）。

## 4. 数据模型（`db/ilife.sqlite`，行数为交接时）
| 表 | 行数 | 内容 |
|---|---|---|
| `members` | 26 | 成员（含已毕业、支援、候补生）：读音、生日、应援色 hex、X 账号、状态等；`sort`/`tl_sort` 为显示顺序 |
| `member_fields_sources` | 229 | 成员每个字段对应的出处 |
| `member_periods` | 30 | 在籍区间（type：r=正式，s=支援，n=非正式/候补生），驱动时间轴 |
| `timeline_marks` | 5 | 时间轴上的标记事件 |
| `eras` | 12 | 时期 e1..e12（起始日、阵容变化、出处） |
| `era_members` | 88 | 各时期阵容（role：支援/副支援/休止，空=正式） |
| `songs` | 44 | 歌曲：MV 公开日、发行日、收录作品、封面 `cover_image_id` |
| `song_videos` | 68 | 官方 YouTube 影像（任务 026）：`kind`=MV/Lyric/Live/Dance/Other、原标题、上传日 `date`、缩略图直链 `thumb`（YouTube CDN，不入 R2） |
| `song_images` | 121 | 歌曲相关图片（任务 026）：引号点名曲名的官方帖图 |
| `costumes` / `costume_images` | 27 / 103 | 打歌服（对应歌曲与时期）及其图片 |
| `lives` | 872 | 公演：日期(JST)、标题、会场、type（ワンマン/主催/対バン/フェス/リリイベ/生誕祭/配信/その他）、开场/开演、note、setlist、主出处 `source_id`、封面 `cover_image_id` |
| `live_members` | 0 | 预留（每场出演成员），尚未填 |
| `venues` | 215 | 会场：名称、都道府县、地址、容量、URL |
| `images` | 4379 | 图片：原图 URL `url`/`orig`、R2 对象键 `local`（如 `img/xxx.webp`，导出时拼成 R2 完整地址）、日期、来源帖 `post_id`(→sources)、类别 category、宽高 w/h、复核 review |
| `image_members` / `image_eras` / `image_lives` | 1348 / 4379 / 684 | 图片与成员 / 时期（按日期自动推导）/ 公演的关联 |
| `sources` | 4321 | 所有出处 URL（唯一） |
| `meta` | 2 | 杂项（timeline 来源与说明） |

要点：
- `*key_order` 列记录原 JSON 键顺序，保证导出逐字节稳定；新增记录照抄同类记录的 key_order。
- `lives.note` 里的约定词：`仅非官方来源`（只有 Eventernote/LiveFans 等第三方出处）、`未出演`（官方公告辞退）、`补充核验：URL`（第三方辅助链接）。
- 图片 category：other 1679、official 1032、live 888、member 381、costume 334、illustration 65。

## 5. 导出与检查命令
```bash
python3 db/export.py --check            # 只校验并与现有 JSON/HTML 版本号逐字节比对，不写文件（每次必跑）
python3 db/export.py                    # 校验通过后写出 data/*.json、version.json，并更新 HTML 的 ?v=
python3 db/export.py --rebuild-derived  # 改了时期起始日或图片日期后用，重算 image_eras
python3 db/check_sources.py [--year 2022]  # 联网抓取校验非 X 出处是否真实且提到 iLiFE!
```
export 会检查：外键、日期/时间格式与先后、时期顺序、重复记录、图片在 R2 清单 `db/r2_manifest.json` 中、成员/时期关联一致。失败则列出问题、非零退出、不写文件。版本号 = style.css + app.js + 全部 JSON 的内容哈希。

## 6. 图片规则与存储
### 6.1 存储：Cloudflare R2（任务 019 起）
- **GitHub 仓库（含全部历史）和 Cloudflare Pages 都不放任何图片**。图片全部在 R2：
  - 桶：`ilife-images`（Cloudflare 账号同 Pages 项目；位置 ENAM，Standard 存储）
  - 公开地址前缀（R2 自定义域名，任务 021 起）：`https://img.ilifefan.dpdns.org/`
    - 域名 `ilifefan.dpdns.org` 托管在 Cloudflare（NS `rommy.ns.cloudflare.com` / `alexia.ns.cloudflare.com`），
      2026-10-22 在 R2 → 桶 → Settings → Custom Domains 绑定 `img` 子域，证书自动签发，状态 Active。
    - 走 Cloudflare 边缘缓存，不再受 r2.dev 限速影响。
  - 备用地址（Public Development URL，仅开发/回滚用）：`https://pub-12b0e8cdf6994377a377f1b1909e1ea9.r2.dev/`（有限速，超限 429）
  - 对象键 = 原相对路径，如 `img/E-1mfcBVQAE82N2.jpg` → `https://img.ilifefan.dpdns.org/img/E-1mfcBVQAE82N2.jpg`
  - 019 迁移时 4048 个对象，851,782,258 字节（3693 jpg + 355 webp），按原字节上传、未转码。
- 唯一配置点：`db/export.py` 的 `IMG_BASE`。数据库 `images.local` 只存对象键；导出 JSON 时拼成完整地址，前端 `app.js` 直接用 JSON 里的地址，所以本地开发（`python3 -m http.server`）也从 R2 读图，本地不需要任何图片文件。换域名只改 `IMG_BASE`、重新导出并部署即可。
- `db/r2_manifest.json` 是 R2 中对象的清单（键 → [字节数, md5, Content-Type]），`export.py` 用它检查"图片存在"。新图必须先上传到 R2 再记入清单，否则导出失败。
- 缓存规则（2026-10-23 已配置）：Cache Rules 匹配 `Hostname equals img.ilifefan.dpdns.org`，
  Cache eligibility = Eligible for cache，Edge TTL / Browser TTL 均 override 为 1 年。
  实测首次 MISS、再次 `cf-cache-status: HIT`，响应 `Cache-Control: max-age=31536000`，10 张抽样 md5 全部一致。
  图片文件名唯一、内容不变，缓存后源站请求接近零；改图必须换文件名（或 purge）。
- 费用：R2 免费额度每月 10 GB 存储，读取流量本身不收费；当前约 0.85 GB。

### 6.2 新增图片的流程
1. 按下面的规则准备图片，放到本地暂存目录 `img/`（不会被 Git 提交、也不会被部署到 Pages）。
2. 上传到 R2（键必须是 `img/<文件名>`，Content-Type 要正确，字节原样）。任选一种，**凭据都不要写进仓库**：
   - wrangler：`npx wrangler login` 后，`python3 db/r2_images.py upload-cmd img/xxx.webp` 打印命令，形如 `npx wrangler r2 object put ilife-images/img/xxx.webp --file "img/xxx.webp" --content-type image/webp --remote`。
   - Cloudflare API（原流程用 Cloudflare MCP 连接器 `execute`）：`PUT /accounts/{account_id}/r2/buckets/ilife-images/objects/img/xxx.webp`，请求体为图片字节、`Content-Type` 为图片类型；返回的 `etag` 应等于文件 md5。连接器单次请求体上限约 4 MB（base64 后），适合少量图片。
   - S3 兼容接口（rclone / aws cli）：在 Cloudflare 面板为该桶创建 R2 API 令牌（Object Read & Write，限定桶 `ilife-images`），endpoint `https://<account_id>.r2.cloudflarestorage.com`；令牌用完删除。
3. `python3 db/r2_images.py add img/xxx.webp`：把字节数/md5/类型记入 `db/r2_manifest.json`。
4. `python3 db/r2_images.py verify img/xxx.webp`：从公开地址下载核对（200、类型、字节、md5 一致）。不带参数默认抽查 20 个，`--all` 全量。
5. 在 `images` 表登记（`local` = `img/xxx.webp`，w、h、date、post_id、source、category），跑 `python3 db/export.py`，提交 `db/ilife.sqlite`、`db/r2_manifest.json`、`data/*`。暂存的 `img/xxx.webp` 之后可删。
- **替换图片必须换新文件名**，不要覆盖 R2 里已有的键（`r2_images.py add` 遇到同名不同内容会拒绝）。删除图片时，R2 对象可以保留（不影响网站），清单里的条目也可保留。

### 6.3 图片内容规则
- 每张图**必须**在 `images` 表登记（local、w、h、date、post_id、source、category）。早期 X 图多为 `<媒体ID>.jpg`（长边 ≤1600）；016 以后新增为 webp，如 `live-<live_id>-<媒体ID>.webp`、`jacket-<JAN>.webp`。
- **只用官方图**：@iLiFE_official、成员官方账号、主办方官方账号/官网、TicketDive 等主办方自建售票页、Apple Music 配信 jacket、官方月度日程图、演后官方感谢合照。
- **Eventernote / LiveFans 等第三方图片一律不用**（016 曾误加 77 张已删除）。
- **不裁剪、不改比例**；X 取 `name=orig`（或 large），转 webp，长边 ≤2048px（等比缩小），单张 ≤1MB。
- 公演封面 `images.date` = **演出日期**；写 `image_lives` 并设 `lives.cover_image_id`。
- **一场要收该场出处帖的全部图片，不是只收一张**（任务 025 起）。归属判断不需要猜：
  同一个 X 帖的图就是该场的图；图片键名约定 `img/live-<live_id>-<媒体ID>.webp` 可直接判重。
  工具：`db/live_images.py`（`--stage` 下载转码 → 上传 R2 + `r2_images.py add` → `--apply-new` 入库 → `--covers` 重算封面；
  另有 `--link` 补挂、`--fix-eras` 补时期）。`--fix-eras` 必须跑，否则导出报「image_eras 与日期不符」。
- **封面取「最能代表这一场」的那张**：演出照（`category='live'`）> 该场专属告知图 > 官方图 > 打歌服/成员 > 其他；
  同档时保持现有封面不动（避免把海报换成更大的时间表）。只有出现更高档的图才覆盖。
  目前 624 场有封面，其中 12 张被 3 场以上共用（多为巡演通版海报，等有当日图再换）。
- 歌曲封面：找不到 CD/配信 jacket 时可用官方 MV 告知图（如第 13、31、43 首），找到 jacket 再替换。
- **歌曲影像与相关图片（任务 026）**：
  - 影像只收**官方 YouTube 频道**（`@iLiFE_official`）。判定：视频标题里出现曲名（NFKC 归一化、去空格、小写），
    类型按 `【MV】` > リリックビデオ/Lyric > LIVE映像/LIVE MOVIE > DANCE 排序；一歌多影像全部保留（MV + LIVE + Dance 版并存）。
    工具 `db/yt_channel_scan.py`（抓频道全量，含 continuation 分页；页面结构已从 `videoRenderer` 改为 `lockupViewModel`）
    + `db/task026_song_media.py --plan/--dates/--thumbs/--apply`。
  - 缩略图用 YouTube CDN 直链（`i.ytimg.com`，优先 maxresdefault），**不入 R2**：它是视频元数据，与视频同源同生共死。
  - 相关图片的判定必须**严格**：帖子文字里曲名要**被引号点名**（「」『』【】“”），且不含票务/抽选/物贩/粉丝数里程碑/卡拉OK 上架等事务性内容，
    并排除插画与该曲打歌服图（打歌服另有 `costumes` 分组）。只按「文字里出现过曲名」收会大量误收（巡演通版海报、里程碑感谢帖）。
  - 2026-10 现状：36/44 首歌有官方影像（MV 24、Lyric 5、Live 30、Dance 6、Other 3，共 68 条）；31 首歌有相关图片（共 121 张）。
    8 首查无官方影像：Sleeping face、Quest×Quest、キラメキダイアリー、HUNGRY!!!、Ride On!、Shout of Joy、メッセージ、i REVOLUTION。
- 017 中节日 cosplay / 万圣节棚拍照**没有**作为演出封面（不能证明出演该场）；3 张已撤封面但保留在图库。用户尚未把这条定为永久规则。

## 7. 前端概览（`app.js`）
- 每个 HTML 只有 `<body data-page=…>` 和空的 header/main，`app.js` 按 `data-page` 渲染：home 首页、members 成员（卡片+在籍时间轴）、songs 歌曲（统一卡片网格→详情，详情含「官方影像 / 相关图片 / 打歌服」三段；列表缩略图优先用 MV 缩略图）、lives 公演（按年卡片网格，每场一张封面；详情显示类型、开场/开演、出处链接、note 原文与 setlist）、venues 会场、calendar 日历、eras 时期/公式图、gallery 图库（按时期/成员/类别筛选）。
- `NAV` 数组定义导航；`V` 为当前版本号，所有 fetch 带 `?v=`；灯箱 `#lb` 支持左右翻页。
- 网格：按行铺满、格子以图片最大分辨率占位，图片用 `object-fit:contain` 不裁剪。
- 页脚声明非官方、版权归原发布者。

## 8. 发布与部署
### 8.1 GitHub Pages
- 仓库 Settings → Pages：Source 为 `main` 分支根目录。push 到 main 后约 1–2 分钟自动发布。
- 需要对 `yyyyfan/ilife-site` 有 push 权限的 GitHub 账号（HTTPS + 个人访问令牌或 SSH key，**自行配置，不在仓库里**）。

### 8.2 Cloudflare Pages（直传项目 `ilife-site`，生产分支 `main`）
所需凭据（都不在仓库中）：
- Cloudflare 账号（登录邮箱即账号所有者）下的 Pages 项目 `ilife-site`。Account ID 在 Cloudflare 面板右侧/URL 中可见。
- 一个有 **Account → Cloudflare Pages: Edit** 权限的 API Token（在 My Profile → API Tokens 创建），用来：
  1. `GET /accounts/{account_id}/pages/projects/ilife-site/upload-token` 取得**短期上传 JWT**（有效期短，每次部署现取）；
  2. `POST /accounts/{account_id}/pages/projects/ilife-site/deployments` 创建部署。
- 原流程里这两步通过 Cloudflare MCP 连接器完成（连接器 `execute` 内置 `accountId` 与 `cloudflare.request`）。换到别的环境时，可用 `curl -H "Authorization: Bearer $CF_API_TOKEN"` 完成同样两步，或直接用 `npx wrangler pages deploy . --project-name ilife-site --branch main`（wrangler 会自动处理 `_headers`；需排除 `.git`、`db/` 等不必要文件时注意体积）。

部署包**不含任何图片**（`cf_upload.py` 跳过 `img/` 和图片扩展名；图片在 R2，见第 6 节），所以部署不会影响线上图片。

步骤（与原流程一致）：
1. 验收通过、合并到 main，`python3 db/export.py --check` 全部通过。
2. 取上传令牌，存到**仓库外**的临时文件，如 `/tmp/cf-upload-token.json`（支持纯 JWT 或 `{"jwt":"…"}`）。
3. 运行 `./deploy.sh "提交说明" /tmp/cf-upload-token.json`：导出 → commit + push（触发 GitHub Pages）→ `cf_upload.py` 计算 blake3 哈希、`check-missing`、分批上传缺失文件、`upsert-hashes` → 生成 `db/cf_deploy.js`（含 manifest 与 `_headers` 表单字段）。可先 `python3 db/cf_upload.py --dry-run 令牌文件` 预检。
4. 在 Cloudflare 连接器 `execute` 中运行 `db/cf_deploy.js` 的内容创建部署（或用 curl 发同样的 multipart：`manifest`、`branch=main`、`_headers`）。
5. **删除令牌文件**和 `db/cf_deploy.js`、`db/cf_manifest.json`（已在 .gitignore，不要提交）。
6. 验证：`curl https://yyyyfan.github.io/ilife-site/data/version.json` 与 `curl https://ilife-site.pages.dev/data/version.json` 都等于仓库 `data/version.json`；抽查受影响页面（桌面与手机宽度）。

## 9. 长期数据规则（用户要求严格执行）
1. **数据只改 `db/ilife.sqlite`**，不手改 `data/*.json`；改完跑 export。
2. **每条事实都要有出处，且出处必须实际打开过**、页面确实提到 iLiFE! 且与日期/会场/活动名一致；不得拼接或猜 URL / 推文 ID / events 编号；查不到就留空并写“未查到”。数字（容量等）要有能直接看到该数字的页面。
3. **Eventernote / LiveFans 只能当线索**：只有第三方出处的公演在 note 写 `仅非官方来源`；尽量升级为官方出处（@iLiFE_official、主办方 X/官网/售票页），原第三方链接可留作 `补充核验：`，不能是唯一出处。
4. 官方出处与现有数据不一致时以官方为准并在结果里列出；官方显示没出演的**不要删**，交用户决定。
5. **日期一律 JST**；推文时间由 post ID 换算（snowflake：`(id>>22)+1288834974657` 毫秒，再 +9h），不要用 UTC 日期。
6. 图片规则见第 6 节（只用官方图、不裁剪不改比例、webp ≤2048px ≤1MB、images.date=演出日期）。
7. 视觉沿用现有偶像应援风与成员应援色；文案简体中文，日文专名保持原文。
8. 一个任务一组提交，提交信息写清改了什么、依据是什么；**不提交令牌/密钥**。

## 10. 工作流程
- **角色**：规划/验收/合并/部署 = 主 AI（原为 Grok Bot）；写代码改数据 = 外部编码代理（默认 Antigravity，备选 Codex）。
- **流程**：规划方在 `docs/tasks/NNN-简短名.md` 写任务单（目标/范围/数据来源/验收标准/状态）→ 新建 worktree 与分支（Antigravity `agy/NNN-slug`，Codex `codex/NNN-slug`，从最新 main 拉出）→ 编码代理只推送自己的分支（绝不推 main、不 force push、不部署），完成后写 `NNN-result.md` 并把状态改为「待验收」→ 规划方逐项验收（按年份逐条打开出处抽查/全查），修正写入 `NNN-acceptance.md` → 合并 main → 部署 → 两站核对版本。
- **启动编码代理**（在 worktree 根目录运行，完全信任、不弹确认）：
  ```bash
  nohup ~/.local/bin/agy -p "先读 AGENTS.md 和 docs/tasks/NNN-xxx.md，严格按任务单完成……" \
    --model gemini-3.8-flash-high --dangerously-skip-permissions --print-timeout 180m \
    </dev/null > /workspace/agy-NNN.log 2>&1 &
  codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox "任务内容" </dev/null
  ```
  `</dev/null` 很重要，否则可能挂起等输入。
- **巡检**：每 20 分钟看 PID 是否存活（`kill -0`）、日志修改时间、是否有新提交；超过 40 分钟无进展则重启，同一任务失败 3 次换 Codex。用户希望**自动观察并修复异常**，只汇报里程碑和阻塞；23:30–08:00 安静时段只静默修复，08:00 后合并汇报。
- 与用户沟通用简体中文；需要用户拍板的事项（如删数据、规则变更）先问再做。

## 11. 历史任务摘要（详见 `docs/tasks/`）
| 编号 | 内容 | 结果 |
|---|---|---|
| 001 | 新增歌曲页与打歌服 | 完成 |
| 002 | 歌曲日期与出处修正（区分 MV 公开日/发行日） | 完成 |
| 003 | 修复 deploy.sh 的 Cloudflare 上传步骤与令牌解析 | 完成 |
| 004 | 歌曲页改统一卡片网格（方案 A） | 完成 |
| 005 | 补歌曲卡片封面与打歌服 | 完成 |
| 006 | 静态资源自动版本号、缓存头 | 完成 |
| 007 | 部署时正确上传 `_headers` | 完成 |
| 008 | 再找 Ride On! / Shout of Joy 官方图 | Shout of Joy 找到，Ride On! 未找到 |
| 009 | 公演数据结构 + 2020–2021 年全部公演 | 完成（36→172 场） |
| 010 | 2022 年公演（第一版） | **撤回**（69 个第三方出处指向无关页面） |
| 011 | 2020–2021 出处换官方 | 完成（随 012 合并） |
| 012 | 2022 年公演严格出处重做 | 完成 |
| 013 | 公演页改卡片并配图（Antigravity 卡住，改 Codex） | 完成 |
| 014 | 补 23/24 场会场 + 2027 年官方配图 | 会场完成；2027 年 11 场未找到配图 |
| 015 | 补全 2023–2026 年公演（严格出处） | 完成，新增 535 场，共 865 场 |
| 016 | 补全所有配图（歌曲 + 公演） | 完成；删 Eventernote 图；图片日期改演出日期；GMOアリーナさいたま 会场改名已用官方出处确认 |
| 017 | 2020–2023 公演配图（逐场找主办方官方原帖） | 完成，有封面 239→277（共 472）；撤 3 张万圣节棚拍照 |
| 018 | 2020–2022 公演逐场换官方出处 | 完成，182 场中 98 场升级，剩 84 场 |
| 019 | 图片全部迁到 Cloudflare R2；仓库全部历史与 Pages 删除图片 | 完成（见 019-result.md；历史已重写，旧提交号作废） |
| 020 | 主流出道单曲『アイドルライフメガパック』发行信息 + 7 场发售纪念活动 | 完成，lives 865→872，会场 210→215 |
| 021 | 图片基地址从 r2.dev 切到 R2 自定义域名 img.ilifefan.dpdns.org | 完成，4310 条图片地址切换，抽查 25 个对象 0 问题 |
| 022 | 统一仓库行尾为 LF | 完成，新增 `.gitattributes`，114 个文件转 LF，`export.py --check` 不再误报 |
| 023 | 2021 年新冠自肃辞退的 5 场统一标「未出演」 | 完成，未出演 2→5，124/126/127 补注并改引 imaginate 公告 |
| 024 | 里程碑公演改用官方公告为源并补开场/开演时间 | 完成，10 条 Wikipedia 源改官方，27→17；新增官方公告索引 |
| 025 | 每场公演收录出处帖的全部图片 + 封面按代表性重算 | 完成，新增 68 张（43 场），多图场 9→42，17 场从无封面到有封面 |
| 026 | 歌曲补官方影像（MV 链接）与相关图片 | 完成，36/44 首有影像（68 条），31 首有相关图片（121 张），歌曲详情新增「官方影像 / 相关图片」两段 |

## 12. 当前覆盖情况（交接时由数据库计算）
| 年份 | 公演数 | 有封面 | 无封面 | 多图场 | 仅非官方来源 | 标记未出演 |
|---|---|---|---|---|---|---|
| 2020 | 45 | 29 | 16 | 2 | 4 | 0 |
| 2021 | 95 | 61 | 34 | 6 | 24 | 5 |
| 2022 | 157 | 83 | 74 | 17 | 56 | 0 |
| 2023 | 175 | 121 | 54 | 8 | 65 | 0 |
| 2024 | 156 | 115 | 41 | 4 | 32 | 0 |
| 2025 | 121 | 113 | 8 | 3 | 12 | 0 |
| 2026 | 111 | 102 | 9 | 0 | 0 |
| 2027 | 12 | 0 | 12 | 0 | 0 | 0 |
| **合计** | **872** | **624** | **248** | **42** | **193** | **5** |

- 歌曲：44 首，有封面 43 首（缺 Ride On!）。
- 歌曲影像（026）：36 首有官方影像共 68 条（MV 24 / Lyric 5 / Live 30 / Dance 6 / Other 3）；
  8 首查无（Sleeping face、Quest×Quest、キラメキダイアリー、HUNGRY!!!、Ride On!、Shout of Joy、メッセージ、i REVOLUTION）。
  交叉校验：31 首有 `mv_date` 的歌里 27 首与对应 MV 上传日完全一致，另 4 首差 1 天（跨日上传）或原 MV 已删后重发（第 13 首）。
- 歌曲相关图片（026）：31 首共 121 张（引号点名曲名的官方帖图，已排除票务/抽选/物贩/里程碑帖与打歌服图）。
- 图片：4379 条（025 新增 68 张 webp，均已上传 R2 并记入清单；R2 清单 4116 个对象）。
  公演图片关联 684 条（`image_lives`），其中 42 场挂了 2–4 张。
- 会场 215 个；时期 12 个；成员 26 人（现役正式 9 人）。
- 里程碑公演（27 条曾以 Wikipedia 为源）经 024 后剩 **17 条**仍为 Wikipedia：live 5、7、8、10、11、13、25–35。
  这 17 条同时 open_time/start_time 为空，官网现存公告不覆盖，等官方公告或 X 帖可确认时再补。

## 13. 未完成 / 待决定事项
1. ~~**2021 年 imaginate 7/21 新冠公告**~~：023 已处理，123/124/125/126/127 共 5 场统一标「未出演」，出处改引 imaginate 公告。
2. **2027-01-11 主流出道单曲『アイドルライフメガパック』**：020 已录入发行信息与 7 场发售纪念活动；
   剩余 CD 各形态 jacket（官方「決まり次第掲載」）与 7 场活动封面（告知图待上传 R2）。
3. **2027 年 12 场 JAPANLiFE! 2027 巡演 + 1/9 发售活动封面**：等官方出海报后补。
4. **2020–2023 年仍有 195 场无封面**（每场查过的地方在 `017-result.md`）；2024–2026 另有 58 场无封面，2027 年 12 场（巡演 + 发售活动）等官方海报。
5. **仅非官方来源仍有 193 场**：2020–2022 共 84 场（明细见 `018-result.md`，多为售票页失效或主办方账号已删），2023: 65、2024: 32、2025: 12。
   **024 已确认 2023 那 65 场无法用官网公告升级**：官网 `topics/detail/<id>` 详情页仍在线，但 ID 段 900–2050 全量扫完只剩
   21 条公告（最早 2023-04-12，2018–2022 已被 JamClip 改版删除），全部是巡演/TIF/成员异动类，不含单场对盘告知；
   Wayback CDX 仍离线，X 站内关键词搜索需登录。要推进只能逐场找主办方官网（018 的路子），成本高，待定。
6. 歌曲 **Ride On!** 封面缺失；**TIF 2025 8/2（live 723）** 封面为空（原图无法核实已撤）。
   026 之后 Ride On! 仍无封面也无影像，是唯一「封面/影像/打歌服」三项全空的歌。
7. **7 首成员个人曲的 MV 不在 `songs` 表**（026 抓频道时发现，官方频道有 MV 但库里没登记）：
   初恋サマーライン♡（若葉のあ）、To be alive（空詩かれん）、フクキタリズム（福丸うさ）、
   PIXEL by PIXEL / i（あいす）、らぶりー属性♡（心花りり）、みんなのあいす屋さん（あいす）。
   要补需先定「个人曲是否与团体曲同表」的规则，并补发行日/收录/出处。
8. **i REVOLUTION（第 44 首）有 `mv_date` 2026-08-26 但官方频道查无此 MV**，可能发布在别的频道或已下架，待查。
9. 规则待定：节日 cosplay / 棚拍照是否永久不算演出封面（目前按不算处理）。
10. `live_members`（每场出演成员）尚未填写，且 `export.py` / `app.js` 均未引用该表（等于未启用）。
   若要做，官方 2025-05-30 公告（topics/1804）给了 2025-06-01 iLiVE! 的 9 人並行特典会排班，可作第一个样本。

## 14. 给接手 AI 的建议起手式
```bash
git clone https://github.com/yyyyfan/ilife-site.git && cd ilife-site
pip install blake3 requests pillow
python3 db/export.py --check          # 应全部“逐字节一致”
python3 -m http.server 8000            # 本地预览（图片直接从 R2 加载，本地无需图片）
```
然后读 `AGENTS.md` → 本文件 → 最近的 `docs/tasks/019-*.md`，从第 13 节挑任务、写任务单 020 开始。
