# 026 歌曲补官方影像（MV 链接）与相关图片

## 需求

用户要求：歌曲补充更多图片和 MV 链接。

## 现状（动手前）

- `songs` 表只有 `mv_date`（31/44 首有值），**没有任何 MV 链接字段**；`songs.json` 只导出
  `id/title/kana/mv_date/release_date/release/note/source/cover/costumes`。
- 歌曲详情页只有「MV 公开日 / 发行日 / 所属作品 / note / 出处 / 打歌服」，
  没有影像入口，也没有除打歌服以外的图片。
- 6 首歌（1、4、5、8、9、19）共用同一张占位封面（image 731）。

## 做法

### 1. 影像：只认官方 YouTube 频道

- `db/yt_channel_scan.py` 走完 `@iLiFE_official` 全量列表：**93 条**视频，写 `db/.cache_yt/channel.json`。
  频道页结构已从 `videoRenderer` 换成 `lockupViewModel`（`contentId` + `metadata.lockupMetadataViewModel.title.content`），
  分页走 `youtubei/v1/browse` 的 `continuationCommand.token`，`INNERTUBE_API_KEY` / `CLIENT_VERSION` 从页面里抓。
- `db/task026_song_media.py --plan`：视频标题里出现曲名（NFKC 归一化、去空格、小写）即命中，
  类型 `【MV】` > リリックビデオ/Lyric > LIVE映像/LIVE MOVIE > DANCE。**一歌多影像全部保留**。
- `--dates`：逐条抓 `youtube.com/watch?v=<id>` 的 `publishDate`（67 条全成功）。
- `--thumbs`：探测 `i.ytimg.com/vi/<id>/{maxres,sd,hq}default.jpg`，优先 maxres（67/67 可用）。
- `--apply`：写 `song_videos`（68 行）。

结果：**36/44 首有官方影像**，共 68 条 —— MV 24、Lyric 5、Live 30、Dance 6、Other 3。
8 首查无：Sleeping face、Quest×Quest、キラメキダイアリー、HUNGRY!!!、Ride On!、Shout of Joy、メッセージ、i REVOLUTION。

**交叉校验**：31 首有 `mv_date` 的歌里，27 首与对应 MV 的上传日**完全一致**，说明两套数据互相印证；
不一致的 4 首：第 15、25 首差 1 天（跨日上传）；第 13 首 `mv_date` 2022-03-26 是初版 MV，
频道上现存的是 2024-02-22 的 Lyric/MV cover 版；第 44 首 `mv_date` 2026-08-26 但频道查无该 MV。

### 2. 相关图片：宁可少收，不可误收

先试过「文字里出现曲名」→ 太多误收（巡演通版海报、㊗️フォロワー4万人感谢帖、
「iLiFE!に会いにKiTE!」这种把歌名当口头禅的句子）。最终规则：

1. 曲名必须**被引号点名**：`「」『』【】“”` 包住（说明是在指这首作品，不是在造句）；
2. 排除事务性内容：`チケット|レギュレーション|注意事項|お申込|抽選|フォロワー|カラオケ|物販|グッズ|販売|予約受付|受付開始|再販|当落|入金|締切|サイン会`；
3. 排除插画（`category='illustration'`）与该曲打歌服图（打歌服另有 `costumes` 分组，避免重复展示）。

结果：**31 首共 121 张**（33 首歌命中，其中 2 首命中的全是打歌服图被排除）。
按此规则命中的典型是 MV 公开告知、配信/jacket 解禁、リリイベ现场照、音番出演。

### 3. 数据与前端

- 新表 `song_videos(song_id, video_id, kind, title, date, thumb, ord)`、
  `song_images(song_id, image_id, ord)`（写进 `db/schema.sql`）。
- `export.py`：`songs.json` 增加 `videos[]`（`id/kind/title/date/url/thumb`）与 `images[]`（同公演图的字段）；
  新增校验：`song_videos.video_id` 必须 11 位 YouTube ID、`thumb` 必须 https 直链、
  `song_images` 的图必须在 R2 清单里。
- `app.js` 歌曲详情新增两段：**官方影像 · N 条**（缩略图 + 类型标签 + 标题 + 日期 + YouTube 外链）、
  **相关图片 · N 张**（16:9 网格 + 灯箱，与打歌服共用 `flat` 索引）。
  列表卡片缩略图改为**优先用 MV 缩略图**（`object-fit:cover`），卡片第三行在没有 `mv_date` 时显示「影像 N 条」。
- `style.css` 新增 `.vidlist/.vid/.vt/.vb/.vtl/.vdt` 与 `.photos.wide`。

## 为什么缩略图不进 R2

缩略图是视频的元数据，和视频同源同生共死：视频挂了缩略图也没意义，单独存一份到 R2 只是多 67 个对象、
多 11 分钟 wrangler 上传，换不来任何可靠性。所以 `song_videos.thumb` 直接存 `i.ytimg.com` 直链，
`export.py` 只校验它是 https。**X 帖图片仍然全部进 R2**（那条规则针对的是会失效的 `pbs.twimg.com`）。

## 验收

- `python db/export.py --check` 全绿，版本 `46b84571`。
- `song_videos` 68 / `song_images` 121；36 首有影像、31 首有图片。
- 浏览器实测（headless Chrome 截图）：`songs.html?s=19` 会いにKiTE! 显示 5 条影像（MV/LIVE/Dance/2×コール動画）
  + 11 张相关图片 + 1 套打歌服；`?s=40` BRAVE GROOVE 显示 1 条 MV + 8 张图；`?s=44` 无影像时显示「未找到官方影像」而不是空白。
- 列表页 44 张卡片里，36 张换成各自的 MV/影像缩略图，不再是一片相同的占位图。

## 踩到的坑

- 频道的 `videoRenderer` 已经不存在，按老结构解析会得到 0 条；必须读 `lockupViewModel`。
- 按曲名做 YouTube **搜索**（`db/song_mv_scan.py`）结果噪声极大（播放列表、别家频道、翻唱），
  改成「整频道抓全量 + 本地按标题匹配」后一次命中 36 首。搜索脚本已删。
- `export.py` 的「逐字节一致」在 Windows 上其实是「语义一致」：`open(...,'w')` 默认把 `\n` 翻成 `\r\n`，
  文件比 `len(s.encode())` 多出的字节正好是换行数（`core.autocrlf=true`，提交时会被规范化回 LF）。
