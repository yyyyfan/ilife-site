#!/usr/bin/env python3
"""016 验收（2024 年演出配图，提交 e536d7a）修正脚本 —— 幂等。
用法（在仓库根目录）：python3 docs/tasks/016-audit/2024-fixes.py [db/ilife.sqlite] [--dry-run] [--keep-unverified]
然后运行 python3 db/export.py 与 python3 db/export.py --check。"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixlib016 import Fixer
f = Fixer(sys.argv)
# 1) 516 HEROINES VALENTINE【OSAKA】2/10：复用的 1626 是「HEROINES WHITEDAY 2024.03.14」告知图（原帖也只写 3/14 WHITEDAY），错绑
if f.live_ok(516, '2024-02-10', 'HEROINES VALENTINE【OSAKA】'):
    f.unbind(516, 'https://pbs.twimg.com/media/GF8aCujbIAAbVmA.jpg?name=medium', '图与原帖都是 3/14 HEROINES WHITEDAY')
# 2) 532 JAPANLiFE! 名古屋 3/24：复用的 1731 原帖写「全国ツアー大阪公演ありがとう」（大阪 3/23 BIGCAT），错绑；
#    改用巡演总海报 4173（官方 1739239656452202834，海报列有 2024年3月24日【日】@NAGOYA ReNY limited）
if f.live_ok(532, '2024-03-24', 'JAPANLiFE!'):
    f.unbind(532, 'https://pbs.twimg.com/media/GJbWidia0AAqONV.jpg?name=medium', '原帖是大阪公演（3/23）的感谢图')
    r = f.c.execute('SELECT id FROM images WHERE url=?', ('https://pbs.twimg.com/media/GCMFPjNaEAA3KjN.jpg?name=orig',)).fetchone()
    f.bind(532, r[0] if r else None)
# 3) 无法核实对应关系（复用旧图，原帖文字没提到该场，图上也没有活动标识）
UNVERIFIED = [
    (551, '2024-05-10', 'iLiFE×JamsCollection', 'https://pbs.twimg.com/media/GNOClV8bEAA0vF9.jpg?name=medium', '原帖只有「衣装かわい？」'),
    (573, '2024-07-06', '超NATSUZOME2024', 'https://pbs.twimg.com/media/GRzF2sbacAEzmuO.jpg?name=medium', '原帖「今日超夏だった」'),
    (578, '2024-07-14', '【7/14】SPARK 2024', 'https://pbs.twimg.com/media/GScJ0g8XQAACjbv.jpg?name=medium', '原帖「SUMMER！！」'),
]
if '--keep-unverified' not in sys.argv:
    for lid, d, t, u, why in UNVERIFIED:
        if f.live_ok(lid, d, t): f.unbind(lid, u, '无法核实：' + why)
f.finish()
