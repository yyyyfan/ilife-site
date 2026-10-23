#!/usr/bin/env python3
"""任务 026：给歌曲补官方影像（MV 链接）与更多图片。

数据来源
  影像：db/.cache_yt/channel.json（官方频道全量 93 条，由 db/yt_channel_scan.py 抓取）
        判定「视频标题里出现曲名」，按 MV > Lyric > LIVE > Dance 排序。
  图片：images.text 里以「」『』【】等引号点名曲名的官方帖，且不含票务/抽奖等事务性内容。

分步执行（每步可单独重跑，产物都缓存在 db/.cache_yt/）
  python3 db/task026_song_media.py --plan      # 曲目 → 影像候选，写 song_plan.json
  python3 db/task026_song_media.py --dates     # 抓每个视频的上传日期，写 dates.json
  python3 db/task026_song_media.py --thumbs    # 探测可用的缩略图规格（YouTube CDN 直链），写 thumbs.json
  python3 db/task026_song_media.py --apply     # 写 song_videos / song_images（加 --dry-run 只看）
缩略图不落 R2：它只是视频的元数据，与视频本身同源（YouTube 挂了两者一起挂），不必再存一份。
"""
import json, os, re, sqlite3, sys, time, unicodedata, urllib.request

D = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(D, '.cache_yt')
DB = os.path.join(D, 'ilife.sqlite')
PLAN = os.path.join(CACHE, 'song_plan.json')
DATES = os.path.join(CACHE, 'dates.json')
THUMBS = os.path.join(CACHE, 'thumbs.json')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36'}
DRY = '--dry-run' in sys.argv
THUMB_SPECS = ('maxresdefault', 'sddefault', 'hqdefault')

# 曲名与视频标题写法不一致的，手工给别名（已人工核对）
ALIAS = {
    '可変三連MIXをおぼえる歌': ['可変3連MIX', '可変３連MIX'],
    'Dokkoi!ロマンティック': ['Dokkoiロマンティック'],
    '君セン！': ['君セン'],
    '完全勝利Love&Good！': ['完全勝利Love'],
}
KIND = [('MV', r'【mv】|\[mv\]'), ('Lyric', r'リリックビデオ|lyric\s*video|【リリック'),
        ('Live', r'live\s*movie|live\s*映像|ライブ映像|【live'), ('Dance', r'dance\s*(video|practice)|【dance')]
KSCORE = {'MV': 100, 'Lyric': 60, 'Live': 50, 'Dance': 30, 'Other': 10}

QUOTE_PAIRS = [('「', '」'), ('『', '』'), ('【', '】'), ('“', '”')]
# 事务性/商业性内容：票务、抽选、物贩、粉丝数里程碑、KTV 上架——不是这首歌的图
NOISE = re.compile(r'チケット|レギュレーション|注意事項|お申込|申込|抽選|フォロワー|カラオケ|'
                   r'物販|グッズ|販売|予約受付|受付開始|再販|当落|入金|締切|サイン会', re.I)


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    return re.sub(r'\s+', '', s).lower()


def kind_of(title):
    t = norm(title)
    for k, pat in KIND:
        if re.search(norm(pat) if k != 'MV' else pat, t):
            return k
    return 'Other'


def quoted(text, title):
    t = norm(title)
    return any(norm(a) + t + norm(b) in norm(text) for a, b in QUOTE_PAIRS)


def q(cur, sql, args=()):
    return cur.execute(sql, args).fetchall()


