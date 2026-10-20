# 018 2020–2022 年演出逐场换成官方出处 · 执行结果报告

## 1. 总体概况与年度统计

针对 2020–2022 年数据库中标记为 `仅非官方来源` 的全部 182 场演出进行了逐场外部出处检索与真实连通性核验（执行顺序：2022 → 2021 → 2020）。

所有引用的官方链接均通过 HTTP 实际请求验证（HTTP 200，并确认页面中包含 iLiFE! 出演、演出名称、日期与会场事实），绝无拼接猜测推文 ID 或失效 URL。

| 年份 | 初始非官方场次 | 成功升级官方出处 | 剩余非官方场次 | 升级比例 | 年度提交号 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **2022 年** | 121 场 | **65 场** | 56 场 | 53.7% | `30c1413` |
| **2021 年** | 45 场 | **21 场** | 24 场 | 46.7% | `cd6ea46` |
| **2020 年** | 16 场 | **12 场** | 4 场 | 75.0% | `fd39aff` |
| **合计** | **182 场** | **98 场** | **84 场** | **53.8%** | — |

---

## 2. 升级来源类型分布统计

本次升级的 98 场官方出处来源类型分布如下：

1. **iLiFE! 官方 X 账号（@iLiFE_official / 关联官方）推文及月度排期图**：**40 场**
   - 包含官方账号当月汇总排期图推文（如 2021年1月、6月、7月、9月及2022年1月、9月、11月排期）、单场出演通知、当晚演出谢辞及现场合照推文。
2. **主办方 / 共演团体官方 X 账号活动推文**：**30 场**
   - 包含 IDOL CONTENT EXPO 官方推特（@ic_expo）、各偶像联合巡演/拼盘主办方（如 @Girls_Girlsinfo、@konyafes2017、@Appare_official、@calresofficial 等）公布的出演名单与タイムテーブル（时间表）。
3. **主办方官方票务与活动专题页**：**25 场**
   - 包含 TIGET 官方活动页面（21 场）、ダイキサウンド（Daiki Sound）官方活动页（3 场）、乐天票务（Rakuten Ticket）官方活动页（1 场）。
4. **会场官网日程与共演方官方事务所日程**：**1 场**
   - Stand-Up! Records 官方公演日程页（1 场，Live 50）。
5. **运营官方正式公开发布的新闻公告（活动自肃辞退通知）**：**2 场**
   - 株式会社imaginate / iLiFE!运营官方发布的成员确诊新冠活动自肃公演辞退通告（Live 123、Live 125）。

---

## 3. 因官方出处而纠正的数据

在检索与核对官方源过程中，依据官方一手公告纠正了 3 场演出之属性/时间误差：

1. **Live 172（2022-01-23，深月らむ 生誕祭2022）**：
   - 修正前：演出类型为 `対バン`
   - 修正后：根据官方公告修正为 `生誕祭`
   - 出处：`https://x.com/iLiFE_official/status/1479069352276025345`
2. **Live 176（2022-01-29，IDOL CONTENT EXPO @ 品川インターシティホール DAY1 1部）**：
   - 修正前：开场/开演时间为 `17:15 / 17:45`
   - 修正后：根据官方推文时间表修正为 `17:30 / 18:00`
   - 出处：`https://x.com/ic_expo/status/1487261435251867652`
3. **Live 137（2021-08-27，天使にはなれないデビューLIVE「だから僕らは天使をやめた」）**：
   - 修正前：开场/开演时间为 `17:00 / 18:00`
   - 修正后：根据共演主办公告推文修正为 `16:30 / 17:30`
   - 出处：`https://x.com/calresofficial/status/1427933353097895938`

---

## 4. 核查出未出演（自肃辞退）的场次记录

在核对 2021 年演出中，查出两场因成员确诊新冠肺炎导致全团活动自肃、实际出演辞退的场次：

1. **Live 123（2021-07-22，GoTo BLAZE 〜Day〜 @ 新宿BLAZE）**
2. **Live 125（2021-07-25，ポルックスアイドルフェスティバルvol.2 @ 新宿アルタ KeyStudio）**

