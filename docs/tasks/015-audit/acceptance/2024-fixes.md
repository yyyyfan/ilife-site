# 2024 年验收修正清单（对应 2024-fixes.py）

适用范围：codex/015-lives-2023-2026 的 1ad0a5f 及之后的提交。已在 1ad0a5f 的副本上测试；在 c33fccb 的副本上先跑 2023-fixes.py 再跑本脚本，也测试过。
用法：在仓库根目录先运行 `python3 /workspace/015-acceptance/2024-fixes.py db/ilife.sqlite`（可加 `--dry-run` 预览），再运行 `python3 db/export.py` 和 `python3 db/export.py --check`。
可以重复运行：已修正的项显示 ALREADY；记录不存在或已被改成别的值时显示 SKIP，脚本不会强改。共 37 项操作，涉及 23 场演出和 1 个会场。

## A. 出处升级（10 场；原链接保留在 note 中作为补充核验）
| ID@1ad0a5f | 日期 | 标题 | 原出处 | 新主出处 |
|---|---|---|---|---|
| 542 | 2024-04-28 | 向日えな生誕祭「プリンセスえなピーチ」 | Eventernote 379965 | https://x.com/iLiFE_official/status/1779827029766230245 （图：04/28 OPEN16:00 START17:00 @ステラボール） |
| 549 | 2024-05-08 | ヒロインズ無銭LIVE 2部(2024/5/8) | Eventernote 379068 | https://x.com/iLiFE_official/status/1782715464789139497 （图：2部 iLiFE! OPEN14:00 START15:00 @CLUB CITTA'） |
| 582 | 2024-07-24 | コカ･コーラ SUMMER STATION 音楽LIVE … iLiFE! | Eventernote 384147 | https://x.com/iLiFE_official/status/1807700783070408990 （「単独出演」，OPEN18:15 START19:00） |
| 610 | 2024-09-29 | HEROINES SUMMER 2024 番外編 DAY2 | Eventernote 392708 | https://ticketdive.com/event/heroinessummer2409 （主办方售票页，Day2 出演有 iLiFE!） |
| 626 | 2024-11-12 | HEROINES アルバムリリースイベント iLiFE! 池袋サンシャイン広場 1部 | Eventernote 400133 | https://x.com/iLiFE_official/status/1855548138523926575 （时间变更告知 ①11:30/②15:00） |
| 629 | 2024-11-17 | HEROINES ALBUM 2025 リリースイベント（COCONO SUSUKINO） | 官方月度排期图 1851966193760112768 | https://x.com/iLiFE_official/status/1855548138523926575 （改为 13:30〜） |
| 636 | 2024-12-07 | HEROINES ALBUM 2025 リリースイベント in兵庫 | Eventernote 405352 | https://x.com/iLiFE_official/status/1864905119185375535 |
| 641 | 2024-12-17 | HEROINES ALBUM 2025 リリースイベント 2部 | Eventernote 410542 | https://x.com/iLiFE_official/status/1864905119185375535 |
| 647 | 2024-12-28 | HEROINES COUNTDOWN Day1 | Eventernote 401471 | https://x.com/iLiFE_official/status/1871450844270666188 |
| 648 | 2024-12-29 | HEROINES COUNTDOWN Day2 | Eventernote 401472 | https://x.com/iLiFE_official/status/1871450844270666188 |
升级后这 9 场 Eventernote 主出处的场次都去掉了 `仅非官方来源` 标注。

## B. 错误修正
- 623（2024-11-03 リリイベ）：会场由「なんばパークス 2F（大阪）」改为新会场「北九州リバーウォーク（福冈）」，地址和容量留空。依据：主出处的官方排期图上写的是「11/3(日) 12:00～ @北九州リバーウォーク(福岡)」。改完后会场「なんばパークス 2F」没有任何演出引用，脚本把它删除。
- 650（2024-11-04 JAPANLiFE! 金沢）：开演时间由 15:30 改为 15:10。依据：官方巡演图写的是「金沢エイトホール OPEN 14:30 START 15:10」。
- 629（2024-11-17 COCONO SUSUKINO）：开演时间由 14:00 改为 13:30。依据：官方 2024-11-10 发的时间变更告知。
- 641（2024-12-17 2部）：开场时间由 16:00 改为 16:20（官方写第2部集合 16:20，开演 17:00）；note 里补记同日第1部 13:30～。
- 582（SUMMER STATION）：类型由「主催」改为「ワンマン」。依据：官方说明这是 iLiFE! 单独出演，主办方是テレビ朝日的 SUMMER STATION，不是 iLiFE! 主办。

## C. 补全（官方主出处告知图上能直接看到时间，库里为空）
- 534 JAPANLiFE! 东京 FINAL（3/30）：16:00 / 17:00
- 536 iLiVE! Vol.12：09:30 / 10:30
- 553 iLiVE! Vol.13：10:00 / 11:00（以官方图为准；TicketDive 写的开演是 10:30，已记入 note）
- 562 Cinderella Fes：开演 14:00
- 564 iLiVE! Vol.14：09:30 / 10:00
- 570 NAMBALiFE!（6/23）：10:30 / 11:15
- 577 馬鹿LiFE!：12:30 / 13:15
- 587 新体制お披露目LIVE：11:15 / 12:00
- 624 DERARALiFE!：10:30 / 11:00
- 573 / 574 超NATSUZOME 两天：note 里补充说明「楽天チケット页是两日通票，只列两天合并的出演者；每天是否出演以 Eventernote / LiveFans 的详情页为依据」。

## 删除
- 演出：0 场。
- 会场：1 个（「なんばパークス 2F」，只有 623 这一场引用它，而且是错的）。
