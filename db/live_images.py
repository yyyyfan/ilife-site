#!/usr/bin/env python3
"""任务 025：每场公演收录「出处帖的全部图片」，并按代表性选封面。

背景：原先一场只挂一张图（607 场中 598 场只有 1 张）。出处 X 帖里常有多张（2–4 张），
多出来的没有入库。用户要求：详情页展示该场所有相关图片，封面取最能代表该场演出的那张。

数据来源：公演出处的 X 帖（`sources.url`），用 fxtwitter 取该帖全部 media（已缓存到 `db/.cache_x/`）。
媒体归属无需猜测——同一个帖子的图就是该场的图；库里已有图片的键名带 `live-<live_id>-<媒体ID>`，
可直接判重。

流程（分三步，因为图片必须先上 R2 才能入库）：

  python3 db/live_images.py --stage            # 1. 下载缺图 → 转 webp（长边≤2048、≤1MB）存 img/，写 db/.cache_x/stage.json
  # 2. 上传 R2（见 docs/HANDOFF.md §6.2），再 python3 db/r2_images.py add img/xxx.webp
  python3 db/live_images.py --apply-new        # 3. 入库 + 挂 image_lives
  python3 db/live_images.py --covers           # 4. 按规则重算封面

  --link    只补「已在库但未挂到该场」的图片（不联网、不需上传）
  --dry-run 只打印，不写库
"""
import json
import os
import re
import sqlite3
import sys
import urllib.request

from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
DB = os.path.join(D, 'ilife.sqlite')
CACHE = os.path.join(D, '.cache_x')
PLAN = os.path.join(CACHE, 'plan.json')
STAGE = os.path.join(CACHE, 'stage.json')
IMG = os.path.join(ROOT, 'img')
UA = {'User-Agent': 'Mozilla/5.0'}
DRY = '--dry-run' in sys.argv
MAXSIDE = 2048
MAXBYTES = 1024 * 1024

# 封面评分：越大越「能代表这一场」
#   演出照 > 该场专属告知图 > 官方图 > 打歌服/成员 > 其他；同分优先出自该场出处帖、再按面积
CAT_SCORE = {'live': 100, 'official': 60, 'costume': 40, 'member': 30, 'other': 20}


def media_id(url):
    m = re.search(r'/media/([A-Za-z0-9_-]+)', url or '')
    return m.group(1) if m else None


def key_of(live_id, mid):
    return f'img/live-{live_id}-{mid}.webp'


def q(cur, sql, args=()):
    return list(cur.execute(sql, args))


def existing_mids(cur):
    """库里已登记的媒体 ID → image id（键名 live-<id>-<mid>.webp 或 url 里的媒体名）。"""
    out = {}
    for r in q(cur, 'SELECT id,url,orig,local FROM images'):
        for v in (r['local'], r['url'], r['orig']):
            mid = media_id(v) if v and '/media/' in v else None
            if not mid and v:
                m = re.search(r'live-\d+-([A-Za-z0-9_-]+)\.webp$', v)
                mid = m.group(1) if m else None
            if mid:
                out.setdefault(mid, r['id'])
    return out


