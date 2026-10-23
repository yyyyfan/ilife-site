#!/usr/bin/env python3
"""扫描：取每场公演「出处 X 帖」的全部媒体，统计新增图片规模（只读，不改库）。

用法：python3 db/live_images_scan.py [--limit N]
结果写 db/.cache_x/plan.json（缓存单帖响应到 db/.cache_x/<status>.json）
"""
import json, os, re, sqlite3, sys, time, urllib.request

D = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(D, '.cache_x')
DB = os.path.join(D, 'ilife.sqlite')
UA = {'User-Agent': 'Mozilla/5.0'}

def fetch(sid):
    p = os.path.join(CACHE, f'{sid}.json')
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8'))
    for attempt in range(3):
        try:
            req = urllib.request.Request(f'https://api.fxtwitter.com/i/status/{sid}', headers=UA)
            d = json.loads(urllib.request.urlopen(req, timeout=25).read().decode('utf-8'))
            if d.get('code') == 200:
                json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
                return d
        except Exception:
            pass
        time.sleep(1.5 * (attempt + 1))
    return None

def main():
    limit = None
    if '--limit' in sys.argv:
        limit = int(sys.argv[sys.argv.index('--limit') + 1])
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    rows = list(c.execute("""select l.id lid, l.date, l.title, s.url src
        from lives l join sources s on s.id=l.source_id
        where s.url like '%/status/%' order by l.date"""))
    if limit: rows = rows[:limit]
    plan, miss, extra = [], 0, 0
    for r in rows:
        m = re.search(r'/status/(\d+)', r['src'])
        if not m:
            continue
        d = fetch(m.group(1))
        if not d:
            miss += 1; continue
        media = (d.get('tweet') or {}).get('media') or {}
        allm = media.get('all') or []
        photos = [x for x in allm if x.get('type') == 'photo']
        plan.append({'live': r['lid'], 'date': r['date'], 'title': r['title'],
                     'status': m.group(1), 'n_media': len(allm), 'n_photo': len(photos),
                     'photos': [{'url': p.get('url'), 'w': p.get('width'), 'h': p.get('height')} for p in photos],
                     'text': ((d.get('tweet') or {}).get('text') or '')[:300]})
        if len(photos) > 1: extra += len(photos) - 1
        time.sleep(0.25)
    json.dump(plan, open(os.path.join(CACHE, 'plan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    multi = [p for p in plan if p['n_photo'] > 1]
    print(f'公演 {len(plan)} 场（失败 {miss}）；单帖多图 {len(multi)} 场；多出来的图片合计 {extra} 张')
    from collections import Counter
    print('每场图片数分布:', sorted(Counter(p['n_photo'] for p in plan).items()))
    print('样例:', [(p['live'], p['date'], p['n_photo']) for p in multi[:8]])

if __name__ == '__main__':
    main()
