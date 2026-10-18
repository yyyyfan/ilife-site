# 数据库说明

网站数据统一保存在 `db/ilife.sqlite`（SQLite），`data/*.json` 只是由它导出的产物，**不要再手改 JSON**。

## 表结构（见 `schema.sql`）
- `members` 成员；`member_fields_sources` 每个字段的出处；`member_periods` 在籍区间（type：r=正式，s=支援，n=非正式/候补生）
- `eras` 时期；`era_members` 各时期阵容（role：支援/副支援/休止，空=正式）；`timeline_marks` 时间轴标记；`meta` 杂项
- `lives` 公演；`venues` 会场；`songs` 歌曲（待填）；`costumes` 服装（待填）
- `images` 图片（尺寸、本地路径、来源推文 `post_id`、日期、类别、复核状态 review/pending）；`image_members`、`image_eras` 关联
- `sources` 所有出处 URL
- `key_order` 列记录原 JSON 键顺序，保证导出逐字节一致；新增记录时按已有同类记录填写即可。

## 如何编辑
用任意 SQLite 工具（如 `sqlite3`、DB Browser for SQLite、Python）修改，例如：
```sql
UPDATE members SET note='…' WHERE name='心花りり';
INSERT INTO sources(url) VALUES('https://…');
```
修改了时期起始日或图片日期后，导出时加 `--rebuild-derived` 重算 `image_eras`。

## 导出与版本管理
```bash
python3 db/export.py                  # 检查并写出 data/*.json、data/version.json 并更新各 HTML 资源版本号
python3 db/export.py --check          # 校验并与现有 JSON 及 HTML 静态资源版本比对（不写文件）
python3 db/export.py --rebuild-derived
python3 db/check_sources.py           # 抓取并校验所有非 X 外部出处及会场容量出处
python3 db/check_sources.py --year 2022 # 仅校验指定年份（如 2022）的外部出处
```
导出前会检查：外键、日期格式与先后顺序、时期顺序、重复记录、图片文件是否存在、成员/时期关联一致性。任何一项失败都会列出问题并以非零码退出，不写文件。`check_sources.py` 用于核验引用的第三方网站（Eventernote、LiveFans、主办方活动页、会场容量页）是否真实存在且与 iLiFE! 演出或会场数据匹配。

### 静态资源缓存控制（Cache Busting）
为避免发布后浏览器强缓存旧版 JS/CSS/JSON 数据：
1. **自动版本号**：`export.py` 根据 `style.css`、`app.js` 及所有导出 JSON 的内容哈希生成统一版本号 `v`，写入 `data/version.json`，并更新所有 HTML 中引用的 `style.css?v=<版本>` 与 `app.js?v=<版本>`。内容无变化时多次导出不会产生无意义的 Git 差异。
2. **动态数据请求带版本号**：`app.js` 初始化时会自动读取当前引用的版本号，并在后续通过 `fetch` 获取 `data/*.json` 时附带 `?v=<版本>`，确保版本更新时全量刷新数据。
3. **响应头策略（`_headers`）**：Cloudflare Pages 根目录下配置 `_headers`，对所有 HTML 页面及根路由设置 `Cache-Control: no-cache`（每次向边缘验证有效性），对带版本号的 `style.css`、`app.js`、`data/*` 设置长效缓存（`max-age=31536000, immutable`）；`/img/*` 因曾有原地替换图片，仅缓存 1 天（`max-age=86400`），替换图片时应改用新文件名。本地使用 `python3 -m http.server` 或直接打开均可正常运行。

## 发布
```bash
./deploy.sh "提交说明" /path/to/upload-token.txt
```
脚本会导出 → 提交并推送 GitHub（Pages 自动更新）→ 上传文件到 Cloudflare Pages 并生成 `db/cf_deploy.js`。
Cloudflare 上传令牌须用 Cloudflare 连接器获取，最后的“创建部署”也须用连接器运行 `db/cf_deploy.js`。

### 令牌与预检说明
- **令牌格式**：令牌文件同时支持纯文本 JWT 与 `{"jwt": "..."}` JSON 格式（自动去除首尾空白字符）。
- **特殊配置文件（`_headers` 等）**：Cloudflare Pages 要求根目录下的 `_headers`、`_redirects` 与 `_routes.json` 不作为普通静态资源上传（不进入 manifest），而须作为创建部署时的同名表单字段发送。`cf_upload.py` 与 `deploy.sh` 会自动检测这些文件并将其排除出 manifest，在生成的 `db/cf_deploy.js` 中作为表单字段发送。
- **预检（dry-run）**：在正式发布前，可使用 `--dry-run` 仅在本地扫描待上传资源并计算哈希，不发起网络请求；检测到的特殊配置文件会在输出中单独列出，不计入 manifest：
  ```bash
  python3 db/cf_upload.py --dry-run /path/to/upload-token.txt
  ```
- **异常处理**：若令牌缺失、格式非法、过期或网络请求失败，脚本将输出明确中文错误提示并以非零码中断，且绝不会保留半成品的 `db/cf_deploy.js`。
- **安全注意**：令牌属于敏感凭据，请将令牌文件存放在仓库目录之外（如 `/tmp/token.txt`），使用完毕后及时删除临时文件，切勿提交到仓库。

`import_from_json.py` 是一次性迁移脚本（已执行），重跑需加 `--force`，会覆盖数据库。