def cmd_stage():
    plan = json.load(open(PLAN, encoding='utf-8'))
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    known = existing_mids(cur)
    os.makedirs(IMG, exist_ok=True)
    staged, skip, fail = [], 0, 0
    for p in plan:
        for ph in p['photos']:
            mid = media_id(ph['url'])
            if not mid:
                continue
            if mid in known:
                skip += 1
                continue
            key = key_of(p['live'], mid)
            dst = os.path.join(ROOT, key)
            if not os.path.exists(dst):
                try:
                    req = urllib.request.Request(ph['url'], headers=UA)
                    raw = urllib.request.urlopen(req, timeout=40).read()
                except Exception as e:
                    print(f'  下载失败 live {p["live"]} {mid}: {e}')
                    fail += 1
                    continue
                tmp = dst + '.tmp'
                open(tmp, 'wb').write(raw)
                im = Image.open(tmp)
                im = im.convert('RGB')
                if max(im.size) > MAXSIDE:
                    r = MAXSIDE / max(im.size)
                    im = im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)
                qlt = 88
                while True:
                    im.save(dst, 'WEBP', quality=qlt, method=6)
                    if os.path.getsize(dst) <= MAXBYTES or qlt <= 60:
                        break
                    qlt -= 8
                os.remove(tmp)
            w, h = Image.open(dst).size
            staged.append({'live': p['live'], 'date': p['date'], 'mid': mid, 'key': key,
                           'w': w, 'h': h, 'bytes': os.path.getsize(dst), 'url': ph['url'],
                           'post': p['status'], 'text': p['text'][:200]})
            print(f'  暂存 live {p["live"]} {p["date"]} {key} {w}x{h} {os.path.getsize(dst)//1024}KB')
    json.dump(staged, open(STAGE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'暂存 {len(staged)} 张；已在库跳过 {skip} 张；失败 {fail} 张 → {STAGE}')


def cmd_apply_new():
    staged = json.load(open(STAGE, encoding='utf-8'))
    man = json.load(open(os.path.join(D, 'r2_manifest.json'), encoding='utf-8'))
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    src_of = {}
    for r in q(cur, 'SELECT l.id lid, l.source_id sid, l.date, l.cover_image_id cov, '
                   'i.category cat FROM lives l LEFT JOIN images i ON i.id=l.cover_image_id'):
        src_of[r['lid']] = r
    added = 0
    for s in staged:
        if s['key'] not in man:
            print(f'  跳过 {s["key"]}：不在 r2_manifest.json（先上传 R2 再 r2_images.py add）')
            continue
        lv = src_of.get(s['live'])
        if not lv:
            continue
        cat = lv['cat'] if lv['cat'] in CAT_SCORE else 'official'
        if DRY:
            print(f'  [dry] 入库 live {s["live"]} {s["key"]}')
            continue
        cur.execute('INSERT INTO images(url,orig,date,post_id,text,category,local,source,kind,w,h,key_order)'
                    " VALUES(?,?,?,?,?,?,?,?,?,?,?,'url,orig,date,post,text,category,local,source,w,h')",
                    (s['url'].replace('name=orig', 'name=large'), s['url'], s['date'], lv['sid'],
                     s['text'], cat, s['key'], 'X 出处帖', None, s['w'], s['h']))
        iid = cur.lastrowid
        cur.execute('INSERT OR IGNORE INTO image_lives(live_id,image_id,ord) VALUES(?,?,?)',
                    (s['live'], iid, next_ord(cur, s['live'])))
        added += 1
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'入库 {added} 张')


def era_of(cur, date):
    """按导出规则由日期推时期：取 start <= date 的最后一个时期。"""
    eras = q(cur, 'SELECT id,start FROM eras ORDER BY start')
    hit = [e['id'] for e in eras if e['start'] <= date]
    return hit[-1] if hit else None


def cmd_fix_eras():
    """给缺 image_eras 的图片补时期（导出强制要求，否则 --check 报「image_eras 与日期不符」）。"""
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    n = 0
    for r in q(cur, """SELECT i.id, i.date FROM images i
                       WHERE NOT EXISTS(SELECT 1 FROM image_eras e WHERE e.image_id=i.id)"""):
        eid = era_of(cur, r['date'])
        if not eid:
            print(f'  跳过 image {r["id"]}：{r["date"]} 无对应时期')
            continue
        if DRY:
            print(f'  [dry] image {r["id"]} {r["date"]} → era {eid}')
        else:
            cur.execute('INSERT INTO image_eras(image_id,era_id) VALUES(?,?)', (r['id'], eid))
            cur.execute('UPDATE images SET era=? WHERE id=? AND era IS NULL', (eid, r['id']))
        n += 1
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'补时期 {n} 张')


