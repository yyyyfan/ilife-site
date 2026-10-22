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
- 交接时线上版本：`data/version.json` = `45ebf2c3`（两站一致）。

## 2. 技术栈
- 纯静态站：8 个很小的 HTML 壳 + 一个 `app.js`（原生 JS，无框架、无构建）+ `style.css`。数据由前端 `fetch('data/*.json?v=版本')` 读取。
- 数据源：SQLite 数据库 `db/ilife.sqlite`（唯一真源）→ `db/export.py`（Python 3 标准库）导出 `data/*.json`。
- 部署脚本：`deploy.sh`（bash）+ `db/cf_upload.py`（需 `pip install blake3 requests`）+ `db/cf_deploy.template.js`（生成的部署脚本在 Cloudflare 连接器里执行）。
- 图片处理：Pillow（转 webp、读宽高）。
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
├─ img/                   全部站内图片（约 4048 个文件，821 MB；平铺一个目录）
├─ db/
│   ├─ ilife.sqlite        数据库（唯一真源）
│   ├─ schema.sql          表结构
│   ├─ export.py           校验 + 导出 JSON + 更新 HTML 资源版本号
│   ├─ check_sources.py    抓取校验非 X 外部出处 / 会场容量出处
│   ├─ cf_upload.py        Cloudflare Pages 资产上传
│   ├─ cf_deploy.template.js  创建部署的连接器脚本模板
│   ├─ import_from_json.py 一次性迁移脚本（已执行，勿重跑）
│   └─ README.md           数据库与发布说明
├─ docs/
│   ├─ HANDOFF.md          本文件
│   └─ tasks/              任务单 001–018、结果(-result)、验收(-acceptance)、审计脚本(015-audit/016-audit/audit)
├─ member-audit.md, photo-audit.md   早期成员与照片核对记录
└─ deploy.sh              一键导出+推送+Cloudflare 上传
```
`.gitignore` 忽略 `db/cf_manifest.json`、`db/cf_deploy.js`、`__pycache__/`（部署临时产物）。

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
| `costumes` / `costume_images` | 27 / 103 | 打歌服（对应歌曲与时期）及其图片 |
| `lives` | 865 | 公演：日期(JST)、标题、会场、type（ワンマン/主催/対バン/フェス/リリイベ/生誕祭/配信/その他）、开场/开演、note、setlist、主出处 `source_id`、封面 `cover_image_id` |
| `live_members` | 0 | 预留（每场出演成员），尚未填 |
| `venues` | 210 | 会场：名称、都道府县、地址、容量、URL |
| `images` | 4311 | 图片：原图 URL `url`/`orig`、站内路径 `local`、日期、来源帖 `post_id`(→sources)、类别 category、宽高 w/h、复核 review |
| `image_members` / `image_eras` / `image_lives` | 1348 / 4311 / 616 | 图片与成员 / 时期（按日期自动推导）/ 公演的关联 |
| `sources` | 4309 | 所有出处 URL（唯一） |
| `meta` | 2 | 杂项（timeline 来源与说明） |

要点：
- `*key_order` 列记录原 JSON 键顺序，保证导出逐字节稳定；新增记录照抄同类记录的 key_order。
- `lives.note` 里的约定词：`仅非官方来源`（只有 Eventernote/LiveFans 等第三方出处）、`未出演`（官方公告辞退）、`补充核验：URL`（第三方辅助链接）。
- 图片 category：official 966、live 886、member 381、costume 334、illustration 65、other 1679。

## 5. 导出与检查命令
```bash
python3 db/export.py --check            # 只校验并与现有 JSON/HTML 版本号逐字节比对，不写文件（每次必跑）
python3 db/export.py                    # 校验通过后写出 data/*.json、version.json，并更新 HTML 的 ?v=
python3 db/export.py --rebuild-derived  # 改了时期起始日或图片日期后用，重算 image_eras
python3 db/check_sources.py [--year 2022]  # 联网抓取校验非 X 出处是否真实且提到 iLiFE!
```
export 会检查：外键、日期/时间格式与先后、时期顺序、重复记录、图片文件存在、成员/时期关联一致。失败则列出问题、非零退出、不写文件。版本号 = style.css + app.js + 全部 JSON 的内容哈希。

## 6. 图片规则与存储
- 文件放 `img/`（平铺），并**必须**在 `images` 表登记（local、w、h、date、post_id、source、category）。早期 X 图多为 `<媒体ID>.jpg`（长边 ≤1600）；016 以后新增为 webp，如 `live-<live_id>-<媒体ID>.webp`、`jacket-<JAN>.webp`。
- **只用官方图**：@iLiFE_official、成员官方账号、主办方官方账号/官网、TicketDive 等主办方自建售票页、Apple Music 配信 jacket、官方月度日程图、演后官方感谢合照。
- **Eventernote / LiveFans 等第三方图片一律不用**（016 曾误加 77 张已删除）。
- **不裁剪、不改比例**；X 取 `name=orig`（或 large），转 webp，长边 ≤2048px（等比缩小），单张 ≤1MB。
- 公演封面 `images.date` = **演出日期**；写 `image_lives` 并设 `lives.cover_image_id`。
- 歌曲封面：找不到 CD/配信 jacket 时可用官方 MV 告知图（如第 13、31、43 首），找到 jacket 再替换。
- 017 中节日 cosplay / 万圣节棚拍照**没有**作为演出封面（不能证明出演该场）；3 张已撤封面但保留在图库。用户尚未把这条定为永久规则。
- `_headers` 对 `/img/*` 只缓存 1 天：**替换图片必须换新文件名**，不要原地覆盖。

## 7. 前端概览（`app.js`）
- 每个 HTML 只有 `<body data-page=…>` 和空的 header/main，`app.js` 按 `data-page` 渲染：home 首页、members 成员（卡片+在籍时间轴）、songs 歌曲（统一卡片网格→详情，含打歌服）、lives 公演（按年卡片网格，每场一张封面；详情显示类型、开场/开演、出处链接、note 原文与 setlist）、venues 会场、calendar 日历、eras 时期/公式图、gallery 图库（按时期/成员/类别筛选）。
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

## 12. 当前覆盖情况（交接时由数据库计算）
| 年份 | 公演数 | 有封面 | 无封面 | 仅非官方来源 | 标记未出演 |
|---|---|---|---|---|---|
| 2020 | 45 | 28 | 17 | 4 | 0 |
| 2021 | 95 | 59 | 36 | 24 | 2 |
| 2022 | 157 | 70 | 87 | 56 | 0 |
| 2023 | 175 | 120 | 55 | 65 | 0 |
| 2024 | 156 | 115 | 41 | 32 | 0 |
| 2025 | 121 | 113 | 8 | 12 | 0 |
| 2026 | 105 | 102 | 3 | 0 | 0 |
| 2027 | 11 | 0 | 11 | 0 | 0 |
| **合计** | **865** | **607** | **258** | **193** | **2** |

- 歌曲：44 首，有封面 43 首（缺 Ride On!）。
- 图片：4311 条（img/ 中 3955 jpg + 355 webp；1 条仅外链 Wayback 原图未落地）。
- 会场 210 个；时期 12 个；成员 26 人（现役正式 9 人）。

## 13. 未完成 / 待决定事项
1. **2021 年 imaginate 7/21 新冠公告（待用户决定）**：公告称 iLiFE! 辞退 4 场：7/22 アナフェス（live 123）、7/23 HEROINES FES vol.2（live 124）、7/25 真夏のShining Days（live 125）、8/1 IDOL CONTENT EXPO 品川 DAY2（live 127）。123、125 已标「未出演」；124（note 仍写“新曲披露公演”）和 127 尚未标注。建议：4 场都保留，124、127 也改「未出演」并引用该公告；用户尚未回复。
2. **2027-01-11 主流出道单曲『アイドルライフメガパック』未录入**（歌曲、发行信息、封面、相关发售活动），需另开任务、找官方出处。
3. **2027 年 11 场 JAPANLiFE! 2027 巡演封面**：等官方出海报后补。
4. **2020–2023 年仍有 195 场无封面**（每场查过的地方在 `017-result.md`）；2024–2026 另有 52 场无封面。
5. **仅非官方来源仍有 193 场**：2020–2022 共 84 场（明细见 `018-result.md`，多为售票页失效或主办方账号已删），2023: 65、2024: 32、2025: 12，可仿照 018 继续逐场升级。
6. 歌曲 **Ride On!** 封面缺失；**TIF 2025 8/2（live 723）** 封面为空（原图无法核实已撤）。
7. 规则待定：节日 cosplay / 棚拍照是否永久不算演出封面（目前按不算处理）。
8. `live_members`（每场出演成员）尚未填写。

## 14. 给接手 AI 的建议起手式
```bash
git clone https://github.com/yyyyfan/ilife-site.git && cd ilife-site
pip install blake3 requests pillow
python3 db/export.py --check          # 应全部“逐字节一致”
python3 -m http.server 8000            # 本地预览
```
然后读 `AGENTS.md` → 本文件 → 最近的 `docs/tasks/018-*.md`，从第 13 节挑任务、写任务单 019 开始。
