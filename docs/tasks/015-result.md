# 015 · 2023–2026 年演出核查结果

状态：待验收。已按 2023 → 2024 → 2025 → 2026 顺序完成、逐年提交并推送。

## 核查方法与边界

逐页打开 Eventernote 的 iLiFE! 专属列表及 LiveFans 的 iLiFE! 年度列表，提取真实链接，再逐个打开详情，读取活动自身的出演者、日期、标题、会场。第三方页面不以页脚的 iLiFE! 字样作为出演依据。官方 X 通过 FxTwitter 公共接口读取正文、作者与原图，告知图逐张人工查看；发帖时间从 post ID 换算为 JST。所有 HTTP 抓取均设置 20 秒超时，Git 推送另设进程超时。

官方告知、主办方和售票页面优先；仅能核实第三方详情的条目明确标记“仅非官方来源”。`015-audit/<年份>.json` 保留每条新增记录、主出处、字段核对摘要及补充出处，供抽查。发现的原始链接不等于可用出处；只有实际打开、核对过的页面才写入 sources。

同日同会场两部公演或多舞台演出合并为一条，保留各部原始标题、时间与出处。新会场先按名称及别名查重；新地址、容量没有直接核实则留空。成员出勤未查到可靠逐场资料，`live_members` 留空，不根据在籍区间推断。可选封面未新增。

官网 NEWS 共 25 条，逐页打开至 2023 年，2024 年新闻没有可补充的演出日程。官方 TimeTree 页面在本次匿名浏览时跳转登录；部分 LivePocket / eplus 页面拒绝访问或内容已下线。不能据此声称官方排期已全部覆盖。只补入可核实的记录，不将“予定”、电视播出、广告车、单独特典会或无出演证据的日期编成演出。

## 2023 年

新增 172 条；原有 3 条保留，合计 175 条。新增逐月场数：1 月 16、2 月 14、3 月 16、4 月 18、5 月 15、6 月 12、7 月 15、8 月 14、9 月 8、10 月 13、11 月 14、12 月 17。新增主出处：官方 X 30 条，官方售票/主办方 14 条，Eventernote 124 条，LiveFans 4 条。仅非官方来源共 128 条（逐场清单见文末）。新增 31 个会场，地址、容量均未填入未经核实的数值。

- 原库 ID 6（2023-09-25 新体制お披露目ライブ）的会场为“未确认”；已打开的官方告知 `https://x.com/iLiFE_official/status/1693564541244989649` 及 LiveFans `https://www.livefans.jp/events/1595281` 指向 Zepp DiverCity。按任务单要求不修改，也不重复新增。
- 同日同会场合并：1/13 リリイベ完走ありがとうLIVE、2/11 HEROINES VALENTINE IN OSAKA、3/8 甘音ゆあ生诞祭、9/16 GALLiFE! / GAOLiFE!、11/11 DOSANKO HYPE! / DOSANKO LiFE!。
- Eventernote 3/5 MARQUEE祭有两条重复登记；LiveFans 的同日多舞台登记与对应 Eventernote 记录去重。
- 未收录：2 月图中的若干“予定”；3/14 排期图只有生诞相关字样、未核实标题会场；8/27 浴衣チェキ会及 12/28 大特典会不作为演唱会；TIF 告知写 8/4–6，但只核实到 8/4、8/5 的 iLiFE! 演出，未凭活动举办区间补 8/6；@JAM 告知写 8/26–27，8/27 为浴衣特典会，未以泛称告知补舞台演出。

## 2024 年

新增 153 条；原有 3 条保留，合计 156 条。新增逐月场数：1 月 12、2 月 10、3 月 13、4 月 10、5 月 15、6 月 12、7 月 16、8 月 12、9 月 12、10 月 10、11 月 15、12 月 16。新增主出处：官方 X 34 条，官方售票/主办方 59 条，Eventernote 60 条；仅非官方来源 60 条。新增 26 个会场，地址、容量均留空。

- 新增春季 JAPANLiFE! 8 站、TRAVELiFE! 5 站与冬季 JAPANLiFE! 年内 9 站，逐一查看官方巡演告知图。金泽 11/4、冲绳 11/30、香川 12/22 为两处第三方列表均未覆盖的补录。冬季东京 FINAL 在 2025-01-08，留到下一年度处理。
- 11/25 的 Eventernote「HEROINES FES 〜新グループお披露目公演〜」与官方资料冲突：官方告知 `https://x.com/iLiFE_official/status/1854404204888310185`、售票页 `https://ticketdive.com/event/heroinesfes1126` 均为 11/26，采用 11/26，排除 11/25 线索。
- 2/10 原定「あいふぇす」取消，官方说明改为 HEROINES VALENTINE OSAKA；取消情况附在当天记录，不虚构第二个会场。
- 未收录：8/7 HEROINES 大浴衣特典会、8/13 幕张翌日大特典会等单独特典会；4/19 あいらいふかふぇ有多店与成员分组，miniLIVE 的具体举办店未核实；11/20、12/17 排期图只写“大阪某所”“池袋某所”，未据此猜会场或增加重复记录（12/17 已有可核实的具体活动）。候补生单独活动不收录。

## 2025 年

新增 117 条（含取消、延期的原定记录）；原有 2 条保留，合计 119 条。新增逐月场数：1 月 10、2 月 10、3 月 11、4 月 11、5 月 9、6 月 7、7 月 11、8 月 9、9 月 9、10 月 10、11 月 9、12 月 11。新增主出处：官方 X 28 条，官方售票/主办方 57 条，Eventernote 31 条，LiveFans 1 条；仅非官方来源 32 条。新增 20 个会场，地址、容量均留空。

- 1/21 あいす生诞祭原定 Spotify O-EAST，延期至 3/7 Zepp Haneda；两条均保留并互相说明。
- 10/7 那蘭のどか生诞祭原定品川ステラボール，官网 8/25 公告取消；保留原定记录，注明取消，关联原始官方告知与官网取消公告。
- 11/29 NSE2025 次元星舞台 in Shanghai 原定上海 瓦肆 VAS est，11/21 官方公告取消/延期并退款，替代日期未公布。只收录告知图明确的 iLiFE! 11/29 舞台，不把活动总区间 11/29–30 或 11/28 特典会当作另两场演出。
- 11/22 仙台 GO!LiFE! 为现场公演，同日横滨 FUURYUUFES 5.0 的出处明确为 iLiFE!（バーチャル），后者已加注虚拟出演。
- 原库 ID 12（2025-10-13 LiFESTART）会场仍为“未确认”。已打开官方告知 `https://x.com/iLiFE_official/status/1974802226867781824` 明确 Zepp Haneda；遵守只新增要求，未修改原记录。
- 未收录：1/28 网络签名会、2/4 翌日特典会、8/16–17 浴衣特典会、8/28 武道馆翌日大特典会、9/14 若葉のあ后日特典会、11/8 万圣节服装特典会、12/14 特别衣装特典会等单独特典活动；单独成员走秀、电视播出和广告车不作为团体演唱会收录。LiveFans 的 IDOL SUMMER JUNGLE 2025“出演日未定”条目没有具体演出日期，排除；另有明确 8/11 的活动详情可核实，按该日收录。

