#!/usr/bin/env python3
"""任务 031：把「不是方形」的歌曲封面换成真正的配信 jacket。

030 只补了完全没封面的歌。剩下 15 首虽然 cover_image_id 不为空，但用的是 X 上的
MV 告知图 / 活动横幅（1200x675、1200x799…），在方形卡片里被裁得很难看。
这里把其中「作品本身有官方 jacket」的几首换成 Apple Music 的方形封面：

  アイライフスターターパック!  → 2 sweet timer / 6 Dokkoi! / 10 HUNGRY!!! / 16 Hands Up!
  君セン!                → 12 君セン！
  アイドルライフスターターパック     → 18 ヒラリラリア
  アイドルライフエクストラパック     → 30 ライフステージ / 33 メッセージ（复用 4003）

剩下的 7 首（黄昏サイクル / 可変三連MIX / Shout of Joy / KiSEK! / ドラマチックミライ /
デリバリサマー!! / LiMiT STRiKER!）与 Ride On! 没有任何官方 jacket，保持原样：
前端会优先用官方 MV 缩略图，两者都没有的才显示占位块。

  python3 db/task031_jacket_fill.py --fetch    # 抓 3 张新 jacket 存 img/
  python3 db/r2_images.py add img/jacket-*.webp   # 上传后登记清单
  python3 db/task031_jacket_fill.py --apply    # 入库并改 cover_image_id
"""
import json
import os
import re
import sqlite3
import sys
import urllib.request

from PIL import Image

from curation import load

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
DB = os.path.join(D, 'ilife.sqlite')
OUT = os.path.join(D, '.cache_it', 'jackets031.json')
DRY = '--dry-run' in sys.argv
UA = {'User-Agent': 'Mozilla/5.0'}

# 哪个作品给哪几首歌用，写在 db/curation/jackets.json（附理由）。
# collectionId 是 iTunes 查到的 iLiFE! 作品；release_date 用库里歌曲的发行日。
_JK = load('jackets')
JOBS = [{'name': a['album'], 'cid': a['collection_id'], 'songs': a['songs']} for a in _JK['albums']]
# 库里已有 jacket，直接改指向：{image_id: [song_id, ...]}
REUSE = {r['image']: r['songs'] for r in _JK['reuse']}


def lookup(cid):
    u = f'https://itunes.apple.com/lookup?id={cid}&country=jp'
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
    for r in d['results']:
        if r.get('wrapperType') == 'collection':
            return r
    return None


def key_of(art):
    """artworkUrl100 形如 .../<JAN>.jpg/100x100bb.jpg —— 取倒数第二段当 JAN。"""
    parts = art.rsplit('/', 2)
    stem = re.sub(r'\.(jpg|png)$', '', parts[-2] if len(parts) == 3 else parts[-1])
    stem = re.sub(r'[^0-9A-Za-z_-]', '', stem)
    return f'img/jacket-{stem}.webp' if stem else None


def main():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    dates = {r['id']: r['release_date'] for r in cur.execute('SELECT id, release_date FROM songs')}

    out = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    if '--fetch' in sys.argv:
        for j in JOBS:
            name, cid = j['name'], j['cid']
            if out.get(name):
                continue
            meta = lookup(cid)
            if not meta:
                print(f'  {name}：lookup 失败')
                continue
            art = meta['artworkUrl100']
            url = art.replace('100x100bb', '1200x1200bb')
            key = key_of(art)
            dst = os.path.join(ROOT, key)
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            im = Image.open(__import__('io').BytesIO(raw)).convert('RGB')
            if max(im.size) > 1200:
                r = 1200 / max(im.size)
                im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
            q = 90
            while True:
                im.save(dst, 'WEBP', quality=q, method=6)
                if os.path.getsize(dst) <= 400 * 1024 or q <= 60:
                    break
                q -= 6
            date = meta.get('releaseDate', '')[:10] or dates.get(j['songs'][0])
            out[name] = {'key': key, 'url': url, 'date': date, 'w': im.width, 'h': im.height,
                         'songs': j['songs'], 'cid': cid}
            print(f'  {name} → {key} {im.width}x{im.height} {os.path.getsize(dst)//1024}KB')
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    if '--apply' not in sys.argv:
        return

    man = json.load(open(os.path.join(D, 'r2_manifest.json'), encoding='utf-8'))
    eras = list(cur.execute('SELECT id, start FROM eras ORDER BY start'))
    changed = 0

    def set_cover(iid, sids, label):
        nonlocal changed
        for sid in sids:
            cur.execute('UPDATE songs SET cover_image_id=? WHERE id=?', (iid, sid))
            changed += 1
        print(f'  {label} → image {iid}，{len(sids)} 首')

    for iid, sids in REUSE.items():
        set_cover(iid, sids, f'复用 {iid}')

    for name, v in out.items():
        if v['key'] not in man:
            print(f'  跳过 {name}：{v["key"]} 不在 r2_manifest.json')
            continue
        era = ([e['id'] for e in eras if e['start'] <= v['date']] or [None])[-1]
        old = cur.execute('SELECT id FROM images WHERE url=?', (v['url'],)).fetchone()
        if old:
            iid = old['id']
        elif DRY:
            iid = -1
        else:
            cur.execute('INSERT INTO images(url,orig,date,post_id,text,category,local,source,kind,era,w,h,key_order)'
                        ' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        (v['url'], v['url'], v['date'], None, f'『{name}』公式配信ジャケット', 'official',
                         v['key'], 'Apple Music', None, era, v['w'], v['h'],
                         'url,orig,date,post,text,category,local,source,w,h'))
            iid = cur.lastrowid
            cur.execute('INSERT OR REPLACE INTO image_eras(image_id, era_id) VALUES(?,?)', (iid, era))
        set_cover(iid, v['songs'], name)

    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'{"[dry] " if DRY else ""}共改 {changed} 首')


if __name__ == '__main__':
    if '--fetch' in sys.argv or '--apply' in sys.argv:
        main()
    else:
        sys.exit(__doc__)
