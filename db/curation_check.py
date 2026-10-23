#!/usr/bin/env python3
"""校验 db/curation/*.json —— 人工复核数据是不是和数据库对得上。

为什么要单独校验：这些 JSON 是手改的，写错一个 id、少一个 reason、改了公演标题，
代码都不会报错，只会**静默地少一条数据**。这个脚本把这类错误提前抓出来。

  python3 db/curation_check.py            # 有错误返回 1，警告不影响
  python3 db/curation_check.py --strict   # 警告也算失败

检查三类问题
------------
1. 结构：字段齐不齐、id 格式、有没有重复、reason 有没有写
2. 引用：指向的公演 / 成员 / 歌曲 / 图片在库里存不存在
3. 一致性：JSON 说的和数据库里实际的状态是否一致（比如「否决的封面却已经挂上了」）
"""
import os
import re
import sqlite3
import sys

from curation import load

D = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(D, 'ilife.sqlite')
STRICT = '--strict' in sys.argv

VID = re.compile(r'^[\w-]{11}$')
STATUSES = ('出演', '支援', '非正式', '休演', '未出演')

E, W = [], []


def err(msg):
    E.append(msg)


def warn(msg):
    W.append(msg)


def check_keys(obj, allowed, where):
    """拼错 key（比如写成 "keep "）会让数据静默失效，这里直接点名。"""
    for k in obj:
        if k != '_readme' and k not in allowed:
            err(f'{where} 有未知字段 {k!r}（允许：{", ".join(allowed)}）')


def check_reason(item, where):
    r = item.get('reason')
    if not isinstance(r, str) or not r.strip():
        err(f'{where} 缺 reason —— 半年后没人知道为什么这么判')
    elif len(r.strip()) < 6:
        err(f'{where} 的 reason 太短（{r!r}），写清楚是哪张图/哪条视频的问题')


def check_dup(items, key, where):
    seen = {}
    for i, it in enumerate(items, 1):
        k = key(it)
        if k in seen:
            err(f'{where} 重复：{k}（第 {seen[k]} 条和第 {i} 条）')
        else:
            seen[k] = i
    return seen


