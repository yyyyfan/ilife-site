#!/usr/bin/env python3
"""016 用户决定（2026-10-20）应用脚本 —— 幂等。
用法（在仓库根目录）：python3 <本文件> db/ilife.sqlite [--dry-run]；然后 python3 db/export.py --rebuild-derived 与 --check。
依据：Grok Bot 2026-10-20 用 X 连接器逐帖打开原帖、curl -m 20 打开原页面并逐张看图核对。"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixlib016 import Fixer
f = Fixer(sys.argv); c = f.c
A = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user-decisions-assets.json')))
def add_src(url):
    if f.src_id(url) is None and not f.dry:
        c.execute('INSERT INTO sources(url) VALUES(?)', (url,)); f.log('DONE', f'add source {url}')
# ---- 决定 7：去掉非主办方账号的 2 张图 ----
f.drop_new_image(4368, 'https://pbs.twimg.com/media/ElFEnemU8AAwmt1.jpg?name=orig', '用户决定：非主办方账号（alma）的图不用')
f.drop_new_image(4239, 'https://pbs.twimg.com/media/FwkezqWacAEohSO.jpg?name=orig', '用户决定：非主办方账号（NARLOW）的图不用')
# ---- 决定 4：12 处无法核实的图重新查找（原图仍无法核实，改用核实过的主办方/官方图） ----
NEW = [  # lid, live date, title prefix, post URL, source label, text
 (551, '2024-05-10', 'iLiFE×JamsCollection', 'https://ticketdive.com/event/jams_life', 'TicketDive',
  'iLiFE×JamsCollection2マンLIVE 『ジャムズライフ！』（JamsLiFE!） 告知画像'),
 (573, '2024-07-06', '超NATSUZOME2024', 'https://x.com/natsuzome_info/status/1809165843667800572', 'X @natsuzome_info',
  '／\n#超NATSUZOME2024\nメインステージ争奪戦配信審査結果🔥\n…\nタイムテーブル最新版も公開⏰✨\n＼（7.6 SAT TIMETABLE：iLiFE! SOMARI 10:55-11:10 / NATSU 13:20-13:35）'),
 (578, '2024-07-14', '【7/14】SPARK 2024', 'https://x.com/SPARK_Fes/status/1812446049568764092', 'X @SPARK_Fes',
  '🎆SPARK STAGE🎆\n20:15-20:45\n\n2日目のSPARKを締めくくるのは…\niLiFE! さんです✨\n(@iLiFE_official )\n\n#SPARK2024'),
 (670, '2025-02-22', 'HEROINES CATITUDE', 'https://x.com/heroines_idol/status/1884919601752096923', 'X @heroines_idol',
  '🐈2月22日は猫の日^. ̫.^\n\n2025/02/22(Sat)\n「HEROINES CATITUDE」\n竹芝ニューピアホール\n\n可愛い猫アイドル達がみんなをお出迎え❣️\n\n#ヒロインズ #猫の日'),
 (672, '2025-02-25', 'Jams Collection presents', 'https://x.com/JamsCollection/status/1889268215685198253', 'X @JamsCollection',
  '⏰タイムテーブル公開⏰\n\n2/25🦋\nJams Collection presents\n『ジャムズセッション!! -vol.5-』\n@ Spotify O-EAST\n\n⏰open15:30/start16:15\n\n#ジャムズ'),
 (684, '2025-04-01', 'iLiFE! ゲリラフリーライブ', 'https://x.com/heroines_idol/status/1906723165252018646', 'X @heroines_idol',
  '【 ⚠️ 速報 ⚠️ 】\n\n毎日ヒロインズ新聞 号外発行。\n\n#ヒロインズ（号外：電撃フリーライブ@新宿ReNY OPEN 13:00 START 14:00；@iLiFE_official 1906730827993735619 引用本帖「本日緊急無銭ライブ開催」）'),
 (714, '2025-07-06', '超NATSUZOME 2025', 'https://x.com/natsuzome_info/status/1936002265523069208', 'X @natsuzome_info',
  '‼️"超"5周年 タイムテーブル解禁‼️\n\n今年は全5ステージ‼️🏟️\n\n#超NATSUZOME 2025🌞\n\n⏰2025/7/5(土)6(日)\n🏟️幕張海浜公園Gブロック（07.06 SUN：iLiFE! NATSU 14:45-15:10 / 超 18:10-18:30）'),
 (730, '2025-08-31', '@JAM EXPO 2025', 'https://x.com/at_jam/status/1962097146808967325', 'X @at_jam',
  '【@ JAM EXPO 2025 supported by UP-T】\n\n🍓ストロベリーステージ🍓\niLiFE! これから出演です！💫\n\n#アットジャム\n#アップティー'),
 (825, '2026-07-05', '超NATSUZOME 2026', 'https://x.com/natsuzome_info/status/2073014052859826221', 'X @natsuzome_info',
  '／\n\n超NATSUZOME2026\n『千葉日報』広告掲載‼️\n\n＼\n\n7/4(土)掲載千葉日報にて、\n超NATSUZOME2026の広告掲載🌞✨\n\n本年は7/5(日)出演のiLiFE! / i-COLより\n 「あいす」さんに夏の一面を飾って頂きました📰✨\n\n#超NATSUZOME2026\n#超あいどる'),
 (427, '2023-07-16', 'SPARK 2023 in YAMANAKAKO', 'https://x.com/SPARK_Fes/status/1680438282054950913', 'X @SPARK_Fes',
  'SPARK STAGE\n\n🎇iLiFE!🎇さんです\n(@iLiFE_official )\n\n#SPARK2023'),
]
for lid, d, t, post, label, text in NEW:
    if not f.live_ok(lid, d, t): continue
    a = A[str(lid)]
    add_src(post)
    iid = f.add_image(dict(url=a['url'], date=d, post=post, text=text, source=label, asset=a['asset'], w=a['w'], h=a['h'], lid=lid, year=d[:4]))
    f.bind(lid, iid)
# 663 HEROINES ALBUM 2025 リリイベ 2/1：复用库里官方 1 月リリイベ日程图（4084，含 2/1 一格；本场出处帖 1885236597198873048 引用该图告知 2/1 改到柏の葉）
if f.live_ok(663, '2025-02-01', 'HEROINES ALBUM 2025'):
    f.bind_existing(663, 'https://pbs.twimg.com/media/GhFn-ILaUAAjZh-.jpg?name=orig')
# ---- 决定 5：MV 告知图保留，note 注明以后换 CD 封面 ----
TAIL = '（封面：MV公开告知图）'
NEWTAIL = '（封面：MV公开告知图，暂无 CD 封面；找到 CD/配信封面后替换）'
for sid in (13, 31, 43):
    n = c.execute('SELECT note FROM songs WHERE id=?', (sid,)).fetchone()[0]
    if NEWTAIL in n: f.log('ALREADY', f'song {sid} note')
    elif n.endswith(TAIL):
        if not f.dry: c.execute('UPDATE songs SET note=? WHERE id=?', (n[:-len(TAIL)] + NEWTAIL, sid))
        f.log('DONE', f'song {sid} note')
    else: f.log('SKIP', f'song {sid} note 非预期: {n!r}')
# ---- 决定 8：35 号 JAPANLiFE! 2027 会场 → GMOアリーナさいたま（さいたまスーパーアリーナ的命名权愛称，2026-04-01 起） ----
VN = 'GMOアリーナさいたま（さいたまスーパーアリーナ）'
PREF_URL = 'https://www.pref.saitama.lg.jp/a1101/news/page/news2026033001.html'
NOTE35 = ('会场：さいたまスーパーアリーナ自 2026-04-01 起愛称「GMOアリーナさいたま」（命名权，GMOインターネットグループ，使用期间 2026-04-01〜2032-03-31，'
          '正式名称并记时写作「GMOアリーナさいたま（さいたまスーパーアリーナ）」；改修后 2027 年 4 月重新开馆）。出处：运营方 https://www.saitama-arena.co.jp/news/2026/03303344.html ，'
          '埼玉县 ' + PREF_URL + ' 。官方 @iLiFE_official 2026-08-27 00:02 JST 帖 https://x.com/iLiFE_official/status/2092628762240426222 写「ファイナルはなんとGMOアリーナさいたまで開催」。')
if f.live_ok(35, '2027-04-06', 'JAPANLiFE! 2027'):
    r = c.execute('SELECT id FROM venues WHERE name=? AND pref=?', (VN, '埼玉')).fetchone()
    if r: vid = r[0]; f.log('ALREADY', f'venue {vid}')
    elif not f.dry:
        vid = c.execute('SELECT max(id)+1 FROM venues').fetchone()[0]
        c.execute('INSERT INTO venues(id,name,pref,address,capacity,url) VALUES(?,?,?,?,?,?)', (vid, VN, '埼玉', '埼玉県さいたま市中央区新都心8', 37000, PREF_URL))
        f.log('DONE', f'add venue {vid} {VN}')
    else: vid = None
    cur = c.execute('SELECT venue_id,note FROM lives WHERE id=35').fetchone()
    if cur[0] == vid and cur[1] == NOTE35: f.log('ALREADY', 'live 35 venue')
    elif cur[0] == 25 and not f.dry:
        c.execute('UPDATE lives SET venue_id=?, note=? WHERE id=35', (vid, NOTE35)); f.log('DONE', f'live 35 venue 25 -> {vid}')
    elif cur[0] != 25: f.log('SKIP', f'live 35 venue 非预期 {cur}')
# ---- 决定 1：演出配图的 images.date = 演出日期（多场取最早） ----
# 只改绑定了演出、且没有被成员/歌曲/服装引用的图片
rows = c.execute('''SELECT i.id, i.date, min(l.date) FROM images i JOIN image_lives il ON il.image_id=i.id JOIN lives l ON l.id=il.live_id
  WHERE i.id NOT IN (SELECT image_id FROM image_members) AND i.id NOT IN (SELECT cover_image_id FROM songs WHERE cover_image_id IS NOT NULL)
    AND i.id NOT IN (SELECT image_id FROM costumes WHERE image_id IS NOT NULL) AND i.id NOT IN (SELECT image_id FROM costume_images)
  GROUP BY i.id''').fetchall()
ch = [(iid, old, new) for iid, old, new in rows if old != new]
for iid, old, new in ch:
    if not f.dry: c.execute('UPDATE images SET date=? WHERE id=?', (new, iid))
print(f'date: {len(rows)} 张演出配图，改 {len(ch)} 张；ALREADY {len(rows)-len(ch)}')
json.dump(ch, open('/tmp/016-date-changes.json', 'w'))
f.finish()
