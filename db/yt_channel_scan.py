#!/usr/bin/env python3
"""抓取官方 YouTube 频道 @ilife_official 的全部视频（含分页），结果写 db/.cache_yt/channel.json。

新版 YouTube 列表项是 lockupViewModel；分页靠 youtubei/v1/browse + continuation token。
"""
import json, os, re, sys, time, urllib.request

D = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(D, '.cache_yt')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept-Language': 'ja,en;q=0.8'}


def get(url, data=None):
    req = urllib.request.Request(url, data=data, headers=UA)
    if data:
        req.add_header('Content-Type', 'application/json')
    return urllib.request.urlopen(req, timeout=45).read().decode('utf-8', 'replace')


def lockups(obj, out):
    if isinstance(obj, dict):
        if 'lockupViewModel' in obj:
            lv = obj['lockupViewModel']
            cid = lv.get('contentId')
            t = ''
            try:
                t = lv['metadata']['lockupMetadataViewModel']['title']['content']
            except Exception:
                pass
            if cid and t:
                out.append({'vid': cid, 'title': t})
        for v in obj.values():
            lockups(v, out)
    elif isinstance(obj, list):
        for v in obj:
            lockups(v, out)


def cont_token(obj):
    """找下一个 continuation token（跳过 shorts 等其它 tab）。"""
    found = []

    def walk(o):
        if isinstance(o, dict):
            cc = o.get('continuationCommand')
            if isinstance(cc, dict) and cc.get('token'):
                found.append(cc['token'])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return found[0] if found else None


def main():
    os.makedirs(CACHE, exist_ok=True)
    h = get('https://www.youtube.com/@ilife_official/videos')
    key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', h).group(1)
    ver = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', h).group(1)
    d = json.loads(re.search(r'var ytInitialData = (\{.*?\});</script>', h, re.S).group(1))
    vids, seen = [], set()
    lockups(d, vids)
    tok = cont_token(d)
    page = 1
    while tok and page <= 12:
        body = json.dumps({'context': {'client': {'clientName': 'WEB', 'clientVersion': ver,
                                                  'hl': 'ja', 'gl': 'JP'}},
                           'continuation': tok}).encode()
        r = json.loads(get(f'https://www.youtube.com/youtubei/v1/browse?key={key}&prettyPrint=false', body))
        batch = []
        lockups(r, batch)
        new = [b for b in batch if b['vid'] not in seen]
        for b in new:
            seen.add(b['vid'])
        vids.extend(new)
        print(f'第 {page} 页 +{len(new)}（累计 {len(vids)}）')
        tok = cont_token(r)
        page += 1
        time.sleep(0.5)
        if not new:
            break
    # 去重保序
    out, s2 = [], set()
    for v in vids:
        if v['vid'] not in s2:
            s2.add(v['vid'])
            out.append(v)
    json.dump(out, open(os.path.join(CACHE, 'channel.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('视频总数', len(out))


if __name__ == '__main__':
    main()