def need_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def main():
    if not os.path.exists(DB):
        raise SystemExit(f'找不到数据库：{DB}')
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row

    lives = {r['id']: r for r in c.execute('SELECT id, date, title, cover_image_id FROM lives')}
    songs = {r['id']: r['title'] for r in c.execute('SELECT id, title FROM songs')}
    members = {r['name']: r['id'] for r in c.execute('SELECT id, name FROM members')}
    images = {r['id'] for r in c.execute('SELECT id FROM images')}

    stat = []

    # ---------- videos.json ----------
    V = load('videos')
    check_keys(V, ('keep', 'reject'), 'videos.json')
    keep, reject = V.get('keep'), V.get('reject')
    if not isinstance(keep, list) or not isinstance(reject, list):
        err('videos.json 的 keep / reject 必须都是数组')
        keep, reject = keep or [], reject or []

    keep_map = {}
    for i, it in enumerate(keep, 1):
        w = f'videos.json keep[{i}]'
        check_keys(it, ('id', 'song', 'reason'), w)
        vid = it.get('id')
        if not (isinstance(vid, str) and VID.match(vid)):
            err(f'{w} 的 id 不是 11 位 YouTube video_id：{vid!r}')
            continue
        if not need_int(it.get('song')):
            err(f'{w} 的 song 必须是 songs.id 整数：{it.get("song")!r}')
        elif it['song'] not in songs:
            err(f'{w} 指向不存在的歌曲 id={it["song"]}')
        check_reason(it, w)
        keep_map[vid] = it.get('song')
    check_dup(keep, lambda x: x.get('id'), 'videos.json keep')

    reject_ids = set()
    for i, it in enumerate(reject, 1):
        w = f'videos.json reject[{i}]'
        check_keys(it, ('id', 'reason'), w)
        vid = it.get('id')
        if not (isinstance(vid, str) and VID.match(vid)):
            err(f'{w} 的 id 不是 11 位 YouTube video_id：{vid!r}')
            continue
        if vid in keep_map:
            err(f'{w} 同时在 keep 和 reject 里：{vid}')
        reject_ids.add(vid)
        check_reason(it, w)
    check_dup(reject, lambda x: x.get('id'), 'videos.json reject')

    db_un = {}
    for r in c.execute('SELECT song_id, video_id FROM song_videos WHERE official=0'):
        db_un[r['video_id']] = r['song_id']
    for vid, sid in db_un.items():
        if vid not in keep_map:
            err(f'库里有非官方影像 {vid}（song={sid}），但 videos.json keep 里没有 —— 补进去或删掉那行')
        elif keep_map[vid] != sid:
            err(f'{vid} 在 videos.json 记的是 song={keep_map[vid]}，库里是 song={sid}')
    for vid in keep_map:
        if vid not in db_un:
            warn(f'{vid} 已在白名单但还没入库（跑 task032_unofficial_scan.py --apply）')
    for vid in reject_ids & set(db_un):
        err(f'{vid} 在 reject 里，却已经入库了')

    stat.append(('videos.json', f'keep {len(keep_map)} / reject {len(reject_ids)}', f'库里非官方影像 {len(db_un)} 条'))

    # ---------- live_covers.json ----------
    L = load('live_covers')
    check_keys(L, ('reject',), 'live_covers.json')
    rej = L.get('reject') or []
    if not isinstance(rej, list):
        err('live_covers.json 的 reject 必须是数组')
        rej = []
    for i, it in enumerate(rej, 1):
        w = f'live_covers.json reject[{i}]'
        check_keys(it, ('live', 'hint', 'reason'), w)
        lid = it.get('live')
        if not need_int(lid) or lid not in lives:
            err(f'{w} 指向不存在的公演 id={lid!r}')
            continue
        lv = lives[lid]
        if it.get('hint') and it['hint'] != lv['title']:
            warn(f'{w} 的 hint 和库里标题不一致（hint 只是给人看的，不影响逻辑）：\n'
                 f'      hint: {it["hint"]}\n' f'      库里: {lv["title"]}')
        if lv['cover_image_id']:
            warn(f'{w} 公演 {lid} 现在已经有封面了，这条否决可能过期')
        check_reason(it, w)
    check_dup(rej, lambda x: x.get('live'), 'live_covers.json reject')
    stat.append(('live_covers.json', f'reject {len(rej)} 场', ''))

    # ---------- live_members.json ----------
    M = load('live_members')
    check_keys(M, ('no_show_lives', 'overrides'), 'live_members.json')
    ns, ov = M.get('no_show_lives') or [], M.get('overrides') or []
    for i, it in enumerate(ns, 1):
        w = f'live_members.json no_show_lives[{i}]'
        check_keys(it, ('live', 'reason'), w)
        lid = it.get('live')
        if not need_int(lid) or lid not in lives:
            err(f'{w} 指向不存在的公演 id={lid!r}')
            continue
        n = c.execute("SELECT COUNT(*) FROM live_members WHERE live_id=? AND status='出演'", (lid,)).fetchone()[0]
        if n:
            warn(f'{w} 公演 {lid} 库里还有 {n} 条「出演」，说明 task028 没重跑过')
        check_reason(it, w)
    check_dup(ns, lambda x: x.get('live'), 'live_members.json no_show_lives')

    for i, it in enumerate(ov, 1):
        w = f'live_members.json overrides[{i}]'
        check_keys(it, ('live', 'member', 'status', 'reason'), w)
        lid, nm = it.get('live'), it.get('member')
        if not need_int(lid) or lid not in lives:
            err(f'{w} 指向不存在的公演 id={lid!r}')
            continue
        if nm not in members:
            err(f'{w} 的成员名 {nm!r} 不在 members 表里（要用全名，别用昵称）')
            continue
        if it.get('status') not in STATUSES:
            err(f'{w} 的 status 必须是 {" / ".join(STATUSES)}：{it.get("status")!r}')
        else:
            row = c.execute('SELECT status FROM live_members WHERE live_id=? AND member_id=?',
                            (lid, members[nm])).fetchone()
            if row is None:
                warn(f'{w} 库里没有 ({lid}, {nm}) 这条，说明 task028 没重跑过')
            elif row['status'] != it['status']:
                warn(f'{w} 库里是「{row["status"]}」，JSON 写「{it["status"]}」—— 重跑 task028 才对得上')
        check_reason(it, w)
    check_dup(ov, lambda x: (x.get('live'), x.get('member')), 'live_members.json overrides')
    stat.append(('live_members.json', f'整场辞退 {len(ns)} 场 / 单人例外 {len(ov)} 条', ''))

    # ---------- jackets.json ----------
    J = load('jackets')
    check_keys(J, ('albums', 'reuse'), 'jackets.json')
    al, ru = J.get('albums') or [], J.get('reuse') or []
    used_song = {}
    for i, it in enumerate(al, 1):
        w = f'jackets.json albums[{i}]'
        check_keys(it, ('album', 'collection_id', 'songs', 'reason'), w)
        if not (isinstance(it.get('album'), str) and it['album'].strip()):
            err(f'{w} 缺 album 名')
        if not need_int(it.get('collection_id')):
            err(f'{w} 的 collection_id 必须是 iTunes 的整数 id：{it.get("collection_id")!r}')
        ss = it.get('songs')
        if not isinstance(ss, list) or not ss:
            err(f'{w} 的 songs 必须是非空数组')
            ss = []
        for sid in ss:
            if not need_int(sid) or sid not in songs:
                err(f'{w} 指向不存在的歌曲 id={sid!r}')
                continue
            if sid in used_song:
                err(f'歌曲 {sid} 同时出现在「{used_song[sid]}」和「{it.get("album")}」下，只会有一个生效')
            used_song[sid] = it.get('album')
            row = c.execute('SELECT i.local FROM songs s LEFT JOIN images i ON i.id=s.cover_image_id'
                            ' WHERE s.id=?', (sid,)).fetchone()
            if row is None or not (row['local'] or '').startswith('img/jacket-'):
                warn(f'歌曲 {sid}（{songs[sid]}）在 jackets.json 里指定了『{it.get("album")}』，'
                     f'但库里封面不是 jacket 图')
        check_reason(it, w)
    check_dup(al, lambda x: x.get('album'), 'jackets.json albums')

    for i, it in enumerate(ru, 1):
        w = f'jackets.json reuse[{i}]'
        check_keys(it, ('image', 'album', 'songs', 'reason'), w)
        if not need_int(it.get('image')) or it['image'] not in images:
            err(f'{w} 指向不存在的图片 id={it.get("image")!r}')
        ss = it.get('songs') or []
        if not isinstance(ss, list) or not ss:
            err(f'{w} 的 songs 必须是非空数组')
        for sid in ss:
            if not need_int(sid) or sid not in songs:
                err(f'{w} 指向不存在的歌曲 id={sid!r}')
        check_reason(it, w)
    check_dup(ru, lambda x: x.get('image'), 'jackets.json reuse')
    stat.append(('jackets.json', f'作品 {len(al)} 个 / 复用 {len(ru)} 条', f'覆盖歌曲 {len(used_song)} 首'))

    # ---------- 汇总 ----------
    print('人工复核数据校验（db/curation/）\n')
    for name, a, b in stat:
        print(f'  {name:<20} {a}' + (f'    {b}' if b else ''))
    print()
    if W:
        print(f'警告 {len(W)} 条：')
        for m in W:
            print(f'  · {m}')
        print()
    if E:
        print(f'错误 {len(E)} 条：')
        for m in E:
            print(f'  ✗ {m}')
        return 1
    if STRICT and W:
        print('--strict：警告按错误处理')
        return 1
    print('全部通过。' if not W else '无错误（有警告，见上）。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
