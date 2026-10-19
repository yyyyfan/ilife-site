#!/usr/bin/env python3
"""016 验收（2020 年演出配图，提交 5471849；Eventernote 图已由 32ea53c 删除）修正脚本 —— 幂等。
用法（在仓库根目录）：python3 docs/tasks/016-audit/2020-fixes.py [db/ilife.sqlite] [--dry-run]
然后运行 python3 db/export.py 与 python3 db/export.py --check。"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixlib016 import Fixer
f = Fixer(sys.argv)
# 1) 61 ビジュアリズム 11/3：复用的 41 是官方 2020-10-31 帖「昨日と本日、LIVEにお越しいただきありがとう…ハロウィンver.」的万圣节合照（10/30、10/31 两场），
#    帖子只是顺带预告「次回は11/3」，图不是本场 → 解除
if f.live_ok(61, '2020-11-03', 'ビジュアリズム'):
    f.unbind(61, 'https://pbs.twimg.com/media/ElpxhKaVMAEUaHl.jpg?name=medium', '图是 10/30–31 万圣节公演合照')
# 2) 66 IDOL CONTENT EXPO 11/22：复用的 50 是同日「惑星ツアー Story.11 ありがとうございました」的照片（已是 65 惑星ツアー 的封面），
#    帖子只是预告「この後…IDOL CONTENT EXPOに出演」→ 解除
if f.live_ok(66, '2020-11-22', 'IDOL CONTENT EXPO'):
    f.unbind(66, 'https://pbs.twimg.com/media/EnapgEpW8AAzb0K.jpg?name=medium', '图是同日惑星ツアー的照片')
f.finish()
