#!/usr/bin/env python3
"""任务 024：里程碑公演改用官方公告为源，并补全开场/开演时间。

背景：lives 表有 27 条 source_id=1（Wikipedia），全是里程碑公演，且 open_time/start_time 全空。
其中 10 条有官网现存公告可覆盖（官网 2023-04 前的公告已被 JamClip 改版删除，只剩 21 条，
索引见 docs/reference/official-news-index.md）。

本次改动（逐条已打开原文核对）：
  lives 14–21  TRAVELiFE! 2026 八场 → source 1948，open/start 按公告，note 记優先物販与特典会规则
  lives 22     MEGALiFE! 2026-08-26 → source 1974，open 16:00 / start 17:30，note 记完売与後日特典会
  lives 9      卒業公演 2024-09-01   → source 1634（公告写明 9/1 豊洲PIT）
  members 22   那蘭のどか left 字段来源 → 1874（公告写明 8/27 当日脱退）

幂等：可重复运行。用法：python3 db/task024_official_news.py [--dry-run]
"""
import os
import sqlite3
import sys

D = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(D, 'ilife.sqlite')
DRY = '--dry-run' in sys.argv

BASE = 'https://ilife-heroines.com/topics/detail/index/'
NEWS = {
    1948: BASE + '1948',   # 2026-03-27 TRAVELiFE! 2026 オフィシャル先行開始（含八场 open/start）
    1973: BASE + '1973',   # 2026-06-01 TRAVELiFE! 2026 特典会に関するご案内
    1974: BASE + '1974',   # 2026-06-02 MEGALiFE! 公演概要
    1988: BASE + '1988',   # 2026-07-10 MEGALiFE! 全席完売
    1999: BASE + '1999',   # 2026-08-16 後日特典会
    1634: BASE + '1634',   # 2024-08-16 所属メンバーに関するお知らせ
    1874: BASE + '1874',   # 2025-08-25 那蘭のどかに関するお知らせ
}

# live_id: (公告ID, open, start, 優先物販, 会场, 日期)
TOUR = {
    14: (1948, '16:30', '17:30', '14:00-15:30', 'Zepp Haneda(TOKYO)', '2026-06-01'),
    15: (1948, '17:00', '18:00', '14:30-16:00', 'Zepp Osaka Bayside', '2026-06-04'),
    16: (1948, '17:00', '18:00', '14:30-16:00', 'Zepp Osaka Bayside', '2026-06-05'),
    17: (1948, '17:00', '18:00', '14:30-16:00', 'Zepp Fukuoka', '2026-06-09'),
    18: (1948, '16:00', '17:00', '13:30-15:00', 'Zepp Sapporo', '2026-06-14'),
    19: (1948, '17:00', '18:00', '14:30-16:00', 'Zepp Nagoya', '2026-06-22'),
    20: (1948, '17:00', '18:00', '14:30-16:00', 'Zepp Nagoya', '2026-06-23'),
    21: (1948, '16:30', '17:30', '13:00-14:30', 'KT Zepp Yokohama', '2026-06-30'),
}

TOUR_NOTE = ('官方公告 2026-03-27（topics/1948）公演概要：{date} @{venue}，OPEN {o} / START {s}'
             '（優先物販 {b}）。特典会规则见 2026-06-01 公告（topics/1973）：B チケット不可参加特典会；'
             '持「新メンバー特典会参加券付きチケット」者仅可参加真守みゅう特典会。'
             '公告另注：サポートメンバー 恋星はるか 不参加本巡演。')

MEGALIFE_NOTE = ('官方公告 2026-06-02（topics/1974）公演概要：2026-08-26(水) @Kアリーナ横浜，'
                 'OPEN 16:00 / START 17:30，出演 iLiFE!。2026-07-10 公告（topics/1988）全席完売。'
                 '後日特典会（2026-08-16 公告 topics/1999）：DAY1 2026-08-27 パシフィコ横浜 展示ホールB（5 部制）、'
                 'DAY2 2026-09-12 東京流通センター 第二展示場Fホール（6 部制）。')

LIVE9_NOTE = ('官方公告 2024-08-16（topics/1634）：向日えな・涼芽なの于 2024-09-01 豊洲PIT '
              '卒業公演后从 iLiFE! 毕业。')

MEMBER22_LEFT = ('2025-08-27 退出（官方 2025-08-25 公告：重大な規約違反，'
                 '当日日本武道館公演为最后出演，此后 8 人体制）')


_MEMO = {}


def sid_of(cur, nid):
    """取（或建）公告 source id。"""
    if nid in _MEMO:
        return _MEMO[nid]
    url = NEWS[nid]
    r = cur.execute('SELECT id FROM sources WHERE url=?', (url,)).fetchone()
    if r:
        _MEMO[nid] = r['id']
        return r['id']
    if DRY:
        print(f'[dry] 新增 source topics/{nid}')
        _MEMO[nid] = -1
        return -1
    cur.execute('INSERT INTO sources(url) VALUES(?)', (url,))
    sid = cur.lastrowid
    _MEMO[nid] = sid
    print(f'新增 source {sid} topics/{nid}')
    return sid