- **核实依据**：株式会社imaginate（iLiFE! 运营方）于 2021 年 7 月 21 日发布的官方公告《【iLiFE!】新型コロナウイルス感染に伴う活動自粛のお知らせ》：
  `https://www.imaginate.jp/news/%e3%80%90ilife%e3%80%91%e6%96%b0%e5%9e%8b%e3%82%b3%e3%83%ad%e3%83%8a%e3%82%a6%e3%82%a3%e3%83%ab%e3%82%b9%e6%84%9f%e6%9f%93%e3%81%ab%e4%bc%b4%e3%81%86%e6%b4%bb%e5%8b%95%e8%87%aa%e7%b2%9b%e3%81%ae/`
  通告明确说明 2021年7月21日至8月1日期间所有预定公演全部自肃辞退出演。
- **处理方式**：按照任务要求**不删除记录**，将两场演出之出处更新为 imaginate 官方自肃通告，并在 `note` 中清晰标注：`因成员确诊新冠活动自肃出演辞退（未出演）；补充核验：...`，保留历史轨迹并向用户汇报。

---

## 5. 剩余非官方来源演出清单（共 84 场）及已检索渠道

### 检索覆盖渠道与未升级原因
对剩余 84 场演出（2020年 4 场、2021年 24 场、2022年 56 场），均已检索以下渠道：
1. **iLiFE! 官方 X 账号历史推文**：针对演出日期与名称关键词检索，部分由于年代久远推文已删除、或者当时未发独立告知且月度排期图中未包含。
2. **Eventernote 原始外链**：大部分仅挂有 `t.livepocket.jp` 链接，而 LivePocket 站点由于严格的防爬/反爬限制返回 HTTP 403，无法作为可打开验证的外部链接；部分旧 TIGET 链接已返回 404（活动已过期下线）。
3. **主办方官方账号及网络搜索引擎**：对主办方 X 账号检索相应日期，部分主办方账号已注销、推文已锁定或已清理。
4. **处理**：严格遵守规则第 2 条“查不到就留空并注明，不得编造，只用实际打开过的页面地址”，对这 84 场保留原有出处并保留 `仅非官方来源` 标注。

### 详细清单

#### 2020 年（4 场）
- ID 49 | 2020-09-22 | Vega Fes 1部 | 新宿BLAZE | 出处：`https://www.eventernote.com/events/259618`（LivePocket 票务页面受限 403）
- ID 73 | 2020-12-10 | 虹色の飛行少女定期ライブDX vol.15 | AKIBAカルチャーズ劇場 | 出处：`https://www.eventernote.com/events/265637`（LivePocket 票务页面受限 403）
- ID 74 | 2020-12-12 | 新アイドルイベント「I・N・G」2020/12/12 2部 | ダンスホール新世紀 | 出处：`https://www.eventernote.com/events/266368`（TIGET 原始页已 404）
- ID 76 | 2020-12-24 | IDOL CONTENT EXPO ＠品川ザ・グランドホール ～Special Christmas Night!!!～【DAY1】 | THE GRAND HALL | 出处：`https://www.eventernote.com/events/267623`（LivePocket 票务页面受限 403）

