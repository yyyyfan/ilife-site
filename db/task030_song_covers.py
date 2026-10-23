#!/usr/bin/env python3
"""任务 030：用配信 jacket 补上缺封面的歌曲。

库里已有 12 张 jacket 的先例：`img/jacket-<JAN>.webp`、category=official、
text=『…』公式配信ジャケット、source=Apple Music。这里沿用同一套约定。

18 首缺封面的歌只对应 8 张 jacket（EP/单曲的收录曲共用封面）：
  みんなのあいす屋さん(4 首) / らぶりー属性(3) / 初恋サマーライン♡(2) / はっぴ〜ばに〜ふぁんたじ〜(3)
  + To be alive / スター☆まむナイズ / Snow Magic / MY HERO
Ride On!（未音源化）与 PIXEL by PIXEL（配信平台没有）没有 jacket，保持空。

  python3 db/task030_song_covers.py --fetch    # 查 Apple Music、下载转 webp 存 img/
  # 上传 R2 后：python3 db/r2_images.py add img/jacket-*.webp
  python3 db/task030_song_covers.py --apply    # 入库并设为歌曲封面
"""
import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request

from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
DB = os.path.join(D, 'ilife.sqlite')
CACHE = os.path.join(D, '.cache_it')
OUT = os.path.join(CACHE, 'jackets.json')
IMG = os.path.join(ROOT, 'img')
DRY = '--dry-run' in sys.argv
UA = {'User-Agent': 'Mozilla/5.0'}


def api(term):
    u = 'https://itunes.apple.com/search?term=' + urllib.parse.quote(term) + '&entity=album&country=jp&limit=20'
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))['results']


def norm(s):
    """去空白、去 Apple 的「 - EP / - Single / - Album」后缀，只留作品名。"""
    s = re.sub(r'\s*-\s*(EP|Single|Album|Compilation)\s*$', '', s or '', flags=re.I)
    s = re.sub(r'[\s♡♥！!？?・、,.]', '', s)   # Apple 会把『らぶりー属性』写成『らぶりー属性♡』
    return s.lower()


def find_album(name):
    """在 Apple Music 里找 iLiFE! 的同名作品，返回 artworkUrl100。"""
    for term in (name, 'iLiFE ' + name):
        try:
            res = api(term)
        except Exception as e:
            print(f'    ! 查询失败 {term}: {e}')
            continue
        for r in res:
            if 'iLiFE' not in r.get('artistName', ''):
                continue
            if norm(r.get('collectionName')) == norm(name):
                return r['artworkUrl100']
    return None


def main():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    rows = list(cur.execute('SELECT id,title,release,release_date FROM songs WHERE cover_image_id IS NULL ORDER BY id'))
    albums = {}
    for r in rows:
        if not r['release'] or r['release'] in ('未音源化',):
            print(f'  跳过 {r["title"]}：{r["release"] or "无收录作品"}')
            continue
        albums.setdefault(r['release'], {'date': r['release_date'], 'songs': []})['songs'].append(r['id'])

    out = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    for name, info in albums.items():
        if name in out:
            continue
        art = find_album(name)
        if not art:
            print(f'  {name}：Apple 上没找到')
            out[name] = None
            continue
        url = art.replace('100x100bb', '1200x1200bb')
        # artworkUrl100 形如 .../4582649617574.jpg/100x100bb.jpg —— 取倒数第二段的文件名当 JAN
        parts = art.rsplit('/', 2)
        stem = re.sub(r'\.(jpg|png)$', '', parts[-2] if len(parts) == 3 else parts[-1])
        stem = re.sub(r'[^0-9A-Za-z_-]', '', stem) or re.sub(r'\W+', '', name)
        key = f'img/jacket-{stem}.webp'
        dst = os.path.join(ROOT, key)
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception as e:
            print(f'  {name}：下载失败 {e}')
            out[name] = None
            continue
        tmp = dst + '.tmp'
        open(tmp, 'wb').write(raw)
        im = Image.open(tmp).convert('RGB')
        if max(im.size) > 1200:
            r = 1200 / max(im.size)
            im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        q = 90
        while True:
            im.save(dst, 'WEBP', quality=q, method=6)
            if os.path.getsize(dst) <= 400 * 1024 or q <= 60:
                break
            q -= 6
        os.remove(tmp)
        out[name] = {'key': key, 'url': url, 'date': info['date'], 'w': im.width, 'h': im.height,
                     'bytes': os.path.getsize(dst), 'songs': info['songs']}
        print(f'  {name} → {key} {im.width}x{im.height} {os.path.getsize(dst)//1024}KB  覆盖 {len(info["songs"])} 首')
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    if '--apply' not in sys.argv:
        return

    man = json.load(open(os.path.join(D, 'r2_manifest.json'), encoding='utf-8'))
    eras = list(cur.execute('SELECT id,start FROM eras ORDER BY start'))
    n = 0
    for name, v in out.items():
        if not v:
            continue
        if v['key'] not in man:
            print(f'  跳过 {v["key"]}：不在 r2_manifest.json')
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
        if not DRY:
            for sid in v['songs']:
                cur.execute('UPDATE songs SET cover_image_id=? WHERE id=? AND cover_image_id IS NULL', (iid, sid))
        n += len(v['songs'])
        print(f'  {name} → image {iid}，{len(v["songs"])} 首')
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'{"[dry] " if DRY else ""}覆盖歌曲 {n} 首')


if __name__ == '__main__':
    if '--fetch' in sys.argv or '--apply' in sys.argv:
        main()
    else:
        sys.exit(__doc__)
