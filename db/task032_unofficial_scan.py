#!/usr/bin/env python3
"""任务 032：为「没有任何官方影像」的歌找粉丝上传的现场/全曲影像。

song_videos 原来只收官方影像，18 首（未音源化的 Ride On!、Shout of Joy，以及一批个人曲）
在详情页只能显示「未找到官方影像」。这里搜 YouTube，把候选存成 JSON 供人工过一遍，
确认后用 --apply 以 official=0 入库。

筛选规则（宁缺勿滥）：
- 标题必须包含规范化后的曲名（去空格、去 ！!♡・、。 等装饰符）
- 排除官方频道（iLiFE! / HEROINES / imaginate 等）
- 时长 ≥ 60 秒（滤掉 shorts / 预告切片）
- 同曲最多留 2 条，按播放量取前二

  python3 db/task032_unofficial_scan.py --scan
  python3 db/task032_unofficial_scan.py --apply
"""
import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request

D = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(D, 'ilife.sqlite')
OUT = os.path.join(D, '.cache_it', 'unofficial_videos.json')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept-Language': 'ja'}
OFFICIAL_CH = re.compile(r'iLiFE|アイライフ|HEROINES|imaginate|ヒロインズ', re.I)
MAX_PER_SONG = 2
# 标题里出现这些就不是「演唱影像」：伴奏、卡拉OK、纯音乐
BAD_WORD = re.compile(r'offvocal|off vocal|instrumental|カラオケ|\u30aa\u30d5\u30dc|純音樂|纯音乐', re.I)
# 人工复核否决（标题含曲名但不是 iLiFE! 的视频，或质量不可用）
REJECT_ID = {
    'RqLlc9ezBVc',   # "Snow Magic 01 - Snow Magic" 是别的艺人的同名单曲
    'rnpsFbtClz0',   # 空音「Snow magic」，同名的别人的歌
    'bSTEMwiu8sI',   # Rotaeno 音游曲「Snow Magic」，同上
}
# 人工复核后的白名单：只有这些 video_id 会入库（scan 只是给候选，不当自动结论）
KEEP = {
    'lkWjBhI0H4o', 'R_6nG7R8GhY', 'InyJ9va0kuM', 'qnwTwJOJcQ8',
    'fu83zxnr4FQ', 'r3qESyN-TjA', 'ZMUFYXIC2tQ', 'Bzj3Y546UhM',
    'ydTyxo8MIMY', 'WQi5EhM-NIA', 'XfbKyRvVYhc', 'b5nvRCqTTbY',
    '5b7ZhEwrJuM', 'a6b2EbVx3fg', 'THc9vFd4KIM', 'DpdwBAoAArs',
    '6IXJFqgoF0k', 'FIJ2CYxs7mI', 'tnajFYyqecc', '3WmDeZDlpH0', 'QAAoXw5U1bM',
    # 已有官方影像的 5 首，补 1 条武道馆/ワンマン 粉丝影像，用来验证「官方/非官方」切换
    'bAHtAHkyyI0', 'Ty00fBY90To', 'p41SjwCDo1Q', 'k28_HPwbu4M', '09b8lGO4QmU',
}


def norm(s):
    s = re.sub(r'[\s♡♥！!？?・、,.\u3000「」『』【】\[\]()（）\-–—]', '', s or '')
    return s.lower()


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'ignore')


def search(q):
    h = get('https://www.youtube.com/results?search_query=' + urllib.parse.quote(q))
    out = []
    for blk in re.findall(r'"videoRenderer":\{(.{0,8000}?)\}\]\}\},', h):
        vid = re.search(r'"videoId":"([\w-]{11})"', blk)
        ti = re.search(r'"title":\{"runs":\[\{"text":"([^"]+)"', blk)
        ch = re.search(r'"ownerText":\{"runs":\[\{"text":"([^"]+)"', blk)
        ln = re.search(r'"lengthText":\{[^}]*\{[^}]*\{"label":"([^"]+)"[^}]*\}[^}]*\}[^}]*"simpleText":"([^"]+)"', blk)
        vc = re.search(r'"viewCountText":\{"simpleText":"([^"]+)"', blk)
        if not (vid and ti):
            continue
        dur = 0
        if ln:
            m = re.match(r'(?:(\d+):)?(\d+):(\d+)', ln.group(2) or '')   # simpleText: 3:27
            if m:
                hh, mm, ss = (int(x) if x else 0 for x in m.groups())
                dur = hh * 3600 + mm * 60 + ss
            else:
                mm2 = re.match(r'(?:(\d+)\s*\u6642\u9593)?\s*(?:(\d+)\s*\u5206)?\s*(?:(\d+)\s*\u79d2)?', ln.group(1) or '')
                if mm2 and any(mm2.groups()):
                    hh, mm, ss = (int(x) if x else 0 for x in mm2.groups())
                    dur = hh * 3600 + mm * 60 + ss
        out.append({'id': vid.group(1), 'title': ti.group(1), 'channel': ch.group(1) if ch else '',
                    'dur': dur, 'views': (vc.group(1) if vc else '')})
    return out