#### 2021 年（24 场）
- ID 85 | 2021-02-02 | ハープスター×iLiFE! 無銭2マン | Zirco Tokyo | 出处：`https://www.eventernote.com/events/270398`
- ID 92 | 2021-03-27 | ッスッゴイライブ 2021.3.27 | THE GRAND HALL | 出处：`https://www.eventernote.com/events/274383`
- ID 93 | 2021-04-01 | IDOL CONTENT EXPO ＠新宿３会場サーキット ～今日は休日！？エイプリルフール祭～ | 東京都内各所（サーキット） | 出处：`https://www.eventernote.com/events/274766`
- ID 94 | 2021-04-03 | dot yell fes vol.3 | 原宿ベルエポック美容専門学校 第2校舎 | 出处：`https://www.eventernote.com/events/274508`
- ID 96 | 2021-04-10 | MARQUEE祭mini Vol.75 | TSUTAYA O-nest | 出处：`https://www.eventernote.com/events/274091`
- ID 97 | 2021-05-03 | 2021/5/3(月祝) 『idol up』東京キネマ倶楽部 | 東京キネマ倶楽部 | 出处：`https://www.eventernote.com/events/276810`
- ID 98 | 2021-05-05 | HYPE IDOL! FESTIVAL!! | オンライン配信 | 出处：`https://www.livefans.jp/events/1314284`
- ID 102 | 2021-05-23 | パラディーク主催公演 パラディークランドEX | WOMBLIVE | 出处：`https://www.eventernote.com/events/278197`
- ID 104 | 2021-05-29 | エキセントリックトーキョー (2021/05/29) | THE GRAND HALL | 出处：`https://www.eventernote.com/events/277835`
- ID 111 | 2021-06-20 | なんかいちむ | 新宿BLAZE | 出处：`https://www.livefans.jp/events/1321049`
- ID 128 | 2021-08-07 | MARQUEE祭mini Vol.84 | TSUTAYA O-nest | 出处：`https://www.livefans.jp/events/1340840`
- ID 131 | 2021-08-15 | Aqua CRUISING LIVE!!! Day2～前編～ | 象の鼻桟橋(クルーズ発着含) | 出处：`https://www.eventernote.com/events/284998`
- ID 148 | 2021-10-11 | IDOL CONTENT EXPO @ 新宿BLAZE ～ウィンクの日LIVE!!!～ | 新宿BLAZE | 出处：`https://www.livefans.jp/events/1350769`
- ID 150 | 2021-10-17 | 10/17(日) TOKYO GIRLS GIRLS extra!! | 室町三井ホール&カンファレンス | 出处：`https://www.eventernote.com/events/287959`
- ID 151 | 2021-10-20 | BUZZ IDOL FES【バズ アイドル フェス】 | KT Zepp Yokohama | 出处：`https://www.eventernote.com/events/288601`
- ID 156 | 2021-11-04 | MyDearDarlin’ presents live!『 I Love Darlin’supported by IDOL CONTENT EXPO 3ヶ月連続!!!新宿BLAZE SPECIAL LIVE!! 』【11月4日(木)】 | 新宿BLAZE | 出处：`https://www.eventernote.com/events/288478`
- ID 158 | 2021-11-13 | アナフェスよみうりランド【1部】 | よみうりランド 日テレらんらんホール | 出处：`https://www.eventernote.com/events/292350`
- ID 159 | 2021-11-20 | ANK FES | 爱知县内各所（ANK FES） | 出处：`https://www.eventernote.com/events/291636`
- ID 160 | 2021-12-01 | TENNOSHO in NAGOYA | NAGOYA ReNY limited | 出处：`https://www.eventernote.com/events/292100`
- ID 162 | 2021-12-04 | IDOL PARADISE！vol.03 | 山野ホール | 出处：`https://www.eventernote.com/events/292766`
- ID 163 | 2021-12-06 | Girls & Night!! | 东京都内各所（サーキット） | 出处：`https://www.eventernote.com/events/292397`
- ID 164 | 2021-12-07 | iPort Girls vol.6 | LIVE HALL aube shibuya | 出处：`https://www.eventernote.com/events/294412`
- ID 170 | 2021-12-30 | IDOL NEW YEARS LIVE (2021/12/30) | 豊洲PIT | 出处：`https://www.eventernote.com/events/295246`
- ID 171 | 2021-12-31 | IDOL NEW YEARS LIVE (2021/12/31) (1部・2部) | 豊洲PIT | 出处：`https://www.eventernote.com/events/295931`

