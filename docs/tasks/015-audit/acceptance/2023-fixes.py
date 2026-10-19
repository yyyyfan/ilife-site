#!/usr/bin/env python3
"""015 验收（2023 年）修正脚本 —— 幂等，可在 Codex 后续提交之上重复运行。

用法：python3 2023-fixes.py [path/to/db/ilife.sqlite]   （默认 ./db/ilife.sqlite）
      加 --dry-run 只打印将要做的修改，不写库。

定位方式：一律按 (date, title) + 当前出处 URL 定位演出，不依赖自增 ID；
会场按 (name, pref) 查找/新建；出处按 url 查找/新建。
若目标记录已是修正后的状态 → 跳过（ALREADY）；若记录不存在或已被他人改成别的值 → 跳过并警告（SKIP），不强改。
所有官方出处均已由 Grok Bot 于 2026-10-19 通过 X 连接器打开原帖并查看告知图核对（iLiFE!、日期 JST、会场一致）。
"""
import sqlite3, sys

X = 'https://x.com/iLiFE_official/status/'
EN = 'https://www.eventernote.com/events/'
UNOFF = '仅非官方来源。'

# 1) 出处升级：Eventernote-only → 官方 X（旧 Eventernote 链接保留为补充核验）
UPGRADES = [
    # date, title, 当前出处(旧), 官方出处(新), 证据说明
    ('2023-01-04', 'iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 1/4', EN+'330354', X+'1609542842975940608',
     '来源为月度排期图（官方リリイベ排期图列出 1/4 タワレコ渋谷B1 CUTUP STUDIO 13:00～）；标题以补充 Eventernote 为准。'),
    ('2023-01-09', 'iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 1/9', EN+'330759', X+'1609542842975940608',
     '来源为月度排期图（官方リリイベ排期图列出 1/9 タワレコ渋谷B1 CUTUP STUDIO 20:00～）；标题以补充 Eventernote 为准。'),
    ('2023-01-15', 'iLiFE! 1stアルバム『アイライフスターターパック』ミニライブ＆特典会 1/15', EN+'330909', X+'1609542842975940608',
     '来源为月度排期图（官方リリイベ排期图列出 1/15 ヴィレッジヴァンガード名古屋PARCO店，未写时间）；标题与时间以补充 Eventernote 为准。'),
    ('2023-01-13', 'iLiFE リリイベ完走ありがとうLIVE（1部・2部）', EN+'330327', X+'1610221073873915904',
     '官方告知图确认 2023.1.13 Veats SHIBUYA，1部 OPEN 12:00 START 13:00、2部 OPEN 17:30 START 18:30。'),
    ('2023-02-03', 'ゲリラ無銭LIVE! 【第1部 iLiFE!編】', EN+'333483', X+'1621101364108734466',
     '官方 2023-02-02 20:00 JST 发帖「明日開催」，告知图确认 @SHIBUYA DIVE、1部 iLiFE! OPEN 14:00。'),
    ('2023-04-05', 'iLiVE! Vol.6', EN+'337077', X+'1637756707563778048',
     '官方时间表图确认 2023 4/05 iLiVE! @Veats SHIBUYA OPEN 14:00；“Vol.6”以补充 Eventernote 为准。'),
    ('2023-04-08', 'femmeLiFE!', EN+'338506', X+'1639583687229706241',
     '官方告知图确认 femmefatale×iLiFE! 2023.4.8 @渋谷WWWX OPEN 16:30 START 17:30。'),
    ('2023-04-17', 'iLiFE!無銭LIVE!', EN+'339638', X+'1644271533106536448',
     '官方告知图确认 2023年4月17日 5大都市ツアー壮行会 @Spotify O-WEST OPEN 14:45 START 15:30。'),
    ('2023-05-22', 'iLiVE! Vol.7', EN+'337076', X+'1643540451117645825',
     '官方正文「iLiVE!vol.7タイムテーブル公開」，图确认 2023 5/22 @Veats SHIBUYA OPEN 14:00。'),
    ('2023-07-15', 'iLiVE! -Premium-', EN+'343567', X+'1664195292315668480',
     '官方时间表图确认 7月15日 @Zepp DiverCity OPEN 9:00 START 10:00。'),
    ('2023-08-07', 'iLiVE! ~Premium- summerスペシャル~', EN+'347237', X+'1683431891012321280',
     '官方时间表图确认 8月7日 @KT Zepp Yokohama OPEN 10:00 START 11:00（Eventernote 写 11:00/12:00，以官方为准）。'),
    ('2023-08-24', 'NAMBA LiFE!', EN+'352587', X+'1690302143486664704',
     '官方告知图确认 NAMBALiFE! 2023.8.24 @BananaHall OPEN 16:20 START 17:00；官方写法为「NAMBALiFE!」。'),
    ('2023-01-22', '罪フェス', EN+'331617', X+'1613131939640406026',
     '官方告知图确认 GILTY×GILTY presents 罪Fes 2023.01.22 @WOMB (SHIBUYA) OPEN 16:30 START 17:00（会场为 WOMB，不是 WOMB LIVE）。'),
    ('2023-12-15', 'iLiVE! vol.11', EN+'360684', X+'1721479638902509666',
     '官方时间表图确认 iLiVE!11 2023.12.15 @KANDA SQUARE HALL OPEN 11:30 START 12:30（同帖另一张图写 10:30/11:30，取时间表）。'),
    ('2023-12-23', 'iLiVE! Xmas', EN+'360837', X+'1731991406699487538',
     '官方时间表图确认 iLiVE! Xmas 2023.12.23 @KT Zepp Yokohama OPEN 9:30 START 10:30。'),
]

