#!/usr/bin/env python3
"""015 验收（2026 年）修正脚本 —— 幂等，可在 Codex 后续提交之上重复运行。

用法：python3 2026-fixes.py [path/to/db/ilife.sqlite]   （默认 ./db/ilife.sqlite）
      加 --dry-run 只打印将要做的修改，不写库。

定位方式：一律按 (date, title) + 当前出处 URL / 当前字段值定位演出，不依赖自增 ID；
出处按 url 查找/新建。
若目标记录已是修正后的状态 → 跳过（ALREADY）；若记录不存在或已被他人改成别的值 → 跳过并警告（SKIP），不强改。
所有官方出处均已由 Grok Bot 于 2026-10-19 打开核对：X 帖子通过 X 连接器打开原帖（作者 @iLiFE_official、日期按 post ID 换算 JST）并查看告知图；
主办方页面用 curl --max-time 20 打开并阅读正文。
"""
import sqlite3, sys

X = 'https://x.com/iLiFE_official/status/'
EN = 'https://www.eventernote.com/events/'
UNOFF = '仅非官方来源。'

# 1) 出处升级：Eventernote-only → 官方 X / 主办方官网（旧 Eventernote 链接保留为补充核验）
UPGRADES = [
    # date, title, 当前出处(旧), 官方出处(新), 证据说明
    ('2026-05-05', 'JAPAN JAM 2026 DAY4', EN+'460553', X+'2029051750460866826',
     '官方 2026-03-04 13:30 JST「5月5日に出演する「JAPAN JAM 2026」のタイムテーブル公開」，图：JAPAN JAM 2026 5.5 Tue WING STAGE 12:20～ iLiFE!（WING STAGE トッパー）；图中未写场馆，会场与开场/开演时间以补充 Eventernote 为准。'),
    ('2026-07-25', 'OSAKA GIGANTIC MUSIC FESTIVAL 2026 -THANKS 10TH GIGA- DAY1', EN+'464750', X+'2036639562936836160',
     '官方 2026-03-25 12:01 JST 告知：大阪舞洲スポーツアイランドにて開催される「OSAKA GIGANTIC MUSIC FESTIVAL 2026 -THANKS 10TH GIGA-」出演決定，出演日は7月25日；官方 2026-05-29 18:00 JST 时间表告知（https://x.com/iLiFE_official/status/2060285046632955943）：SKYARENA STAGE 11:00 起出演。'),
    ('2026-08-01', 'TOKYO IDOL FESTIVAL 2026 supported by にしたんクリニック【DAY2】 8/1', EN+'467335', X+'2075188858132799916',
     '官方 2026-07-09 21:02 JST TIF2026 时间表告知：8月1日 14:55〜15:25 HOT STAGE（NEO JAPONISM ×iLiFE!）、20:20〜20:40 SMILE GARDEN；会场据官方 2026-04-08 出演决定图（https://x.com/iLiFE_official/status/2041727779398672384）：開催場所 お台場・青海周辺エリア。开场/开演为整场活动时间（Eventernote）。'),
    ('2026-08-02', 'TOKYO IDOL FESTIVAL 2026 supported by にしたんクリニック【DAY3】 8/2', EN+'467331', X+'2075188858132799916',
     '官方 2026-07-09 21:02 JST TIF2026 时间表告知：8月2日 18:30〜19:00 HOT STAGE（同时发的 2075188605157511191 误写 19:30〜19:00，已被本帖替换）；会场据官方 2026-04-08 出演决定图（https://x.com/iLiFE_official/status/2041727779398672384）：お台場・青海周辺エリア。开场/开演为整场活动时间（Eventernote）。'),
    ('2026-08-10', 'LuckyFes’26 DAY3', EN+'466546', X+'2046786097171329114',
     '官方 2026-04-22 12:00 JST 告知「LuckyFes\'26」出演决定，iLiFE!の出演は8月10日，图：2026/8/8,9,10,11 国営ひたち海浜公園；时间表告知 https://x.com/iLiFE_official/status/2064543256202052043 （RAINBOW ステージ）。开场/开演为整场活动时间（Eventernote）。'),
    ('2026-09-19', "rockin'on presents ROCK IN JAPAN FESTIVAL 2026 9/19", EN+'479208', X+'2062013958916304953',
     '官方 2026-06-03 12:30 JST 告知『ROCK IN JAPAN FES.2026』出演決定，出演日は9月19日（图：iLiFE! at ROCK IN JAPAN FES. 2026. on0919）；官方 2026-06-17 时间表告知（https://x.com/iLiFE_official/status/2067087534388318491）：19:15〜 PARK STAGE。官方帖未写场馆，会场以补充 Eventernote 为准。'),
    ('2026-10-10', 'GFEST.2026 DAY1', EN+'490691', X+'2075512987088269587',
     '官方 2026-07-10 18:30 JST 告知「GFEST.2026」iLiFE!の出演日は10月10日DAY1，图：2026 10.10(土)/10.11(日) Gメッセ群馬，DAY1 10.10 出演者有 iLiFE!。开场/开演以补充 Eventernote 为准。'),
    ('2026-08-29', '2026年プロ野球 パーソル パシフィック・リーグ公式戦北海道日本ハムファイターズ対千葉ロッテマリーンズ21回戦試合終了後イベント〈AFTER GAME〉iLiFE!スペシャルライブ',
     EN+'485432', 'https://www.fighters.co.jp/news/detail/202600904692.html',
     '主办方北海道日本ハムファイターズ官网 2026/06/27「8/29(土)「iLiFE!」出演決定！」：8月29日(土) vs. 千葉ロッテ @ES CON FIELD HOKKAIDO，13:40ごろ ファーストピッチ，〈AFTER GAME〉スペシャルライブ于ヒーローインタビュー終了45分後（予定）、约30分钟，エスコンフィールド・グラウンド内。'),
]