## 2026 年

新增 93 条；原有 12 条保留，合计 105 条。新增逐月场数：1 月 10、2 月 10、3 月 10、4 月 10、5 月 12、6 月 3、7 月 10、8 月 5、9 月 6、10 月 7、11 月 6、12 月 4。新增主出处：官方 X 32 条，官网 3 条，主办方官网 3 条，官方售票/主办方 36 条，Eventernote 19 条；仅非官方来源 19 条。新增 19 个会场，地址、容量均留空。

- JAPANLiFE! 2025 跨年部分补入 7 场；名称仍沿用官方原文“2025”。1/8 小熊まむ生诞祭亦沿用告知原文“2025”，不擅改成 2026。
- 未来场次只录入已公布信息，包括 iLiVE! TOUR 10/26 东京、11/9 名古屋、11/16 札幌、12/8 福冈、12/15 大阪及 12/30 COUNTDOWN JAPAN；未公布的时间、具体舞台不推测。iLiVE! TOUR 三站主出处为官网 2006 号公告，同时关联明确 iLiFE! 参与的官方募集告知。
- 万圣节主办方官网的 iLiFE! 日割为 10/31、11/1；排除 LiveFans 的 10/30 条目和售票页以 10/30 为开始日的三日通票，不把活动开始日当出演日。
- 11/29 GIFT：Eventernote 会场写成お台場青海，与主办方官网及告知图冲突；采用官网“SGCホール有明 / トヨタアリーナ東京”，具体出演舞台未查到。12/30 COUNTDOWN JAPAN 同样保留官网告知的整体会场，具体舞台未查到。
- 3/18 V・ファーレン長崎 #推し活NIGHT：官方与俱乐部页面核实日期、17:45 特别演唱会，但所打开页面没有明确写出体育场正式名称；复用“未确认”会场，说明城市及未查到字段，不凭常识猜名。
- 1/28 天羽しおり生诞祭明确仅心花りり、あいす嘉宾出演；7/14 心花りり生诞祭 DAY1 为初期成员重聚，均已加注，不把全员出勤作为事实。5/1 体育祭归入“その他”，备注不能据此推断有常规歌唱舞台。5/16、10/18 +HEROINE 两部按同日同会场合并。
- 未收录：GFEST 的活动区间 10/10–11 中未核实 iLiFE! 出演的 10/11；7/31 TIF 没有核实到团体舞台（已核实 8/1、8/2）；纯特典会、候补生单独活动及仅写“予定”的排期线索。巡演和生诞祭均依实际告知核实，不推演未发布日期。

## 验证与提交

各年均运行导出、逐字节检查及年份出处检查。公演、日历、会场页面分别在 1280 和 390 像素宽度打开；查看图片加载、页面错误与横向溢出。原库所有表逐行比对，已有记录不得删除或修改。

2023：`export.py --rebuild-derived`、`export.py --check` 通过。`check_sources.py --year 2023` 新增 142 个非 X 主出处及 2 个会场容量检查全部通过；原有 ID 5、7 的 Wikipedia 页面未匹配到对应日期，退出码为 1，零新增失败。桌面/手机三页面检查通过，原有 328 场及其余各表旧行全部保留。2023 已提交并推送：`0425dc8`。2024 已提交并推送：`1ad0a5f`。

2024：导出与逐字节检查通过；年份出处检查共 124 项，只有原有 ID 8 的 Wikipedia 日期识别失败，零新增失败。补查指定月份日历时发现长英文标题会撑宽手机网格，`style.css` 给日历七列使用 `minmax(0,1fr)`，并让单元格文字可换行；配色、图片和其他页面布局不变。修正后桌面/手机三页面检查通过。2025：导出与逐字节检查通过，年份出处检查 93 项全部通过、零失败；指定 2025 年 1 月的日历及公演/会场页在桌面、手机均通过，所有原有记录仍完整保留。2026：导出与逐字节检查通过；桌面、手机三页面无页面报错、无图片加载失败、无横向溢出。出处检查共 72 项，新增 61 个非 X 主出处全部通过；8 条原有 Wikipedia 记录（ID 13、15–21）未识别到对应日期，退出码为 1，零新增失败。原有会场容量出处检查通过。未推送 main，未部署；线上双站 JSON 一致性由 Grok Bot 合并部署后验收。

## 逐月场数与出处统计

统计包含取消、延期的原定记录；同日同会场合并后计一条。逐月数字为“新增 / 本年合计”，合计包含保留的原有记录。

| 月份 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|
| 1 月 | 16 / 17 | 12 / 12 | 10 / 10 | 10 / 10 |
| 2 月 | 14 / 14 | 10 / 10 | 10 / 10 | 10 / 11 |
| 3 月 | 16 / 16 | 13 / 13 | 11 / 11 | 10 / 10 |
| 4 月 | 18 / 18 | 10 / 10 | 11 / 11 | 10 / 10 |
| 5 月 | 15 / 15 | 15 / 15 | 9 / 9 | 12 / 12 |
| 6 月 | 12 / 12 | 12 / 12 | 7 / 7 | 3 / 11 |
| 7 月 | 15 / 15 | 16 / 16 | 11 / 11 | 10 / 10 |
| 8 月 | 14 / 14 | 12 / 13 | 9 / 10 | 5 / 6 |
| 9 月 | 8 / 9 | 12 / 13 | 9 / 9 | 6 / 6 |
| 10 月 | 13 / 13 | 10 / 11 | 10 / 11 | 7 / 9 |
| 11 月 | 14 / 14 | 15 / 15 | 9 / 9 | 6 / 6 |
| 12 月 | 17 / 18 | 16 / 16 | 11 / 11 | 4 / 4 |
| 全年 | 172 / 175 | 153 / 156 | 117 / 119 | 93 / 105 |

以下按新增记录的主出处统计；补充出处不重复计数。

| 主出处类型 | 2023 | 2024 | 2025 | 2026 | 合计 |
|---|---:|---:|---:|---:|---:|
| 官方 X | 30 | 34 | 28 | 32 | 124 |
| 官网 | 0 | 0 | 0 | 3 | 3 |
| 主办方官网 | 0 | 0 | 0 | 3 | 3 |
| 官方售票/主办方 | 14 | 59 | 57 | 36 | 166 |
| Eventernote | 124 | 60 | 31 | 19 | 234 |
| LiveFans | 4 | 0 | 1 | 0 | 5 |

## 仅非官方来源逐场清单

共 239 条，全部在数据库 note 标记“仅非官方来源”。链接为逐个打开核实过的主出处；补充出处见年度审计 JSON。

### 2023 年（128 条）