# 2) 字段修正：(date, title, 列, 期望旧值, 新值, 依据)
FIELD_FIXES = [
    ('2023-08-07', 'iLiVE! ~Premium- summerスペシャル~', 'open_time', '11:00', '10:00', X+'1683431891012321280'),
    ('2023-08-07', 'iLiVE! ~Premium- summerスペシャル~', 'start_time', '12:00', '11:00', X+'1683431891012321280'),
    ('2023-07-12', 'LiFE!TIMEiLiFE', 'open_time', None, '16:30', X+'1660231792107061251'),
    ('2023-07-12', 'LiFE!TIMEiLiFE', 'start_time', None, '17:30', X+'1660231792107061251'),
    ('2023-12-27', 'FULL OF LiFE!', 'open_time', None, '16:00', X+'1720742806342537285'),
    ('2023-12-27', 'FULL OF LiFE!', 'start_time', None, '17:00', X+'1720742806342537285'),
    ('2023-11-03', '2023年度 成城大学 柳祭 Bフェスティバル', 'start_time', None, '11:00', X+'1719981224197075345'),
    # 他团成员的生诞活动，iLiFE! 只是嘉宾；库内「生誕祭」类型只用于 iLiFE! 成员生诞（2020–2022 惯例）
    ('2023-03-22', 'ワンダーウィード 天 白川ゆめか生誕祭 (3/22)', 'type', '生誕祭', '対バン', EN+'337078'),
    ('2023-04-11', 'LEADING ID #いどみん生誕ツアー2023 東京', 'type', '生誕祭', '対バン', EN+'337569'),
]

# 3) 备注文字修正：(date, title, 旧片段, 新片段)
NOTE_FIXES = [
    ('2023-11-03', '2023年度 成城大学 柳祭 Bフェスティバル', '具体舞台未查到。',
     '官方告知图写明 11:00～、中庭メインステージ（荒天时2号館地下1階002教室）。'),
]

