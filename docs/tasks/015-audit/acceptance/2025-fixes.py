#!/usr/bin/env python3
"""015 验收（2025 年）修正脚本 —— 幂等，可在 Codex 后续提交之上重复运行。

用法：python3 2025-fixes.py [path/to/db/ilife.sqlite]   （默认 ./db/ilife.sqlite）
      加 --dry-run 只打印将要做的修改，不写库。

定位方式：一律按 (date, title) + 当前出处 URL / 当前字段值定位演出，不依赖自增 ID；
出处按 url 查找/新建。
若目标记录已是修正后的状态 → 跳过（ALREADY）；若记录不存在或已被他人改成别的值 → 跳过并警告（SKIP），不强改。
所有官方出处均已由 Grok Bot 于 2026-10-19 通过 X 连接器打开原帖并查看告知图核对（作者 @iLiFE_official、日期 JST、会场一致）。
"""
import sqlite3, sys

X = 'https://x.com/iLiFE_official/status/'
EN = 'https://www.eventernote.com/events/'
UNOFF = '仅非官方来源。'

# 1) 出处升级：Eventernote-only → 官方 X（旧 Eventernote 链接保留为补充核验）
UPGRADES = [
    # date, title, 当前出处(旧), 官方出处(新), 证据说明
    ('2025-01-17', 'iLiFE! アルバム『HEROINES ALBUM 2025』ミニライブ＆特典会', EN+'455610', X+'1878397590510924110',
     '来源为月度排期图（官方 2025-01-12 20:04 JST「HEROINES ALBUM2025 リリイベ…スケジュール」图列出 1/17(金) 17:00～ @DiverCity）；具体场所与开场时间以补充 Eventernote 为准。'),
    ('2025-02-01', 'HEROINES ALBUM 2025 ミニライブ&特典会', EN+'417070', X+'1885236597198873048',
     '官方 2025-01-31 17:00 JST 告知：2/1 リリイベ场地由お台場改为ららぽーと柏の葉 本館2F センタープラザ，開演 17:30，10:00 起发放优先区入场券（Eventernote 的 10:00/11:30 为整场活动时间，以官方为准）。'),
    ('2025-03-14', 'HEROINES WHITEDAY 2025 Day2', EN+'455614', X+'1894704198337561061',
     '官方 2025-02-26 20:00 JST「3月13日,14日は！」告知，第 2 张图确认 HEROINES WHITEDAY 2025 @KANDA SQUARE HALL 2025.03.14 DAY2 OPEN 12:00 START 12:30，时间表中有 iLiFE!。'),
    ('2025-04-01', 'iLiFE! ゲリラフリーライブ @ 新宿ReNY', EN+'424202', X+'1906730827993735619',
     '官方 2025-04-01 00:30 JST「本日緊急無銭ライブ開催」，引用 @heroines_idol 号外图（1906723165252018646）：電撃フリーライブ@新宿ReNY OPEN 13:00 / START 14:00。'),
    ('2025-09-24', 'HEROINES LEAGUE Ⅰ【Sep. part2】', EN+'444475', X+'1965024931953176985',
     '官方 2025-09-08 21:10 JST「9月24日は！」告知，图确认 09.24 HEROINES LEAGUE I Sep. Part 2 @EX Theater Roppongi OPEN 14:00 / START 15:00。'),
    ('2025-09-27', '「東京ゲームショウ2025」コナミデジタルエンタテインメントブース VR×ライブアイドル 新サービス発表記念 iLiFE!スペシャルライブ', EN+'444181', X+'1971137865330679823',
     '官方 2025-09-25 18:01 JST 案内：9/27（土）iLiFE! スペシャルステージ 出演 15:00〜，コナミデジタルエンタテインメントブース 05-S01（ホール5）；出演决定告知 https://x.com/iLiFE_official/status/1967068430307389932 。'),
    ('2025-10-31', 'HEROINES HALLOWEEN -PREMIUM-  2025/10/31', EN+'491486', X+'1974023027160473670',
     '官方 2025-10-03 17:05 JST「10月31日は！」告知，图确认 HEROINES HALLOWEEN PREMIUM 2025.10.31(Fri) @Spotify O-EAST OPEN 10:00 / START 10:30，出演者有 iLiFE!。'),
    ('2025-11-09', '昭和女子大学 第33回秋桜祭 iLiFE! 秋桜祭 LIVE 2025', EN+'446971', X+'1973592128010985815',
     '官方 2025-10-02 12:33 JST「11月9日は！昭和女子大学「秋桜祭」」告知，图确认 iLiFE! 秋桜祭LIVE2025 2025/11/9(sun) @人見記念講堂 OPEN 16:00 START 17:00。'),
    ('2025-12-31', 'HEROINES COUNTDOWN 2025-2026', EN+'491487', X+'1969310642772590606',
     '官方 2025-09-20 17:00 JST「12月31日は！」告知，图确认 HEROINES COUNTDOWN 2025-2026 2025.12.31 @Kanadevia Hall（=TOKYO DOME CITY HALL），告知时 OPEN/START TBD；开场/开演时间以补充 Eventernote 为准。'),
]

