#!/usr/bin/env python3
"""任务 023：2021 年 imaginate 新冠自肃辞退的 5 场统一标注「未出演」。

依据（已实际打开确认）：
  imaginate 2021-07-21 公告
  https://www.imaginate.jp/news/【ilife】新型コロナウィルス感染に伴う活動自粛の/
  原文列出 5 场出演キャンセル：
    7/22 アナフェス #無銭MAX @ZeppTokyo          → live 123（已标）
    7/23 HEROINES FES @ZeppTokyo                 → live 124
    7/25 真夏のShining Days @白金高輪SELENE b2   → live 125（已标）
    7/31 STAND OUT IDOL vol.10-SUN- @恵比寿CreAto → live 126
    8/1  IDOL CONTENT EXPO @品川インターシティホール → live 127

另外核实过两条原出处：
  x.com/iLiFE_official/status/1417031455268491267（2021-07-19）是「7月ライブまとめ」日程推文，只证明原定出演；
  x.com/ic_expo/status/1420274098681176074（2021-07-28）是主办方的出演取消公告，但主体是同场的 Stand-Up! Next!，未提 iLiFE!。

幂等：可重复运行。用法：python3 db/task023_covid_absent.py [--dry-run]
"""
import os
import sqlite3
import sys

D = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(D, 'ilife.sqlite')
DRY = '--dry-run' in sys.argv

ANNOUNCE = ('https://www.imaginate.jp/news/%e3%80%90ilife%e3%80%91%e6%96%b0%e5%9e%8b%e3%82%b3%e3%83%ad%e3%83%8a'
            '%e3%82%a6%e3%82%a3%e3%83%ab%e3%82%b9%e6%84%9f%e6%9f%93%e3%81%ab%e4%bc%b4%e3%81%86%e6%b4%bb%e5%8b%95'
            '%e8%87%aa%e7%b2%9b%e3%81%ae/')

NOTES = {
    124: '新曲披露公演；因成员确诊新冠活动自肃出演辞退（未出演）；'
         '补充核验：https://tokyogirlsstyle.jp/live/detail.php?id=1090154',
    126: '因成员确诊新冠活动自肃出演辞退（未出演）；'
         '原排期出处：https://x.com/iLiFE_official/status/1417031455268491267'
         '（2021-07-19「7月ライブまとめ」日程推文，仅证明原定出演）',
    127: '因成员确诊新冠活动自肃出演辞退（未出演）；'
         '注：主办方 ic_expo 2021-07-28 的出演取消公告主体为同场 Stand-Up! Next!，未提 iLiFE!，故不作本场出处。',
}


def main():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    r = cur.execute('SELECT id FROM sources WHERE url=?', (ANNOUNCE,)).fetchone()
    if r:
        sid = r['id']
    elif DRY:
        sid = -1
        print('[dry] 新增 imaginate 公告 source')
    else:
        cur.execute('INSERT INTO sources(url) VALUES(?)', (ANNOUNCE,))
        sid = cur.lastrowid
        print(f'新增 source {sid} imaginate 公告')

    for live_id, note in NOTES.items():
        row = cur.execute('SELECT id,note FROM lives WHERE id=?', (live_id,)).fetchone()
        if not row:
            print(f'跳过 {live_id}：不存在')
            continue
        if DRY:
            print(f'[dry] 更新 live {live_id}\n      {note}')
            continue
        cur.execute('UPDATE lives SET note=?, source_id=? WHERE id=?', (note, sid, live_id))
        print(f'更新 live {live_id}（原 note: {row["note"]}）')

    if DRY:
        c.rollback()
    else:
        c.commit()
        n = cur.execute("SELECT count(*) FROM lives WHERE note LIKE '%未出演%'").fetchone()[0]
        print(f'标记「未出演」总数：{n}')


if __name__ == '__main__':
    main()
