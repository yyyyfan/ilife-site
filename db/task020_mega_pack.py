#!/usr/bin/env python3
"""任务 020：主流出道单曲『アイドルライフメガパック』(2027-01-11) 与发售纪念活动。

数据全部来自官方（已实际打开确认）：
  总公告        https://www.sonymusic.co.jp/artist/iLiFE/info/587699   (2026.10.16)
  各场详情      587717 / 587718 / 587721 / 587722 / 587723
  特设站        https://il-mp.com/    (商品形态・品番・价格・收录曲・会场细分)
  官方 X        https://x.com/iLiFE_official/status/2111064749173879281  (2026-10-16 21:00 JST)

幂等：可重复运行。
用法：python3 db/task020_mega_pack.py [--dry-run]
"""
import os
import sqlite3
import sys

D = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(D, 'ilife.sqlite')
DRY = '--dry-run' in sys.argv

SONY = 'https://www.sonymusic.co.jp/artist/iLiFE/info/'
SRC_TOTAL = SONY + '587699'
SRC_CHIBA = SONY + '587717'
SRC_AICHI = SONY + '587718'
SRC_FUKUOKA = SONY + '587721'
SRC_TOKYO = SONY + '587722'
SRC_OSAKA = SONY + '587723'
SRC_SITE = 'https://il-mp.com/'
SRC_TWEET = 'https://x.com/iLiFE_official/status/2111064749173879281'

TITLE_RI = '『アイドルライフメガパック』発売記念リリースイベント ミニライブ＆特典会'
TITLE_ONLINE = '『アイドルライフメガパック』発売記念 オンラインサイン会＆ビンゴ大会'

# (name, pref, address)
VENUES = [
    ('セブンパークアリオ柏 屋外 スマイルパーク', '千叶', '千葉県柏市大島田1丁目6番地1'),
    ('アリオ札幌 1F えんとつ広場', '北海道', None),
    ('三井ショッピングパーク ららぽーと福岡 1F オーバルパーク', '福冈', '福岡県福岡市博多区那珂6丁目23-1'),
    ('イオンモールむさし村山 駐車場特設ステージ', '东京', '東京都武蔵村山市榎1丁目1-3'),
    ('セブンパーク天美 屋外駐車場 特設ステージ', '大阪', '大阪府松原市天美東三丁目500番地'),
]

# (date, venue_name, pref, type, start_time, source, note)
NOTE_COMMON = ('メジャー1stシングル『アイドルライフメガパック』（2027-01-11 月・祝 発売、Sony Music Labels）'
               'の発売記念リリースイベント。内容：ミニライブ＋特典会＋特典抽選会（ミニライブ観覧はフリー）。')
LIVES = [
    ('2026-11-06', 'セブンパークアリオ柏 屋外 スマイルパーク', '千叶', 'リリイベ', '17:00', SRC_CHIBA,
     NOTE_COMMON + '会場：セブンパークアリオ柏 屋外 スマイルパーク（千葉県柏市大島田1丁目6番地1）。'),
    ('2026-11-08', 'ららぽーと名古屋みなとアクルス', '爱知', 'リリイベ', '14:00', SRC_AICHI,
     NOTE_COMMON + '会場：ららぽーと名古屋みなとアクルス デカゴン（愛知県名古屋市港区港明2丁目3番2号）。'),
    ('2026-11-14', 'オンライン配信', '—', 'リリイベ', None, SRC_TOTAL,
     NOTE_COMMON + '本场为线上活动：オンラインサイン会＋ビンゴ大会（リミスタ）。参加方法・開催時間は公式で未定（後日案内）。'),
    ('2026-11-17', 'アリオ札幌 1F えんとつ広場', '北海道', 'リリイベ', None, SRC_TOTAL,
     NOTE_COMMON + '会場：アリオ札幌 1F えんとつ広場（北海道）。開催時間は公式で「調整中」。'),
    ('2026-12-09', '三井ショッピングパーク ららぽーと福岡 1F オーバルパーク', '福冈', 'リリイベ', '15:00', SRC_FUKUOKA,
     NOTE_COMMON + '会場：三井ショッピングパーク ららぽーと福岡 1F オーバルパーク（福岡県福岡市博多区那珂6丁目23-1）。'),
    ('2026-12-11', 'イオンモールむさし村山 駐車場特設ステージ', '东京', 'リリイベ', '17:00', SRC_TOKYO,
     NOTE_COMMON + '会場：イオンモールむさし村山 駐車場特設ステージ（東京都武蔵村山市榎1丁目1-3）。特典会の場所は後日案内。'),
    ('2027-01-09', 'セブンパーク天美 屋外駐車場 特設ステージ', '大阪', 'リリイベ', '14:00', SRC_OSAKA,
     NOTE_COMMON + '会場：セブンパーク天美 屋外駐車場 特設ステージ（大阪府松原市天美東三丁目500番地）。特典会は 1F AMAMI STADIUM を予定。'),
]