def main():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    changed = 0

    # ---- 1. TRAVELiFE! 2026 八场 ----
    for lid, (nid, o, s, b, venue, date) in TOUR.items():
        row = cur.execute('SELECT id,date,title,source_id,open_time,start_time FROM lives WHERE id=?',
                          (lid,)).fetchone()
        if not row:
            print(f'跳过 live {lid}：不存在')
            continue
        if row['date'] != date:
            print(f'跳过 live {lid}：日期不符（库 {row["date"]} != 公告 {date}）')
            continue
        sid = sid_of(cur, nid)
        note = TOUR_NOTE.format(date=date, venue=venue, o=o, s=s, b=b)
        if DRY:
            print(f'[dry] live {lid} {date} source {row["source_id"]}→{sid} '
                  f'open {row["open_time"]}→{o} start {row["start_time"]}→{s}')
            continue
        cur.execute('UPDATE lives SET source_id=?, open_time=?, start_time=?, note=? WHERE id=?',
                    (sid, o, s, note, lid))
        changed += 1
        print(f'更新 live {lid} {date} {venue} {o}/{s}')

    # ---- 2. MEGALiFE! ----
    row = cur.execute('SELECT id,date,source_id,open_time,start_time FROM lives WHERE id=22').fetchone()
    if row and row['date'] == '2026-08-26':
        sid = sid_of(cur, 1974)
        if DRY:
            print(f'[dry] live 22 source {row["source_id"]}→{sid} open→16:00 start→17:30')
        else:
            cur.execute('UPDATE lives SET source_id=?, open_time=?, start_time=?, note=? WHERE id=22',
                        (sid, '16:00', '17:30', MEGALIFE_NOTE))
            changed += 1
            print('更新 live 22 MEGALiFE! 16:00/17:30')
    else:
        print('跳过 live 22：不存在或日期不符')

    # ---- 3. 卒業公演 ----
    row = cur.execute('SELECT id,date,source_id FROM lives WHERE id=9').fetchone()
    if row and row['date'] == '2024-09-01':
        sid = sid_of(cur, 1634)
        if DRY:
            print(f'[dry] live 9 source {row["source_id"]}→{sid}')
        else:
            cur.execute('UPDATE lives SET source_id=?, note=? WHERE id=9', (sid, LIVE9_NOTE))
            changed += 1
            print('更新 live 9 卒業公演 出处')
    else:
        print('跳过 live 9：不存在或日期不符')

    # ---- 4. 那蘭のどか left 字段来源 ----
    sid = sid_of(cur, 1874)
    r = cur.execute("SELECT source_id FROM member_fields_sources WHERE member_id=22 AND field='left'").fetchone()
    if DRY:
        print(f'[dry] member 22 left source {r["source_id"] if r else "(缺行)"}→{sid}，left_ 文案补当日最后出演')
    else:
        if r:
            cur.execute("UPDATE member_fields_sources SET source_id=? WHERE member_id=22 AND field='left'", (sid,))
        else:
            cur.execute("INSERT INTO member_fields_sources(member_id,field,source_id,ord) VALUES(22,'left',?,0)",
                        (sid,))
        cur.execute('UPDATE members SET left_=? WHERE id=22', (MEMBER22_LEFT,))
        changed += 1
        print('更新 member 22 那蘭のどか 离开日期来源与文案')

    # ---- 5. 会场命名统一：Zepp Haneda → Zepp Haneda (TOKYO) ----
    # 官方公告写作「Zepp Haneda(TOKYO)」，库里同系列已统一为「Zepp DiverCity (TOKYO)」「Zepp Namba (OSAKA)」，
    # 唯独本会场缺括注，一并补齐。
    v = cur.execute("SELECT id,name FROM venues WHERE name='Zepp Haneda'").fetchone()
    if v:
        if DRY:
            print(f'[dry] venue {v["id"]} Zepp Haneda → Zepp Haneda (TOKYO)')
        else:
            cur.execute("UPDATE venues SET name='Zepp Haneda (TOKYO)' WHERE id=?", (v['id'],))
            changed += 1
            print(f'更新 venue {v["id"]} 命名 → Zepp Haneda (TOKYO)')
    else:
        print('跳过会场改名：未找到 Zepp Haneda（可能已改）')

    if DRY:
        c.rollback()
        print('[dry] 回滚，未写入')
    else:
        c.commit()
        n = cur.execute('SELECT count(*) FROM lives WHERE source_id=1').fetchone()[0]
        print(f'写入完成，改动 {changed} 组；剩余 Wikipedia 源公演 {n} 条')


if __name__ == '__main__':
    main()