def main():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    ids = []
    for a in sys.argv:
        if a.startswith('--ids='):
            ids = [int(x) for x in a.split('=', 1)[1].split(',') if x.strip()]
    if ids:
        # 指定歌：给「已有官方影像」的歌补 1 条粉丝影像，用来验证切换 UI
        q = 'SELECT id, title FROM songs WHERE id IN (%s) ORDER BY id' % ','.join('?' * len(ids))
        rows = list(c.execute(q, ids))
        globals()['MAX_PER_SONG'] = 1
        print(f'指定 {len(rows)} 首')
    else:
        rows = list(c.execute("""SELECT s.id, s.title FROM songs s
            LEFT JOIN song_videos v ON v.song_id=s.id GROUP BY s.id HAVING COUNT(v.id)=0 ORDER BY s.id"""))
        print(f'无官方影像的歌 {len(rows)} 首')

    if '--scan' in sys.argv:
        res = {}
        for r in rows:
            sid, title = r['id'], r['title']
            seen, picks = set(), []
            for q in (f'iLiFE! {title}', f'{title} iLiFE ライブ'):
                try:
                    hits = search(q)
                except Exception as e:
                    print(f'  ! {title}: {e}')
                    continue
                for h in hits:
                    if h['id'] in seen:
                        continue
                    seen.add(h['id'])
                    if norm(title) not in norm(h['title']):
                        continue
                    if OFFICIAL_CH.search(h['channel']):
                        continue
                    if h['dur'] < 60:
                        continue
                    if BAD_WORD.search(h['title']):
                        continue
                    if h['id'] in REJECT_ID:
                        continue
                    picks.append(h)
            picks.sort(key=lambda x: -int(re.sub(r'\D', '', x['views']) or 0))
            picks = picks[:MAX_PER_SONG]
            for pk in picks:
                try:
                    h2 = get('https://www.youtube.com/watch?v=' + pk['id'])
                    m = re.search(r'"publishDate":"(\d{4}-\d{2}-\d{2})', h2) or \
                        re.search(r'"uploadDate":"(\d{4}-\d{2}-\d{2})', h2)
                    pk['date'] = m.group(1) if m else None
                except Exception:
                    pk['date'] = None
            res[str(sid)] = {'title': title, 'picks': picks}
            print(f"  {sid:>2} {title[:20]:<22} {len(picks)} 条" + ('' if picks else '  ← 无'))
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        dst = OUT if not ids else OUT.replace('.json', '_extra.json')
        json.dump(res, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return

    if '--apply' in sys.argv:
        res = {}
        for f in (OUT, OUT.replace('.json', '_extra.json')):
            if os.path.exists(f):
                res.update(json.load(open(f, encoding='utf-8')))
        n = 0
        for sid, v in res.items():
            for i, p in enumerate(v['picks']):
                if p['id'] not in KEEP:
                    continue
                if c.execute('SELECT 1 FROM song_videos WHERE video_id=?', (p['id'],)).fetchone():
                    continue
                t = p['title']
                kind = 'Lyric' if re.search(r'lyric|歌詞|歌词|color coded', t, re.I) else \
                       'Live' if re.search(r'live|生誕|劇場|剧场|映像', t, re.I) else 'Other'
                c.execute('INSERT INTO song_videos(song_id,video_id,kind,title,date,thumb,ord,official,channel)'
                          ' VALUES(?,?,?,?,?,?,?,0,?)',
                          (int(sid), p['id'], kind, t, p.get('date'),
                           f"https://i.ytimg.com/vi/{p['id']}/mqdefault.jpg", 10 + i, p['channel']))
                n += 1
        c.commit()
        print(f'入库 {n} 条非官方影像')


if __name__ == '__main__':
    if '--scan' in sys.argv or '--apply' in sys.argv:
        main()
    else:
        sys.exit(__doc__)
