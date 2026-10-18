# 012 返工：010 的 2022 年演出出处（验收未通过）

状态：待开工（另：ID 44、59、115 的出处推文正文没提 iLiFE!，请换成能直接看到出演的帖子）

## 问题
010 验收时逐条打开了全部 169 个 Eventernote/LiveFans 出处（2020–2022），**69 个（全在 2022 年）指向与 iLiFE! 无关的页面**（页面上没有 iLiFE!，日期也不符），即出处 ID 是编造的。逐条结果：`/workspace/audit/ext_src_check.json`。

另外两处官方推文不符：
- ID 192 向日えな生誕祭：推文 1492403557764845572 标题是『え、なにする？』，库里写成『えなぴわーるど』。
- ID 279 ficfes vol.2（2022-09-27）：推文 1566756781615104001 是『i-LAND!!』告知，正文里没有这场演出。
- ID 313 HYPEIDOL！DX（12-02）：推文只讲特典贴纸，没提这场演出，需换成告知帖。

新增会场（38 个）的容纳人数，在所引官网首页上 8 个里只核到 1 个（渋谷近未来会館 300）。每个容纳人数都要给出能看到这个数字的具体页面 URL，找不到就留空。

## 要求
1. 下面 69 场逐场重新找真实出处（优先官方 X/主办方），找到就替换 URL 并核对日期、会场、标题；找不到真实页面的场次**删除**，不得保留无出处的数据。
2. 修正 192、279、313。
3. 会场容纳人数逐个补具体出处，否则置空。
4. 写一个校验脚本 `db/check_sources.py`：抓取每个非官方出处页面，确认页面含 iLiFE! 且日期一致，并加入 export --check 的流程说明。
5. `python3 db/export.py --check` 通过后提交推送，状态改为待验收。不要部署。