# 2) 字段修正：(date, title, 列, 期望旧值, 新值, 依据)
FIELD_FIXES = [
    # 官方告知 開演 17:30；10:00 是优先区入场券发放时间，不是开场时间
    ('2025-02-01', 'HEROINES ALBUM 2025 ミニライブ&特典会', 'start_time', '11:30', '17:30', X+'1885236597198873048'),
    ('2025-02-01', 'HEROINES ALBUM 2025 ミニライブ&特典会', 'open_time', '10:00', None, X+'1885236597198873048'),
    # 官方 2025-06-05 告知变更后的时间
    ('2025-06-08', 'iLiFE! Zepp6venue tour -TRAVE LiFE!- 台北公演', 'open_time', None, '17:30', X+'1930588831113531395'),
    ('2025-06-08', 'iLiFE! Zepp6venue tour -TRAVE LiFE!- 台北公演', 'start_time', None, '18:30', X+'1930588831113531395'),
    # 主办方（高嶺のなでしこ官网）页面：第二部[OPEN/START] 17:30/18:30 出演：iLiFE!
    ('2025-04-06', '高嶺のなでしこ 〜たかねこフェスvol.4 出張編〜 福岡 第二部 iLiFE!', 'open_time', None, '17:30', 'takanenonadeshiko.jp 主出处页'),
    ('2025-04-06', '高嶺のなでしこ 〜たかねこフェスvol.4 出張編〜 福岡 第二部 iLiFE!', 'start_time', None, '18:30', 'takanenonadeshiko.jp 主出处页'),
    # 主办方官网：開場12:30予定 / 開演13:50予定
    ('2025-12-31', '第9回 ももいろ歌合戦', 'open_time', None, '12:30', 'https://www.momoclo.net/momoiroutagassen_9/'),
    ('2025-12-31', '第9回 ももいろ歌合戦', 'start_time', None, '13:50', 'https://www.momoclo.net/momoiroutagassen_9/'),
]

# 3) 备注追加：(date, title, 追加片段)
NOTE_APPENDS = [
    ('2025-06-08', 'iLiFE! Zepp6venue tour -TRAVE LiFE!- 台北公演',
     '官方 2025-06-05 告知变更后为开场 17:30、开演 18:30（https://x.com/iLiFE_official/status/1930588831113531395）。'),
]

# 4) 删除：无（全部新增记录都能打开出处并核实）
DELETES = []


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
        return con.execute('SELECT l.id, s.url, l.note, l.venue_id FROM lives l JOIN sources s ON s.id=l.source_id '
                           'WHERE l.date=? AND l.title=?', (date, title)).fetchall()

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
        if cur == newv: log('ALREADY', f'{date} {title} {col}={newv!r}'); continue
        if cur != oldv: log('SKIP', f'{date} {title} {col}: 当前值 {cur!r} 与预期旧值 {oldv!r} 不符'); continue
        if not dry: con.execute(f'UPDATE lives SET {col}=? WHERE id=?', (newv, lid))
        log('APPLY', f'{date} {title} {col}: {cur!r} → {newv!r}（依据 {src}）')

    for date, title, frag in NOTE_APPENDS:
        rows = con.execute('SELECT id, note FROM lives WHERE date=? AND title=?', (date, title)).fetchall()
        if len(rows) != 1: log('SKIP', f'{date} {title} note: 找到 {len(rows)} 条'); continue
        lid, note = rows[0]; note = (note or '').strip()
        if frag in note: log('ALREADY', f'{date} {title} note 已含追加内容'); continue
        if not dry: con.execute('UPDATE lives SET note=? WHERE id=?', ((note + ' ' + frag).strip(), lid))
        log('APPLY', f'{date} {title} note 追加：{frag}')

    for date, title, url in DELETES:
        rows = find(date, title)
        if not rows: log('ALREADY', f'{date} {title}: 已不存在'); continue
        if len(rows) != 1 or rows[0][1] != url: log('SKIP', f'{date} {title}: 未唯一匹配出处 {url}'); continue
        if not dry:
            con.execute('DELETE FROM image_lives WHERE live_id=?', (rows[0][0],))
            con.execute('DELETE FROM live_members WHERE live_id=?', (rows[0][0],))
            con.execute('DELETE FROM lives WHERE id=?', (rows[0][0],))
        log('APPLY', f'{date} {title}: 删除')

    if dry: con.rollback()
    else: con.commit()
    print(f"完成：applied={stats['applied']} already={stats['already']} skip={stats['skip']}{' (dry-run)' if dry else ''}")
    return 1 if stats['skip'] else 0


if __name__ == '__main__':
    sys.exit(main())
