#!/usr/bin/env python3
"""015 验收（2024 年）修正脚本 —— 幂等，可在 Codex 后续提交之上重复运行。

用法：python3 2024-fixes.py [path/to/db/ilife.sqlite]   （默认 ./db/ilife.sqlite）
      加 --dry-run 只打印将要做的修改，不写库。

定位方式：一律按 (date, title) + 当前出处 URL / 当前字段值定位演出，不依赖自增 ID；
会场按 (name, pref) 查找/新建；出处按 url 查找/新建。
若目标记录已是修正后的状态 → 跳过（ALREADY）；若记录不存在或已被他人改成别的值 → 跳过并警告（SKIP），不强改。
所有官方出处均已由 Grok Bot 于 2026-10-19 通过 X 连接器打开原帖（作者 @iLiFE_official，发帖时间换算为 JST）
并查看告知图核对；TicketDive 页面已用 curl 打开核对出演者栏。
"""
import sqlite3, sys

X = 'https://x.com/iLiFE_official/status/'
EN = 'https://www.eventernote.com/events/'
TD = 'https://ticketdive.com/event/'
UNOFF = '仅非官方来源。'

# 1) 出处升级：(date, title, 当前出处(旧), 新出处, 证据说明)；旧链接写进 note 作为补充核验
UPGRADES = [
    ('2024-04-28', '向日えな生誕祭「プリンセスえなピーチ」', EN+'379965', X+'1779827029766230245',
     '官方 2024-04-15 20:00 JST 告知「えな生誕祭 プリンセスえなピーチ 2024/04/28 品川ステラボール」，告知图写 04/28 SUN OPEN16:00 START17:00 @ステラボール，出演 iLiFE!/田中みう(GUEST)。'),
    ('2024-05-08', 'ヒロインズ無銭LIVE 2部(2024/5/8)', EN+'379068', X+'1782715464789139497',
     '官方 2024-04-23 19:17 JST 告知 5月8日ヒロインズ無銭LIVE，告知图写 HEROINES 2024 05/08 @CLUB CITTA\'，2部 iLiFE! OPEN 14:00 START 15:00。'),
    ('2024-07-24', 'コカ･コーラ SUMMER STATION 音楽LIVE 2024/07/24 iLiFE!', EN+'384147', X+'1807700783070408990',
     '官方 2024-07-01 18:00 JST 告知「7月24日 SUMMER STATION 音楽LIVE に単独出演」，告知图写 2024年7月24日(水) @SUMMER STATION LIVE アリーナ OPEN 18:15 START 19:00。'),
    ('2024-09-29', 'HEROINES SUMMER 2024 番外編 DAY2', EN+'392708', TD+'heroinessummer2409',
     '主办方售票页（主催・企画 株式会社imaginate）Day2 日時 2024/9/29(日) 開場 10:00 / 開演 10:45，会場 東武動物公園 イベントステージ HOLA!，出演栏有 iLiFE!。'),
    ('2024-11-12', 'HEROINES アルバムリリースイベント\u3000iLiFE! 池袋サンシャイン広場\u30001部', EN+'400133', X+'1855548138523926575',
     '官方 2024-11-10 18:48 JST 时间变更告知：11/12(火) サンシャインシティ 噴水広場 ①11:30〜/②15:00〜（集合 ①10:50/②14:20）；1部若葉のあ休演。'),
    ('2024-11-17', 'HEROINES ALBUM 2025 リリースイベント', X+'1851966193760112768', X+'1855548138523926575',
     '官方 2024-11-10 18:48 JST 时间变更告知：11/17(日) COCONO SUSUKINO 13:30〜（集合 12:50 / 優先エリア入場 13:00～）。'),
    ('2024-12-07', 'HEROINES ALBUM 2025 リリースイベント in兵庫', EN+'405352', X+'1864905119185375535',
     '官方 2024-12-06 14:30 JST 告知：12/7 @兵庫・あまがさきキューズモール 2F Q’s park 集合 14:50 開演 15:30〜。'),
    ('2024-12-17', 'HEROINES ALBUM 2025 リリースイベント 2部', EN+'410542', X+'1864905119185375535',
     '官方 2024-12-06 14:30 JST 告知：12/17 @東京・サンシャインシティ 噴水広場 第1部 集合 12:50 開演 13:30～，第2部 集合 16:20 開演 17:00～（两部合并为一条）。'),
    ('2024-12-28', 'HEROINES COUNTDOWN Day1', EN+'401471', X+'1871450844270666188',
     '官方 2024-12-24 16:00 JST 告知，图写 2024.12.28(SAT) HEROINES COUNTDOWN @KANDA SQUARE HALL【28日】OPEN 11:00 / START 11:30，12月28日出演グループ有 iLiFE!，时间表 iLiFE! 19:50～20:15。'),
    ('2024-12-29', 'HEROINES COUNTDOWN Day2', EN+'401472', X+'1871450844270666188',
     '官方 2024-12-24 16:00 JST 告知，图写 2024.12.29(SUN)【29日】OPEN 10:30 / START 11:00，12月29日出演グループ有 iLiFE!，时间表 iLiFE! 19:45～20:10。'),
]