def next_ord(cur, live_id):
    """image_lives.ord 是 NOT NULL 且无默认值，必须自己算（否则 INSERT OR IGNORE 会静默丢行）。"""
    r = q(cur, 'SELECT COALESCE(MAX(ord),-1)+1 n FROM image_lives WHERE live_id=?', (live_id,))
    return r[0]['n'] if r else 0


def cmd_link():
    """把已入库但未挂到对应公演的图片补挂（按键名 live-<live_id>-）。"""
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    n = 0
    for r in q(cur, "SELECT id,local FROM images WHERE local LIKE 'img/live-%'"):
        m = re.match(r'img/live-(\d+)-', r['local'])
        if not m:
            continue
        lid = int(m.group(1))
        if not q(cur, 'SELECT 1 FROM lives WHERE id=?', (lid,)):
            continue
        if q(cur, 'SELECT 1 FROM image_lives WHERE live_id=? AND image_id=?', (lid, r['id'])):
            continue
        if DRY:
            print(f'  [dry] 补挂 live {lid} ← image {r["id"]} {r["local"]}')
        else:
            cur.execute('INSERT OR IGNORE INTO image_lives(live_id,image_id,ord) VALUES(?,?,?)',
                        (lid, r['id'], next_ord(cur, lid)))
        n += 1
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'补挂 {n} 张')


def cmd_order():
    """把封面排到该场图片的第一位（详情页画廊第一张 = 封面）。"""
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    n = 0
    for lv in q(cur, 'SELECT id, cover_image_id FROM lives WHERE cover_image_id IS NOT NULL'):
        rows = q(cur, 'SELECT image_id, ord FROM image_lives WHERE live_id=? ORDER BY ord, image_id', (lv['id'],))
        if not rows:
            continue
        ids = [r['image_id'] for r in rows]
        if lv['cover_image_id'] not in ids:
            continue
        want = [lv['cover_image_id']] + [i for i in ids if i != lv['cover_image_id']]
        if want == ids:
            continue
        if DRY:
            print(f'  [dry] live {lv["id"]} 重排 {ids} → {want}')
        else:
            for idx, iid in enumerate(want):
                cur.execute('UPDATE image_lives SET ord=? WHERE live_id=? AND image_id=?', (idx, lv['id'], iid))
        n += 1
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'重排 {n} 场（封面置首位）')


def cmd_covers():
    """按代表性重算封面。"""
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    rows = q(cur, """SELECT il.live_id, il.image_id, i.category, i.w, i.h, i.post_id,
                            l.source_id, l.cover_image_id
                     FROM image_lives il
                     JOIN images i ON i.id=il.image_id
                     JOIN lives l ON l.id=il.live_id""")
    best = {}
    for r in rows:
        score = CAT_SCORE.get(r['category'], 20)
        if r['post_id'] == r['source_id']:
            score += 10
        area = (r['w'] or 0) * (r['h'] or 0)
        cur_bonus = 3 if r['image_id'] == r['cover_image_id'] else 0
        cand = (score + cur_bonus, area, -r['image_id'])
        if r['live_id'] not in best or cand > best[r['live_id']][0]:
            best[r['live_id']] = (cand, r['image_id'], r['category'])
    changed = 0
    for lid, (_, iid, cat) in best.items():
        old = q(cur, 'SELECT cover_image_id FROM lives WHERE id=?', (lid,))[0]['cover_image_id']
        if old == iid:
            continue
        if DRY:
            print(f'  [dry] live {lid} 封面 {old} → {iid}（{cat}）')
        else:
            cur.execute('UPDATE lives SET cover_image_id=? WHERE id=?', (iid, lid))
        changed += 1
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'封面改动 {changed} 场（共 {len(best)} 场有图）')


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--stage' in a:
        cmd_stage()
    elif '--apply-new' in a:
        cmd_apply_new()
    elif '--link' in a:
        cmd_link()
    elif '--fix-eras' in a:
        cmd_fix_eras()
    elif '--covers' in a:
        cmd_covers()
    elif '--order' in a:
        cmd_order()
    else:
        print(__doc__)
