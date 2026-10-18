# 歌曲卡片封面与打歌服补全结果（Task 005）

对 19 首原无打歌服记录的歌曲逐首核查，按照任务单优先级（1. 专属打歌服 → 2. MV/发布告知衣装 → 3. 配信封面 → 4. 未找到）确定结论与关联图片。

## 统计概览
- **核查歌曲总数**：19 首
- **MV 衣装（登记入 costumes 表）**：2 首（可変三連MIXをおぼえる歌、完全勝利Love&Good！）
- **封面（登记入 songs.cover_image_id）**：15 首（sweet timer、Sleeping face、Quest×Quest、Dokkoi!ロマンティック、黄昏サイクル、青春のパズルは埋まらない、キラメキダイアリー、HUNGRY!!!、Hands Up!、ヒラリラリア、KiSEK!、ドラマチックミライ、ライフステージ、メッセージ、i REVOLUTION）
- **未找到（保持占位，note 注明）**：2 首（Ride On!、Shout of Joy）
- **卡片有图数量**：由 25/44 首增加至 42/44 首
- **筛选「有打歌服」数量**：由 25 首增加至 27 首，与 `costumes` 表数据完全一致

---

## 19 首逐首核查结论清单

| 序号 | 歌曲 ID | 歌名 | 结论 | 图片 ID / 路径 | 日期 (JST) | 出处链接 | 说明 |
| :---: | :---: | :--- | :---: | :--- | :---: | :--- | :--- |
| 1 | 2 | sweet timer | **封面** | [1288] `img/F8UCQodaEAAFGB5.jpg` (1200×675) | 2023-10-13 | [X @iLiFE_official](https://x.com/i/status/1712777723024912590) | 官方 YouTube LIVE MOVIE プレミア公开告知图，印有「sweet timer」艺术字，向日えな舞台特写 |
| 2 | 4 | Sleeping face | **封面** | [731] `img/Fkp6Y-naMAEvO6j.jpg` (1200×1200) | 2022-12-23 | [X @iLiFE_official](https://x.com/i/status/1606230795265662978) | 收录于 1st 专辑『アイライフスターターパック』（Type-C 甘音ゆあ盘收录曲），采用官方公布的专辑封面作为卡片封面 |
| 3 | 5 | Quest×Quest | **封面** | [731] `img/Fkp6Y-naMAEvO6j.jpg` (1200×1200) | 2022-12-23 | [X @iLiFE_official](https://x.com/i/status/1606230795265662978) | 收录于 1st 专辑『アイライフスターターパック』（Type-F 有栖るな盘收录曲），采用官方公布的专辑封面作为卡片封面 |
| 4 | 6 | Dokkoi!ロマンティック | **封面** | [53] `img/Envrh_4UwAAsAOM.jpg` (1200×675) | 2020-11-26 | [X @iLiFE_official](https://x.com/i/status/1331917087510392833) | 官方 LIVE 映像公开告知图，印有「Dokkoi ロマンティック iLiFE!」艺术字及心花りり舞台照 |
| 5 | 7 | 黄昏サイクル | **封面** | [1636] `img/GF-c3fNasAAnUbS.jpg` (1200×675) | 2024-02-10 | [X @iLiFE_official](https://x.com/i/status/1756294865326133399) | 官方 YouTube TDC Hall 演唱会 LIVE MOVIE プレミア公开告知图，印有「黄昏サイクル LIVE MOVIE」标志及向日えな感人舞台画面 |
| 6 | 8 | 青春のパズルは埋まらない | **封面** | [731] `img/Fkp6Y-naMAEvO6j.jpg` (1200×1200) | 2022-12-23 | [X @iLiFE_official](https://x.com/i/status/1606230795265662978) | 收录于 1st 专辑『アイライフスターターパック』（亦收录于 2nd 专辑），采用官方公布的 1st 专辑封面作为卡片封面 |
| 7 | 9 | キラメキダイアリー | **封面** | [731] `img/Fkp6Y-naMAEvO6j.jpg` (1200×1200) | 2022-12-23 | [X @iLiFE_official](https://x.com/i/status/1606230795265662978) | 收录于 1st 专辑『アイライフスターターパック』（Type-D 深月らむ盘收录曲），采用官方公布的专辑封面作为卡片封面 |
| 8 | 10 | HUNGRY!!! | **封面** | [130] `img/E1BYjdLVoAQCs3J.jpg` (1200×800) | 2021-05-10 | [X @iLiFE_official](https://x.com/i/status/1391709666091028480) | 官方 HEROINES FES @ Zepp Tokyo 新曲初披露告知图，印有「新曲初披露 HUNGRY!!」字样及全员舞台姿态 |
| 9 | 13 | 可変三連MIXをおぼえる歌 | **MV 衣装** | [374] `img/FOxmN_xaQAMC2k_.jpg` (1200×675) | 2022-03-26 | [X @iLiFE_official](https://x.com/i/status/1507692377989066753) | 官方 MV 公开告知，MV 中全员穿着专门的格子衬衫、头巾、粗框眼镜与荧光棒经典宅系 MV 打歌服，登记为衣装「可変三連MIXをおぼえる歌 オタク風MV衣装」（costume id: 26, era: e4） |
| 10 | 14 | Ride On! | **未找到** | 无 | — | 无 | 早期 Live 披露曲，未音源化，无 MV、无专属打歌服，在官方 X 及官网均未查到官方图片。保持音符占位，note 写明「未找到官方图片。」 |
| 11 | 16 | Hands Up! | **封面** | [539] `img/FcM7XLjaMAAcSD7.jpg` (1200×675) | 2022-09-09 | [X @iLiFE_official](https://x.com/i/status/1568162368462671873) | 官方 LIVE MV 公开告知图，印有「Hands Up! iLiFE!」艺术字及心花りり舞台特写 |
| 12 | 17 | Shout of Joy | **未找到** | 无 | — | [サンスポ 会见报道](https://www.sanspo.com/article/20220726-KNYRKXU6MNLGZPPPFXMYSFGJSA/) | 手球日本传达 100 周年官方应援曲，未音源化，仅于手球协会官网短期公开，官方 X 未发布歌曲官方图片。保持音符占位，note 写明「未找到官方图片。」 |
| 13 | 18 | ヒラリラリア | **封面** | [622] `img/FfwRuzRakAAjLcV.jpg` (1200×675) | 2022-10-23 | [X @iLiFE_official](https://x.com/i/status/1584160784007180289) | 官方 YouTube Lyric Video 公开告知插画，印有「ヒラリラリア iLiFE!」艺术字及全员女仆/侍应插画 |
| 14 | 20 | KiSEK! | **封面** | [818] `img/Fork-6vaUAAUKyP.jpg` (1200×675) | 2023-02-11 | [X @iLiFE_official](https://x.com/i/status/1624362394326827009) | 官方情人节企划 LIVE MV 公开告知图，印有「LIVEMV KiSEK! iLiFE! 2023.1.25」标志与舞台照 |
| 15 | 22 | ドラマチックミライ | **封面** | [1842] `img/GNxjSbNbYAA42r8.jpg` (1200×675) | 2024-05-17 | [X @iLiFE_official](https://x.com/i/status/1791415926761623929) | 官方 YouTube LIVE MOVIE プレミア公开告知图，印有「ドラマチックミライ iLiFE! LIVEMOVIE 2024.3.30」艺术字与福丸うさ特写 |
| 16 | 30 | ライフステージ | **封面** | [2042] `img/GVaeFW6aMAErjkD.jpg` (1200×675) | 2024-08-20 | [X @iLiFE_official](https://x.com/i/status/1825820518379123055) | 官方幕张ワンマン LIVE MOVIE 公开告知图，印有「2024.8.12 ライフステージ iLiFE! LiVE YOUR LiFE! LIVE MOVIE」艺术字与涼芽なの特写 |
| 17 | 33 | メッセージ | **封面** | [2635] `img/Gps-eWmboAAtI0g.jpg` (1200×800) | 2025-04-29 | [X @iLiFE_official](https://x.com/i/status/1917194779932467648) | 收录于 2nd 专辑『アイドルライフエクストラパック』第 3 曲，采用官方 X 发布的该专辑全 18 曲サブスク配信告知图（右侧清晰印有第 3 首「メッセージ」） |
| 18 | 38 | 完全勝利Love&Good！ | **MV 衣装** | [3275] `img/G_bkJvOaQAADKYq.jpg` (1200×675) | 2026-01-24 | [X @iLiFE_official](https://x.com/i/status/2015048750767714393) | 官方舞蹈视频プレミア公开告知图，全员 9 人在聚光灯下穿着涂鸦牛仔风打歌服，印有「完全勝利 Love&Good! iLiFE!」标志，登记为衣装「完全勝利Love&Good！ ダンス動画衣装」（costume id: 27, era: e11；附图 3274） |
| 19 | 44 | i REVOLUTION | **封面** | [3955] `img/1200214845070.jpg` (1200×1200) | 2026-08-26 | [Apple Music i REVOLUTION](https://music.apple.com/jp/album/i-revolution-single/6802605792) | 2026-08-26 配信限定单曲（Fear, and Loathing in Las Vegas 乐曲提供），采用官方配信单曲封面（迪斯科球与霓虹图腾），高清原图保存至 `img/1200214845070.jpg` 并登记入 images 表与 sources 表 |

---

## 新增数据与改动说明
1. **数据库结构**：
   - `db/schema.sql`：在 `songs` 表新增 `cover_image_id INTEGER REFERENCES images(id)` 字段。
   - `db/ilife.sqlite`：应用相应变更，添加外键约束。
2. **新增图片**：
   - 下载官方配信封面原图至 `img/1200214845070.jpg`（1200×1200，无裁剪，无变形）。
   - 登记至 `images` 表（id: 3955, date: '2026-08-26', source: 'Apple Music', post_id: 2833）。
   - 关联时期至 `image_eras`（image_id: 3955, era_id: 'e12'）。
3. **新增服装**：
   - Costume 26: `可変三連MIXをおぼえる歌 オタク風MV衣装` (song_id: 13, era: e4, debut_date: '2022-03-26', image_id: 374, source_id: 341)。关联 `costume_images`。
   - Costume 27: `完全勝利Love&Good！ ダンス動画衣装` (song_id: 38, era: e11, debut_date: '2026-01-24', image_id: 3275, source_id: 2360)。关联 `costume_images`（主图 3275，附图 3274）。
4. **歌曲卡片封面关联**：
   - 15 首歌曲通过 `songs.cover_image_id` 关联官方卡片封面。
   - 2 首未找到官方图片的歌曲（Ride On!、Shout of Joy）在 `songs.note` 标明「未找到官方图片。」，保持 ♪ 音符占位。
5. **数据导出与检查**：
   - `db/export.py`：导出 `songs.json` 的 `cover` 字段，并在完整性检查中增加歌曲封面文件存在性核验。
   - 运行 `python3 db/export.py --check` 全部通过（6 个 JSON 逐字节一致）。
6. **前端展示**：
   - `app.js`：更新歌曲列表封面取图逻辑 `const i = imgs(s)[0] || s.cover`。
   - 歌曲筛选「有打歌服」与 `costumes` 表保持一致（27 套 / 27 首）。
