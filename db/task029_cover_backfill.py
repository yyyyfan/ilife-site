#!/usr/bin/env python3
"""任务 029：为缺封面的公演，从出处页面取活动告知图/海报。

背景：025 只收「出处 X 帖自己的图」，帖里没图就永远没封面。剩 248 场里有 153 场的出处是
eventernote 活动页、13 场是 tiget 售票页——这些页面都带主办方的活动主视觉，正好补这个洞。

分四步（图片必须先上 R2 才能入库）：

  python3 db/task029_cover_backfill.py --scan     # 抓各出处页的 og:image，写 db/.cache_img/plan.json
  python3 db/task029_cover_backfill.py --fetch    # 下载 → 校验 → 转 webp（长边≤2048、≤1MB）存 img/
  # 上传 R2（见 docs/HANDOFF.md §6.2），再 python3 db/r2_images.py add img/xxx.webp
  python3 db/task029_cover_backfill.py --apply    # 入库 + 挂 image_lives + 设为封面

  --dry-run 只打印，不写库
"""
import hashlib
import html as htmllib
import io
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
CACHE = os.path.join(D, '.cache_img')
PLAN = os.path.join(CACHE, 'plan.json')
STAGE = os.path.join(CACHE, 'stage.json')
IMG = os.path.join(ROOT, 'img')
DRY = '--dry-run' in sys.argv
MAXSIDE = 2048
MAXBYTES = 1024 * 1024
MINW = 340                      # 小于这个宽度的当缩略图/占位图，不要（350–500 的多是售票站的小图，卡面够用）

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Accept-Language': 'ja,en;q=0.9'}

# 站点级占位图/logo：og:image 指向它们说明这个页面没有活动主视觉
BAD = re.compile(r'ogp\.webp|/logo|noimage|no_image|no-img|default\.(?:png|jpg)|placeholder'
                 r'|ext_tw_video_thumb|/spskin/|profile_images|/icon', re.I)

# 人工复核后剔除的：都不是活动主视觉
#   316 / 675  og:image 只是站点的 1200x630 分享卡（渐变底 + 小 logo）
#   417        售票页登录墙的空白截图
#   503        极暗的翻拍屏摄，看不清
#   558/602/603/604  同一个「9」logo 被四场共用（主办方默认图，不是单场海报）
#   580 / 581  黑色窄条 banner，只有一个看不清的 logo
REJECT = {316, 417, 503, 558, 580, 581, 602, 603, 604, 675}

# 已知取不到图的域名，扫的时候直接跳过，省时间
SKIP_HOST = {
    'www.livefans.jp',      # 403，需要登录态
    'x.com', 'twitter.com', # 出处帖本身没图（025 已把帖内媒体收完），og:image 只是视频封面
    'ja.wikipedia.org',     # 条目页没有活动图
    'ameblo.jp', 'lineblog.me',  # 博客页 og:image 是博客头图，不是活动海报
}


def host(u):
    return re.sub(r'^https?://', '', u or '').split('/')[0]