# 2) 字段修正：(date, title, 列, 期望旧值, 新值, 依据)
TD = 'https://ticketdive.com/event/'
FIELD_FIXES = [
    # TicketDive 页面「開場開演時刻は未定です」，0:00 为占位值；官方时间表图：OPEN 10:15(ロビーのみ)/10:30(フロア) START 11:20
    ('2026-04-01', '超iLiVE! supported by refrear', 'open_time', '00:00', '10:15', X+'2036397839182688276'),
    ('2026-04-01', '超iLiVE! supported by refrear', 'start_time', '00:00', '11:20', X+'2036397839182688276'),
    # 10:00 为球场开门、13:40 为 ファーストピッチ，不是演出时间；演出为试合终了后，时间未定
    ('2026-08-29', '2026年プロ野球 パーソル パシフィック・リーグ公式戦北海道日本ハムファイターズ対千葉ロッテマリーンズ21回戦試合終了後イベント〈AFTER GAME〉iLiFE!スペシャルライブ', 'open_time', '10:00', None, 'https://www.fighters.co.jp/news/detail/202600904692.html'),
    ('2026-08-29', '2026年プロ野球 パーソル パシフィック・リーグ公式戦北海道日本ハムファイターズ対千葉ロッテマリーンズ21回戦試合終了後イベント〈AFTER GAME〉iLiFE!スペシャルライブ', 'start_time', '13:40', None, 'https://www.fighters.co.jp/news/detail/202600904692.html'),
    # 主出处 TicketDive 当日日程块：開場 13:00 / 開演 13:40（库里为空）
    ('2026-03-30', 'HEROINES FES -春- DAY1', 'open_time', None, '13:00', TD+'heroinesfes260330_31'),
    ('2026-03-30', 'HEROINES FES -春- DAY1', 'start_time', None, '13:40', TD+'heroinesfes260330_31'),
    # 主办方官网：16:00〜開場 / 17:00〜開演（库里为空）
    ('2026-02-11', 'Idol Valentine Fes 2026', 'open_time', None, '16:00', 'https://idol-valentine-fes.com/'),
    ('2026-02-11', 'Idol Valentine Fes 2026', 'start_time', None, '17:00', 'https://idol-valentine-fes.com/'),
    # 生誕祭：note 中已关联的 TicketDive（HEROINES 官方售票）页面，当日块出演有 iLiFE!，时间如下（库里为空）
    ('2026-01-08', '小熊まむ生誕祭2025', 'open_time', None, '16:00', TD+'mamu260108'),
    ('2026-01-08', '小熊まむ生誕祭2025', 'start_time', None, '17:00', TD+'mamu260108'),
    ('2026-01-30', 'みんなのあいす屋さん2026 前夜祭', 'open_time', None, '13:30', TD+'ice260130'),
    ('2026-01-30', 'みんなのあいす屋さん2026 前夜祭', 'start_time', None, '14:30', TD+'ice260130'),
    ('2026-01-31', 'みんなのあいす屋さん2026 〜あいすが溶けないうちに〜', 'open_time', None, '16:00', TD+'ice260131'),
    ('2026-01-31', 'みんなのあいす屋さん2026 〜あいすが溶けないうちに〜', 'start_time', None, '17:00', TD+'ice260131'),
    ('2026-02-25', '福丸うさ生誕祭2026', 'open_time', None, '16:00', TD+'fukumaru260225'),
    ('2026-02-25', '福丸うさ生誕祭2026', 'start_time', None, '17:00', TD+'fukumaru260225'),
    ('2026-03-26', '虹羽みに生誕祭2026', 'open_time', None, '16:00', TD+'mini260326'),
    ('2026-03-26', '虹羽みに生誕祭2026', 'start_time', None, '17:00', TD+'mini260326'),
    ('2026-09-27', '若葉のあ生誕祭2026', 'open_time', None, '16:00', TD+'noa260927'),
    ('2026-09-27', '若葉のあ生誕祭2026', 'start_time', None, '17:30', TD+'noa260927'),
]

# 3) 备注追加：(date, title, 追加片段)
NOTE_APPENDS = [
    ('2026-04-01', '超iLiVE! supported by refrear',
     '售票页写「開場開演時刻は未定です」（0:00 为占位）；时间据官方 2026-03-24 20:00 JST 时间表图：OPEN 10:15（ロビーのみ）/10:30（フロア） START 11:20（https://x.com/iLiFE_official/status/2036397839182688276）。'),
    ('2026-08-29', '2026年プロ野球 パーソル パシフィック・リーグ公式戦北海道日本ハムファイターズ対千葉ロッテマリーンズ21回戦試合終了後イベント〈AFTER GAME〉iLiFE!スペシャルライブ',
     '开场/开演留空：Eventernote 的 10:00/13:40 是球场开门与 ファーストピッチ 时间，演出在试合终了后（ヒーローインタビュー終了45分後予定），具体时刻未公布。'),
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
