#!/usr/bin/env python3
"""Cloudflare R2 图片清单工具（任务 019）。图片不进 Git、不进 Cloudflare Pages，只放在 R2 桶 ilife-images。

  python3 db/r2_images.py add img/xxx.webp [...]   新图上传到 R2 之后，把本地暂存文件的字节数/md5/类型记入 db/r2_manifest.json
  python3 db/r2_images.py upload-cmd img/xxx.webp  打印用 wrangler 上传的命令（需先 npx wrangler login，见 docs/HANDOFF.md）
  python3 db/r2_images.py verify [--all | --sample N] [键...]
                                                   从公开地址下载并核对 HTTP 200、Content-Type、字节数与 md5（默认抽查 20 个）

公开地址前缀 = db/export.py 的 IMG_BASE。清单格式：{"img/xxx.webp": [字节数, "md5", "Content-Type"]}。
本地 img/ 目录只作暂存（已在 .gitignore），上传并 add 之后可以删除。不需要也不保存任何令牌。"""
import hashlib, json, os, random, sys, urllib.request
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
MAN = os.path.join(D, 'r2_manifest.json')
BUCKET = 'ilife-images'
CT = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.png': 'image/png', '.gif': 'image/gif'}

def img_base():
    src = open(os.path.join(D, 'export.py'), encoding='utf-8').read()
    return src.split("IMG_BASE = '", 1)[1].split("'", 1)[0]

def load():
    return json.load(open(MAN, encoding='utf-8')) if os.path.exists(MAN) else {}

def save(m):
    s = '{\n' + ',\n'.join(f' {json.dumps(k)}: {json.dumps(m[k])}' for k in sorted(m)) + '\n}\n'
    open(MAN, 'w', encoding='utf-8').write(s)

def key_of(p):
    rel = os.path.relpath(os.path.abspath(p), ROOT).replace(os.sep, '/')
    if not rel.startswith('img/'): sys.exit(f'只接受 img/ 下的文件：{p}')
    return rel

def ctype(p):
    ext = os.path.splitext(p)[1].lower()
    if ext not in CT: sys.exit(f'不支持的图片类型：{p}')
    return CT[ext]

def main(a):
    if not a: sys.exit(__doc__)
    cmd, rest = a[0], a[1:]
    if cmd == 'add':
        m = load()
        for p in rest:
            data = open(p, 'rb').read(); k = key_of(p)
            if k in m and m[k][1] != hashlib.md5(data).hexdigest():
                sys.exit(f'{k} 已存在且内容不同：替换图片请换新文件名（不要原地覆盖）')
            m[k] = [len(data), hashlib.md5(data).hexdigest(), ctype(p)]; print('记入', k, m[k])
        save(m)
    elif cmd == 'upload-cmd':
        for p in rest:
            print(f'npx wrangler r2 object put {BUCKET}/{key_of(p)} --file "{p}" --content-type {ctype(p)} --remote')
    elif cmd == 'verify':
        m = load(); base = img_base()
        keys = [x for x in rest if not x.startswith('--') and not x.isdigit()]
        if not keys:
            keys = sorted(m)
            if '--all' not in rest:
                n = int(rest[rest.index('--sample') + 1]) if '--sample' in rest else 20
                keys = random.sample(keys, min(n, len(keys)))
        bad = 0
        for k in keys:
            try:
                r = urllib.request.urlopen(urllib.request.Request(base + k, headers={'User-Agent': 'ilife-r2-verify'}), timeout=60)
                d = r.read(); got = [len(d), hashlib.md5(d).hexdigest(), r.headers.get('Content-Type')]
                ok = r.status == 200 and got == m.get(k)
            except Exception as e:
                got, ok = str(e), False
            if not ok: bad += 1; print('不一致', k, got, m.get(k))
        print(f'核对 {len(keys)} 个对象，问题 {bad} 个（{base}）'); sys.exit(1 if bad else 0)
    else:
        sys.exit(__doc__)

if __name__ == '__main__':
    main(sys.argv[1:])
