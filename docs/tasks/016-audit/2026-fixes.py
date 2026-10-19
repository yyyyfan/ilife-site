#!/usr/bin/env python3
"""016 验收（2026 年演出配图，提交 b638b5e）修正脚本 —— 幂等。
用法（在仓库根目录）：python3 docs/tasks/016-audit/2026-fixes.py [db/ilife.sqlite] [--dry-run] [--keep-unverified]
然后运行 python3 db/export.py 与 python3 db/export.py --check。
依据均由 Grok Bot 于 2026-10-20 打开原帖（X 连接器）/原页面（curl -m 20）并逐张看图核对。"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixlib016 import Fixer
f = Fixer(sys.argv)
X = 'https://x.com/iLiFE_official/status/'
TT = 'https://pbs.twimg.com/media/HTsjIwAbwAAburF.jpg?name=orig'   # 4040：iLiVE! TOUR 东京 2026.10.26 @Zepp Haneda 时间表
# 1) 4040 只是东京场（10/26）时间表，错绑到名古屋/札幌/福冈/大阪
for lid, d in [(855, '2026-11-09'), (856, '2026-11-16'), (860, '2026-12-08'), (861, '2026-12-15')]:
    if f.live_ok(lid, d, 'iLiVE! TOUR'):
        f.unbind(lid, TT, '图上是 iLiVE! TOUR TOKYO 2026.10.26 @Zepp Haneda 时间表，不是本场')
# 2) 名古屋场改用同一官方帖的第 2 张图（2026.11.09 @Zepp Nagoya 时间表）
if f.live_ok(855, '2026-11-09', 'iLiVE! TOUR NAGOYA'):
    iid = f.add_image(dict(url='https://pbs.twimg.com/media/HTsjIvyaAAAxXzg.jpg?name=orig', date='2026-11-09', post=X+'2106315903826833668',
        text='【iLiVE! TOUR】\n\n10月26日東京公演・11月9日名古屋公演のタイムテーブルの詳細を公開❤︎\n\nたくさんのご応募の中から選ばれた、各地方で活動されてるグループさんにも注目です！\niLiFE',
        source='X @iLiFE_official', asset='2a9947a0.webp', w=1448, h=2048, lid=855, year=2026))
    f.bind(855, iid)
# 3) 无法核实对应关系（复用的旧图）：官方帖只写「夏初まったぞー」，没提超NATSUZOME，图是户外合照、无活动标识
if '--keep-unverified' not in sys.argv and f.live_ok(825, '2026-07-05', '超NATSUZOME 2026'):
    f.unbind(825, 'https://pbs.twimg.com/media/HMdBDRSbMAAGh7j.jpg?name=medium', '原帖未提及本场，无法确认对应')
f.finish()