# ---------------- 1. 曲目 → 影像候选 ----------------
def cmd_plan():
    vids = json.load(open(os.path.join(CACHE, 'channel.json'), encoding='utf-8'))
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    songs = list(c.execute('SELECT id,title FROM songs ORDER BY id'))
    plan, used = [], {}
    for s in songs:
        keys = [norm(s['title'])] + [norm(a) for a in ALIAS.get(s['title'], [])]
        cands = []
        for v in vids:
            nt = norm(v['title'])
            if not any(k and k in nt for k in keys):
                continue
            k = kind_of(v['title'])
            cands.append({'vid': v['vid'], 'kind': k, 'title': v['title'],
                          'score': KSCORE[k] - len(v['title']) / 500})
        cands.sort(key=lambda x: -x['score'])
        for v in cands:
            used.setdefault(v['vid'], []).append(s['id'])
        plan.append({'id': s['id'], 'title': s['title'],
                     'videos': [{k: v[k] for k in ('vid', 'kind', 'title')} for v in cands]})
        top = cands[0] if cands else None
        print(f"{s['id']:>2} {s['title'][:22]:<24} {len(cands)} 条 | {top['kind'] if top else '—':<6} "
              f"{(top['title'][:44] if top else '无官方影像')}")
    dup = {v: ids for v, ids in used.items() if len(ids) > 1}
    if dup:
        print('\n一个视频命中多首歌（需人工确认）：')
        for v, ids in dup.items():
            print(' ', v, ids, [p['title'] for p in plan if p['id'] in ids])
    json.dump(plan, open(PLAN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    n = sum(len(p['videos']) for p in plan)
    print(f'\n{sum(1 for p in plan if p["videos"])}/{len(plan)} 首歌有影像，合计 {n} 条 → {PLAN}')


# ---------------- 2. 上传日期 ----------------
def cmd_dates():
    plan = json.load(open(PLAN, encoding='utf-8'))
    cache = json.load(open(DATES, encoding='utf-8')) if os.path.exists(DATES) else {}
    vids = [v['vid'] for p in plan for v in p['videos']]
    todo = [v for v in vids if v not in cache]
    print(f'待抓 {len(todo)} / {len(vids)} 条')
    for i, vid in enumerate(todo, 1):
        url = f'https://www.youtube.com/watch?v={vid}'
        try:
            html = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode('utf-8', 'ignore')
            m = re.search(r'"(?:publishDate|uploadDate)":"(\d{4}-\d{2}-\d{2})', html)
            cache[vid] = m.group(1) if m else None
        except Exception as e:
            print(f'  失败 {vid}: {e}')
            cache[vid] = None
        print(f'  {i}/{len(todo)} {vid} {cache[vid]}')
        time.sleep(0.4)
    json.dump(cache, open(DATES, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('已写', DATES)


# ---------------- 3. 缩略图直链 ----------------
def cmd_thumbs():
    plan = json.load(open(PLAN, encoding='utf-8'))
    out = json.load(open(THUMBS, encoding='utf-8')) if os.path.exists(THUMBS) else {}
    vids = []
    for p in plan:
        for v in p['videos']:
            if v['vid'] not in vids:
                vids.append(v['vid'])
    todo = [v for v in vids if v not in out]
    print(f'待探测 {len(todo)} / {len(vids)} 条')
    for i, vid in enumerate(todo, 1):
        url = None
        for spec in THUMB_SPECS:
            u = f'https://i.ytimg.com/vi/{vid}/{spec}.jpg'
            try:
                r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30)
                if r.status == 200 and int(r.headers.get('Content-Length') or 0) > 2000:
                    url = u
                    break
            except Exception:
                pass
        out[vid] = url
        print(f'  {i}/{len(todo)} {vid} {url or "无缩略图"}')
    json.dump(out, open(THUMBS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'可用 {sum(1 for v in out.values() if v)}/{len(out)} → {THUMBS}')


# ---------------- 4. 写库 ----------------
def cmd_apply():
    plan = json.load(open(PLAN, encoding='utf-8'))
    dates = json.load(open(DATES, encoding='utf-8')) if os.path.exists(DATES) else {}
    th = json.load(open(THUMBS, encoding='utf-8')) if os.path.exists(THUMBS) else {}
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; cur = c.cursor()

    # 影像
    nv = 0
    cur.execute('DELETE FROM song_videos')
    for p in plan:
        for i, v in enumerate(p['videos']):
            if not DRY:
                cur.execute('INSERT INTO song_videos(song_id,video_id,kind,title,date,thumb,ord) VALUES(?,?,?,?,?,?,?)',
                            (p['id'], v['vid'], v['kind'], v['title'], dates.get(v['vid']), th.get(v['vid']), i))
            nv += 1

    # 图片：引号点名曲名 + 非事务性内容 + 非该曲打歌服图
    bypost = {}
    for r in q(cur, 'SELECT id,post_id,date,category,text FROM images ORDER BY id'):
        bypost.setdefault(r['post_id'], []).append(r)
    cos_imgs = {r[0] for r in q(cur, 'SELECT image_id FROM costume_images')}
    cur.execute('DELETE FROM song_images')
    ni = 0
    for p in plan:
        key = norm(p['title'])
        picked = []
        for post, rows in bypost.items():
            tx = rows[0]['text'] or ''
            if key not in norm(tx) or not quoted(tx, p['title']) or NOISE.search(tx):
                continue
            for r in rows:
                if r['category'] == 'illustration' or r['id'] in cos_imgs:
                    continue
                picked.append(r)
        picked.sort(key=lambda r: (r['date'], r['id']))
        for i, r in enumerate(picked):
            if not DRY:
                cur.execute('INSERT INTO song_images(song_id,image_id,ord) VALUES(?,?,?)', (p['id'], r['id'], i))
            ni += 1
        if picked:
            print(f"  {p['id']:>2} {p['title'][:22]:<24} 影像 {len(p['videos'])} 图 {len(picked)}")
    if DRY:
        c.rollback()
    else:
        c.commit()
    print(f'{"[dry] " if DRY else ""}影像 {nv} 条，图片 {ni} 张')


if __name__ == '__main__':
    for flag, fn in (('--plan', cmd_plan), ('--dates', cmd_dates), ('--thumbs', cmd_thumbs), ('--apply', cmd_apply)):
        if flag in sys.argv:
            fn()
            break
    else:
        sys.exit(__doc__)
