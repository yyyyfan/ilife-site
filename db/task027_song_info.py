#!/usr/bin/env python3
"""任务 027：补齐歌曲信息 + 收录成员个人曲。

做四件事：
  1. songs 加两列：`duration`（曲长）与 `member_id`（个人曲的演唱成员，团体曲为 NULL）。
  2. 用 Apple Music 目录（db/.cache_it/itunes.json）补 52 首的曲长。
  3. 修正发行信息：LiMiT STRiKER! 归入 2027-01-11 的 CD 单曲；无 MV 的歌在 note 里写明「MV 未制作」。
  4. 新增 17 首成员个人曲（配信 EP/シングル収録），带演唱成员、发行日、曲长。

  python3 db/task027_song_info.py --migrate    # 建列（幂等）
  python3 db/task027_song_info.py --apply      # 写数据（--dry-run 只看）
  python3 db/task027_song_info.py --finalize   # 用 song_videos 里 kind=MV 的上传日回填 songs.mv_date
曲长来源：Apple Music（itunes.apple.com，jp 区），只取「该曲首次收录作品」里的时长。
"""
import json, os, re, sqlite3, sys

D = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(D, 'ilife.sqlite')
DRY = '--dry-run' in sys.argv
WIKI = 'https://ja.wikipedia.org/wiki/ILiFE!'

# ---------- 曲长（Apple Music，首次收录版本） ----------
DURATION = {
    '星色トラベラー': '4:12', 'sweet timer': '4:17', '初恋リバイバル': '4:15', 'Sleeping face': '3:33',
    'Quest×Quest': '3:09', 'Dokkoi!ロマンティック': '3:15', '青春のパズルは埋まらない': '4:38',
    'キラメキダイアリー': '4:05', 'HUNGRY!!!': '4:22', 'むげんだいすき': '3:39', '君セン！': '4:14',
    'アイドルライフスターターパック': '3:51', 'Hands Up!': '4:07', 'ヒラリラリア': '4:22',
    '会いにKiTE!': '4:04', 'ころころガール': '3:46', 'ナイナイ恋煩い♡': '3:40',
    'アイドルライフブースターパック': '3:50', 'サイクロンライフ！': '3:42', 'のびしろグリッター': '3:44',
    'キスハグ侵略者！': '3:51', '#ラブコード': '4:35', 'ガンバッテンダー': '3:21', 'ライフステージ': '4:14',
    'アイドルライフエクストラパック': '3:37', 'メッセージ': '3:36', 'LOML': '3:53',
    'くりてぃかる♡ぷりちー': '3:43', 'キュンとクラフト': '3:29', 'ユメクライミング': '3:11',
    '完全勝利Love&Good！': '3:20', 'メロメラ': '4:05', 'BRAVE GROOVE': '3:50',
    'きゃわぽっぴんどぅー': '3:11', 'アイドルライフメガパック': '3:36', 'i REVOLUTION': '3:19',
    'To be alive': '3:29', 'スター☆まむナイズ': '3:38', 'Snow Magic': '4:34', 'MY HERO': '2:54',
    'i': '4:20', 'みんなのあいす屋さん': '3:11', '愛キョウ！最キョウ！逆キョウ上等！': '3:20',
    '私はかわいいよ絶対': '3:50', 'HAPPY IDOL♡': '4:12', 'らぶりー属性♡': '3:39',
    '特別ダメハート♡': '3:37', '初恋サマーライン♡': '4:16', 'だいすき宣言っ！': '3:55',
    'Star*Rise': '3:47', 'フクキタリズム': '3:58', 'かわいくてあいらびゅー': '2:42',
}

# ---------- 无 MV 的歌：在 note 里写明，别让「MV 公开日 —」看着像缺数据 ----------
NO_MV = {
    'sweet timer': 'MV 未制作（LIVE映像のみ）。',
    '初恋リバイバル': 'MV 未制作（LIVE映像のみ）。',
    'Dokkoi!ロマンティック': 'MV 未制作（LIVE映像のみ）。',
    '青春のパズルは埋まらない': 'MV 未制作（LIVE映像のみ）。',
    '完全勝利Love&Good！': 'MV 未制作（Dance Video のみ）。',
    'Sleeping face': 'MV・映像なし。',
    'Quest×Quest': 'MV・映像なし。',
    'キラメキダイアリー': 'MV・映像なし。',
    'HUNGRY!!!': 'MV・映像なし。',
    'メッセージ': 'MV・映像なし。',
}

# ---------- 发行信息修正 ----------
RELEASE_FIX = {
    # LiMiT STRiKER! 未收录于配信版专辑，首发是 2027-01-11 的 CD 单曲（初回限定盤/通常盤 3 曲目）
    'LiMiT STRiKER!': ('アイドルライフメガパック（CD）', '2027-01-11',
                    '2027-01-11 発売の CD シングル『アイドルライフメガパック』収録（配信版には未収録）。'),
}

NOTE_PATCH = {
    '可変三連MIXをおぼえる歌':
        'Apple Music 等の主要配信に iLiFE! 版が見当たらず（2026-10 時点、Medansy 原曲のみ）、配信日は未確認。',
}

