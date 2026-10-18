# Ride On! 与 Shout of Joy 官方图片再核查结果（Task 008）

对 Task 005 中未找到官方图片的 2 首歌曲（Ride On!、Shout of Joy）进行针对性深度核查，核查范围覆盖官方 X（@iLiFE_official）、成员个人 X、日本手球协会（日本ハンドボール協会）官网及官方 SNS、新闻媒体报道（Sanspo 等）、官方 YouTube、创作者资讯与演出履历（LiveFans 等）。

---

## 核查结论一览

| 歌曲 ID | 歌名 | 最终结论 | 图片 ID / 路径 | 分辨率 | 日期 (JST) | 来源出处 | 说明 |
| :---: | :--- | :---: | :--- | :---: | :---: | :--- | :--- |
| 17 | **Shout of Joy** | **找到官方发布会报道照片，登记为封面** | [3956] `img/VV6UFTFIZNIE7CSXSZEWTNXUKQ.jpg` | 1478 × 1108 | 2022-07-25 | [サンスポ 会見報道](https://www.sanspo.com/article/20220726-KNYRKXU6MNLGZPPPFXMYSFGJSA/) | 2022-07-25 日本手球协会在东京举办「手球日本传入100周年纪念」发布会，公布 iLiFE! 担当主题曲「Hands Up!」与应援曲「Shout of Joy」。サンスポ 报道配发 6 名成员在官方赞助商背景板前合影高清原图（图说「テーマソングと応援ソングを歌うｉＬｉＦＥ！」），原比例保存并登记为 `songs.cover_image_id`。 |
| 14 | **Ride On!** | **未找到官方图片，保持音符占位** | 无 | — | — | [Wikipedia iLiFE!](https://ja.wikipedia.org/wiki/ILiFE!) | 未音源化、未配信、无 MV、无专属打歌服的早期 Live 曲（粉丝间被称为「干され曲」）。经全方位排查各官方及公开渠道，无官方单曲封面、告知海报或专属图片，按任务单规范保持 ♪ 音符占位并在 note 注明。 |

---

## 逐首详细核查过程与来源记录

### 1. Shout of Joy（歌曲 ID: 17）

#### 背景与事实核实
- **曲目性质**：日本ハンドボール協会（日本手球协会）「ハンドボール日本伝来100年記念」公式应援曲（作词・作曲：桑原 佑介）。
- **发表时间**：2022-07-25 协会在东京都内举办新闻发布会宣布。
- **音源公开**：2022-09-03 12:00 ～ 09-10 23:59 期间在日本手球协会官网特设网页限时公开试听/下载；无 MV、无商业正式配信、无实体 CD 发行。

#### 核查的来源清单
1. **产经体育（サンスポ）会见报道**：
   - 文章链接：`https://www.sanspo.com/article/20220726-KNYRKXU6MNLGZPPPFXMYSFGJSA/`
   - 发布时间：2022-07-26 15:47 JST（报道 7 月 25 日会见内容）
   - 报道明确提及：
     > 「また、女性グループ、ｉＬｉＦＥ！（アイライフ）がハンドボール日本伝来１００年記念テーマソング「Ｈａｎｄｓ　Ｕｐ」と応援ソング「Ｓｈｏｕｔ　ｏｆ　Ｊｏｙ！」を担当することも会見で発表した。」
   - **配发会见官方现场照片**：
     - 原图 URL：`https://cloudfront-ap-northeast-1.images.arcpublishing.com/sankei/VV6UFTFIZNIE7CSXSZEWTNXUKQ.jpg`
     - 图说：`「テーマソングと応援ソングを歌うｉＬｉＦＥ！」`
     - 图片内容：iLiFE! 当期 6 名成员（深月らむ、あいす、心花りり、甘音ゆあ、有栖るな、天羽しおり）在手球协会官方赞助商背景板前（含 hummel、三機工業、キョーレオピン、味の素、JAPAN 等标志）合影，摆出手球相关手势，着 2 周年白色舞台服装。
     - 尺寸：1478 × 1108（未裁剪、原图完整）。
2. **日本ハンドボール協会官网特设页面**：
   - 页面链接：`http://www.handball.or.jp/special/theme100.html` 及公告 `https://handball.or.jp/system/prog/content.php?article_idno=560&c=15&sc=1&sd=g`
   - 页面设有「応援ソング Shout of Joy（作詞・作曲 桑原 佑介）」试听播放器及歌词 PDF。
   - 艺人介绍部分配图为 iLiFE! 甜点主题公式艺人照（`http://www.handball.or.jp/special/image/100/iLiFE!.jpg`，900×600）。
   - 经比对，サンスポ 会见现场报道照片是专为本次 100 周年歌曲发布会拍摄的官方新闻照，且图说精确标注为演唱主题曲与应援曲的 iLiFE!，完全符合任务单要求的「明确是官方提供/发布会照片时使用，并注明出处」。

#### 处理动作
- 下载高清原图至 `img/VV6UFTFIZNIE7CSXSZEWTNXUKQ.jpg`（1478 × 1108，未经任何裁剪与变形）。
- 登记至 `images` 表（id: 3956, date: '2022-07-25', post_id: 2832, category: 'official', source: 'サンスポ', w: 1478, h: 1108）。
- 关联时期至 `image_eras`（image_id: 3956, era_id: 'e5'）。
- 更新 `songs` 表：`cover_image_id = 3956`，`source_id = 2832`，更新 `note` 描述。

---

### 2. Ride On!（歌曲 ID: 14）

#### 背景与事实核实
- **曲目性质**：作词：彩未 凛，作曲・编曲：まっつん。为早期 Live 披露曲。
- **音源状态**：未音源化、未配信、无 MV、无实体专辑收录（Wikipedia サブスク分类明确列为「未公開」）。

#### 核查的来源清单
1. **官方 X（@iLiFE_official）历史推文**：
   - 检索关键词：`Ride On`、`Ride on`、`ライドオン`、`まっつん`、`彩未 凛`、`新曲披露`、`初披露`。
   - 结果：数据库中抓取的官方推文文本以及在线检索中，均未出现该曲的官方专属告知图、单曲封面或宣传海报。
2. **成员个人 X（深月らむ、心花りり、有栖るな、天羽しおり、向日えな、甘音ゆあ、琥珀しえる 等）**：
   - 检索各成员历史推文，未见带有「Ride On」专曲图样或披露宣传画面的官方图片。
3. **官方 YouTube 频道（@iLiFE_official）**：
   - 该曲从未发布过官方 MV、Lyric Video 或 Live Movie。
   - 唯一提及该曲的官方视频为 2022-09-21 发布的直播回放 `【生配信アーカイブ】第一回アイライファーミーティング後編【コールを考える編】`（视频 ID: `0MZ4PNzpKkk`），视频简介中列出了成员与粉丝共同讨论的 `◇Ride on(ライドオン) MIX◇` 呼号表（含 Standard MIX、勘定奉行 MIX、混沌 MIX、Spain MIX 等）。该视频缩略图为全员通用的生配信插画（「YouTube生配信会議！「俺らで作ろうiLiFE!コール編」」），并非歌曲封面。
4. **LiveFans 演出记录与曲目数据库**：
   - LiveFans 曲目编号：`songs/712745`（演奏率约 1%）。
   - 仅记录了 2022-04-12 在 Spotify O-EAST 举办的拼盘演出 `LEADING ID -Birthday Special-` 的演出歌单中包含《Ride on!》（同场演唱歌曲：初恋リバイバル、可変3連MIXをおぼえる歌、君セン!、Ride on!、むげんだいすき）。该活动为编舞师 いどみん 的多团联合生日活动，非 iLiFE! 专场，亦无针对该曲的官方图片。
5. **创作者公开资讯（彩未 凛、まっつん）**：
   - 词曲作者虽然在商业作品与自主制作中多次合作，但在各自主页、SNS 上均未单独为《Ride On!》制作或公开官方视觉图/Jacket。
6. **粉丝社群与 Yahoo! 知恵袋**：
   - 粉丝提问「iLiFE!公式YouTubeからRide On!と言う曲って出てないんですか？」，获答确认「曲自体はありますが完全干され曲です」（属于未公开发行、演出频次极低的非主打未公开曲目）。

#### 处理动作
- 确认该曲在所有官方与正规渠道均不存在可用图片，严格遵照规范保持 ♪ 音符占位，不编造、不使用非官方二次创作图。
- 数据库 `songs.cover_image_id` 保持为 `NULL`，`songs.note` 完整记录核查事实。

---

## 数据库与代码改动一览

1. **新增图片登记**：
   - 文件：`img/VV6UFTFIZNIE7CSXSZEWTNXUKQ.jpg`（1478 × 1108，222,411 bytes）
   - 表 `images`：新增 id `3956`，日期 `2022-07-25`，出处 `サンスポ`，关联来源 `post_id = 2832`。
   - 表 `image_eras`：新增 `(3956, 'e5')`。
2. **歌曲封面关联**：
   - 表 `songs`：更新 id `17`（Shout of Joy），设置 `cover_image_id = 3956`，`source_id = 2832`。
3. **数据导出与静态校验**：
   - 运行 `python3 db/export.py` 重新生成 `data/*.json`、`data/version.json` 及更新 HTML 资源版本。
   - 运行 `python3 db/export.py --check`，全部 7 个 JSON 文件（members、eras、lives、timeline、images、songs、version）及 8 个 HTML 文件检查全部通过，逐字节一致。
