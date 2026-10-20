# 017 任务结果：2020–2023 年演出配图补全

- 执行方：Antigravity
- 任务分支：`agy/017-images-2020-2023`
- 对应任务单：`docs/tasks/017-images-2020-2023.md`
- 最终状态：**待验收**

---

## 1. 总体成果概述

针对 016 审计剔除第三方（Eventernote）非官方配图后 2020–2023 年出现的封面缺失（共核对 233 场无封面场次），严格遵循规则，不使用任何第三方搬运网站或非主办同行团体推文，逐场检索官方推特（`@iLiFE_official`、主办方官方推特）、会场官方演出表（LIQUIDROOM、SHIBUYA DIVE、duo MUSIC EXCHANGE、白金高轮SELENE b2）、主办方合作官方机构（ダイキサウンド / Daiki Sound）、官方售票页面（TIGET、Rakuten Ticket）以及商业通告（PR TIMES）。

本次任务共**净增 41 场**官方配图（其中 **36 场新下载转换 WebP 官方配图**，**5 场复用已收录的官方日程海报或专属感谢合照**）。全部图片未经裁剪、保留原比例，最长边均缩放至 2048px 以内，文件大小均严格控制在 1MB 以内（平均 100~600KB）。数据变更仅修改 `db/ilife.sqlite` 并通过 `python3 db/export.py --rebuild-derived` 与 `python3 db/export.py --check`（100% 逐字节一致通过）。

### 年份推进与提交总览

| 年份 | 演出总场次 | 任务前覆盖 | **最终覆盖** | **覆盖率** | 净增场次 | 新增图片 | 复用旧图 | 对应提交哈希 |
|---|---|---|---|---|---|---|---|---|
| **2023 年** | 175 场 | 106 / 175 | **122 / 175** | **69.7%** | +16 场 | 16 张 | 0 场 | `98de3e5` |
| **2022 年** | 157 场 | 61 / 157 | **71 / 157** | **45.2%** | +10 场 | 8 张 | 2 场 | `e8f48f9` |
| **2021 年** | 95 场 | 48 / 95 | **59 / 95** | **62.1%** | +11 场 | 9 张 | 2 场 | `a4eb668` |
| **2020 年** | 45 场 | 24 / 45 | **28 / 45** | **62.2%** | +4 场 | 3 张 | 1 场 | `755f2b1` |
| **合计** | **472 场** | **239 / 472** | **280 / 472** | **59.3%** | **+41 场** | **36 张** | **5 场** | **4 次推进提交** |

---

## 2. 官方来源类型分布统计（本次新增 36 张图）

所有新图均真实可查，对应官方来源渠道分布如下：

1. **官方售票平台（TIGET / Rakuten Ticket）**：14 张
   - TIGET 官方活动页面：9 张（2023 年 4 场、2022 年 3 场、2021 年 2 场）
   - 乐天票务（Rakuten Ticket / r-t.jp）官方活动页面：5 张（2023 年 2 场、2022 年 3 场）
2. **主办合作官方机构（ダイキサウンド / Daiki Sound）**：3 张
   - Daiki Sound 官方活动资讯页（IDOL CONTENT EXPO 主办与联合企划）：3 张（2021 年 1 场、2020 年 2 场）
3. **会场官方日程与通告（LIQUIDROOM / SHIBUYA DIVE / duo MUSIC EXCHANGE / SELENE b2）**：4 张
   - 恵比寿LIQUIDROOM 官网活动表：1 张（2020 年 1 场）
   - SHIBUYA DIVE 官网活动表：2 张（2021 年 2 场）
   - 白金高轮SELENE b2 官网活动表：1 张（2021 年 1 场）
   - duo MUSIC EXCHANGE 官网活动表：1 张（2021 年 1 场）
4. **官方推特（X @iLiFE_official / @heroines_idol / 主办官方账号）**：14 张
   - `@iLiFE_official` 现场官方演出记录 / 告知：5 张（2023 年 4 场、2022 年 1 场）
   - `@heroines_idol` / 各音乐节主办官方 X：9 张（2023 年 9 场）
5. **官方新闻稿（PR TIMES）**：1 张
   - PR TIMES 官方商业通告：1 张（2022 年 1 场）

---

## 3. 本次补全场次明细清单（41 场）

