# 2025 年验收修正清单（对应 2025-fixes.py）

适用：codex/015-lives-2023-2026 的 c33fccb 及之后的提交（已在 c33fccb 的仓库副本上测试；与 2023-fixes.py 叠加运行无冲突；在 Codex 最新提交 c4fd0d7 的 DB 副本上 --dry-run 为 applied=18 skip=0）。
用法：在仓库根目录先运行 `python3 /workspace/015-acceptance/2025-fixes.py db/ilife.sqlite`（可加 `--dry-run` 预览），再运行 `python3 db/export.py` 和 `python3 db/export.py --check`。
重复运行是安全的：已修正的项显示 ALREADY；记录不存在或已被改成别的值时显示 SKIP，脚本不会强改。

## A. 出处升级：Eventernote → 官方 X（9 场，原 Eventernote 链接保留在 note 中作为补充核验）
| ID@c33fccb | 日期 | 标题 | 新主出处 |
|---|---|---|---|
| 657 | 2025-01-17 | iLiFE! アルバム『HEROINES ALBUM 2025』ミニライブ＆特典会 | https://x.com/iLiFE_official/status/1878397590510924110 （1 月リリイベ排期图：1/17(金) 17:00～ @DiverCity；note 注明「来源为月度排期图」） |
| 663 | 2025-02-01 | HEROINES ALBUM 2025 ミニライブ&特典会 | https://x.com/iLiFE_official/status/1885236597198873048 （场地改为ららぽーと柏の葉，開演 17:30） |
| 677 | 2025-03-14 | HEROINES WHITEDAY 2025 Day2 | https://x.com/iLiFE_official/status/1894704198337561061 （第 2 张图 DAY2 @KANDA SQUARE HALL 12:00/12:30） |
| 684 | 2025-04-01 | iLiFE! ゲリラフリーライブ @ 新宿ReNY | https://x.com/iLiFE_official/status/1906730827993735619 （「本日緊急無銭ライブ開催」，引用 @heroines_idol 号外图 13:00/14:00） |
| 738 | 2025-09-24 | HEROINES LEAGUE Ⅰ【Sep. part2】 | https://x.com/iLiFE_official/status/1965024931953176985 （@EX Theater Roppongi 14:00/15:00） |
| 739 | 2025-09-27 | 「東京ゲームショウ2025」…iLiFE!スペシャルライブ | https://x.com/iLiFE_official/status/1971137865330679823 （出演 15:00〜，コナミブース ホール5） |
| 749 | 2025-10-31 | HEROINES HALLOWEEN -PREMIUM-  2025/10/31 | https://x.com/iLiFE_official/status/1974023027160473670 （@Spotify O-EAST 10:00/10:30） |
| 752 | 2025-11-09 | 昭和女子大学 第33回秋桜祭 iLiFE! 秋桜祭 LIVE 2025 | https://x.com/iLiFE_official/status/1973592128010985815 （@人見記念講堂 16:00/17:00） |
| 768 | 2025-12-31 | HEROINES COUNTDOWN 2025-2026 | https://x.com/iLiFE_official/status/1969310642772590606 （@Kanadevia Hall，告知时 OPEN/START TBD；时间仍以 Eventernote 为准） |

## B. 错误修正
- 663 HEROINES ALBUM 2025 ミニライブ&特典会（2025-02-01）：start_time 11:30 → 17:30，open_time 10:00 → 留空。依据：官方 2025-01-31 告知「開演時間:17:30／10:00より優先エリア入場券配布開始」；原值是 Eventernote 上整场活动的时间。

## C. 补全（官方/主办方页面上能直接看到）
- 705 TRAVE LiFE! 台北公演：open 17:30、start 18:30（官方 2025-06-05 告知 1930588831113531395；note 追加此依据）
- 687 たかねこフェスvol.4 出張編 福岡 第二部 iLiFE!：open 17:30、start 18:30（高嶺のなでしこ官网主出处页「第二部[OPEN/START] 17:30/18:30 出演：iLiFE!」）
- 769 第9回 ももいろ歌合戦：open 12:30、start 13:50（ももクロ官网「開場12:30予定 / 開演13:50予定」）

## 删除
无。

## 未修改、只作线索（见 2025.md「发现的问题」第 4、5 条）
- 可能漏收：5/11、7/14 HEROINES LEAGUE I（官方出演告知 1919605492437205427、1933436251853763047），10/8 LEAGUE 決勝戦（排期图上写「開催予定」）。
- 类型待定：745 HEROINES HALLOWEEN in OSAKA、751 Rikkyo Idol Stage 目前为「対バン」。