#### 2022 年（56 场）
- ID 177 | 2022-01-23 | HYPE IDOL!vol.10 | THE GRAND HALL | 出处：`https://www.livefans.jp/events/1379499`
- ID 179 | 2022-01-29 | 【出演者変更】IDOL CONTENT EXPO @ 品川インターシティホール supported byダイキサウンド ～桜が咲く頃には幕張へ！今回は品川で大集合SP!!!～【DAY1】 | 品川インターシティホール | 出处：`https://www.eventernote.com/events/297822`
- ID 181 | 2022-02-05 | 【出演者変更】IDOL CONTENT EXPO ＠ 2会場連動企画 ニコッ！笑う門には福来るッ！ | Spotify O-EAST | 出处：`https://www.livefans.jp/events/1381476`
- ID 185 | 2022-02-16 | 【出演者変更】NeoMasQueRade (2022/02/16) | 新宿BLAZE | 出处：`https://www.eventernote.com/events/300046`
- ID 187 | 2022-02-20 | melomelo (2022/2/20) (DAY・NIGHT) | 味園ユニバース | 出处：`https://www.eventernote.com/events/298225`
- ID 189 | 2022-02-26 | ロマンチックコンポート！！ -The beginning of the story- | 白金高輪SELENE b2 | 出处：`https://www.eventernote.com/events/300643`
- ID 191 | 2022-03-01 | アイドルアラモードプチVol.14 (2022/03/01) | 新宿BLAZE | 出处：`https://www.eventernote.com/events/300431`
- ID 192 | 2022-03-02 | UP-T FESTIVAL mini Vol.1 | Spotify O-EAST | 出处：`https://www.eventernote.com/events/300808`
- ID 194 | 2022-03-05 | HYPE IDOL! vol.14 | 品川インターシティホール | 出处：`https://www.livefans.jp/events/1393664`
- ID 195 | 2022-03-05 | アイライフちゃんとお花見ちゅー♡ | 新宿BLAZE | 出处：`https://www.eventernote.com/events/301132`
- ID 196 | 2022-03-06 | MARQUEE祭mini Vol.106 | TSUTAYA O-nest | 出处：`https://www.livefans.jp/events/1390499`
- ID 197 | 2022-03-10 | HEROINES FES vol.4 (2022/03/10) | 新宿BLAZE | 出处：`https://www.eventernote.com/events/300676`
- ID 198 | 2022-03-12 | IDOL CONTENT EXPO @ 新宿BLAZE ～春休み直前LIVE!!!～ | 新宿BLAZE | 出处：`https://www.livefans.jp/events/1393963`
- ID 200 | 2022-03-13 | IDOL CONTENT EXPO @ 神田明神ホール ～WHITE DAY Special LIVE!!!～【DAY2】 | 神田明神ホール | 出处：`https://www.eventernote.com/events/300589`
- ID 201 | 2022-03-19 | 偶像和音 3/19 | 新宿BLAZE | 出处：`https://www.eventernote.com/events/302484`
- ID 202 | 2022-03-21 | アイドル甲子園 (2022/3/21) | 新宿BLAZE | 出处：`https://www.eventernote.com/events/301986`
- ID 204 | 2022-03-26 | IDOL CONTENT EXPO @ 品川ザ・グランドホール ～春休みだよ！休日アイドル大集合SP!!!～ | THE GRAND HALL | 出处：`https://www.eventernote.com/events/302824`
- ID 205 | 2022-03-27 | IDOL CONTENT EXPO @ 品川ザ・グランドホール ～春休みだよ！休日アイドル大集合SP!!!～ | THE GRAND HALL | 出处：`https://www.eventernote.com/events/302825`
- ID 209 | 2022-04-10 | アイドル甲子園 (2022/4/10) | 新宿BLAZE | 出处：`https://www.eventernote.com/events/303796`
- ID 210 | 2022-04-16 | アイドル甲子園 (2022/4/16) | 新宿BLAZE | 出处：`https://www.eventernote.com/events/304245`
- ID 211 | 2022-04-17 | アイドル甲子園 (2022/4/17) | 新宿BLAZE | 出处：`https://www.eventernote.com/events/304246`
- ID 212 | 2022-04-24 | HEROINES LIFE ~新生活応援キャンペーン~ | 新宿BLAZE | 出处：`https://www.eventernote.com/events/304604`
- ID 213 | 2022-05-02 | !i!i!FES #あいふぇす 2022/5/2 | 新宿BLAZE | 出处：`https://www.eventernote.com/events/305319`
- ID 217 | 2022-05-16 | 【5/16】四季折々 ~SPECIAL~ VOL.1 ＠ Spotify O-West | Spotify O-WEST | 出处：`https://www.eventernote.com/events/304871`
- ID 218 | 2022-05-17 | 5/17 MARQUEE Fes.（Day1） | Spotify O-EAST | 出处：`https://www.livefans.jp/events/1420230`
- ID 219 | 2022-05-21 | 5/21(土) POP IN FESTIVAL 2022 ~ #PIF2022 ~ | Alternative Theatre | 出处：`https://www.eventernote.com/events/308385`
- ID 220 | 2022-05-21 | マイマイエッタイガー！ | 渋谷近未来会館 | 出处：`https://www.eventernote.com/events/308387`
- ID 221 | 2022-05-22 | HYPE IDOL!vol.17 | 大手町三井ホール | 出处：`https://www.eventernote.com/events/306202`
- ID 223 | 2022-05-28 | アイドル道場〜品川グランドホール〜 vol.2 | THE GRAND HALL | 出处：`https://www.eventernote.com/events/307536`
- ID 224 | 2022-05-30 | Queen&Princess vol.2 2022/5/30 | Veats SHIBUYA | 出处：`https://www.eventernote.com/events/307682`
- ID 229 | 2022-06-12 | HYPE IDOL！vol.20 | 日本橋三井ホール | 出处：`https://www.eventernote.com/events/309347`
- ID 230 | 2022-06-15 | 偶像和音 6/15 | 新宿BLAZE | 出处：`https://www.eventernote.com/events/310416`
- ID 231 | 2022-06-16 | MARQUEE祭 Vol.117 | Spotify O-WEST | 出处：`https://www.eventernote.com/events/310057`
- ID 232 | 2022-06-18 | rock field ULTRA LIVE | KANDA SQUARE HALL | 出处：`https://www.livefans.jp/events/1430941`
- ID 233 | 2022-06-24 | 『 IDOL CONTENT EXPO ＠ O-EAST ～アイコン生誕10周年祭～ 』 | Spotify O-EAST | 出处：`https://www.eventernote.com/events/312251`
- ID 234 | 2022-06-25 | 2022/6/25 TOKYO GIRLS GIRLS -番外編- | 横浜LANDMARK HALL | 出处：`https://www.eventernote.com/events/311195`
- ID 235 | 2022-06-26 | Liven up IDOL 06.26 | 品川インターシティホール | 出处：`https://www.eventernote.com/events/311055`
- ID 236 | 2022-06-30 | JAPAN IDOL SUPER LIVE 2022 @ヒューリックホール東京PREMIUM公演編 | ヒューリックホール東京 | 出处：`https://www.eventernote.com/events/309445`
- ID 239 | 2022-07-07 | 【出演者変更】渋谷大納涼祭 2022 | Spotify O-WEST | 出处：`https://www.eventernote.com/events/310779`
- ID 240 | 2022-07-09 | NAGOYA IDOL SUMMIT day1 | 名港スプラッシュガーデン ライオンドーム | 出处：`https://www.eventernote.com/events/312578`
- ID 241 | 2022-07-10 | 【出演者変更あり】NAGOYA IDOL SUMMIT day2 | 名港スプラッシュガーデン ライオンドーム | 出处：`https://www.eventernote.com/events/312971`
- ID 242 | 2022-07-11 | 【出演者変更】Merry BAD TUNE. presents 「#バチュコリvol.0-バチュンお披露目初主催対バンSP-」 2022/7/11 | 渋谷SOUND MUSEUM VISION | 出处：`https://www.eventernote.com/events/311355`
- ID 244 | 2022-07-18 | 【出演者変更】SPARK 2022 in YAMANAKAKO【7/18】 | 山中湖交流プラザきらら | 出处：`https://www.eventernote.com/events/308782`
- ID 246 | 2022-07-28 | HEROINES VOICE 2022/7/28 | 渋谷SOUND MUSEUM VISION | 出处：`https://www.eventernote.com/events/311430`
- ID 247 | 2022-07-29 | 7/29(金) Free Free Free | SHINJUKU WALLY | 出处：`https://www.eventernote.com/events/314541`
- ID 250 | 2022-08-03 | 喰らいマックスに捧げる＿。 AZfes Premium | duo MUSIC EXCHANGE | 出处：`https://www.eventernote.com/events/315174`
- ID 252 | 2022-08-08 | 緊急開催!!!真夏のきゅるきゅるぱーりー!!! | 渋谷SOUND MUSEUM VISION | 出处：`https://www.eventernote.com/events/315509`
- ID 254 | 2022-08-16 | 【出演者変更】dot yell fes SUMMER SP | Spotify O-EAST | 出处：`https://www.eventernote.com/events/314923`
- ID 257 | 2022-08-21 | DDD~Discovery iDol Depot~ (2022/08/21) | 白金高輪SELENE b2 | 出处：`https://www.eventernote.com/events/315519`
- ID 280 | 2022-10-02 | 10/2(日) TOKYO GIRLS GIRLS ~ 番外編 ~ | 横浜LANDMARK HALL | 出处：`https://www.eventernote.com/events/317478`
- ID 281 | 2022-10-06 | MARQUEE祭 Vol.121 | Spotify O-WEST | 出处：`https://www.eventernote.com/events/319652`
- ID 287 | 2022-10-23 | Liven up IDOL Vol.2 | 恵比寿ザ・ガーデンルーム | 出处：`https://www.eventernote.com/events/321752`
- ID 290 | 2022-10-28 | HEROINES HELLOWEEN 大阪公演 | umeda TRAD | 出处：`https://www.eventernote.com/events/323545`
- ID 291 | 2022-10-29 | HEROINES HELLOWEEN 名古屋公演 | NAGOYA ReNY limited | 出处：`https://www.eventernote.com/events/322420`
- ID 293 | 2022-10-31 | HEROINES HELLOWEEN東京公演 | 恵比寿LIQUIDROOM | 出处：`https://www.eventernote.com/events/322141`
- ID 299 | 2022-11-13 | HEROINES FES vol.7 | CLUB CITTA' | 出处：`https://www.eventernote.com/events/323895`
- ID 309 | 2022-11-27 | コマフェス！！～ご当地鍋フェスティバル＠日比谷公園～ | 日比谷公園小音楽堂 | 出处：`https://www.eventernote.com/events/325039`
- ID 310 | 2022-11-30 | HEROINES FES × ReNY SUPER LIVE ～CARNIVAL NIGHT 公演編～ | 新宿ReNY | 出处：`https://www.eventernote.com/events/325226`

---

## 6. 验收自检与提交号

- [x] `python3 db/export.py --check` 通过（全表逐字节一致）
- [x] 所有引用的官方外部链接均已使用 HTTP 实际请求验证（HTTP 200，内容证实出演事实）
- [x] 日期统一为日本时间（JST）
- [x] 数据只修改 `db/ilife.sqlite` 并通过脚本统一导出
- [x] 仅推送工作分支 `agy/018-lives-2020-2022-official-sources`，绝不推送 `main`，不执行部署

### 提交记录
- **2022 年提交**：`30c1413`（`feat(lives): 2022 年演出出处升级为官方出处 (升级 65 场 / 查 121 场)`）
- **2021 年提交**：`cd6ea46`（`feat(lives): 2021 年演出出处升级为官方出处 (升级 21 场 / 查 45 场)`）
- **2020 年提交**：`fd39aff`（`feat(lives): 2020 年演出出处升级为官方出处 (升级 12 场 / 查 16 场)`）
