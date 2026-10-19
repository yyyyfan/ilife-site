#!/usr/bin/env python3
"""016 验收（2025 年演出配图，提交 7d7cb4e）修正脚本 —— 幂等。
用法（在仓库根目录）：python3 docs/tasks/016-audit/2025-fixes.py [db/ilife.sqlite] [--dry-run] [--keep-unverified]
然后运行 python3 db/export.py 与 python3 db/export.py --check。
TicketDive 页面均为主办方 株式会社imaginate（iLiFE! 所属 HEROINES 运营）建立的官方售票页；每天一张告知图，Antigravity 把第 1 天的图套到了其他天。
正确的图取自同一页面，Grok Bot 于 2026-10-20 下载后逐张看过图上的日期/会场（且对应日程块的出演栏有 iLiFE!）。"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixlib016 import Fixer
f = Fixer(sys.argv)
TD = 'https://ticketdive.com/event/'
G = 'https://storage.googleapis.com/playyte-ticket-prod_event/VKH7oL4gezijY2J1WnUj_'
X = 'https://x.com/iLiFE_official/status/'
def td_fix(lid, date, title, wrong_url, page, name, text, asset, w, h):
    if not f.live_ok(lid, date, title): return
    f.unbind(lid, wrong_url, '图上是另一天的告知图')
    iid = f.add_image(dict(url=G+name, date=date, post=TD+page, text=text, source='TicketDive', asset=asset, w=w, h=h, lid=lid, year=2025))
    f.bind(lid, iid)
# 1) HEROINES成人式2025：4123 图上是 2025.1.11；1/12 场改用页面上的 2025.1.12 图
td_fix(656, '2025-01-12', 'HEROINES成人式2025 1/12', G+'401968_1735628601259.webp', 'heroines250111_12', '849243_1735628601259.jpeg',
       'HEROINES成人式2025 1/12公演 告知画像', 'be553dd7.webp', 1440, 2037)
# 2) HEROINES VALENTINE 2025：4130 图上是 2025.02.14 DAY1；2/15、2/16 改用 DAY2、DAY3 图
td_fix(668, '2025-02-15', 'TOKYO DOME presents HEROINES VALENTINE 2025', G+'323683_1738236954530.webp', 'heroinesvalentine2025', '71442_1738236954530.jpeg',
       'TOKYO DOME presents HEROINES VALENTINE 2025 2/15 DAY2 告知画像', '910c311a.webp', 1000, 1415)
td_fix(669, '2025-02-16', 'TOKYO DOME presents HEROINES VALENTINE 2025', G+'323683_1738236954530.webp', 'heroinesvalentine2025', '809846_1738236954530.jpeg',
       'TOKYO DOME presents HEROINES VALENTINE 2025 2/16 DAY3 告知画像', '0d429b40.webp', 595, 842)
# 3) HEROINES Xmas：4168 图上是 2025.12.24 Day1；12/25 改用 Day2 图
td_fix(766, '2025-12-25', 'HEROINES Xmas DAY2', G+'817380_1765764671719.webp', 'heroinesxmas251224_25', '133695_1765764671719.jpeg',
       'HEROINES Xmas DAY2 告知画像', 'b7c187ba.webp', 1440, 2037)
# 4) HEROINES HALLOWEEN：4163 图上是 2025.10.27 Day1（iLiFE! 不在 Day1 出演栏），两场都错。
#    4163 原地改为页面上的 10/28 DAY2 图（仍绑 747）；748 改用 10/29 DAY3 图
if f.live_ok(747, '2025-10-28', 'HEROINES HALLOWEEN DAY2'):
    f.replace_image(4163, G+'628401_1758987704189.jpeg', dict(url=G+'521356_1758987704189.jpeg', text='HEROINES HALLOWEEN DAY2 告知画像',
                    asset='9ead602f.webp', w=1440, h=2037, lid=747, year=2025))
td_fix(748, '2025-10-29', 'HEROINES HALLOWEEN DAY3', G+'521356_1758987704189.jpeg', 'heroineshalloween2510', '731082_1760591735690.jpeg',
       'HEROINES HALLOWEEN DAY3 告知画像', 'ebfa4d2d.webp', 640, 905)
# 5) HEROINES WHITEDAY 2025 Day2（3/14）：4088 选了官方帖的第 1 张（2025.03.13 DAY1），原地改为同帖第 2 张（2025.03.14 DAY2）
if f.live_ok(677, '2025-03-14', 'HEROINES WHITEDAY 2025'):
    f.replace_image(4088, 'https://pbs.twimg.com/media/GktXap0WoAA5VUo.jpg?name=orig', dict(url='https://pbs.twimg.com/media/GktXapTagAApY2b.jpg?name=orig',
                    text='3月13日,14日は！「HEROINES WHITEDAY 2025」に出演いたします❤︎\n\n超キュートなホワイトデー特別衣装着ます🫶🏻\niLiFE!からのお返し受け取りにきてくれる？♡\n\n🎫2月27',
                    asset='54baddbe.webp', w=1448, h=2048, lid=677, year=2025))
# 6) 无法核实对应关系（复用旧图，原帖文字没提到该场，图上也没有活动标识）
UNVERIFIED = [
    (663, '2025-02-01', 'HEROINES ALBUM 2025', 'https://pbs.twimg.com/media/GisuZ1IbUAEm5Tr.jpg?name=medium', '原帖写オリコン1位感谢'),
    (670, '2025-02-22', 'HEROINES CATITUDE', 'https://pbs.twimg.com/media/GkZGKcpaoAEOg68.jpg?name=medium', '原帖「あいらいふだにゃん」后台合照'),
    (672, '2025-02-25', 'Jams Collection', 'https://pbs.twimg.com/media/GkpDbgfWQAAOPUi.jpg?name=medium', '原帖写おやすみ衣装，23:55 发'),
    (684, '2025-04-01', 'iLiFE! ゲリラフリーライブ', 'https://pbs.twimg.com/media/GnYKnEZaAAA7ZWg.jpg?name=medium', '原帖 4/1 00:00「ガールズバンドはじめます」重大発表，非本场告知'),
    (714, '2025-07-06', '超NATSUZOME 2025', 'https://pbs.twimg.com/media/GvK7j7HWAAAasnS.jpg?name=medium', '原帖「スペシャルな夏にしよう」'),
    (723, '2025-08-02', 'TOKYO IDOL FESTIVAL 2025', 'https://pbs.twimg.com/media/GxVRT_EaIAIV4Xr.jpg?name=medium', '原帖未写 TIF'),
    (730, '2025-08-31', '@JAM EXPO 2025', 'https://pbs.twimg.com/media/GzrknM0aIAAovkZ.jpg?name=medium', '原帖「お姫様なあいらいふ」'),
]
if '--keep-unverified' not in sys.argv:
    for lid, d, t, u, why in UNVERIFIED:
        if f.live_ok(lid, d, t): f.unbind(lid, u, '无法核实：' + why)
f.finish()
