#!/usr/bin/env python3
"""任务 028：按在籍区间推导每场公演的出演成员，写入 live_members。

规则
----
1. 成员的「在籍区间」以 `member_periods` 为准（`date_from` / `date_to` 均为**闭区间**：
   离团日当天仍算在籍——卒業公演就在那天）。
2. 同一成员同一天可能命中多段（如 福丸うさ 2023-08-19 当天既是「非正式」末段也是「正式」首段），
   按 `r`（正式）> `n`（非正式）> `s`（支援）取最高的那一段。
3. 默认全员到场。已知例外写在 `db/curation/live_members.json` 里，逐条给依据。
4. 対バン / フェス 存在「只到几个人」的情况，库里没有逐场名单，前端按公演类型标「推定」，
   不在数据层区分——避免 563 场都挂一条无信息的备注。

用法
----
  python3 db/task028_live_members.py --dry-run   # 只看统计
  python3 db/task028_live_members.py             # 写入（先清空再重建，幂等）
"""
import sqlite3, os, sys
from collections import Counter, defaultdict

from curation import load

D = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(D, 'ilife.sqlite')
DRY = '--dry-run' in sys.argv

# 例外数据在 db/curation/live_members.json，加一场只改 JSON，不用动这个脚本。
_CUR = load('live_members')

# 整场辞退（新冠自肃）：成员本来在籍但当天没上台，标「未出演」而不是直接不写行，
# 这样前端能区分「没数据」和「确实没上」。
NO_SHOW = {x['live'] for x in _CUR['no_show_lives']}

# 个别成员缺场：(live_id, 成员名) -> (状态, 依据)
OVERRIDE = {(x['live'], x['member']): (x['status'], x['reason']) for x in _CUR['overrides']}

RANK = {'r': 3, 'n': 2, 's': 1}
STATUS = {'r': '出演', 'n': '非正式', 's': '支援'}


def main():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()

    name = {r['id']: r['name'] for r in cur.execute('SELECT id,name FROM members')}
    sort = {r['id']: r['sort'] for r in cur.execute('SELECT id,sort FROM members')}
    periods = list(cur.execute('SELECT member_id,type,date_from,date_to FROM member_periods'))
    lives = list(cur.execute('SELECT id,date,type FROM lives ORDER BY date,id'))

    # 成员 -> 区间列表
    by_member = defaultdict(list)
    for p in periods:
        by_member[p['member_id']].append(p)

    rows, empty, per_live = [], [], {}
    for l in lives:
        d = l['date']
        got = {}
        for mid, ps in by_member.items():
            best = None
            for p in ps:
                if p['date_from'] <= d and (not p['date_to'] or d <= p['date_to']):
                    if best is None or RANK[p['type']] > RANK[best['type']]:
                        best = p
            if best:
                got[mid] = STATUS[best['type']]
        if not got:
            empty.append((l['id'], d, l['type']))
            continue

        if l['id'] in NO_SHOW:
            for mid in got:
                got[mid] = '未出演'

        for (lid, nm), (st, _why) in OVERRIDE.items():
            if lid != l['id']:
                continue
            mid = next((k for k, v in name.items() if v == nm), None)
            if mid and mid in got:
                got[mid] = st

        for mid in sorted(got, key=lambda k: sort.get(k, 999)):
            rows.append((l['id'], mid, got[mid]))
        per_live[l['id']] = len(got)

    dist = Counter(per_live.values())
    st = Counter(r[2] for r in rows)
    print(f'公演 {len(lives)} 场 → live_members {len(rows)} 行')
    print('每场人数分布:', dict(sorted(dist.items())))
    print('状态分布:', dict(st))
    print('推导为空:', len(empty), empty[:5])

    # 自检：每位成员的出场场次，看看有没有明显不合理的
    cnt = Counter(r[1] for r in rows if r[2] in ('出演', '支援', '非正式'))
    print('\n出场场次 Top / Bottom:')
    order = sorted(cnt.items(), key=lambda x: -x[1])
    for mid, n in order[:5] + order[-3:]:
        print(f'  {name[mid]:<8} {n:>4} 场')

    if DRY:
        print('\n[dry] 未写入')
        return
    cur.execute('DELETE FROM live_members')
    cur.executemany('INSERT INTO live_members(live_id,member_id,status) VALUES(?,?,?)', rows)
    c.commit()
    print(f'\n已写入 {len(rows)} 行')


if __name__ == '__main__':
    main()
