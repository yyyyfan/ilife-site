# 2023 年验收修正清单（对应 2023-fixes.py）

适用：codex/015-lives-2023-2026 的 0425dc8 及之后的提交（已在 0425dc8 和 1ad0a5f 的副本上测试）。
用法：在仓库根目录先运行 `python3 /workspace/015-acceptance/2023-fixes.py db/ilife.sqlite`（可加 `--dry-run` 预览），再运行 `python3 db/export.py` 和 `python3 db/export.py --check`。
重复运行是安全的：已修正的项显示 ALREADY；记录不存在或已被改成别的值时显示 SKIP，脚本不会强改。

## A. 出处升级：Eventernote → 官方 X（15 场，原 Eventernote 链接保留在 note 中作为补充核验）
| ID@0425dc8 | 日期 | 标题 | 新主出处 |
|---|---|---|---|
| 330 | 2023-01-04 | 1stアルバム ミニライブ＆特典会 1/4 | https://x.com/iLiFE_official/status/1609542842975940608 （月度排期图） |
| 333 | 2023-01-09 | 同 1/9 | 同上 |
| 340 | 2023-01-15 | 同 1/15（ヴィレッジヴァンガード名古屋パルコ店） | 同上 |
| 337 | 2023-01-13 | リリイベ完走ありがとうLIVE（1部・2部） | https://x.com/iLiFE_official/status/1610221073873915904 |
| 345 | 2023-02-03 | ゲリラ無銭LIVE! 【第1部 iLiFE!編】 | https://x.com/iLiFE_official/status/1621101364108734466 |
| 375 | 2023-04-05 | iLiVE! Vol.6 | https://x.com/iLiFE_official/status/1637756707563778048 |
| 376 | 2023-04-08 | femmeLiFE! | https://x.com/iLiFE_official/status/1639583687229706241 |
| 383 | 2023-04-17 | iLiFE!無銭LIVE! | https://x.com/iLiFE_official/status/1644271533106536448 |
| 401 | 2023-05-22 | iLiVE! Vol.7 | https://x.com/iLiFE_official/status/1643540451117645825 |
| 426 | 2023-07-15 | iLiVE! -Premium- | https://x.com/iLiFE_official/status/1664195292315668480 |
| 437 | 2023-08-07 | iLiVE! ~Premium- summerスペシャル~ | https://x.com/iLiFE_official/status/1683431891012321280 |
| 444 | 2023-08-24 | NAMBA LiFE! | https://x.com/iLiFE_official/status/1690302143486664704 |
| 342 | 2023-01-22 | 罪フェス | https://x.com/iLiFE_official/status/1613131939640406026 |
| 490 | 2023-12-15 | iLiVE! vol.11 | https://x.com/iLiFE_official/status/1721479638902509666 |
| 494 | 2023-12-23 | iLiVE! Xmas | https://x.com/iLiFE_official/status/1731991406699487538 |

## B. 错误修正
- 342 罪フェス：会场由 WOMBLIVE 改为新会场「渋谷WOMB」（东京，地址和容量留空）。依据：官方告知图「@WOMB (SHIBUYA)」，Eventernote 也写「渋谷WOMB」。
- 437 iLiVE! Premium summer：open/start 由 11:00/12:00 改为 10:00/11:00。依据：官方时间表图。
- 367 ワンダーウィード 天 白川ゆめか生誕祭、379 LEADING ID #いどみん生誕ツアー2023 東京：type 由「生誕祭」改为「対バン」（这两场是他团生诞，iLiFE! 为嘉宾）。

## C. 补全（官方图上能直接看到）
- 424 LiFE!TIMEiLiFE：open 16:30、start 17:30（1660231792107061251）
- 497 FULL OF LiFE!：open 16:00、start 17:00（1720742806342537285）
- 469 成城大学 柳祭：start 11:00；note 的「具体舞台未查到。」改为「官方告知图写明 11:00～、中庭メインステージ（荒天时2号館地下1階002教室）。」（1719981224197075345）

## 删除
无。