# 2) 字段修正：(date, title, 列, 期望旧值, 新值, 依据)
FIELD_FIXES = [
    # 错误
    ('2024-11-04', 'JAPANLiFE! 2024winter', 'start_time', '15:30', '15:10', X+'1843229931989573868'),  # 官方图：金沢エイトホール OPEN 14:30 START 15:10
    ('2024-11-17', 'HEROINES ALBUM 2025 リリースイベント', 'start_time', '14:00', '13:30', X+'1855548138523926575'),  # 官方时间变更
    ('2024-12-17', 'HEROINES ALBUM 2025 リリースイベント 2部', 'open_time', '16:00', '16:20', X+'1864905119185375535'),  # 官方：第2部集合 16:20
    # 官方写「単独出演」，主办为テレビ朝日 SUMMER STATION，不是 iLiFE! 主催
    ('2024-07-24', 'コカ･コーラ SUMMER STATION 音楽LIVE 2024/07/24 iLiFE!', 'type', '主催', 'ワンマン', X+'1807700783070408990'),
    # 补全：官方主出处告知图上直接可见、库里为空
    ('2024-03-30', 'JAPANLiFE! 〜日本アイライファー計画〜', 'open_time', None, '16:00', X+'1739239656452202834'),
    ('2024-03-30', 'JAPANLiFE! 〜日本アイライファー計画〜', 'start_time', None, '17:00', X+'1739239656452202834'),
    ('2024-04-08', 'iLiVE! Vol.12', 'open_time', None, '09:30', X+'1763504633161609343'),
    ('2024-04-08', 'iLiVE! Vol.12', 'start_time', None, '10:30', X+'1763504633161609343'),
    ('2024-05-14', 'iLiVE! Vol.13', 'open_time', None, '10:00', X+'1767128984905720236'),
    ('2024-05-14', 'iLiVE! Vol.13', 'start_time', None, '11:00', X+'1767128984905720236'),
    ('2024-06-09', 'Cinderella Fes', 'start_time', None, '14:00', X+'1795796928015597570'),
    ('2024-06-10', 'iLiVE! Vol.14', 'open_time', None, '09:30', X+'1786708851854839993'),
    ('2024-06-10', 'iLiVE! Vol.14', 'start_time', None, '10:00', X+'1786708851854839993'),
    ('2024-06-23', 'NAMBALiFE!', 'open_time', None, '10:30', X+'1791424222574899201'),
    ('2024-06-23', 'NAMBALiFE!', 'start_time', None, '11:15', X+'1791424222574899201'),
    ('2024-07-13', '馬鹿LiFE!', 'open_time', None, '12:30', X+'1788131793075671424'),
    ('2024-07-13', '馬鹿LiFE!', 'start_time', None, '13:15', X+'1788131793075671424'),
    ('2024-07-30', 'iLiFE! 新体制お披露目LIVE', 'open_time', None, '11:15', X+'1808440579233382840'),
    ('2024-07-30', 'iLiFE! 新体制お披露目LIVE', 'start_time', None, '12:00', X+'1808440579233382840'),
    ('2024-11-08', 'DERARALiFE!', 'open_time', None, '10:30', X+'1845053621467218053'),
    ('2024-11-08', 'DERARALiFE!', 'start_time', None, '11:00', X+'1845053621467218053'),
]