### 2023 年（16 场新图，Commit: `98de3e5`）
1. **Live 334 (2023-01-09)**: HYPE IDOL! Vol.30 @ 渋谷ストリーム ホール -> 来源: [Rakuten Ticket](https://r-t.jp/hypeidol-vol30) (`img/live-2023-334-035f8e5f.webp`)
2. **Live 377 (2023-04-09)**: HEROINES ViViD @ Spotify O-EAST -> 来源: [X @heroines_idol](https://x.com/heroines_idol/status/1643916298139889665) (`img/live-2023-377-a8412e84.webp`)
3. **Live 388 (2023-04-26)**: #2i2 PRODUCE 【64 ep.05】 @ 新宿BLAZE -> 来源: [X @iLiFE_official](https://x.com/iLiFE_official/status/1651203024508026880) (`img/live-2023-388-b2ef62b6.webp`)
4. **Live 393 (2023-05-04)**: HYPE IDOL! GW DX！ @ 山野ホール -> 来源: [Rakuten Ticket](https://r-t.jp/hypeidol-gwdx) (`img/live-2023-393-4bf64639.webp`)
5. **Live 394 (2023-05-06)**: 歌舞伎町UP GATE↑↑DAY1 @ Zepp Shinjuku -> 来源: [歌舞伎町UP GATE↑↑公式サイト](http://kabukicho-upgate.com/2023/index.html) (`img/live-2023-394-013fa0e9.webp`)
6. **Live 396 (2023-05-13)**: MAWA LOOP OSAKA 2023 (5/13) @ なんばHatch -> 来源: [X @mawa_loop](https://x.com/mawa_loop/status/1657335606627065857) (`img/live-2023-396-f9446d49.webp`)
7. **Live 400 (2023-05-21)**: 5/21(日) TOKYO GIRLS GIRLS @ 品川インターシティホール -> 来源: [TIGET](https://tiget.net/events/246416) (`img/live-2023-400-f5a044bc.webp`)
8. **Live 403 (2023-05-27)**: 【DAY1】手羽先セッションFESTIVAL @ Lives NAGOYA -> 来源: [X @iLiFE_official](https://x.com/iLiFE_official/status/1662444558503022592) (`img/live-2023-403-cbceee8c.webp`)
9. **Live 414 (2023-06-17)**: RAD JAM 2023 @ Aichi Sky Expo -> 来源: [X @RADJAM2020](https://x.com/RADJAM2020/status/1669641774028169216) (`img/live-2023-414-04beeaec.webp`)
10. **Live 433 (2023-07-30)**: TOKYO GIRLS GIRLS ~ 3rd Anniversary day2~ @ 品川インターシティホール -> 来源: [TIGET](https://tiget.net/events/258522) (`img/live-2023-433-2895689d.webp`)
11. **Live 442 (2023-08-16)**: ガラフェス〜鸣かない蝉〜 @ 日比谷野外大音楽堂 -> 来源: [TIGET](https://tiget.net/events/257321) (`img/live-2023-442-5dbce2b3.webp`)
12. **Live 464 (2023-10-18)**: ガールズ・ポップ・アンビシャス4MAN @ duo MUSIC EXCHANGE -> 来源: [X @iLiFE_official](https://x.com/iLiFE_official/status/1714603957866385642) (`img/live-2023-464-90be5c94.webp`)
13. **Live 465 (2023-10-19)**: HEROINES HALLOWEEN mini @ 新宿BLAZE -> 来源: [X @heroines_idol](https://x.com/heroines_idol/status/1714597379683619128) (`img/live-2023-465-4f052441.webp`)
14. **Live 467 (2023-10-24)**: MARQUEE Fes. -day1- @ Spotify O-EAST -> 来源: [X @MARQUEE_matsuri](https://x.com/MARQUEE_matsuri/status/1715699419268686129) (`img/live-2023-467-f4e9185a.webp`)
15. **Live 468 (2023-10-25)**: アイドル・アラモード Vol.15 @ KT Zepp Yokohama -> 来源: [TIGET](https://tiget.net/events/271708) (`img/live-2023-468-b7eb4623.webp`)
16. **Live 478 (2023-11-20)**: 【DAY1】豆柴の大群の道玄坂パーティー 2DAYS @ duo MUSIC EXCHANGE -> 来源: [X @iLiFE_official](https://x.com/iLiFE_official/status/1726569106063990868) (`img/live-2023-478-f7396fe7.webp`)

### 2022 年（8 场新图 + 2 场复用，Commit: `e8f48f9`）
1. **Live 174 (2022-01-09)**: IDOL CONTENT EXPO ＠ ヒューリックホール東京～年明け3DAYS SPライブ!!!～【DAY2】 -> 来源: [TIGET](https://tiget.net/events/161278) (`img/live-2022-174-884382bf.webp`)
2. **Live 212 (2022-04-30)**: HYPE IDOL! GWSP DAY2 @ 山野ホール -> 来源: [Rakuten Ticket](https://r-t.jp/hypeidol-gwsp) (`img/live-2022-212-be206ee8.webp`)
3. **Live 214 (2022-05-03)**: HYPE IDOL! GWDX【DAY1】 @ NEW PIER HALL -> 来源: [Rakuten Ticket](https://r-t.jp/hypeidol-gwdxd1) (`img/live-2022-214-411ea999.webp`)
4. **Live 215 (2022-05-04)**: 【出演者変更】HYPE IDOL! GWDX【DAY2】 @ NEW PIER HALL -> 来源: [Rakuten Ticket](https://r-t.jp/hypeidol-gwdxd2) (`img/live-2022-215-6db2e646.webp`)
5. **Live 225 (2022-05-31)**: JAPAN IDOL SUPER LIVE 2022 @豊洲PIT公演 春の大祭典編 @ 豊洲PIT -> 来源: [TIGET](https://tiget.net/events/182607) (`img/live-2022-225-b4aa0fe0.webp`)
6. **Live 243 (2022-07-12)**: JAPAN IDOL SUPER LIVE 2022 @豊洲PIT公演 夏の大祭典編 @ 豊洲PIT -> 来源: [TIGET](https://tiget.net/events/189709) (`img/live-2022-243-ea7c9803.webp`)
7. **Live 289 (2022-10-27)**: ツンデレフェス Vol.1 〜新宿テディベア パレード〜 supported by Amilige @ 都内各所 -> 来源: [PR TIMES](https://prtimes.jp/main/html/rd/p/000000007.000085732.html) (`img/live-2022-289-4bba6c7d.webp`)
8. **Live 293 (2022-10-31)**: HEROINES HELLOWEEN東京公演 @ 恵比寿LIQUIDROOM -> 来源: [X @iLiFE_official](https://x.com/iLiFE_official/status/1585642944320921600) (`img/live-2022-293-27eb874d.webp`)
9. **Live 296 (2022-11-09)**: iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 11/9 @ タワーレコード渋谷店 -> 来源: [官方巡回日程图](https://x.com/iLiFE_official/status/1589574483785830400) (`img/cd-release-tour-2022.webp (复用 Image 705)`)
10. **Live 302 (2022-11-16)**: iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 11/16 @ タワーレコード渋谷店 -> 来源: [官方巡回日程图](https://x.com/iLiFE_official/status/1589574483785830400) (`img/cd-release-tour-2022.webp (复用 Image 705)`)

### 2021 年（9 场新图 + 2 场复用，Commit: `a4eb668`）
1. **Live 103 (2021-05-26)**: HEROINES MEETING 1部mini LIVE @ 白金高輪SELENE b2 -> 来源: [TIGET](https://tiget.net/events/131912) (`img/live-2021-103-112af4fb.webp`)
2. **Live 109 (2021-06-13)**: ッスッゴイライブ 2021.6.13 @ 大手町三井ホール -> 来源: [官方6月日程海报](https://twitter.com/iLiFE_official/status/1398971936353349633) (`img/schedule-2021-06.webp (复用 Image 140)`)
3. **Live 110 (2021-06-19)**: かみやど主催 ROAD TO KT Zepp Yokohama supported byダイキサウンド @ 新宿住友ホール -> 来源: [ダイキサウンド公式サイト](https://www.daiki-sound.jp/news/14758/) (`img/live-2021-110-bb7d2245.webp`)
4. **Live 114 (2021-07-01)**: Summer Typhoon Festival (2021/07/01) @ 新宿ReNY -> 来源: [官方7月前半日程海报](https://twitter.com/iLiFE_official/status/1410189032647184384) (`img/schedule-2021-07-a.webp (复用 Image 166)`)
5. **Live 129 (2021-08-11)**: 【出演者変更】IDOL CONTENT EXPO @TSUTAYA O-EAST ～まだまだ夏休み真っ只中～ -> 来源: [TIGET](https://tiget.net/events/142686) (`img/live-2021-129-1619df89.webp`)
6. **Live 138 (2021-09-12)**: 水瀬ぴあの生誕祭 PIF（Piano Idol Festival） @ duo MUSIC EXCHANGE -> 来源: [duo MUSIC EXCHANGE公式サイト](http://www.duomusicexchange.com/schedule/2021/09/index.html) (`img/live-2021-138-dba3d49d.webp`)
7. **Live 139 (2021-09-13)**: Fabulous Night メイビーME主催ライブ @ 白金高輪SELENE b2 -> 来源: [白金高輪SELENE b2公式サイト](https://selene.studio/hall/schedule/events/index.html?r=1629612480.31693900) (`img/live-2021-139-18023e18.webp`)
8. **Live 145 (2021-10-01)**: 永月十華生誕祭「誕生日おめでとうか！」 @ SHIBUYA DIVE -> 来源: [SHIBUYA DIVE公式サイト](https://shibuya-dive.com/schedule/date/2021-10-01/) (`img/live-2021-145-4faaab6f.webp`)
9. **Live 146 (2021-10-09)**: 『 IDOL CONTENT EXPO @ 品川インターシティホール supported byダイキサウンド 』DAY1 -> 来源: [ダイキサウンド公式サイト](https://www.daiki-sound.jp/news/15806/) (`img/live-2021-146-dfd27319.webp`)
10. **Live 149 (2021-10-17)**: 『 IDOL CONTENT EXPO @品川ザ・グランドホール ～あわてんぼうのハロウィンLIVE!!!～ 』 -> 来源: [TIGET](https://tiget.net/events/151075) (`img/live-2021-149-89981c45.webp`)
11. **Live 157 (2021-11-08)**: よるあみ主催「４MAN LIVE 無銭」 @ SHIBUYA DIVE -> 来源: [SHIBUYA DIVE公式サイト](https://shibuya-dive.com/schedule/2021-11-08/) (`img/live-2021-157-b4b585d6.webp`)

### 2020 年（3 场新图 + 1 场复用，Commit: `755f2b1`）
1. **Live 55 (2020-10-17)**: IDOL CONTENT EXPO @ 品川インターシティホール supported byダイキサウンド ～幕張じゃないよ！帰ってきた、品川で大集合SP!!!～【DAY1】 -> 来源: [ダイキサウンド公式サイト](https://www.daiki-sound.jp/news/4175/) (`img/live-2020-55-8dc3a004.webp`)
2. **Live 56 (2020-10-25)**: iLiFE! presents「come to life.」 @ 恵比寿LIQUIDROOM -> 来源: [LIQUIDROOM公式サイト](https://www.liquidroom.net/schedule/ilife20201025) (`img/live-2020-56-45437fcc.webp`)
3. **Live 62 (2020-11-11)**: IDOL CONTENT EXPO @ 神田明神ホール Vol.10 ～ポッキー＆プリッツの日SP!!!～ -> 来源: [官方演后专属合照](https://x.com/iLiFE_official/status/1326508930768396288) (`img/live-2020-62-costume.webp (复用 Image 47)`)
4. **Live 77 (2020-12-27)**: IDOL CONTENT EXPO @ 品川インターシティホール supported byダイキサウンド ～やっぱりまだダメだった幕張！年納めは品川で大集合～ DAY1 -> 来源: [ダイキサウンド公式サイト](https://www.daiki-sound.jp/news/7175/) (`img/live-2020-77-7c456fde.webp`)

---

## 4. 未配图场次清单及原因说明

### 2023 年未配图场次清单（共 53 场）

| ID | 日期 | 演出标题 | 会场 | 原出处链接 | 未配图原因说明 |
|---|---|---|---|---|---|
| 329 | 2023-01-03 | TOKYO IDOL PROJECT × @JAM ニューイヤープレミアムパーティー2023【3日(火)】 | お台場・青海特設会場 | https://www.eventernote.com/events/326589 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 338 | 2023-01-14 | うるトラすフェスタ vol.11＠ヒューリックホール東京 | ヒューリックホール東京 | https://www.eventernote.com/events/328990 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 339 | 2023-01-15 | 名古屋・来世邂逅物語 | Lives NAGOYA | https://www.eventernote.com/events/330710 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 341 | 2023-01-17 | 【出演者変更】STRIPE【O-EAST】 | Spotify O-EAST | https://www.eventernote.com/events/331072 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 352 | 2023-02-20 | ZUTTOMOTTO DEBUT 4MAN LIVE | CLUB CITTA' | https://www.eventernote.com/events/334057 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 354 | 2023-02-23 | New Generations!! Vol.8 ~Premium~ | 室町三井ホール&カンファレンス | https://www.eventernote.com/events/333724 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 356 | 2023-02-26 | ッスッゴイライブ (2023/02/26) | KT Zepp Yokohama | https://www.eventernote.com/events/333682 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 367 | 2023-03-22 | ワンダーウィード 天 白川ゆめか生誕祭 (3/22) | 新宿BLAZE | https://www.eventernote.com/events/337078 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 380 | 2023-04-14 | アイドル甲子園 PREMIUM in 新宿BLAZE（2023/4/14） | 新宿BLAZE | https://www.eventernote.com/events/336752 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 381 | 2023-04-15 | drown in your night OSAKA Vol.2 | 梅田CLUB QUATTRO | https://www.livefans.jp/events/1526886 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 382 | 2023-04-16 | NEO JAPONISM 主催公演 「合戦 KASSEN」 | Spotify O-EAST | https://www.eventernote.com/events/338417 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 384 | 2023-04-17 | ちゅらまちゅり (2023/04/17) | 渋谷WWW X | https://www.eventernote.com/events/334427 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 390 | 2023-04-29 | HEROINES FES in 肉フェス®︎ Supported by New Generations!! | お台場・青海特設会場 | https://www.eventernote.com/events/338840 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 391 | 2023-04-30 | RAD LIVE × Be Rise Lab presents「RAD JAM EXTREM -Be Rise Edition-」 | Zepp DiverCity (TOKYO) | https://www.eventernote.com/events/336722 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 399 | 2023-05-19 | アキシブproject無銭乱舞-2MAN TOUR- (2023/05/19) | Spotify O-WEST | https://www.eventernote.com/events/342641 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 404 | 2023-05-28 | 【DAY2】手羽先セッションFESTIVAL～Supported by アイドルアラモード（2023/5/28） | Maker's Pier | https://www.eventernote.com/events/344033 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 408 | 2023-06-03 | ANCHOR主催音楽フェス #ANFES | KT Zepp Yokohama | https://twitter.com/a_idolproject/status/1659891820325924864 | 仅非主办同行团体推文或正文无专属配图，按规则不予采用 |
| 413 | 2023-06-16 | IDOL CONTENT EXPO ＠ヒューリックホール東京～Premium Live!!!～ | ヒューリックホール東京 | https://www.eventernote.com/events/344459 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 415 | 2023-06-20 | シンデレラ宣言!Zepp目前 SP LIVE『超・シンデレラ PARTY!』Vol.2 | Spotify O-WEST | https://www.livefans.jp/events/1554391 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 416 | 2023-06-22 | 【出演者変更】ちゅらまちゅり (2023/06/22) | Spotify O-EAST | https://www.eventernote.com/events/342125 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 417 | 2023-06-24 | GIGA・GIGA SONIC ~Road to 幕張メッセ vol.2~ | ヒューリックホール東京 | https://www.eventernote.com/events/343733 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 421 | 2023-07-04 | 特区2023 | 新宿BLAZE | https://www.eventernote.com/events/345657 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 422 | 2023-07-07 | 渋谷大納涼祭 2023 | Spotify O-WEST | https://www.eventernote.com/events/346724 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 423 | 2023-07-08 | 「IDOL GALAXY」supported by テレビ愛知【DAY1】 | Maker's Pier | https://www.eventernote.com/events/343711 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 428 | 2023-07-17 | IDOL SQUARE Summer Festival 2023 | KT Zepp Yokohama | https://www.eventernote.com/events/343723 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 429 | 2023-07-22 | SEKIGAHARA IDOL WARS 2023〜関ケ原唄姫合戦〜 2日目 | 桃配運動公園(関ヶ原町) | https://www.eventernote.com/events/346270 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 430 | 2023-07-23 | SEKIGAHARA IDOL WARS 2023〜関ケ原唄姫合戦〜 3日目 | 桃配運動公園(関ヶ原町) | https://www.eventernote.com/events/346273 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 432 | 2023-07-29 | 六本木アイドルフェスティバル2023［DAY-1］ | 六本木ヒルズアリーナ | https://www.eventernote.com/events/344510 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 438 | 2023-08-11 | New Generations!! - 真夏の超・Premium Circuit - Day1 | Maker's Pier | https://www.eventernote.com/events/348286 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 440 | 2023-08-15 | ジャムズセッション!!-真夏のプレミアム- | KT Zepp Yokohama | https://www.eventernote.com/events/349284 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 443 | 2023-08-19 | UP-T presents かがやきフェス2023【8/19】 | 石川県内各所（サーキット） | https://www.eventernote.com/events/341341 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 448 | 2023-09-09 | OPC Fes. -Q&..Q!?- | GARDEN 新木場 FACTORY | https://www.eventernote.com/events/352351 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 449 | 2023-09-10 | IDOL☆STAR vol.1 | KT Zepp Yokohama | https://www.eventernote.com/events/353745 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 451 | 2023-09-14 | MARQUEE Fes. day2 | Spotify O-EAST | https://www.eventernote.com/events/351818 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 452 | 2023-09-15 | 日テレプラス秋のアイドル祭り Supported by U-ZONE | Spotify O-EAST | https://www.eventernote.com/events/354232 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 454 | 2023-09-23 | バンドじゃないもん！MAXX NAKAYOSHI主催「NAKAYOSHI FES.2023」 | 東京都内各所（サーキット） | https://www.eventernote.com/events/347246 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 459 | 2023-10-07 | GIGA・GIGA SONIC ~ 2周年大感謝祭SPECIAL in 幕張メッセ~ presented by ドラゴンエッグ | 幕張メッセ 国際展示場ホール | https://www.eventernote.com/events/352126 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 460 | 2023-10-08 | あいふぇす vol.1 | Zepp Namba (OSAKA) | https://www.eventernote.com/events/353418 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 461 | 2023-10-09 | DERARALiFE! | NAGOYA ReNY limited | https://www.eventernote.com/events/356916 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 463 | 2023-10-14 | TOKOROLiFE! | ところざわサクラタウン ジャパンパビリオン ホールA | https://www.eventernote.com/events/357664 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 466 | 2023-10-29 | Appare! HALLOWEEN 2023 DAY2 10/29 | GARDEN 新木場 FACTORY | https://www.eventernote.com/events/355561 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 470 | 2023-11-09 | 罪フェスvol.3 | duo MUSIC EXCHANGE | https://www.livefans.jp/events/1610756 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 474 | 2023-11-17 | YANFES2023 | KANDA SQUARE HALL | https://www.eventernote.com/events/360830 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 475 | 2023-11-18 | かすみ草とステラ主催公演『むれなでしこ -群撫子- vol.8』 | スタァライト劇場 | https://www.eventernote.com/events/358743 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 477 | 2023-11-19 | SPA!フェス35 | 東京都内各所（サーキット） | https://www.eventernote.com/events/358353 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 479 | 2023-11-23 | DERARALiFE!Vol.2 | Zephyr Hall | https://www.livefans.jp/events/2012731 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 483 | 2023-12-01 | HEROINES FES Vol.10 | CLUB CITTA' | https://www.eventernote.com/events/362215 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 484 | 2023-12-04 | アンスぱーくっ！！！！！！in Spotify O-EAST 12/4 | Spotify O-EAST | https://www.eventernote.com/events/357587 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 485 | 2023-12-05 | dot yell fes WINTER SP | ヒューリックホール東京 | https://www.eventernote.com/events/362801 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 487 | 2023-12-10 | ッスッゴイライブ〜5th anniversary SP LIVE〜 | 品川プリンスホテル ステラボール | https://www.eventernote.com/events/360313 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 488 | 2023-12-11 | ちゅらまちゅり〜サーキット編〜　2023/12/11 | 東京都内各所（サーキット） | https://www.eventernote.com/events/362738 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 489 | 2023-12-14 | NEO JAPONISMデビュー4周年イベント "NEO START" | Spotify O-EAST | https://www.eventernote.com/events/358625 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 495 | 2023-12-24 | NEO JAPONISM presents NEO X'mas PARTY | GARDEN 新木場 FACTORY | https://www.eventernote.com/events/359881 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |


### 2022 年未配图场次清单（共 86 场）

| ID | 日期 | 演出标题 | 会场 | 原出处链接 | 未配图原因说明 |
|---|---|---|---|---|---|
| 173 | 2022-01-08 | HYPE IDOL！EX | 横浜LANDMARK HALL | https://www.eventernote.com/events/296241 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 175 | 2022-01-15 | HYPE IDOL！vol.8 | 品川インターシティホール | https://www.eventernote.com/events/295579 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 177 | 2022-01-23 | HYPE IDOL!vol.10 | THE GRAND HALL | https://www.livefans.jp/events/1379499 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 178 | 2022-01-26 | 【出演者変更】JAPAN IDOL SUPER LIVE 2022 @Zepp Haneda編 1/26 | Zepp Haneda | https://www.eventernote.com/events/297090 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 179 | 2022-01-29 | 【出演者変更】IDOL CONTENT EXPO @ 品川インターシティホール supported byダイキサウンド ～桜が咲く頃には幕張へ！今回は品川で大集合SP!!!～【DAY1】 | 品川インターシティホール | https://www.eventernote.com/events/297822 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 180 | 2022-02-02 | 【出演者変更】ツインテールフェス 2022 | duo MUSIC EXCHANGE | https://www.livefans.jp/events/1380695 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 181 | 2022-02-05 | 【出演者変更】IDOL CONTENT EXPO ＠ 2会場連動企画 ニコッ！笑う門には福来るッ！ | Spotify O-EAST | https://www.livefans.jp/events/1381476 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 183 | 2022-02-11 | 【出演者変更】IDOL CONTENT EXPO ＠品川ザ・グランドホール ～バレンタインSP LIVE!!!～ | THE GRAND HALL | https://www.eventernote.com/events/299903 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 184 | 2022-02-13 | HEROINES VALENTINE'S | 1000 CLUB | https://www.livefans.jp/events/1380356 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 185 | 2022-02-16 | 【出演者変更】NeoMasQueRade (2022/02/16) | 新宿BLAZE | https://www.eventernote.com/events/300046 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 187 | 2022-02-20 | melomelo (2022/2/20) (DAY・NIGHT) | 味園ユニバース | https://www.eventernote.com/events/298225 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 189 | 2022-02-26 | ロマンチックコンポート！！！！ | 白金高輪SELENE b2 | https://www.eventernote.com/events/299284 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 190 | 2022-03-02 | 【出演者変更】10祭~TENSAI~ | 新宿BLAZE | https://www.eventernote.com/events/300180 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 191 | 2022-03-06 | MAGNETIC FESTIVAL in 大手町三井ホール　ひな祭りスペシャル　DAY2 | 大手町三井ホール | https://www.eventernote.com/events/301920 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 193 | 2022-03-10 | 【出演者変更】なんキニ！presents live! 『キニなるフェス！会場拡大SP！』supported by IDOL CONTENT EXPO | Spotify O-EAST | https://www.eventernote.com/events/301881 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 194 | 2022-03-12 | 【出演者変更】IDORISE!! FESTIVAL 2022【DAY1】 | duo MUSIC EXCHANGE | https://www.livefans.jp/events/1393930 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 195 | 2022-03-13 | GoTo BLAZE〜NIGHT〜 (2022/03/13) | 新宿BLAZE | https://www.eventernote.com/events/302002 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 196 | 2022-03-15 | HEROINES WHITEDAY | Veats SHIBUYA | https://www.eventernote.com/events/301700 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 197 | 2022-03-17 | MARQUEE祭 Vol.114 | Spotify O-WEST | https://www.eventernote.com/events/300568 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 198 | 2022-03-19 | LEADING!!!（2022/03/19） | duo MUSIC EXCHANGE | https://www.eventernote.com/events/302785 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 199 | 2022-03-20 | エキセントリックオッドー 2022/03/20 | 代官山SPACE ODD | https://www.eventernote.com/events/302533 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 200 | 2022-03-22 | TYAO！vol.2 | 新宿BLAZE | https://www.eventernote.com/events/302036 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 201 | 2022-03-27 | HYPE IDOL！vol.15 | THE GRAND HALL | https://www.livefans.jp/events/1401603 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 202 | 2022-04-03 | dot yell fes 1周年sp | ところざわサクラタウン ジャパンパビリオン ホールA | https://www.livefans.jp/events/1399412 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 203 | 2022-04-11 | 〇〇しか勝たんフェス in spotify O-EAST | Spotify O-EAST | https://www.eventernote.com/events/303224 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 204 | 2022-04-12 | LEADING ID -Birthday Special- 2022/04/12 | Spotify O-WEST | https://www.livefans.jp/events/1400134 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 207 | 2022-04-15 | AION CINDERELLA -DX- | 神奈川県民ホール 大ホール | https://www.eventernote.com/events/299702 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 208 | 2022-04-15 | 偶像和音 | 新宿BLAZE | https://www.eventernote.com/events/304181 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 210 | 2022-04-27 | Girls & Night!!(2022/04/27) | duo MUSIC EXCHANGE | https://www.livefans.jp/events/1395312 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 211 | 2022-04-28 | NEW HEROINES LIFE ~新生活応援キャンペーン~ | 新宿BLAZE | https://www.eventernote.com/events/304604 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 213 | 2022-05-02 | !i!i!FES #あいふぇす 2022/5/2 | 新宿BLAZE | https://www.eventernote.com/events/305319 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 217 | 2022-05-16 | 【5/16】四季折々 ~SPECIAL~ VOL.1 ＠ Spotify O-West | Spotify O-WEST | https://www.eventernote.com/events/304871 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 218 | 2022-05-17 | 5/17 MARQUEE Fes.（Day1） | Spotify O-EAST | https://www.livefans.jp/events/1420230 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 219 | 2022-05-21 | 5/21(土) POP IN FESTIVAL 2022 ~ #PIF2022 ~ | Alternative Theatre | https://www.eventernote.com/events/308385 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 220 | 2022-05-21 | マイマイエッタイガー！ | 渋谷近未来会館 | https://www.eventernote.com/events/308387 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 221 | 2022-05-22 | HYPE IDOL!vol.17 | 大手町三井ホール | https://www.eventernote.com/events/306202 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 222 | 2022-05-27 | HEROINES Party | 白金高輪SELENE b2 | https://www.eventernote.com/events/308374 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 223 | 2022-05-28 | アイドル道場〜品川グランドホール〜 vol.2 | THE GRAND HALL | https://www.eventernote.com/events/307536 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 224 | 2022-05-30 | Queen&Princess vol.2 2022/5/30 | Veats SHIBUYA | https://www.eventernote.com/events/307682 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 226 | 2022-06-02 | HEROINES FES | CLUB CITTA' | https://www.eventernote.com/events/308375 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 229 | 2022-06-12 | HYPE IDOL！vol.20 | 日本橋三井ホール | https://www.eventernote.com/events/309347 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 230 | 2022-06-15 | 偶像和音 6/15 | 新宿BLAZE | https://www.eventernote.com/events/310416 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 231 | 2022-06-16 | MARQUEE祭 Vol.117 | Spotify O-WEST | https://www.eventernote.com/events/310057 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 232 | 2022-06-18 | rock field ULTRA LIVE | KANDA SQUARE HALL | https://www.livefans.jp/events/1430941 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 233 | 2022-06-24 | 『 IDOL CONTENT EXPO ＠ O-EAST ～アイコン生誕10周年祭～ 』 | Spotify O-EAST | https://www.eventernote.com/events/312251 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 234 | 2022-06-25 | 2022/6/25 TOKYO GIRLS GIRLS -番外編- | 横浜LANDMARK HALL | https://www.eventernote.com/events/311195 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 235 | 2022-06-26 | Liven up IDOL 06.26 | 品川インターシティホール | https://www.eventernote.com/events/311055 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 236 | 2022-06-30 | JAPAN IDOL SUPER LIVE 2022 @ヒューリックホール東京PREMIUM公演編 | ヒューリックホール東京 | https://www.eventernote.com/events/309445 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 237 | 2022-07-02 | HEROINESの夏開き 2022/7/2 | 原宿スペース | https://www.eventernote.com/events/311264 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 239 | 2022-07-07 | 【出演者変更】渋谷大納涼祭 2022 | Spotify O-WEST | https://www.eventernote.com/events/310779 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 240 | 2022-07-09 | NAGOYA IDOL SUMMIT day1 | 名港スプラッシュガーデン ライオンドーム | https://www.eventernote.com/events/312578 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 241 | 2022-07-10 | 【出演者変更あり】NAGOYA IDOL SUMMIT day2 | 名港スプラッシュガーデン ライオンドーム | https://www.eventernote.com/events/312971 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 242 | 2022-07-11 | 【出演者変更】Merry BAD TUNE. presents 「#バチュコリvol.0-バチュンお披露目初主催対バンSP-」 2022/7/11 | 渋谷SOUND MUSEUM VISION | https://www.eventernote.com/events/311355 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 244 | 2022-07-18 | 【出演者変更】SPARK 2022 in YAMANAKAKO【7/18】 | 山中湖交流プラザきらら | https://www.eventernote.com/events/308782 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 246 | 2022-07-28 | HEROINES VOICE 2022/7/28 | 渋谷SOUND MUSEUM VISION | https://www.eventernote.com/events/311430 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 247 | 2022-07-29 | 7/29(金) Free Free Free | SHINJUKU WALLY | https://www.eventernote.com/events/314541 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 248 | 2022-07-31 | ももクロ夏のバカ騒ぎ2022 -MOMOFEST- 外周パーク「MOCK IN JAPAN2022」 | ベルーナドーム横レッドパーキング特設会場 | https://www.livefans.jp/events/1456573 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 250 | 2022-08-03 | 喰らいマックスに捧げる＿。 AZfes Premium | duo MUSIC EXCHANGE | https://www.eventernote.com/events/315174 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 252 | 2022-08-08 | 緊急開催!!!真夏のきゅるきゅるぱーりー!!! | 渋谷SOUND MUSEUM VISION | https://www.eventernote.com/events/315509 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 253 | 2022-08-14 | HEROINES SUMMER FES | CLUB CITTA' | https://www.eventernote.com/events/315188 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 254 | 2022-08-16 | 【出演者変更】dot yell fes SUMMER SP | Spotify O-EAST | https://www.eventernote.com/events/314923 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 255 | 2022-08-18 | MARQUEE祭 Vol.119 | Spotify O-WEST | https://www.eventernote.com/events/314922 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 257 | 2022-08-21 | DDD~Discovery iDol Depot~ (2022/08/21) | 白金高輪SELENE b2 | https://www.eventernote.com/events/315519 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 263 | 2022-09-01 | Vega Fes | duo MUSIC EXCHANGE | https://www.eventernote.com/events/315576 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 264 | 2022-09-02 | Bomaye! 1番罪な女はだーれだ!? | Veats SHIBUYA | https://www.eventernote.com/events/317117 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 265 | 2022-09-03 | GIRLS☆DELIGHT#136 | 神田明神ホール | https://www.eventernote.com/events/316815 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 270 | 2022-09-15 | HEROINES PARTY vol.3.5 | Veats SHIBUYA | https://www.eventernote.com/events/319310 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 280 | 2022-10-02 | 10/2(日) TOKYO GIRLS GIRLS ~ 番外編 ~ | 横浜LANDMARK HALL | https://www.eventernote.com/events/317478 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 281 | 2022-10-06 | MARQUEE祭 Vol.121 | Spotify O-WEST | https://www.eventernote.com/events/319652 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 282 | 2022-10-09 | HYPE IDOL！vol.25【9日(日)】 | よみうりランド 日テレらんらんホール | https://www.eventernote.com/events/318930 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 285 | 2022-10-19 | 煌めき☆アンフォレント 達家真姫宝生誕公演 | Spotify O-EAST | https://www.eventernote.com/events/319648 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 287 | 2022-10-23 | Liven up IDOL Vol.2 | 恵比寿ザ・ガーデンルーム | https://www.eventernote.com/events/321752 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 290 | 2022-10-28 | HEROINES HELLOWEEN 大阪公演 | umeda TRAD | https://www.eventernote.com/events/323545 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 291 | 2022-10-29 | HEROINES HELLOWEEN 名古屋公演 | NAGOYA ReNY limited | https://www.eventernote.com/events/322420 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 299 | 2022-11-13 | HEROINES FES vol.7 | CLUB CITTA' | https://www.eventernote.com/events/323895 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 304 | 2022-11-19 | ツンデレフェス Vol.2 〜横濱パンパンにしチャイナ〜 | 横浜LANDMARK HALL | https://www.eventernote.com/events/324674 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 305 | 2022-11-20 | ARTIST TRY IDOL FESTIVAL 2022 | メルパルクホール大阪 | https://www.eventernote.com/events/319865 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 307 | 2022-11-23 | New Generations!! Vol.3 ~Premium~ Presented by AZfes | 北とぴあ2F さくらホール | https://www.eventernote.com/events/324391 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 309 | 2022-11-27 | コマフェス！！～ご当地鍋フェスティバル＠日比谷公園～ | 日比谷公園小音楽堂 | https://www.eventernote.com/events/325039 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 310 | 2022-11-30 | HEROINES FES × ReNY SUPER LIVE ～CARNIVAL NIGHT 公演編～ | 新宿ReNY | https://www.eventernote.com/events/325226 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 311 | 2022-12-02 | HYPEIDOL！DX！(2022/12/02) | 新宿BLAZE | https://www.eventernote.com/events/326259 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 316 | 2022-12-11 | @JAM PARTY vol.79 (1部・2部) | 横浜みなとみらいブロンテ | https://www.eventernote.com/events/326382 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 318 | 2022-12-13 | iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 12/13 | タワーレコード渋谷店B1F CUTUP STUDIO | https://www.eventernote.com/events/327944 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 322 | 2022-12-24 | HEROINES CHRISTMAS | 恵比寿ザ・ガーデンホール | https://www.eventernote.com/events/328114 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 324 | 2022-12-25 | Appare!クリスマス2022 | 室町三井ホール&カンファレンス | https://www.eventernote.com/events/326685 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 327 | 2022-12-31 | IDOL NEW YEARS LIVE HEROINES COUNTDOWN (1部・2部) | 豊洲PIT | https://www.eventernote.com/events/328831 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |


### 2021 年未配图场次清单（共 36 场）

| ID | 日期 | 演出标题 | 会场 | 原出处链接 | 未配图原因说明 |
|---|---|---|---|---|---|
| 85 | 2021-02-02 | ハープスター×iLiFE! 無銭2マン | Zirco Tokyo | https://www.eventernote.com/events/270398 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 92 | 2021-03-27 | ッスッゴイライブ 2021.3.27 | THE GRAND HALL | https://www.eventernote.com/events/274383 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 93 | 2021-04-01 | IDOL CONTENT EXPO ＠新宿３会場サーキット ～今日は休日！？エイプリルフール祭～ | 東京都内各所（サーキット） | https://www.eventernote.com/events/274766 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 94 | 2021-04-03 | dot yell fes vol.3 | 原宿ベルエポック美容専門学校 第2校舎 | https://www.eventernote.com/events/274508 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 96 | 2021-04-10 | MARQUEE祭mini Vol.75 | TSUTAYA O-nest | https://www.eventernote.com/events/274091 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 97 | 2021-05-03 | 2021/5/3(月祝) 『idol up』東京キネマ倶楽部 | 東京キネマ倶楽部 | https://www.eventernote.com/events/276810 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 98 | 2021-05-05 | HYPE IDOL! FESTIVAL!! | オンライン配信 | https://www.livefans.jp/events/1314284 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 102 | 2021-05-23 | パラディーク主催公演 パラディークランドEX | WOMBLIVE | https://www.eventernote.com/events/278197 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 104 | 2021-05-29 | エキセントリックトーキョー (2021/05/29) | THE GRAND HALL | https://www.eventernote.com/events/277835 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 111 | 2021-06-20 | なんかいちむ | 新宿BLAZE | https://www.livefans.jp/events/1321049 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 115 | 2021-07-03 | CHALLENGE!!（二部） | 赤羽ReNY alpha | https://x.com/PrifanOfficial/status/1410222056822632451 | 仅非主办同行团体推文或正文无专属配图，按规则不予采用 |
| 116 | 2021-07-06 | IDOL CONTENT EXPO @ 新宿BLAZE ～七夕前夜祭～ | 新宿BLAZE | https://www.eventernote.com/events/281661 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 118 | 2021-07-11 | IDOL CIRCUS TOKYO | 神田明神文化交流館 EDOCCO STUDIO | https://x.com/PrifanOfficial/status/1410845929976918023 | 仅非主办同行团体推文或正文无专属配图，按规则不予采用 |
| 124 | 2021-07-23 | HEROINES FES vol.2 | Zepp Tokyo | https://tokyogirlsstyle.jp/live/detail.php?id=1090154 | 活动辞退/取消（因疫情活动自肃或成员身体原因辞退） |
| 125 | 2021-07-25 | 真夏のShining Days【iLiFE!×Non¬Fiction】トーク&ゲーム会 (1部・2部) | 白金高輪SELENE b2 | https://www.eventernote.com/events/282533 | 活动辞退/取消（因疫情活动自肃或成员身体原因辞退） |
| 127 | 2021-08-01 | 【出演者変更】IDOL CONTENT EXPO @ 品川インターシティホール supported byダイキサウンド～まだ諦めきれない幕張!夏休みだよ品川で大集合SP!!!～【DAY2】 | 品川インターシティホール | https://x.com/ic_expo/status/1420274098681176074 | 活动辞退/取消（因疫情活动自肃或成员身体原因辞退） |
| 128 | 2021-08-07 | MARQUEE祭mini Vol.84 | TSUTAYA O-nest | https://www.livefans.jp/events/1340840 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 131 | 2021-08-15 | Aqua CRUISING LIVE!!! Day2～前編～ | 象の鼻桟橋(クルーズ発着含) | https://www.eventernote.com/events/284998 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 137 | 2021-09-03 | 天使にはなれないデビューLIVE | 新宿BLAZE | https://www.eventernote.com/events/285510 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 148 | 2021-10-11 | IDOL CONTENT EXPO @ 新宿BLAZE ～ウィンクの日LIVE!!!～ | 新宿BLAZE | https://www.livefans.jp/events/1350769 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 150 | 2021-10-17 | 10/17(日) TOKYO GIRLS GIRLS extra!! | 室町三井ホール&カンファレンス | https://www.eventernote.com/events/287959 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 151 | 2021-10-20 | BUZZ IDOL FES【バズ アイドル フェス】 | KT Zepp Yokohama | https://www.eventernote.com/events/288601 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 154 | 2021-10-31 | HEROINES HELLOWEEN | 新宿ReNY | https://lineblog.me/akishibuproject/archives/67317815.html | 经检索主办方官网与官方推特无公开专属配图 |
| 155 | 2021-11-02 | IDOL CONTENT EXPO @秋葉原ZEST ～湯井のん卒業記念！緊急3マンLIVE!!!～ | 秋葉原ZEST | https://www.eventernote.com/events/291273 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 156 | 2021-11-04 | MyDearDarlin’ presents live!『 I Love Darlin’supported by IDOL CONTENT EXPO 3ヶ月連続!!!新宿BLAZE SPECIAL LIVE!! 』【11月4日(木)】 | 新宿BLAZE | https://www.eventernote.com/events/288478 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 158 | 2021-11-13 | アナフェスよみうりランド【1部】 | よみうりランド 日テレらんらんホール | https://www.eventernote.com/events/292350 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 159 | 2021-11-20 | ANK FES | 愛知県内各所（ANK FES） | https://www.eventernote.com/events/291636 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 160 | 2021-12-01 | TENNOSHO in NAGOYA | NAGOYA ReNY limited | https://www.eventernote.com/events/292100 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 162 | 2021-12-04 | IDOL PARADISE！vol.03 | 山野ホール | https://www.eventernote.com/events/292766 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 163 | 2021-12-06 | Girls & Night!! | 東京都内各所（サーキット） | https://www.eventernote.com/events/292397 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 164 | 2021-12-07 | iPort Girls vol.6 | LIVE HALL aube shibuya | https://www.eventernote.com/events/294412 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 166 | 2021-12-21 | IDOL CONTENT EXPO ＠神田明神ホール まだクリスマスじゃないの？！あわてんぼうのサンタLIVE!!! | 神田明神ホール | https://www.eventernote.com/events/295838 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 167 | 2021-12-25 | 寂しンボフェス | Yokohama Bay Hall | https://lineblog.me/akishibuproject/archives/67318586.html | 经检索主办方官网与官方推特无公开专属配图 |
| 169 | 2021-12-26 | IDOL CONTENT EXPO ＠品川ザ・グランドホール ～クリスマス後夜祭LIVE!!!～ | THE GRAND HALL | https://www.eventernote.com/events/295607 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 170 | 2021-12-30 | IDOL NEW YEARS LIVE (2021/12/30) | 豊洲PIT | https://www.eventernote.com/events/295246 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 171 | 2021-12-31 | IDOL NEW YEARS LIVE (2021/12/31) (1部・2部) | 豊洲PIT | https://www.eventernote.com/events/295931 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |


### 2020 年未配图场次清单（共 17 场）

| ID | 日期 | 演出标题 | 会场 | 原出处链接 | 未配图原因说明 |
|---|---|---|---|---|---|
| 0 | 2020-06-27 | プレデビューLIVE（无观众） | 渋谷ストリームホール | https://ja.wikipedia.org/wiki/ILiFE! | 无观众预出道演出，无公开发布官方告知海报 |
| 40 | 2020-08-07 | IDOL CONTENT EXPO @ 神田明神ホール Vol.3 ～夏休みだよスペシャルLIVE!!!～ | 神田明神ホール | https://www.eventernote.com/events/256662 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 45 | 2020-08-28 | IDOL CONTENT EXPO @ 神田明神ホール Vol.5 ～夏休みラストスペシャルLIVE!!!～ | 神田明神ホール | https://www.eventernote.com/events/257902 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 47 | 2020-09-12 | IDOL CONTENT EXPO ＠ 神田明神ホール Vol.6 ～超緊急！休日アイドル大集合!!!～ 後編 | 神田明神ホール | https://www.eventernote.com/events/258969 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 49 | 2020-09-22 | Vega Fes 1部 | 新宿BLAZE | https://www.eventernote.com/events/259618 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 50 | 2020-09-27 | IDOL CONTENT EXPO ＠品川ザ・グランドホール 緊急！休日アイドル大集合!!! | THE GRAND HALL | https://www.eventernote.com/events/259888 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 52 | 2020-10-06 | Keystudio Presents IDOL Future LIVE Rize special supported by lopi lopi | 新宿アルタKeyStudio | https://www.eventernote.com/events/260708 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 58 | 2020-10-27 | MyDearDarlin' presents『 My dear Holloween 』Supported by IDOL CONTENT EXPO | 新宿BLAZE | https://ameblo.jp/mydear-darlin/entry-12632793440.html | 经检索主办方官网与官方推特无公开专属配图 |
| 60 | 2020-10-31 | 推しメンってどこっ！？~ハロウィンSP~ | TSUTAYA O-WEST | https://x.com/alma___official/status/1319911618000506880 | 仅非主办同行团体推文或正文无专属配图，按规则不予采用 |
| 61 | 2020-11-03 | ビジュアリズム Vol,1【1部】 | 白金高輪SELENE b2 | https://x.com/i/status/1322494277402853377 | 仅非主办同行团体推文或正文无专属配图，按规则不予采用 |
| 63 | 2020-11-14 | エキセントリックトーキョー 2020/11/14 昼公演 | THE GRAND HALL | https://www.eventernote.com/events/263798 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 66 | 2020-11-22 | IDOL CONTENT EXPO @ 新宿アルタ KeyStudio ～超緊急！アイドル大集合！～ | 新宿アルタKeyStudio | https://x.com/i/status/1330437114329063425 | 仅非主办同行团体推文或正文无专属配图，按规则不予采用 |
| 68 | 2020-11-25 | LIVE on your LIFE | 新宿BLAZE | https://www.eventernote.com/events/264940 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 70 | 2020-12-04 | IDOL CONTENT EXPO @神田明神ホール Vol.11 ～December First Live!!!～ | 神田明神ホール | https://www.eventernote.com/events/265889 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 73 | 2020-12-10 | 虹色の飛行少女定期ライブDX vol.15 | AKIBAカルチャーズ劇場 | https://www.eventernote.com/events/265637 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 74 | 2020-12-12 | 新アイドルイベント「I・N・G」2020/12/12 2部 | ダンスホール新世紀 | https://www.eventernote.com/events/266368 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |
| 76 | 2020-12-24 | IDOL CONTENT EXPO ＠品川ザ・グランドホール ～Special Christmas Night!!!～【DAY1】 | THE GRAND HALL | https://www.eventernote.com/events/267623 | 仅第三方票务索引，主办/官方推特无可考独立告知图或已注销 |


---

## 5. 验收自检清单

- [x] `python3 db/export.py --rebuild-derived` 与 `python3 db/export.py --check` 全部 100% 逐字节一致通过。
- [x] 数据仅修改 `db/ilife.sqlite`，未手改 `data/*.json`。
- [x] 新增图片全部转换成 webp，长边 $\le 2048$ px，文件大小 $\le 1$ MB，未做任何裁剪，严格保持原比例。
- [x] 每张图片均对应真实有效的官方或会场/票务出处，写入 `sources` 表并关联 `images`。
- [x] 未拼接、未猜测推文 ID 或第三方 URL，严格杜绝非官方来源与非主办同行团体推文。
- [x] 严格按 2023 → 2022 → 2021 → 2020 倒序逐年提交并推送到任务分支 `agy/017-images-2020-2023`，未推送 main，未执行部署。