## 69 场出处无效的演出
| ID | 日期 | 标题 | 出处 | 实际页面 |
|---|---|---|---|---|
| 174 | 2022-01-09 | IDOL CONTENT EXPO ＠ ヒューリックホール東京～年明け3DAYS SPライブ!!!～【DAY2】 | https://www.livefans.jp/events/1376880 | 三浦祐太朗 ＠ 千葉市民会館 大ホール (千葉県) (2022.03.13) / ライブ・セットリスト情報サービス【 L |
| 179 | 2022-01-29 | 【出演者変更】IDOL CONTENT EXPO @ 品川インターシティホール supported byダイキサウンド ～桜が咲く頃には幕張へ！今回は品川で大集合SP!!!～【DAY1】 | https://www.livefans.jp/events/1378103 | Mr.ふぉるて ＠ 生配信ライブ (2022.01.17) / ライブ・セットリスト情報サービス【 LiveFans ( |
| 180 | 2022-02-02 | 【出演者変更】ツインテールフェス 2022 | https://www.livefans.jp/events/1381254 | BAND FOR HAPPY Tour 2022 ＠ 豊橋club KNOT (愛知県) (2022.06.11) /  |
| 181 | 2022-02-05 | 【出演者変更】IDOL CONTENT EXPO ＠ 2会場連動企画 ニコッ！笑う門には福来るッ！ | https://www.livefans.jp/events/1384078 | くれよんちゅーどく ＠ 白金高輪SELENE b2 (東京都) (2022.02.13) / ライブ・セットリスト情報サ |
| 183 | 2022-02-11 | 【出演者変更】IDOL CONTENT EXPO ＠品川ザ・グランドホール ～バレンタインSP LIVE!!!～ | https://www.livefans.jp/events/1384090 | Bety ＠ 白金高輪SELENE b2 (東京都) (2022.02.13) / ライブ・セットリスト情報サービス【  |
| 184 | 2022-02-13 | HEROINES VALENTINE'S | https://www.livefans.jp/events/1387216 | LiveFans / ライブ・セットリスト情報サービス【 LiveFans (ライブファンズ) 】 |
| 187 | 2022-02-20 | melomelo (2022/2/20) (DAY・NIGHT) | https://www.eventernote.com/events/300223 | 『ブルーサーマル』学生証試写会　3回目 Eventernote イベンターノート |
| 188 | 2022-02-22 | #にゃんなな | https://www.eventernote.com/events/300898 | アキバ大作戦-NIGHT- ☑mate. Eventernote イベンターノート |
| 189 | 2022-02-26 | ロマンチックコンポート！！！！ | https://www.eventernote.com/events/300994 | アイドル好きで何がわるい（2022/2/28） SPRISE-スプライズ- Eventernote イベンターノート |
| 191 | 2022-03-06 | MAGNETIC FESTIVAL in 大手町三井ホール　ひな祭りスペシャル　DAY2 | https://www.livefans.jp/events/1390494 | AIRFLIP ＠ 八戸LIVE HOUSE FOR ME (青森県) (2022.03.05) / ライブ・セットリス |
| 194 | 2022-03-12 | 【出演者変更】IDORISE!! FESTIVAL 2022【DAY1】 | https://www.livefans.jp/events/1384074 | 【eN】 ＠ 白金高輪SELENE b2 (東京都) (2022.02.13) / ライブ・セットリスト情報サービス【  |
| 195 | 2022-03-13 | GoTo BLAZE〜NIGHT〜 (2022/03/13) | https://www.eventernote.com/events/302824 | 伊東歌詞太郎 TVアニメ「乙女ゲー世界はモブに厳しい世界です」オープニングテーマ「サイレントマイノリティー」発売記念イベ |
| 196 | 2022-03-15 | HEROINES WHITEDAY | https://www.eventernote.com/events/302061 | イケてるハーツ6大都市ツアー「日・SING・月・歩」福岡公演前日!!特別フリーライブ イケてるハーツ(Stand-Up! |
| 197 | 2022-03-17 | MARQUEE祭 Vol.114 | https://www.eventernote.com/events/301552 | 楽遊アイドルフェス～ひなまつりSP〜 虹色幻想曲～プリズム・ファンタジア～ Eventernote イベンターノート |
| 198 | 2022-03-19 | LEADING!!!（2022/03/19） | https://www.eventernote.com/events/302905 | 舞台「東京リベンジャーズ ―血のハロウィン編―」3/26 17:30 木津つばさ Eventernote イベンターノー |
| 199 | 2022-03-20 | エキセントリックオッドー 2022/03/20 | https://www.eventernote.com/events/302825 | TVアニメ『SPY×FAMILY』第1話・第2話最速プレミア上映＆トークショー 江口拓也 Eventernote イベン |
| 200 | 2022-03-22 | TYAO！vol.2 | https://www.eventernote.com/events/301041 | BS11「虹マジ」Presents 虹のコンキスタドールSpecial LIVE 〜ラストに本気出していいですか!?〜  |
| 201 | 2022-03-27 | HYPE IDOL！vol.15 | https://www.livefans.jp/events/1393668 | LiveFans / ライブ・セットリスト情報サービス【 LiveFans (ライブファンズ) 】 |
| 202 | 2022-04-03 | dot yell fes 1周年sp | https://www.livefans.jp/events/1402263 | シャニムニ=パレード ＠ mistFES2022 (出演日未定) / ライブ・セットリスト情報サービス【 LiveFan |
| 203 | 2022-04-11 | 〇〇しか勝たんフェス in spotify O-EAST | https://www.eventernote.com/events/303975 | Re:BRE FUNTOS名阪弾丸ツアー『ONE SHOT』〜名古屋狼煙編〜【4/3 サンシャインサカエ 3部】 Re: |
| 204 | 2022-04-12 | LEADING ID -Birthday Special- 2022/04/12 | https://www.livefans.jp/events/1403649 | BLUE FOREST &amp; ONE TO ONE AGENCY COUPLING TOUR『 GREAT VIG |
| 205 | 2022-04-13 | 「ReNY SUPER LIVE 2022」Presented by SHINJUKU ReNY～APRIL.SUPER PREMIUM公演編 | https://www.eventernote.com/events/304724 | FOUR SHOTS -free- (2022/04/07) ポスタルジア Eventernote イベンターノート |
| 206 | 2022-04-14 | MARQUEE祭 Vol.115 | https://www.eventernote.com/events/303358 | シャニムニ=パレード サンシャインサカエ定期LIVE vol.17 シャニムニ=パレード Eventernote イベン |
| 210 | 2022-04-27 | Girls & Night!!(2022/04/27) | https://www.livefans.jp/events/1410291 | セカモノ ＠ 新宿ReNY (東京都) (2022.04.25) / ライブ・セットリスト情報サービス【 LiveFan |
| 211 | 2022-04-28 | NEW HEROINES LIFE ~新生活応援キャンペーン~ | https://www.eventernote.com/events/305273 | 【4/27】『オフィスの国のアリス』【延期公演】 松村芽久未 Eventernote イベンターノート |
| 212 | 2022-04-30 | HYPE IDOL! GWSP DAY2 | https://www.eventernote.com/events/304677 | 【キャスト変更】eeo Stage reading 朗読劇『この色、君の声で聞かせて』◆チームVOICE 5/28 11 |
| 213 | 2022-05-02 | !i!i!FES #あいふぇす 2022/5/2 | https://www.eventernote.com/events/305713 | ゲキモリdeパーリナイVol.47 あいたいね！ Eventernote イベンターノート |
| 214 | 2022-05-03 | HYPE IDOL! GWDX【DAY1】 | https://www.livefans.jp/events/1412555 | the studs ＠ Electric Lady Land (愛知県) (2008.07.12) / ライブ・セットリ |
| 215 | 2022-05-04 | 【出演者変更】HYPE IDOL! GWDX【DAY2】 | https://www.livefans.jp/events/1412560 | CROSS GATE 2008～The Colored World～ ＠ BIGCAT (大阪府) (2008.07.1 |
| 217 | 2022-05-16 | 【5/16】四季折々 ~SPECIAL~ VOL.1 ＠ Spotify O-West | https://www.eventernote.com/events/307405 | HIMEMI＆ayaho presents Lupinus  ayaho Eventernote イベンターノート |
| 218 | 2022-05-17 | 5/17 MARQUEE Fes.（Day1） | https://www.livefans.jp/events/1414441 | 打首獄門同好会 ＠ Electric Lady Land (愛知県) (2022.04.23) / ライブ・セットリスト |
| 221 | 2022-05-22 | HYPE IDOL!vol.17 | https://www.eventernote.com/events/308006 | 劇団ココア二大悲劇「PIERROT×プロとコントラ」『プロとコントラ』 2022年6月8日 19:30 小鳥遊彩乃 Ev |
| 222 | 2022-05-27 | HEROINES Party | https://www.eventernote.com/events/308630 | 鉄の七拍子～東名七組のグループがDtに集結！～ 1部 逆転ねこぱんちっ！(ex.#あんのわーるど) Eventernot |
| 223 | 2022-05-28 | アイドル道場〜品川グランドホール〜 vol.2 | https://www.eventernote.com/events/308298 | 2022年5月22日(日)  『SAY-LA 小椋妃奈乃 復帰公演』 SAY-LA Eventernote イベンターノ |
| 224 | 2022-05-30 | Queen&Princess vol.2 2022/5/30 | https://www.eventernote.com/events/307412 | 舞台『ダディ』 東京公演 7/18 13:00 中山優馬 Eventernote イベンターノート |
| 225 | 2022-05-31 | JAPAN IDOL SUPER LIVE 2022 @豊洲PIT公演 春の大祭典編 | https://www.livefans.jp/events/1416327 | 桃色革命 ＠ SPACE ODD (東京都) (2019.01.27) / ライブ・セットリスト情報サービス【 Live |
| 226 | 2022-06-02 | HEROINES FES | https://www.eventernote.com/events/308890 | 「利根健太朗・緒方佑奈の検証TV！～秋の検証祭り2022～」夜の部 利根健太朗 Eventernote イベンターノート |
| 229 | 2022-06-12 | HYPE IDOL！vol.20 | https://www.eventernote.com/events/309995 | 令和四年 三条凧合戦 開会式 稲垣好 Eventernote イベンターノート |
| 230 | 2022-06-15 | 偶像和音 6/15 | https://www.eventernote.com/events/310344 | GRANRODEO『15th Anniversary Book　G15/G16 ROCK☆SHOW』発売記念お渡し会イベ |
| 231 | 2022-06-16 | MARQUEE祭 Vol.117 | https://www.eventernote.com/events/309449 | 第8回 リバコメ!!「PSYCHO-PASS サイコパス」昼公演 関智一 Eventernote イベンターノート |
| 233 | 2022-06-24 | 『 IDOL CONTENT EXPO ＠ O-EAST ～アイコン生誕10周年祭～ 』 | https://www.livefans.jp/events/1430154 | knowone ＠ SAKAE SP-RING 2022 (2022.06.05) / ライブ・セットリスト情報サービス |
| 234 | 2022-06-25 | 2022/6/25 TOKYO GIRLS GIRLS -番外編- | https://www.livefans.jp/events/1431665 | CANDY GO!GO! ＠ 庄和総合公園 (2018.05.20) / ライブ・セットリスト情報サービス【 LiveF |
| 235 | 2022-06-26 | Liven up IDOL 06.26 | https://www.livefans.jp/events/1433282 | 踊ってばかりの国 ＠ SHIBUYA SOUND RIVERSE 2022 (2022.06.05) / ライブ・セット |
| 236 | 2022-06-30 | JAPAN IDOL SUPER LIVE 2022 @ヒューリックホール東京PREMIUM公演編 | https://www.eventernote.com/events/310931 | Kiyono Yasuno 5th Anniversary Live Tour 2023 ～It’s A PIECE O |
| 237 | 2022-07-02 | HEROINESの夏開き 2022/7/2 | https://www.eventernote.com/events/310780 | unichan 定期公演 Vol.2 unichan Eventernote イベンターノート |
| 239 | 2022-07-07 | 【出演者変更】渋谷大納涼祭 2022 | https://www.livefans.jp/events/1436109 | FROM ME. ＠ Music Bar SINKAGURA (大阪府) (2022.03.30) / ライブ・セットリ |
| 240 | 2022-07-09 | NAGOYA IDOL SUMMIT day1 | https://www.livefans.jp/events/1435277 | エガフェス 2022 ＠ LINE CUBE SHIBUYA (東京都) (2022.09.30) / ライブ・セットリ |
| 243 | 2022-07-12 | JAPAN IDOL SUPER LIVE 2022 @豊洲PIT公演 夏の大祭典編 | https://www.livefans.jp/events/1439294 | 輝山立 ＠ Water Rand (2022.08.07) / ライブ・セットリスト情報サービス【 LiveFans ( |
| 244 | 2022-07-18 | 【出演者変更】SPARK 2022 in YAMANAKAKO【7/18】 | https://www.livefans.jp/events/1446733 | 水中、それは苦しい ＠ 金沢21世紀美術館 シアター21 (石川県) (2022.08.14) / ライブ・セットリスト |
| 246 | 2022-07-28 | HEROINES VOICE 2022/7/28 | https://www.eventernote.com/events/313364 | KissBee 7/12発売 ニューシングル「時空ノイズ」発売記念イベント ミニライブ＆特典会 7/17 17:00 K |
| 247 | 2022-07-29 | 7/29(金) Free Free Free | https://www.eventernote.com/events/313884 | ジャンプビクトリーカーニバル2022 遊戯王ゴーラッシュ!!声優スペシャルデュエルステージ 3回目 福島香々 Event |
| 250 | 2022-08-03 | 喰らいマックスに捧げる＿。 AZfes Premium | https://www.eventernote.com/events/313795 | TVアニメ「ラブライブ！スーパースター!!」2期 結ヶ丘のみんなで振り返り上映会☆☆【第3回】 Liella! Even |
| 252 | 2022-08-08 | 緊急開催!!!真夏のきゅるきゅるぱーりー!!! | https://www.eventernote.com/events/314781 | &quot;危険な&quot;アナフェス 〜閉館前ラスト!!〜 SUPER JYAPON(JYA☆PON 2.0) Ev |
| 253 | 2022-08-14 | HEROINES SUMMER FES | https://www.eventernote.com/events/314120 | 新山詩織 アコースティックlive 2022 ～夏の終わり～ ＜1st＞  新山詩織 Eventernote イベンター |
| 255 | 2022-08-18 | MARQUEE祭 Vol.119 | https://www.eventernote.com/events/314545 | 人生ゆるふわぷれい勢vol.5 -夜の部- KiMiNiAiTAi Eventernote イベンターノート |
| 257 | 2022-08-21 | DDD~Discovery iDol Depot~ (2022/08/21) | https://www.livefans.jp/events/1454652 | DIAURA ＠ 梅田バナナホール (大阪府) (2022.07.30) / ライブ・セットリスト情報サービス【 Liv |
| 259 | 2022-08-27 | 「 Tokyo Asoba Night!! 」 - VISION IDOL Last Live - | https://www.eventernote.com/events/316024 | “お家からはじめる” Dream声優オーディション2022 ～君の声が未来を切り開く～ アリオ倉敷 最終公開オーディショ |
| 260 | 2022-08-30 | 偶像和音-HEROINES JACK- | https://www.livefans.jp/events/1462060 | SECRET 7 LINE ＠ LIVE HOUSE enn 2nd (宮城県) (2022.08.21) / ライブ・ |
| 269 | 2022-09-14 | 9/14 MARQUEE Fes.<day2> | https://www.livefans.jp/events/1460594 | THE STARBEMS ＠ CLUB CITTA&#039;川崎 (神奈川県) (2022.09.23) / ライブ・ |
| 270 | 2022-09-15 | HEROINES PARTY vol.3.5 | https://www.eventernote.com/events/318182 | W.ダブルヴィ一定期公演#36 W.ダブルヴィー Eventernote イベンターノート |
| 272 | 2022-09-18 | HYPE IDOL！vol.21 | https://www.eventernote.com/events/318285 | 虹のコンキスタドール 全国美味いもの征服ツアー2022 高知公演 虹のコンキスタドール Eventernote イベンタ |
| 282 | 2022-10-02 | 10/2(日) TOKYO GIRLS GIRLS ~ 番外編 ~ | https://www.eventernote.com/events/320144 | にじさんじフェス 2022 1日目視聴覚室鈴木勝 鈴木勝 Eventernote イベンターノート |
| 283 | 2022-10-06 | MARQUEE祭 Vol.121 | https://www.eventernote.com/events/319692 | 秋のヘッドフォン祭2022（ベストアルバム「ZAQPOT」発売記念　ZAQトークイベント supported by HI |
| 284 | 2022-10-09 | HYPE IDOL！vol.25【9日(日)】 | https://www.eventernote.com/events/320499 | アムホール37周年記念LiveDarling SP. ～Okagesamadesu！Day～ W.ダブルヴィー Even |
| 287 | 2022-10-19 | 煌めき☆アンフォレント 達家真姫宝生誕公演 | https://www.livefans.jp/events/1474945 | 絵恋ちゃん&amp;でか美ちゃん ＠ NAKAYOSHI FES. 2022 (2022.09.24) / ライブ・セッ |
| 289 | 2022-10-23 | Liven up IDOL Vol.2 | https://www.eventernote.com/events/322305 | FRUITS ZIPPER 1st LIVE TOUR 2023 WINTER 〜FRUITSの日〜 FRUITS ZI |
| 295 | 2022-10-31 | HEROINES HELLOWEEN東京公演 | https://www.eventernote.com/events/323287 | アンジュルム 31stシングル『悔しいわ/Piece of Peace～しあわせのパズル～』発売記念 ＜チェキ・サイン・ |
| 298 | 2022-11-04 | HEROINES FES vol.6 | https://www.eventernote.com/events/323385 | アナフェス新宿【1部】 ネコプラpixx. Eventernote イベンターノート |
| 299 | 2022-11-05 | アイドルアラモードVol.11 | https://www.eventernote.com/events/322896 | 「hy4_4yh（ハイパーヨーヨ）のYAVAYトークGIG！〜ハイパヨの歴史を振り返っちゃおうSPその6〜」 hy4_4 |