SONG_NOTE = (
    '作詞・作曲・編曲：Medansy（TRIFRONTIER）。4th配信アルバム『アイドルライフメガパック』表題曲（2026-08-26 配信）。'
    '2026-08-16 MV公開。'
    'メジャー1stシングルとして 2027-01-11（月・祝）に Sony Music Labels から CD 発売（3 形態・全 3 曲収録：'
    'アイドルライフメガパック / LiMiT STRiKER! / きゃわぽっぴんどぅー）：'
    '初回生産限定盤（CD+Blu-ray）SRCL-13950〜13951 2,500 円、'
    'メンバー盤 全 9 種 SRCL-13952〜13960 各 1,500 円（各盤にメンバーセレクト曲 1 首）、'
    '通常盤 SRCL-13961 1,500 円。'
    '各形態の CD ジャケット写真は公式で「決まり次第掲載」のため未反映（現封面为配信版 jacket）。'
)


def main():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    log = []

    def src_id(url):
        r = cur.execute('SELECT id FROM sources WHERE url=?', (url,)).fetchone()
        if r:
            return r['id']
        if DRY:
            log.append(f'[dry] 新增 source {url}')
            return -1
        cur.execute('INSERT INTO sources(url) VALUES(?)', (url,))
        log.append(f'新增 source {url}')
        return cur.lastrowid

    for u in [SRC_TOTAL, SRC_CHIBA, SRC_AICHI, SRC_FUKUOKA, SRC_TOKYO, SRC_OSAKA, SRC_SITE, SRC_TWEET]:
        src_id(u)

    def venue_id(name, pref, address=None):
        r = cur.execute('SELECT id FROM venues WHERE name=? AND pref=?', (name, pref)).fetchone()
        if r:
            return r['id']
        if DRY:
            log.append(f'[dry] 新增会场 {name} ({pref})')
            return -1
        cur.execute('INSERT INTO venues(name,pref,address) VALUES(?,?,?)', (name, pref, address))
        log.append(f'新增会场 {name} ({pref})')
        return cur.lastrowid

    for name, pref, addr in VENUES:
        venue_id(name, pref, addr)

    for date, vname, pref, typ, start, surl, note in LIVES:
        vid = venue_id(vname, pref)
        sid = src_id(surl)
        r = cur.execute('SELECT id FROM lives WHERE date=? AND venue_id=?', (date, vid)).fetchone()
        if r:
            if not DRY:
                cur.execute('UPDATE lives SET title=?, type=?, start_time=?, note=?, source_id=? WHERE id=?',
                            (TITLE_ONLINE if typ == 'リリイベ' and vname == 'オンライン配信' else TITLE_RI,
                             typ, start, note, sid, r['id']))
            log.append(f'更新 live {date} {vname}')
        else:
            if not DRY:
                cur.execute('INSERT INTO lives(date,title,venue_id,type,start_time,note,source_id) VALUES(?,?,?,?,?,?,?)',
                            (date, TITLE_ONLINE if vname == 'オンライン配信' else TITLE_RI, vid, typ, start, note, sid))
            log.append(f'新增 live {date} {vname} {start or "时间未定"}')

    s = cur.execute("SELECT id FROM songs WHERE title='アイドルライフメガパック'").fetchone()
    if s:
        if not DRY:
            cur.execute('UPDATE songs SET note=?, source_id=? WHERE id=?', (SONG_NOTE, src_id(SRC_TOTAL), s['id']))
        log.append(f'更新歌曲 {s["id"]} note/source')

    if DRY:
        c.rollback()
    else:
        c.commit()
    print('\n'.join(log) or '无变化')
    print('(dry-run)' if DRY else '已提交')


if __name__ == '__main__':
    main()