# ---------- 17 首成员个人曲 ----------
# 官方推文把其中 5 首明确称作「生誕曲」（生日公演公开的 SOLO 曲），照录；其余只写收录作品。
SOLO = [
    # title, kana, member, release, release_date, note
    ('To be alive', 'とぅー びー あらいぶ', '空詩かれん', 'To be alive', '2025-11-10',
     '空詩かれん 2025 生誕曲。配信シングル『To be alive』収録（同曲の前に SE「The prelude」）。'),
    ('スター☆まむナイズ', 'すたー まむないず', '小熊まむ', 'スター☆まむナイズ', '2026-01-09',
     '小熊まむ ソロ曲。配信シングル『スター☆まむナイズ』収録（同曲の前に SE「Prologue」）。'),
    ('Snow Magic', 'すのー まじっく', '虹羽みに', 'Snow Magic', '2026-05-05',
     '虹羽みに ソロ曲。配信シングル『Snow Magic』収録（同曲の前に SE「fluffy」）。'),
    ('MY HERO', 'まい ひーろー', '純嶺みき', 'MY HERO', '2026-05-13',
     '純嶺みき ソロ曲。配信シングル『MY HERO』収録（SE「〜Beginning of Bloom〜」＋Instrumental 付き）。'),
    ('i', 'あい', 'あいす', 'みんなのあいす屋さん', '2025-03-28',
     'あいす ソロ曲。配信 EP『みんなのあいす屋さん』収録。'),
    ('みんなのあいす屋さん', 'みんなの あいすやさん', 'あいす', 'みんなのあいす屋さん', '2025-03-28',
     'あいす ソロ曲。配信 EP『みんなのあいす屋さん』表題曲。'),
    ('愛キョウ！最キョウ！逆キョウ上等！', 'あいきょう さいきょう ぎゃくきょうじょうとう', 'あいす',
     'みんなのあいす屋さん', '2025-03-28', 'あいす ソロ曲。配信 EP『みんなのあいす屋さん』収録。'),
    ('私はかわいいよ絶対', 'わたしは かわいいよ ぜったい', 'あいす', 'みんなのあいす屋さん', '2025-03-28',
     'あいす ソロ曲。配信 EP『みんなのあいす屋さん』収録。'),
    ('HAPPY IDOL♡', 'はっぴー あいどる', '心花りり', 'らぶりー属性', '2025-12-25',
     '心花りり ソロ曲。配信 EP『らぶりー属性』収録（同 EP 冒頭に SE「♡♡♡」）。'),
    ('らぶりー属性♡', 'らぶりー ぞくせい', '心花りり', 'らぶりー属性', '2025-12-25',
     '心花りり 生誕曲。配信 EP『らぶりー属性』表題曲。'),
    ('特別ダメハート♡', 'とくべつ だめはーと', '心花りり', 'らぶりー属性', '2025-12-25',
     '心花りり ソロ曲。配信 EP『らぶりー属性』収録。'),
    ('初恋サマーライン♡', 'はつこい さまーらいん', '若葉のあ', '初恋サマーライン♡', '2026-01-21',
     '若葉のあ 2025 生誕曲。配信 EP『初恋サマーライン♡』表題曲（Instrumental も同 EP 収録）。'),
    ('だいすき宣言っ！', 'だいすき せんげん', '若葉のあ', '初恋サマーライン♡', '2026-01-21',
     '若葉のあ ソロ曲。配信 EP『初恋サマーライン♡』収録。'),
    ('Star*Rise', 'すたー らいず', '福丸うさ', 'はっぴ〜ばに〜ふぁんたじ〜', '2026-02-26',
     '福丸うさ ソロ曲。配信 EP『はっぴ〜ばに〜ふぁんたじ〜』収録（冒頭に SE「Starry Fanfare」）。'),
    ('フクキタリズム', 'ふくきたりずむ', '福丸うさ', 'はっぴ〜ばに〜ふぁんたじ〜', '2026-02-26',
     '福丸うさ 2025 生誕曲。配信 EP『はっぴ〜ばに〜ふぁんたじ〜』収録。'),
    ('かわいくてあいらびゅー', 'かわいくて あいらびゅー', '福丸うさ', 'はっぴ〜ばに〜ふぁんたじ〜', '2026-02-26',
     '福丸うさ ソロ曲。配信 EP『はっぴ〜ばに〜ふぁんたじ〜』収録。'),
    ('PIXEL by PIXEL', 'ぴくせる ばい ぴくせる', 'あいす', 'PIXEL by PIXEL', None,
     'あいす 2026 生誕曲（iLiFE! / i-COL 名義）。主要配信平台未见该曲（2026-10 时点），配信日未确认。'),
]


def add_note(note, add):
    """把补充说明插到「（封面：…）」之前，保持原备注的收尾格式。"""
    if not add or add in note:
        return note
    i = note.find('（封面：')
    return note[:i] + add + note[i:] if i >= 0 else note + add