# 3) 备注：(date, title, 旧片段 或 None=追加, 新片段)
NOTE_FIXES = [
    ('2024-11-17', 'HEROINES ALBUM 2025 リリースイベント', '来源为月度排期图。',
     '（原月度排期图写 14:00～，后经官方告知变更为 13:30～。）'),
    ('2024-05-14', 'iLiVE! Vol.13', None,
     '时间取官方告知图 OPEN 10:00 START 11:00（TicketDive 写開演 10:30，Eventernote 写 11:00）。'),
    ('2024-07-06', '超NATSUZOME2024<7/6>', None,
     '楽天チケット页为两日通票，只列两日合并出演者；按日出演依据 Eventernote / LiveFans 详情页。'),
    ('2024-07-07', '超NATSUZOME2024<7/7>', None,
     '楽天チケット页为两日通票，只列两日合并出演者；按日出演依据 Eventernote / LiveFans 详情页。'),
]

# 4) 会场修正：(date, title, 期望旧会场名, 新会场 (name, pref), 依据)
VENUE_FIXES = [
    ('2024-11-03', 'HEROINES ALBUM 2025 リリースイベント', 'なんばパークス 2F', ('北九州リバーウォーク', '福冈'),
     X+'1851966193760112768'),  # 官方排期图：11/3(日) 12:00～ @北九州リバーウォーク(福岡)
]

# 5) 修正后若无演出引用则删除的会场：(name, pref)
ORPHAN_VENUES = [
    ('なんばパークス 2F', '大阪'),  # 只被 11/3 那一场引用，而官方图写的是北九州リバーウォーク
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

    def source_id(url):
        r = con.execute('SELECT id FROM sources WHERE url=?', (url,)).fetchone()
        if r: return r[0]
        return con.execute('INSERT INTO sources(url) VALUES(?)', (url,)).lastrowid

    def find(date, title):
        return con.execute('SELECT l.id, s.url, l.note FROM lives l JOIN sources s ON s.id=l.source_id '
                           'WHERE l.date=? AND l.title=?', (date, title)).fetchall()

    for date, title, old, new, ev in UPGRADES:
        rows = find(date, title)
        if len(rows) != 1:
            log('SKIP', f'{date} {title}: 找到 {len(rows)} 条，未修改'); continue
        lid, cur, note = rows[0]
        if cur == new:
            log('ALREADY', f'{date} {title}: 出处已是 {new}'); continue
        if cur != old:
            log('SKIP', f'{date} {title}: 当前出处 {cur} 既非旧值也非新值，未修改'); continue
        note = (note or '').strip()
        if note.startswith(UNOFF): note = note[len(UNOFF):].strip()
        parts = [ev]
        if old not in note: parts.append(f'补充核验：{title}（{old}）')
        if note: parts.append(note)
        if not dry:
            con.execute('UPDATE lives SET source_id=?, note=? WHERE id=?', (source_id(new), ' '.join(parts), lid))
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
        if oldfrag is None:
            newnote = (note.strip() + ' ' + newfrag).strip()
        else:
            if oldfrag not in note: log('SKIP', f'{date} {title} note: 未找到旧片段'); continue
            newnote = note.replace(oldfrag, newfrag)
        if not dry: con.execute('UPDATE lives SET note=? WHERE id=?', (newnote, lid))
        log('APPLY', f'{date} {title} note: {"追加" if oldfrag is None else "「"+oldfrag+"」→"}「{newfrag}」')

    for date, title, oldname, (vname, pref), src in VENUE_FIXES:
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
        log('APPLY', f'{date} {title} 会场: {cur} → {vname}（{pref}）；地址/容量留空（依据 {src}）')

    for vname, pref in ORPHAN_VENUES:
        r = con.execute('SELECT id FROM venues WHERE name=? AND pref=?', (vname, pref)).fetchone()
        if not r: log('ALREADY', f'会场 {vname}（{pref}）已不存在'); continue
        n = con.execute('SELECT COUNT(*) FROM lives WHERE venue_id=?', (r[0],)).fetchone()[0]
        if n and not dry: log('SKIP', f'会场 {vname}（{pref}）仍被 {n} 场演出引用，未删除'); continue
        if n and dry: print(f'[INFO] dry-run：会场 {vname} 当前仍被 {n} 场引用，实际运行时会先改会场再删除')
        if not dry: con.execute('DELETE FROM venues WHERE id=?', (r[0],))
        log('APPLY', f'删除无引用会场 {vname}（{pref}，id={r[0]}）')

    if dry: con.rollback()
    else: con.commit()
    print(f"完成：applied={stats['applied']} already={stats['already']} skip={stats['skip']}{' (dry-run)' if dry else ''}")
    return 1 if stats['skip'] else 0


if __name__ == '__main__':
    sys.exit(main())