| ID | JST 日期 | 公演 | 会场 | 出处 |
|---:|---|---|---|---|
| 329 | 2023-01-03 | TOKYO IDOL PROJECT × @JAM ニューイヤープレミアムパーティー2023【3日(火)】 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/326589) |
| 330 | 2023-01-04 | iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 1/4 | タワーレコード渋谷店B1F CUTUP STUDIO | [Eventernote](https://www.eventernote.com/events/330354) |
| 331 | 2023-01-06 | ツンデレフェス Vol.3 〜新年明けましてSP〜 | 品川インターシティホール | [Eventernote](https://www.eventernote.com/events/329120) |
| 333 | 2023-01-09 | iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 1/9 | タワーレコード渋谷店B1F CUTUP STUDIO | [Eventernote](https://www.eventernote.com/events/330759) |
| 337 | 2023-01-13 | iLiFE リリイベ完走ありがとうLIVE（1部・2部） | Veats SHIBUYA | [Eventernote](https://www.eventernote.com/events/330327) |
| 338 | 2023-01-14 | うるトラすフェスタ vol.11＠ヒューリックホール東京 | ヒューリックホール東京 | [Eventernote](https://www.eventernote.com/events/328990) |
| 339 | 2023-01-15 | 名古屋・来世邂逅物語 | Lives NAGOYA | [Eventernote](https://www.eventernote.com/events/330710) |
| 340 | 2023-01-15 | iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 1/15 | ヴィレッジヴァンガード名古屋パルコ店 | [Eventernote](https://www.eventernote.com/events/330909) |
| 341 | 2023-01-17 | 【出演者変更】STRIPE【O-EAST】 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/331072) |
| 342 | 2023-01-22 | 罪フェス | WOMBLIVE | [Eventernote](https://www.eventernote.com/events/331617) |
| 343 | 2023-01-28 | Girl’s Bomb!! 〜真冬の大祭典〜TOKYO DOME CITY HALL | TOKYO DOME CITY HALL | [Eventernote](https://www.eventernote.com/events/331665) |
| 344 | 2023-02-02 | ツインテールフェス 2023 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/327947) |
| 345 | 2023-02-03 | ゲリラ無銭LIVE! 【第1部 iLiFE!編】 | SHIBUYA DIVE | [Eventernote](https://www.eventernote.com/events/333483) |
| 346 | 2023-02-04 | でらロックフェスティバル２０２３【２/４(土)】 | 愛知県内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/332627) |
| 347 | 2023-02-09 | MARQUEE祭 Vol.127 | Spotify O-WEST | [Eventernote](https://www.eventernote.com/events/330620) |
| 348 | 2023-02-11 | HEROINES VALENTINE IN OSAKA（1部・2部） | なんばHatch | [Eventernote](https://www.eventernote.com/events/332407) |
| 349 | 2023-02-13 | HEROINES VALENTINE 東京 | CLUB CITTA' | [Eventernote](https://www.eventernote.com/events/332405) |
| 351 | 2023-02-18 | キニなる！fes. (2023/02/18) | Veats SHIBUYA | [Eventernote](https://www.eventernote.com/events/332759) |
| 352 | 2023-02-20 | ZUTTOMOTTO DEBUT 4MAN LIVE | CLUB CITTA' | [Eventernote](https://www.eventernote.com/events/334057) |
| 353 | 2023-02-21 | 【出演者変更】超姫祭 (2023/02/21) | CLUB CITTA' | [Eventernote](https://www.eventernote.com/events/334584) |
| 354 | 2023-02-23 | New Generations!! Vol.8 ~Premium~ | 室町三井ホール&カンファレンス | [Eventernote](https://www.eventernote.com/events/333724) |
| 355 | 2023-02-24 | 夜の馬鹿LIFE! | Veats SHIBUYA | [Eventernote](https://www.eventernote.com/events/331070) |
| 356 | 2023-02-26 | ッスッゴイライブ (2023/02/26) | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/333682) |
| 357 | 2023-02-28 | dot yell fes 2周年SP (DAY1) | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/334054) |
| 360 | 2023-03-04 | TENRIN VS iLiFE! | Veats SHIBUYA | [Eventernote](https://www.eventernote.com/events/335255) |
| 361 | 2023-03-05 | MARQUEE祭 Vol.128 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/332750) |
| 363 | 2023-03-11 | IDORISE!! FESTIVAL 2023【11日(土)】 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/331349) |
| 365 | 2023-03-18 | HEROINESFES White | KANDA SQUARE HALL | [Eventernote](https://www.eventernote.com/events/336223) |
| 366 | 2023-03-19 | brute eyes vol.1 | 恵比寿LIQUIDROOM | [Eventernote](https://www.eventernote.com/events/338375) |
| 367 | 2023-03-22 | ワンダーウィード 天 白川ゆめか生誕祭 (3/22) | 新宿BLAZE | [Eventernote](https://www.eventernote.com/events/337078) |
| 368 | 2023-03-23 | NIG FES2023【23日(木)】 | TOKYO DOME CITY HALL | [Eventernote](https://www.eventernote.com/events/330560) |
| 370 | 2023-03-25 | 瀬戸内アイドルフェスティバル（2023/3/25） | 広島県内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/338215) |
| 371 | 2023-03-26 | 瀬戸内アイドルフェスティバル（2023/3/26） | 広島県内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/338217) |
| 372 | 2023-03-28 | ちゅらまちゅり〜特別編〜 (2023/03/28) | duo MUSIC EXCHANGE | [Eventernote](https://www.eventernote.com/events/336792) |
| 374 | 2023-04-01 | NATSUZOME2023〈DAY1〉 | 稲毛海浜公園野外音楽堂 | [Eventernote](https://www.eventernote.com/events/335265) |
| 375 | 2023-04-05 | iLiVE! Vol.6 | Veats SHIBUYA | [Eventernote](https://www.eventernote.com/events/337077) |
| 376 | 2023-04-08 | femmeLiFE! | 渋谷WWW X | [Eventernote](https://www.eventernote.com/events/338506) |
| 377 | 2023-04-09 | HEROINES ViViD | 大手町三井ホール | [Eventernote](https://www.eventernote.com/events/337639) |
| 378 | 2023-04-10 | HEROINES FES vol.7 (2023/04/10) | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/337079) |
| 379 | 2023-04-11 | LEADING ID #いどみん生誕ツアー2023 東京 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/337569) |
| 380 | 2023-04-14 | アイドル甲子園 PREMIUM in 新宿BLAZE（2023/4/14） | 新宿BLAZE | [Eventernote](https://www.eventernote.com/events/336752) |
| 381 | 2023-04-15 | drown in your night OSAKA Vol.2 | 梅田CLUB QUATTRO | [LiveFans](https://www.livefans.jp/events/1526886) |
| 382 | 2023-04-16 | NEO JAPONISM 主催公演 「合戦 KASSEN」 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/338417) |
| 383 | 2023-04-17 | iLiFE!無銭LIVE! | Spotify O-WEST | [Eventernote](https://www.eventernote.com/events/339638) |
| 384 | 2023-04-17 | ちゅらまちゅり (2023/04/17) | 渋谷WWW X | [Eventernote](https://www.eventernote.com/events/334427) |
| 386 | 2023-04-21 | -anison.idol fes-LIVE HIKING!! vol.00 | Zepp DiverCity (TOKYO) | [Eventernote](https://www.eventernote.com/events/339027) |
| 387 | 2023-04-22 | クロフェス2023～野外フェスでキュンからのバッキューン♡だしん！！～DAY1 | 海の森水上競技場 | [Eventernote](https://www.eventernote.com/events/332781) |
| 388 | 2023-04-26 | #2i2 PRODUCE 【64 ep.05】 | WOMBLIVE | [Eventernote](https://www.eventernote.com/events/339770) |
| 389 | 2023-04-28 | 4/28(金) TOKYO GIRLS GIRLS | 品川インターシティホール | [Eventernote](https://www.eventernote.com/events/336610) |
| 390 | 2023-04-29 | HEROINES FES in 肉フェス®︎ Supported by New Generations!! | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/338840) |
| 391 | 2023-04-30 | RAD LIVE × Be Rise Lab presents「RAD JAM EXTREM -Be Rise Edition-」 | Zepp DiverCity (TOKYO) | [Eventernote](https://www.eventernote.com/events/336722) |
| 393 | 2023-05-04 | HYPE IDOL! GW DX！ | 山野ホール | [Eventernote](https://www.eventernote.com/events/338673) |
| 394 | 2023-05-06 | 歌舞伎町UP GATE↑↑DAY1 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/337036) |
| 396 | 2023-05-13 | MAWA LOOP OSAKA 2023 (5/13) | 大阪府内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/341474) |
| 398 | 2023-05-17 | MARQUEE Fes.-day2- (2023/05/17) | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/339578) |
| 399 | 2023-05-19 | アキシブproject無銭乱舞-2MAN TOUR- (2023/05/19) | Spotify O-WEST | [Eventernote](https://www.eventernote.com/events/342641) |
| 400 | 2023-05-21 | 5/21(日) TOKYO GIRLS GIRLS | 新都市ホール | [Eventernote](https://www.eventernote.com/events/340655) |
| 401 | 2023-05-22 | iLiVE! Vol.7 | Veats SHIBUYA | [Eventernote](https://www.eventernote.com/events/337076) |
| 403 | 2023-05-27 | 【DAY1】手羽先セッションFESTIVAL～Supported by アイドルアラモード（2023/5/27） | Maker's Pier | [Eventernote](https://www.eventernote.com/events/342752) |
| 404 | 2023-05-28 | 【DAY2】手羽先セッションFESTIVAL～Supported by アイドルアラモード（2023/5/28） | Maker's Pier | [Eventernote](https://www.eventernote.com/events/344033) |
| 405 | 2023-05-28 | BUZZ IDOL! Vol.1 | 恵比寿LIQUIDROOM | [Eventernote](https://www.eventernote.com/events/343884) |
| 408 | 2023-06-03 | ANCHOR主催音楽フェス #ANFES | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/341339) |
| 411 | 2023-06-12 | 女性限定サーキットイベント Queen&Princess SP【#キュープリ】(6/12) | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/341608) |
| 413 | 2023-06-16 | IDOL CONTENT EXPO ＠ヒューリックホール東京～Premium Live!!!～ | ヒューリックホール東京 | [Eventernote](https://www.eventernote.com/events/344459) |
| 414 | 2023-06-17 | RAD JAM 2023 | Aichi Sky Expo(愛知県国際展示場) | [Eventernote](https://www.eventernote.com/events/338723) |
| 415 | 2023-06-20 | シンデレラ宣言!Zepp目前 SP LIVE『超・シンデレラ PARTY!』Vol.2 | Spotify O-WEST | [LiveFans](https://www.livefans.jp/events/1554391) |
| 416 | 2023-06-22 | 【出演者変更】ちゅらまちゅり (2023/06/22) | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/342125) |
| 417 | 2023-06-24 | GIGA・GIGA SONIC ~Road to 幕張メッセ vol.2~ | ヒューリックホール東京 | [Eventernote](https://www.eventernote.com/events/343733) |
| 419 | 2023-07-01 | 超NATSUZOME2023【DAY1】 | 幕張海浜公園 Gブロック特設会場 | [Eventernote](https://www.eventernote.com/events/343505) |
| 420 | 2023-07-02 | 超NATSUZOME2023【DAY2】 | 幕張海浜公園 Gブロック特設会場 | [Eventernote](https://www.eventernote.com/events/343523) |
| 421 | 2023-07-04 | 特区2023 | 新宿BLAZE | [Eventernote](https://www.eventernote.com/events/345657) |
| 422 | 2023-07-07 | 渋谷大納涼祭 2023 | Spotify O-WEST | [Eventernote](https://www.eventernote.com/events/346724) |
| 423 | 2023-07-08 | 「IDOL GALAXY」supported by テレビ愛知【DAY1】 | Maker's Pier | [Eventernote](https://www.eventernote.com/events/343711) |
| 425 | 2023-07-14 | うるトラすフェスタ2023〜夏スペシャルin豊洲PIT〜 | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/340182) |
| 426 | 2023-07-15 | iLiVE! -Premium- | Zepp DiverCity (TOKYO) | [Eventernote](https://www.eventernote.com/events/343567) |
| 427 | 2023-07-16 | SPARK 2023 in YAMANAKAKO【16日(日)】 | 山中湖交流プラザきらら | [Eventernote](https://www.eventernote.com/events/340910) |
| 428 | 2023-07-17 | IDOL SQUARE Summer Festival 2023 | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/343723) |
| 429 | 2023-07-22 | SEKIGAHARA IDOL WARS 2023〜関ケ原唄姫合戦〜 2日目 | 桃配運動公園(関ヶ原町) | [Eventernote](https://www.eventernote.com/events/346270) |
| 430 | 2023-07-23 | SEKIGAHARA IDOL WARS 2023〜関ケ原唄姫合戦〜 3日目 | 桃配運動公園(関ヶ原町) | [Eventernote](https://www.eventernote.com/events/346273) |
| 432 | 2023-07-29 | 六本木アイドルフェスティバル2023［DAY-1］ | 六本木ヒルズアリーナ | [Eventernote](https://www.eventernote.com/events/344510) |
| 433 | 2023-07-30 | TOKYO GIRLS GIRLS ~ 3rd Anniversary day2~ | 品川インターシティホール | [Eventernote](https://www.eventernote.com/events/350112) |
| 435 | 2023-08-04 | TOKYO IDOL FESTIVAL 2023 supported by にしたんクリニック【4日(金)】 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/340553) |
| 436 | 2023-08-05 | TOKYO IDOL FESTIVAL 2023 supported by にしたんクリニック【5日(土)】 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/340554) |
| 437 | 2023-08-07 | iLiVE! ~Premium- summerスペシャル~ | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/347237) |
| 438 | 2023-08-11 | New Generations!! - 真夏の超・Premium Circuit - Day1 | Maker's Pier | [Eventernote](https://www.eventernote.com/events/348286) |
| 439 | 2023-08-13 | ツンデレフェス Vol.4 〜常夏！法被で超ハッピ〜SP!!〜 | 品川インターシティホール | [Eventernote](https://www.eventernote.com/events/350092) |
| 440 | 2023-08-15 | ジャムズセッション!!-真夏のプレミアム- | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/349284) |
| 441 | 2023-08-17 | NEO KASSEN 2023 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/347941) |
| 442 | 2023-08-18 | TOKYO GIRLS GIRLS(2023.08.18) | 品川インターシティホール | [Eventernote](https://www.eventernote.com/events/348577) |
| 443 | 2023-08-19 | UP-T presents かがやきフェス2023【8/19】 | 石川県内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/341341) |
| 444 | 2023-08-24 | NAMBA LiFE! | 梅田バナナホール | [Eventernote](https://www.eventernote.com/events/352587) |
| 445 | 2023-08-26 | ＠JAM EXPO 2023 supported by UP-T【26日(土)】 | 横浜アリーナ | [Eventernote](https://www.eventernote.com/events/343524) |
| 446 | 2023-08-31 | エンドレスサマー2023 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/351171) |
| 447 | 2023-08-31 | 赤レンガスプラッシュ-祭-Day2 | 横浜赤レンガ倉庫 | [Eventernote](https://www.eventernote.com/events/346924) |
| 448 | 2023-09-09 | OPC Fes. -Q&..Q!?- | GARDEN 新木場 FACTORY | [Eventernote](https://www.eventernote.com/events/352351) |
| 449 | 2023-09-10 | IDOL☆STAR vol.1 | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/353745) |
| 451 | 2023-09-14 | MARQUEE Fes. day2 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/351818) |
| 452 | 2023-09-15 | 日テレプラス秋のアイドル祭り Supported by U-ZONE | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/354232) |
| 454 | 2023-09-23 | バンドじゃないもん！MAXX NAKAYOSHI主催「NAKAYOSHI FES.2023」 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/347246) |
| 456 | 2023-10-01 | 10/1(日) TOKYO GIRLS GIRLS | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/355429) |
| 457 | 2023-10-02 | かすみ草とステラ presents「大青春祭」 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/354082) |
| 459 | 2023-10-07 | GIGA・GIGA SONIC ~ 2周年大感謝祭SPECIAL in 幕張メッセ~ presented by ドラゴンエッグ | 幕張メッセ 国際展示場ホール | [Eventernote](https://www.eventernote.com/events/352126) |
| 460 | 2023-10-08 | あいふぇす vol.1 | Zepp Namba (OSAKA) | [Eventernote](https://www.eventernote.com/events/353418) |
| 461 | 2023-10-09 | DERARALiFE! | NAGOYA ReNY limited | [Eventernote](https://www.eventernote.com/events/356916) |
| 462 | 2023-10-11 | FUURYUU FES 5.0 supported by Girl’s Bomb!! | さいたまスーパーアリーナ | [Eventernote](https://www.eventernote.com/events/355015) |
| 463 | 2023-10-14 | TOKOROLiFE! | ところざわサクラタウン ジャパンパビリオン ホールA | [Eventernote](https://www.eventernote.com/events/357664) |
| 464 | 2023-10-16 | ちゅらららいふ！ | 渋谷ストリームホール | [Eventernote](https://www.eventernote.com/events/357662) |
| 465 | 2023-10-22 | 10/22(日) TOKYO GIRLS GIRLS 2023/10/22 | 新都市ホール | [Eventernote](https://www.eventernote.com/events/351964) |
| 466 | 2023-10-29 | Appare! HALLOWEEN 2023 DAY2 10/29 | GARDEN 新木場 FACTORY | [Eventernote](https://www.eventernote.com/events/355561) |
| 467 | 2023-10-30 | HEROINESHALLOWEEN 10/30 | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/356798) |
| 468 | 2023-10-31 | HEROINESHALLOWEEN 10/31 | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/355880) |
| 470 | 2023-11-09 | 罪フェスvol.3 | duo MUSIC EXCHANGE | [LiveFans](https://www.livefans.jp/events/1610756) |
| 472 | 2023-11-14 | MARQUEE FES. (2023/11/14) | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/355908) |
| 473 | 2023-11-16 | iLiVE! vol.10 | KANDA SQUARE HALL | [Eventernote](https://www.eventernote.com/events/360542) |
| 474 | 2023-11-17 | YANFES2023 | KANDA SQUARE HALL | [Eventernote](https://www.eventernote.com/events/360830) |
| 475 | 2023-11-18 | かすみ草とステラ主催公演『むれなでしこ -群撫子- vol.8』 | スタァライト劇場 | [Eventernote](https://www.eventernote.com/events/358743) |
| 477 | 2023-11-19 | SPA!フェス35 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/358353) |
| 479 | 2023-11-23 | DERARALiFE!Vol.2 | Zephyr Hall | [LiveFans](https://www.livefans.jp/events/2012731) |
| 483 | 2023-12-01 | HEROINES FES Vol.10 | CLUB CITTA' | [Eventernote](https://www.eventernote.com/events/362215) |
| 484 | 2023-12-04 | アンスぱーくっ！！！！！！in Spotify O-EAST 12/4 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/357587) |
| 485 | 2023-12-05 | dot yell fes WINTER SP | ヒューリックホール東京 | [Eventernote](https://www.eventernote.com/events/362801) |
| 487 | 2023-12-10 | ッスッゴイライブ〜5th anniversary SP LIVE〜 | 品川プリンスホテル ステラボール | [Eventernote](https://www.eventernote.com/events/360313) |
| 488 | 2023-12-11 | ちゅらまちゅり〜サーキット編〜　2023/12/11 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/362738) |
| 489 | 2023-12-14 | NEO JAPONISMデビュー4周年イベント "NEO START" | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/358625) |
| 490 | 2023-12-15 | iLiVE! vol.11 | KANDA SQUARE HALL | [Eventernote](https://www.eventernote.com/events/360684) |
| 492 | 2023-12-17 | ケンズカフェ東京 PRESENTS ガラフェス -日比谷野音 デリシャスサンデー- | 日比谷公園大音楽堂 | [Eventernote](https://www.eventernote.com/events/357680) |
| 494 | 2023-12-23 | iLiVE! Xmas | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/360837) |
| 495 | 2023-12-24 | NEO JAPONISM presents NEO X'mas PARTY | GARDEN 新木場 FACTORY | [Eventernote](https://www.eventernote.com/events/359881) |

### 2024 年（60 条）

| ID | JST 日期 | 公演 | 会场 | 出处 |
|---:|---|---|---|---|
| 500 | 2024-01-02 | 謹賀新年！アイドル初夢ライブ supported by @JAM（1月2日） | Zepp DiverCity (TOKYO) | [Eventernote](https://www.eventernote.com/events/365002) |
| 501 | 2024-01-03 | アイドル甲子園PREMIUM 2024 -NIGHT- | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/361838) |
| 502 | 2024-01-06 | ニューイヤーだよ！六本木アイドルフェスティバル 2024 | EX THEATER ROPPONGI | [Eventernote](https://www.eventernote.com/events/360890) |
| 503 | 2024-01-07 | HYPE IDOL！NewYear SP | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/364648) |
| 504 | 2024-01-13 | カオガトウダイ | 恵比寿ザ・ガーデンホール | [Eventernote](https://www.eventernote.com/events/366161) |
| 507 | 2024-01-21 | でびぱっぱ冬祭 in 野音 | 日比谷公園大音楽堂 | [Eventernote](https://www.eventernote.com/events/363287) |
| 510 | 2024-01-26 | chuLa 東名阪Zeppツアー 〜君と約束した夢を叶えるために〜 愛知公演 | Zepp Nagoya | [Eventernote](https://www.eventernote.com/events/368162) |
| 514 | 2024-02-03 | AGEFES PREMIUM | THE GRAND HALL | [Eventernote](https://www.eventernote.com/events/368712) |
| 515 | 2024-02-04 | EVOLUTION POP! Vo.71 | Spotify O-WEST | [Eventernote](https://www.eventernote.com/events/367444) |
| 525 | 2024-03-09 | IDORISE!! FESTIVAL 2024【9日(土)】 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/364813) |
| 527 | 2024-03-13 | JAPAN IDOL FESTIVAL supported by カラオケまねきねこVol.2 2024/3/13 | LINE CUBE SHIBUYA | [Eventernote](https://www.eventernote.com/events/371920) |
| 533 | 2024-03-26 | ッスッゴイフェス (2024/3/26) | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/372162) |
| 535 | 2024-04-07 | 4/7(日) TOKYO GIRLS GIRLS "Day2" supported by TIGET 2024/04/07 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/367122) |
| 537 | 2024-04-10 | LEADING ID #いどみん生誕祭 2024 2024/04/10 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/374463) |
| 538 | 2024-04-12 | うるトラすフェスタ桜満開SP版 | Zepp DiverCity (TOKYO) | [Eventernote](https://www.eventernote.com/events/374632) |
| 540 | 2024-04-14 | アンスぱーくっ!!!!! in 名古屋 2024/04/14 | NAGOYA ReNY limited | [Eventernote](https://www.eventernote.com/events/374477) |
| 541 | 2024-04-26 | B.L.T. Wonderland LIVE | 品川プリンスホテル ステラボール | [Eventernote](https://www.eventernote.com/events/375707) |
| 542 | 2024-04-28 | 向日えな生誕祭「プリンセスえなピーチ」 | 品川プリンスホテル ステラボール | [Eventernote](https://www.eventernote.com/events/379965) |
| 543 | 2024-04-29 | 「GiRLS SUMMiT IN GORILLA HALL OSAKA」 | GORILLA HALL OSAKA | [Eventernote](https://www.eventernote.com/events/374132) |
| 544 | 2024-04-30 | New Generations!! ~Premium~ ✖︎ 肉フェス®︎ (2024年4月30日) | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/377064) |
| 546 | 2024-05-04 | NEO JAPONISM PRESENTS KASSEN2024 in 肉フェス | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/375708) |
| 548 | 2024-05-06 | 歌舞伎町UP GATE↑↑2024 DAY2 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/368019) |
| 549 | 2024-05-08 | ヒロインズ無銭LIVE 2部(2024/5/8) | CLUB CITTA' | [Eventernote](https://www.eventernote.com/events/379068) |
| 552 | 2024-05-12 | ガラフェス～鳴らせ！絆ファンファーレ～ | 日比谷公園大音楽堂 | [Eventernote](https://www.eventernote.com/events/377694) |
| 558 | 2024-05-26 | @JAM 2024 Day2～SUPER LIVE～ 2部 | Zepp DiverCity (TOKYO) | [Eventernote](https://www.eventernote.com/events/377026) |
| 563 | 2024-06-09 | クロフェス2024～5周年だよ！全員集合だしん！～DAY4(6/9) | 海の森水上競技場 | [Eventernote](https://www.eventernote.com/events/379396) |
| 569 | 2024-06-22 | パラダイス 2024.6.22 | ところざわサクラタウン ジャパンパビリオン ホールA | [Eventernote](https://www.eventernote.com/events/385584) |
| 575 | 2024-07-09 | HEROINES LEAGUE1 2024.7.9 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/385575) |
| 578 | 2024-07-14 | 【7/14】SPARK 2024 in KAWASAKI | 川崎市東扇島東公園 | [Eventernote](https://www.eventernote.com/events/383116) |
| 579 | 2024-07-15 | SPARK 2024 in KAWASAKI【15日(月祝)】 | 川崎市東扇島東公園 | [Eventernote](https://www.eventernote.com/events/383108) |
| 580 | 2024-07-20 | SEKIGAHARA IDOL WARS 2024〜関ケ原唄姫合戦〜 2日目 | 桃配運動公園(関ヶ原町) | [Eventernote](https://www.eventernote.com/events/384207) |
| 581 | 2024-07-21 | SEKIGAHARA IDOL WARS 2024〜関ケ原唄姫合戦〜 3日目 | 桃配運動公園(関ヶ原町) | [Eventernote](https://www.eventernote.com/events/384414) |
| 582 | 2024-07-24 | コカ･コーラ SUMMER STATION 音楽LIVE 2024/07/24 iLiFE! | 六本木ヒルズアリーナ | [Eventernote](https://www.eventernote.com/events/384147) |
| 583 | 2024-07-26 | TOKYO GIRLS GIRLS ~ 4th Anniversary day1 ~ | 品川インターシティホール | [Eventernote](https://www.eventernote.com/events/384187) |
| 588 | 2024-08-02 | TOKYO IDOL FESTIVAL 2024 supported by にしたんクリニック【2日(金)】 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/380431) |
| 589 | 2024-08-03 | TOKYO IDOL FESTIVAL 2024 supported by にしたんクリニック【3日(土)】 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/380432) |
| 590 | 2024-08-04 | TOKYO IDOL FESTIVAL 2024 supported by にしたんクリニック【4日(日)】 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/380433) |
| 591 | 2024-08-15 | NEO KASSEN2024 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/377644) |
| 592 | 2024-08-17 | Devil ANTHEM. 10th Anniversary Year でびぱっぱ夏祭2024〜東の陣〜 | 三崎公園野外音楽堂 | [Eventernote](https://www.eventernote.com/events/381088) |
| 597 | 2024-08-27 | エンドレスサマー2024 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/387402) |
| 599 | 2024-08-31 | 24時間テレビ47 日産チャリティーイベント Day1 | 日産グローバル本社ギャラリー | [Eventernote](https://www.eventernote.com/events/389754) |
| 600 | 2024-09-08 | UP-T presents かがやきフェス2024【9/8】 | 石川県内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/391249) |
| 602 | 2024-09-14 | @JAM EXPO 2024 supported by UP-T【14日(土)】 | 横浜アリーナ | [Eventernote](https://www.eventernote.com/events/380436) |
| 603 | 2024-09-15 | @JAM EXPO 2024 supported by UP-T【15日(日)】 | 横浜アリーナ | [Eventernote](https://www.eventernote.com/events/380437) |
| 604 | 2024-09-16 | @JAM EXPO 2024 supported by UP-T【16日(月・祝)】 | 横浜アリーナ | [Eventernote](https://www.eventernote.com/events/380438) |
| 610 | 2024-09-29 | HEROINES SUMMER 2024 番外編 DAY2 | 東武動物公園 イベントステージHOLA！ | [Eventernote](https://www.eventernote.com/events/392708) |
| 613 | 2024-10-05 | 【10/5】LARME fes vol.1 | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/391865) |
| 614 | 2024-10-06 | ぐんまちゃんアイドルフェスティバル | 群馬県内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/385076) |
| 616 | 2024-10-19 | GIGA•GIGA SONIC in 幕張メッセ presented by ドラゴンエッグ | 幕張メッセ 国際展示場ホール | [Eventernote](https://www.eventernote.com/events/394648) |
| 618 | 2024-10-27 | 大阪造船所アイドルフェス（2024/10/27） | CCOクリエイティブセンター大阪 | [Eventernote](https://www.eventernote.com/events/397113) |
| 621 | 2024-10-31 | 高嶺のなでしこ「たかねこフェス Vol.3 〜オータムセッション～」 | EX THEATER ROPPONGI | [Eventernote](https://www.eventernote.com/events/391889) |
| 625 | 2024-11-09 | YBSよっちゃばれfestival 2024 Day.1 | 舞鶴城公園(甲府城跡) | [Eventernote](https://www.eventernote.com/events/396627) |
| 626 | 2024-11-12 | HEROINES アルバムリリースイベント　iLiFE! 池袋サンシャイン広場　1部 | 池袋サンシャインシティ アルパB1F 噴水広場 | [Eventernote](https://www.eventernote.com/events/400133) |
| 632 | 2024-11-23 | にゃんぽこらフェス！ DAY1 | 品川プリンスホテル ステラボール | [Eventernote](https://www.eventernote.com/events/393144) |
| 633 | 2024-11-24 | ART SOUND presents “SOUND GARDEN 2024”supported by テレビ愛知 11/24 | 愛知県内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/394934) |
| 636 | 2024-12-07 | HEROINES ALBUM 2025 リリースイベント in兵庫 | あまがさきキューズモール 2F屋外 Q's park | [Eventernote](https://www.eventernote.com/events/405352) |
| 640 | 2024-12-16 | NEO JAPONISM5周年記念対バン NEO START | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/401748) |
| 641 | 2024-12-17 | HEROINES ALBUM 2025 リリースイベント 2部 | 池袋サンシャインシティ アルパB1F 噴水広場 | [Eventernote](https://www.eventernote.com/events/410542) |
| 647 | 2024-12-28 | HEROINES COUNTDOWN Day1 | KANDA SQUARE HALL | [Eventernote](https://www.eventernote.com/events/401471) |
| 648 | 2024-12-29 | HEROINES COUNTDOWN Day2 | KANDA SQUARE HALL | [Eventernote](https://www.eventernote.com/events/401472) |

### 2025 年（32 条）

| ID | JST 日期 | 公演 | 会场 | 出处 |
|---:|---|---|---|---|
| 657 | 2025-01-17 | iLiFE! アルバム『HEROINES ALBUM 2025』ミニライブ＆特典会 | ダイバーシティ東京プラザ 2Fフェスティバル広場 | [Eventernote](https://www.eventernote.com/events/455610) |
| 663 | 2025-02-01 | HEROINES ALBUM 2025 ミニライブ&特典会 | ららぽーと柏の葉 本館2F センタープラザ | [Eventernote](https://www.eventernote.com/events/417070) |
| 670 | 2025-02-22 | HEROINES CATITUDE | NEW PIER HALL | [Eventernote](https://www.eventernote.com/events/417308) |
| 672 | 2025-02-25 | Jams Collection presents ジャムズセッション!! vol.5 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/458250) |
| 675 | 2025-03-08 | IDORISE!!FESTIVAL 2025 [ 8日(土) ] | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/411502) |
| 677 | 2025-03-14 | HEROINES WHITEDAY 2025 Day2 | KANDA SQUARE HALL | [Eventernote](https://www.eventernote.com/events/455614) |
| 680 | 2025-03-22 | YOEI FES × iLiFE! | KABUKICHO TOWER STAGE | [Eventernote](https://www.eventernote.com/events/422486) |
| 683 | 2025-03-30 | DJ KOO presents「KOOmic idol Festa」DAY2 | 品川プリンスホテル ステラボール | [Eventernote](https://www.eventernote.com/events/417161) |
| 684 | 2025-04-01 | iLiFE! ゲリラフリーライブ @ 新宿ReNY | 新宿ReNY | [Eventernote](https://www.eventernote.com/events/424202) |
| 685 | 2025-04-02 | NIG FES 2025 DAY1 | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/423026) |
| 689 | 2025-04-10 | LEADING ID ~いどみん生誕祭2025~ | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/421709) |
| 694 | 2025-04-27 | HEROINES FES@豊洲PIT 2025.04.27 | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/435284) |
| 695 | 2025-05-01 | 【音楽と食の祭典】埼玉MUSIC ＆ FOOD FESTIVAL 5/1 Part1 | 大宮ソニックシティ 大ホール | [Eventernote](https://www.eventernote.com/events/425900) |
| 708 | 2025-06-21 | Popteen & Cuugal × ONE AND ONLY ポップキューフェス2025 | KT Zepp Yokohama | [Eventernote](https://www.eventernote.com/events/432087) |
| 710 | 2025-06-28 | IDOL DANCE BATTLE『VERSUS』 | Zepp Shinjuku (TOKYO) | [Eventernote](https://www.eventernote.com/events/432969) |
| 714 | 2025-07-06 | 超NATSUZOME 2025 【DAY2】 | 幕張海浜公園 Gブロック特設会場 | [Eventernote](https://www.eventernote.com/events/430659) |
| 718 | 2025-07-19 | SEKIGAHARA IDOL WARS 2025 -関ケ原唄姫合戦-【DAY1】 | 桃配運動公園(関ヶ原町) | [Eventernote](https://www.eventernote.com/events/430660) |
| 722 | 2025-08-01 | TOKYO IDOL FESTIVAL 2025 supported by にしたんクリニック 08.01 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/425163) |
| 723 | 2025-08-02 | TOKYO IDOL FESTIVAL 2025 supported by にしたんクリニック 08.02 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/425164) |
| 724 | 2025-08-03 | TOKYO IDOL FESTIVAL 2025 supported by にしたんクリニック 08.03 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/425165) |
| 726 | 2025-08-06 | 関西コレクション 2025 AUTUMN & WINTER ／ KANSAI COLLECTION 2025 AUTUMN & WINTER | 京セラドーム大阪 | [Eventernote](https://www.eventernote.com/events/429844) |
| 728 | 2025-08-13 | NEO KASSEN 2025 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/427372) |
| 730 | 2025-08-31 | @JAM EXPO 2025 | 横浜アリーナ | [LiveFans](https://www.livefans.jp/events/1836033) |
| 736 | 2025-09-20 | NAKAYOSHI FES.2025 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/434516) |
| 738 | 2025-09-24 | HEROINES LEAGUE Ⅰ【Sep. part2】 | EX THEATER ROPPONGI | [Eventernote](https://www.eventernote.com/events/444475) |
| 739 | 2025-09-27 | 「東京ゲームショウ2025」コナミデジタルエンタテインメントブース VR×ライブアイドル 新サービス発表記念 iLiFE!スペシャルライブ | 幕張メッセ 国際展示場ホール | [Eventernote](https://www.eventernote.com/events/444181) |
| 749 | 2025-10-31 | HEROINES HALLOWEEN -PREMIUM-  2025/10/31 | Spotify O-EAST | [Eventernote](https://www.eventernote.com/events/491486) |
| 752 | 2025-11-09 | 昭和女子大学 第33回秋桜祭 iLiFE! 秋桜祭 LIVE 2025 | 昭和女子大学 人見記念講堂 | [Eventernote](https://www.eventernote.com/events/446971) |
| 754 | 2025-11-22 | 【FUURYUUFES 5.0 2025】 | ぴあアリーナMM | [Eventernote](https://www.eventernote.com/events/444858) |
| 758 | 2025-11-30 | ISE GIRLS FRONTIER 2025 DAY2［11/30］ | 三重県営サンアリーナ | [Eventernote](https://www.eventernote.com/events/449595) |
| 764 | 2025-12-23 | 超十代 -ULTRA TEENS FES- 2025@NAGOYA | COMTEC PORTBASE | [Eventernote](https://www.eventernote.com/events/446058) |
| 768 | 2025-12-31 | HEROINES COUNTDOWN 2025-2026 | TOKYO DOME CITY HALL | [Eventernote](https://www.eventernote.com/events/491487) |

### 2026 年（19 条）

| ID | JST 日期 | 公演 | 会场 | 出处 |
|---:|---|---|---|---|
| 774 | 2026-01-19 | COSMIC CIRCUS vol.4 | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/450083) |
| 791 | 2026-03-07 | IDORISE!!FESTIVAL 2026 Day1 | 東京都内各所（サーキット） | [Eventernote](https://www.eventernote.com/events/456406) |
| 792 | 2026-03-12 | HEROINES WHITEDAY 2026 DAY2 | 豊洲PIT | [Eventernote](https://www.eventernote.com/events/465772) |
| 794 | 2026-03-20 | MEGA VEGAS 2026 DAY1 | 神戸ワールド記念ホール | [Eventernote](https://www.eventernote.com/events/443747) |
| 801 | 2026-04-04 | 歌舞伎町ゲームフェスティバル2026 DAY1 | 歌舞伎町シネシティ広場 | [Eventernote](https://www.eventernote.com/events/492406) |
| 802 | 2026-04-05 | KANSAI COLLECTION 2026S/S | 京セラドーム大阪 | [Eventernote](https://www.eventernote.com/events/467326) |
| 804 | 2026-04-12 | ABEMA 最強バズりソング歌謡祭【30時間限界突破フェス】番組観覧 | ぴあアリーナMM | [Eventernote](https://www.eventernote.com/events/474318) |
| 808 | 2026-04-25 | GIRLS GROOVE INNOVAION 2026@豊崎海浜公園 美らSUNビーチ | 豊崎海浜公園・豊崎美らSUNビーチ | [Eventernote](https://www.eventernote.com/events/464994) |
| 810 | 2026-05-01 | HEROINES 体育祭 (2026/5/1) | 東京体育館 メインアリーナ | [Eventernote](https://www.eventernote.com/events/474798) |
| 814 | 2026-05-05 | JAPAN JAM 2026 DAY4 | 千葉市蘇我スポーツ公園 | [Eventernote](https://www.eventernote.com/events/460553) |
| 825 | 2026-07-05 | 超NATSUZOME 2026【DAY 2】 | 幕張海浜公園 Gブロック特設会場 | [Eventernote](https://www.eventernote.com/events/470850) |
| 827 | 2026-07-10 | iLiFE!×のんふぃく！ FC限定2MAN LIVE | KANDA SQUARE HALL | [Eventernote](https://www.eventernote.com/events/484871) |
| 834 | 2026-07-25 | OSAKA GIGANTIC MUSIC FESTIVAL 2026 -THANKS 10TH GIGA- DAY1 | 舞洲スポーツアイランド | [Eventernote](https://www.eventernote.com/events/464750) |
| 835 | 2026-08-01 | TOKYO IDOL FESTIVAL 2026 supported by にしたんクリニック【DAY2】 8/1 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/467335) |
| 836 | 2026-08-02 | TOKYO IDOL FESTIVAL 2026 supported by にしたんクリニック【DAY3】 8/2 | お台場・青海特設会場 | [Eventernote](https://www.eventernote.com/events/467331) |
| 838 | 2026-08-10 | LuckyFes’26 DAY3 | 国営ひたち海浜公園 | [Eventernote](https://www.eventernote.com/events/466546) |
| 839 | 2026-08-29 | 2026年プロ野球 パーソル パシフィック・リーグ公式戦北海道日本ハムファイターズ対千葉ロッテマリーンズ21回戦試合終了後イベント〈AFTER GAME〉iLiFE!スペシャルライブ | ES CON FIELD HOKKAIDO | [Eventernote](https://www.eventernote.com/events/485432) |
| 841 | 2026-09-19 | rockin'on presents ROCK IN JAPAN FESTIVAL 2026 9/19 | 千葉市蘇我スポーツ公園 | [Eventernote](https://www.eventernote.com/events/479208) |
| 847 | 2026-10-10 | GFEST.2026 DAY1 | Gメッセ群馬 | [Eventernote](https://www.eventernote.com/events/490691) |

## 原有数据问题汇总

原有 ID 6、12 的未确认会场见对应年度说明。年份出处脚本未识别到日期的原有 Wikipedia 记录为 ID 5、7（2023），ID 8（2024），ID 13、15–21（2026），合计 11 条；并非本任务新增链接失败。原有 2026 年巡演可由已打开的官方资料核验，但依本任务“只新增”约束不替换其出处。全部旧表行均完整保留；原有 2020–2022 年 297 条、2023–2026 年 20 条、2027 年 11 条均未修改。

最终数据库 863 条演出；新增 535 条、96 个会场、953 个去重出处 URL。全库按 date + venue_id 分组无重复。数据只在 SQLite 修改，JSON 由导出脚本生成；未新增图片、地址、容量或推断成员出勤。

## 年度提交与待验收项

| 年份 | 新增 | 本年合计 | 提交 |
|---|---:|---:|---|
| 2023 | 172 | 175 | `0425dc8` |
| 2024 | 153 | 156 | `1ad0a5f` |
| 2025 | 117 | 119 | `c33fccb` |
| 2026 | 93 | 105 | `d5e4e51` |

四次年度提交均已推送到 `origin/codex/015-lives-2023-2026`。执行检查摘要见 [015-audit/checks.json](015-audit/checks.json)。本地桌面、手机页面检查已通过；原导出 JSON 中 328 条演出也逐项与任务前版本一致。Grok Bot 每年 ≥20 场的独立抽查尚未执行；main 合并、部署和线上双站 JSON 一致性检查留待验收通过后执行。