def fetch(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def og_image(html):
    """取 og:image（其次 twitter:image）。"""
    for pat in (r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
                r'<meta[^>]+name=["\']twitter:image["\'][^>]*content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*name=["\']twitter:image["\']'):
        m = re.search(pat, html)
        if m:
            return m.group(1)
    return None


def best_image(page_url, html):
    """返回该活动页最合适的图 URL；没有就 None。"""
    cand = og_image(html)
    if not cand:
        return None
    cand = htmllib.unescape(cand)
    if BAD.search(cand):
        return None
    h = host(page_url)
    # eventernote 的 og:image 是 _s 缩略图（654px），换成原图（2000px 左右）
    if 'eventernote' in h and re.search(r'_s\.(jpg|png)$', cand):
        full = re.sub(r'_s\.(jpg|png)$', r'.\1', cand)
        return full
    return cand


def cmd_scan():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    rows = list(c.execute('''SELECT l.id, l.date, l.type, l.title, s.url src
                             FROM lives l JOIN sources s ON s.id = l.source_id
                             WHERE l.cover_image_id IS NULL ORDER BY l.date'''))
    plan, skip = [], []
    for i, r in enumerate(rows, 1):
        h = host(r['src'])
        if h in SKIP_HOST:
            skip.append({'id': r['id'], 'why': 'host skipped', 'src': r['src']})
            continue
        try:
            html = fetch(r['src']).decode('utf-8', 'ignore')
        except Exception as e:
            skip.append({'id': r['id'], 'why': f'fetch: {e}', 'src': r['src']})
            print(f'  {i}/{len(rows)} {r["id"]} 抓取失败 {e}')
            continue
        img = best_image(r['src'], html)
        if not img:
            skip.append({'id': r['id'], 'why': 'no og:image', 'src': r['src']})
        else:
            plan.append({'id': r['id'], 'date': r['date'], 'type': r['type'],
                         'title': r['title'], 'src': r['src'], 'img': img})
        if i % 20 == 0:
            print(f'  {i}/{len(rows)} 候选 {len(plan)}')
    os.makedirs(CACHE, exist_ok=True)
    json.dump({'plan': plan, 'skip': skip}, open(PLAN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'候选 {len(plan)} / 跳过 {len(skip)} → {PLAN}')


def boilerplate(im):
    """识别站点样板图：LivePocket 的「不正なリクエスト」错误页、imaginate 的 logo。

    海报/Timetable 一定是彩色且不满屏单色的；这两类恰好是「几乎纯黑」或「几乎纯白 + 零饱和」。
    """
    small = im.convert('RGB').resize((96, 96))
    px = list(small.getdata())
    n = len(px)
    white = sum(1 for r, g, b in px if r > 235 and g > 235 and b > 235) / n
    dark = sum(1 for r, g, b in px if r < 40 and g < 40 and b < 40) / n
    sat = sum(0 if max(r, g, b) == 0 else (max(r, g, b) - min(r, g, b)) / max(r, g, b) for r, g, b in px) / n
    return sat < 0.06 and (white > 0.5 or dark > 0.5)


def key_of(live_id, url):
    return f'img/live-{live_id}-ev{hashlib.md5(url.encode()).hexdigest()[:8]}.webp'


def cmd_fetch():
    d = json.load(open(PLAN, encoding='utf-8'))
    out = json.load(open(STAGE, encoding='utf-8')) if os.path.exists(STAGE) else {}
    os.makedirs(IMG, exist_ok=True)
    for i, p in enumerate(d['plan'], 1):
        key = key_of(p['id'], p['img'])
        if key in out:
            continue
        try:
            raw = fetch(p['img'], timeout=60)
        except Exception as e:
            print(f'  {i} {p["id"]} 下载失败 {e}')
            out[key] = None
            continue
        try:                       # 直接从内存解码，不落临时文件（避免触发批量删除保护）
            im = Image.open(io.BytesIO(raw))
            im.load()
        except Exception:
            out[key] = None
            continue
        w, h = im.size
        if w < MINW:
            print(f'  {i} {p["id"]} 太小 {w}x{h}')
            out[key] = None
            continue
        im = im.convert('RGB')
        if boilerplate(im):
            print(f'  {i} {p["id"]} 样板图（logo/错误页），跳过')
            out[key] = None
            continue
        if max(im.size) > MAXSIDE:
            r = MAXSIDE / max(im.size)
            im = im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)
        dst = os.path.join(ROOT, key)
        q = 88
        while True:
            im.save(dst, 'WEBP', quality=q, method=6)
            if os.path.getsize(dst) <= MAXBYTES or q <= 60:
                break
            q -= 8
        out[key] = {'live': p['id'], 'date': p['date'], 'url': p['img'], 'src': p['src'],
                    'w': im.width, 'h': im.height, 'bytes': os.path.getsize(dst)}
        print(f'  {i}/{len(d["plan"])} {p["id"]} {key} {im.width}x{im.height} {os.path.getsize(dst)//1024}KB')
        if i % 10 == 0:      # 增量落盘，中途挂掉不用重下
            json.dump(out, open(STAGE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(out, open(STAGE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ok = sum(1 for v in out.values() if v)
    print(f'可用 {ok} / {len(out)} → {STAGE}')


def cmd_upload():
    """逐个 wrangler r2 object put（一次 ~8s，55 个约 8 分钟）。"""
    import subprocess
    stage = json.load(open(STAGE, encoding='utf-8'))
    man = json.load(open(os.path.join(D, 'r2_manifest.json'), encoding='utf-8'))
    todo = [k for k, v in stage.items() if v and v['live'] not in REJECT and k not in man]
    print(f'待传 {len(todo)} 张')
    for i, key in enumerate(todo, 1):
        r = subprocess.run(['npx', 'wrangler', 'r2', 'object', 'put', f'ilife-images/{key}',
                            '--file', key, '--content-type', 'image/webp', '--remote'],
                           cwd=ROOT, shell=(os.name == 'nt'), capture_output=True, text=True)
        print(f'  {i}/{len(todo)} {key} {"ok" if r.returncode == 0 else "FAIL"}')
        if r.returncode != 0:
            print((r.stderr or r.stdout)[-300:])
    if todo:
        subprocess.run([sys.executable, os.path.join(D, 'r2_images.py'), 'add'] + todo, cwd=ROOT)


def cmd_apply():
    stage = json.load(open(STAGE, encoding='utf-8'))
    man = json.load(open(os.path.join(D, 'r2_manifest.json'), encoding='utf-8'))
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    cur = c.cursor()
    eras = list(cur.execute('SELECT id, start FROM eras ORDER BY start'))
    n_img = n_live = 0
    for key, v in sorted(stage.items()):
        if not v:
            continue
        if key not in man:
            print(f'  跳过 {key}：不在 r2_manifest.json（还没上传）')
            continue
        live = v['live']
        if live in REJECT:
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
                        (v['url'], v['url'], v['date'], None, None, 'official', key, host(v['src']),
                         None, era, v['w'], v['h'], 'url,orig,date,post,text,category,local,source,w,h'))
            iid = cur.lastrowid
        if not DRY and not old:
            cur.execute('INSERT OR REPLACE INTO image_eras(image_id, era_id) VALUES(?,?)', (iid, era))
            n_img += 1
        if not DRY:
            cur.execute('INSERT OR IGNORE INTO image_lives(live_id,image_id,ord) VALUES(?,?,0)', (live, iid))
            cur.execute('UPDATE lives SET cover_image_id=? WHERE id=? AND cover_image_id IS NULL', (iid, live))
            n_live += 1
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'{"[dry] " if DRY else ""}新增图片 {n_img} 张，覆盖公演 {n_live} 场')


if __name__ == '__main__':
    if '--scan' in sys.argv:
        cmd_scan()
    elif '--fetch' in sys.argv:
        cmd_fetch()
    elif '--upload' in sys.argv:
        cmd_upload()
    elif '--apply' in sys.argv:
        cmd_apply()
    else:
        sys.exit(__doc__)