def connect():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def cmd_migrate():
    c = connect()
    cols = {r['name'] for r in c.execute('PRAGMA table_info(songs)')}
    for name, ddl in (('member_id', 'INTEGER REFERENCES members(id)'), ('duration', 'TEXT')):
        if name in cols:
            print(f'  已有 songs.{name}')
        else:
            c.execute(f'ALTER TABLE songs ADD COLUMN {name} {ddl}')
            print(f'  新增 songs.{name}')
    c.commit()
    print('迁移完成')


def cmd_apply():
    c = connect()
    cur = c.cursor()
    mid = {r['name']: r['id'] for r in cur.execute('SELECT id,name FROM members')}
    songs = {r['title']: dict(r) for r in cur.execute('SELECT * FROM songs')}
    n_dur = n_note = n_rel = n_new = n_upd = 0

    solo_titles = {x[0] for x in SOLO}
    for title, dur in DURATION.items():
        s = songs.get(title)
        if not s:
            if title not in solo_titles:      # 个人曲在下面 INSERT 时直接带上曲长
                print(f'  ! 曲长找不到歌曲：{title}')
            continue
        if s['duration'] != dur:
            if not DRY:
                cur.execute('UPDATE songs SET duration=? WHERE id=?', (dur, s['id']))
            n_dur += 1

    for title, add in NO_MV.items():
        s = songs.get(title)
        if not s:
            print(f'  ! MV 说明找不到歌曲：{title}')
            continue
        new = add_note(s['note'] or '', add)
        if new != s['note']:
            if not DRY:
                cur.execute('UPDATE songs SET note=? WHERE id=?', (new, s['id']))
            n_note += 1

    for title, add in NOTE_PATCH.items():
        s = songs.get(title)
        if not s:
            print(f'  ! 备注补丁找不到歌曲：{title}')
            continue
        new = add_note(s['note'] or '', add)
        if new != s['note']:
            if not DRY:
                cur.execute('UPDATE songs SET note=? WHERE id=?', (new, s['id']))
            n_note += 1

    for title, (rel, date, add) in RELEASE_FIX.items():
        s = songs.get(title)
        if not s:
            print(f'  ! 发行修正找不到歌曲：{title}')
            continue
        new_note = add_note(s['note'] or '', add)
        if not DRY:
            cur.execute('UPDATE songs SET release=?, release_date=?, note=? WHERE id=?', (rel, date, new_note, s['id']))
        n_rel += 1
        print(f'  发行修正 {title}: {s["release"]} {s["release_date"]} → {rel} {date}')

    nxt = max(songs.values(), key=lambda r: r['id'])['id'] + 1
    src_wiki = cur.execute('SELECT id FROM sources WHERE url=?', (WIKI,)).fetchone()[0]
    for title, kana, member, rel, date, note in SOLO:
        if member not in mid:
            print(f'  ! 成员不存在：{member}')
            continue
        want = (kana, rel, date, note, mid[member], DURATION.get(title))
        if title in songs:
            s = songs[title]
            have = (s['kana'], s['release'], s['release_date'], s['note'], s['member_id'], s['duration'])
            if have != want:
                if not DRY:
                    cur.execute('UPDATE songs SET kana=?,release=?,release_date=?,note=?,member_id=?,duration=? WHERE id=?',
                                (*want, s['id']))
                n_upd += 1
                print(f'  ~ {s["id"]:>2} {title[:24]:<26} 更新个人曲信息')
            continue
        if not DRY:
            cur.execute('INSERT INTO songs(id,title,kana,mv_date,release_date,release,note,source_id,cover_image_id,'
                        'member_id,duration) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                        (nxt, title, kana, None, date, rel, note, src_wiki, None, mid[member], DURATION.get(title)))
        print(f'  + {nxt:>2} {title[:24]:<26} {member} {rel} {date or "—"} {DURATION.get(title) or "—"}')
        nxt += 1
        n_new += 1

    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'{"[dry] " if DRY else ""}曲长 {n_dur} 首、备注 {n_note} 首、发行修正 {n_rel} 首、'
          f'新增个人曲 {n_new} 首、更新个人曲 {n_upd} 首')


def cmd_finalize():
    """MV 上传日回填 mv_date：只认 kind=MV 的第一条，且 mv_date 为空。"""
    c = connect()
    cur = c.cursor()
    rows = cur.execute('''SELECT s.id, s.title, s.mv_date, v.date FROM songs s
                          JOIN song_videos v ON v.song_id=s.id AND v.kind='MV' AND v.ord=0
                          WHERE s.mv_date IS NULL AND v.date IS NOT NULL ORDER BY s.id''').fetchall()
    for r in rows:
        print(f'  mv_date {r["id"]:>2} {r["title"][:24]:<26} → {r["date"]}')
        if not DRY:
            cur.execute('UPDATE songs SET mv_date=? WHERE id=?', (r['date'], r['id']))
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'{"[dry] " if DRY else ""}回填 {len(rows)} 首')


if __name__ == '__main__':
    for flag, fn in (('--migrate', cmd_migrate), ('--apply', cmd_apply), ('--finalize', cmd_finalize)):
        if flag in sys.argv:
            fn()
            break
    else:
        sys.exit(__doc__)