# 4) 会场修正：(date, title, 期望旧会场名, 新会场 (name, pref))
VENUE_FIXES = [
    ('2023-01-22', '罪フェス', 'WOMBLIVE', ('渋谷WOMB', '东京')),
]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv
    path = args[0] if args else 'db/ilife.sqlite'
    con = sqlite3.connect(path)
    con.execute('PRAGMA foreign_keys=ON')
    stats = {'applied': 0, 'already': 0, 'skip': 0}

    def log(kind, msg):
        stats[{'APPLY': 'applied', 'ALREADY': 'already', 'SKIP': 'skip'}[kind]] += 1
        print(f'[{kind}] {msg}')

    def source_id(url, create=True):
        r = con.execute('SELECT id FROM sources WHERE url=?', (url,)).fetchone()
        if r: return r[0]
        if not create: return None
        return con.execute('INSERT INTO sources(url) VALUES(?)', (url,)).lastrowid

    def find(date, title):
        rows = con.execute('SELECT l.id, s.url, l.note, l.venue_id FROM lives l JOIN sources s ON s.id=l.source_id '
                           'WHERE l.date=? AND l.title=?', (date, title)).fetchall()
        return rows

    for date, title, old, new, ev in UPGRADES:
        rows = find(date, title)
        if len(rows) != 1:
            log('SKIP', f'{date} {title}: 找到 {len(rows)} 条，未修改'); continue
        lid, cur, note, _ = rows[0]
        if cur == new:
            log('ALREADY', f'{date} {title}: 出处已是官方'); continue
        if cur != old:
            log('SKIP', f'{date} {title}: 当前出处 {cur} 既非旧值也非新值，未修改'); continue
        note = (note or '').strip()
        if note.startswith(UNOFF): note = note[len(UNOFF):].strip()
        parts = [ev]
        if old not in note: parts.append(f'补充核验：{title}（{old}）')
        if note: parts.append(note)
        newnote = ' '.join(parts)
        if not dry:
            con.execute('UPDATE lives SET source_id=?, note=? WHERE id=?', (source_id(new), newnote, lid))
        log('APPLY', f'{date} {title}: 出处 {old} → {new}')

    for date, title, col, oldv, newv, src in FIELD_FIXES:
        rows = con.execute(f'SELECT id, {col} FROM lives WHERE date=? AND title=?', (date, title)).fetchall()
        if len(rows) != 1:
            log('SKIP', f'{date} {title} {col}: 找到 {len(rows)} 条'); continue
        lid, cur = rows[0]
        if cur == newv: log('ALREADY', f'{date} {title} {col}={newv}'); continue
        if cur != oldv: log('SKIP', f'{date} {title} {col}: 当前值 {cur!r} 与预期旧值 {oldv!r} 不符'); continue
        if not dry: con.execute(f'UPDATE lives SET {col}=? WHERE id=?', (newv, lid))
        log('APPLY', f'{date} {title} {col}: {cur!r} → {newv!r}（依据 {src}）')

    for date, title, oldfrag, newfrag in NOTE_FIXES:
        rows = con.execute('SELECT id, note FROM lives WHERE date=? AND title=?', (date, title)).fetchall()
        if len(rows) != 1: log('SKIP', f'{date} {title} note: 找到 {len(rows)} 条'); continue
        lid, note = rows[0]; note = note or ''
        if newfrag in note: log('ALREADY', f'{date} {title} note'); continue
        if oldfrag not in note: log('SKIP', f'{date} {title} note: 未找到旧片段'); continue
        if not dry: con.execute('UPDATE lives SET note=? WHERE id=?', (note.replace(oldfrag, newfrag), lid))
        log('APPLY', f'{date} {title} note: 「{oldfrag}」→「{newfrag}」')

    for date, title, oldname, (vname, pref) in VENUE_FIXES:
        rows = con.execute('SELECT l.id, v.name FROM lives l JOIN venues v ON v.id=l.venue_id WHERE l.date=? AND l.title=?',
                           (date, title)).fetchall()
        if len(rows) != 1: log('SKIP', f'{date} {title} venue: 找到 {len(rows)} 条'); continue
        lid, cur = rows[0]
        if cur == vname: log('ALREADY', f'{date} {title} 会场={vname}'); continue
        if cur != oldname: log('SKIP', f'{date} {title} 会场当前为 {cur}，未修改'); continue
        if not dry:
            r = con.execute('SELECT id FROM venues WHERE name=? AND pref=?', (vname, pref)).fetchone()
            vid = r[0] if r else con.execute('INSERT INTO venues(name, pref) VALUES(?,?)', (vname, pref)).lastrowid
            con.execute('UPDATE lives SET venue_id=? WHERE id=?', (vid, lid))
        log('APPLY', f'{date} {title} 会场: {cur} → {vname}（{pref}）；地址/容量留空')

    if dry: con.rollback()
    else: con.commit()
    print(f"完成：applied={stats['applied']} already={stats['already']} skip={stats['skip']}{' (dry-run)' if dry else ''}")
    return 1 if stats['skip'] else 0


if __name__ == '__main__':
    sys.exit(main())
