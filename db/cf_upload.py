#!/usr/bin/env python3
import os
import sys
import json
import base64
import mimetypes
import argparse
import blake3
import requests

API_BASE = 'https://api.cloudflare.com/client/v4/pages/assets/'


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"错误：参数错误：{message}\n")
        sys.stderr.write("用法：python3 db/cf_upload.py [--dry-run] <令牌文件>\n")
        sys.exit(2)


def parse_args():
    parser = CustomArgumentParser(description="Cloudflare Pages 静态资源上传工具")
    parser.add_argument("token_file", help="Cloudflare 上传令牌文件路径（支持纯文本 JWT 或 JSON 格式）")
    parser.add_argument("--dry-run", action="store_true", help="只列出待上传文件和哈希，不调用网络")
    return parser.parse_args()


def load_token(token_path):
    if not os.path.exists(token_path):
        sys.stderr.write(f"错误：令牌文件不存在：{token_path}\n")
        sys.exit(1)
    if not os.path.isfile(token_path):
        sys.stderr.write(f"错误：指定的令牌路径不是普通文件：{token_path}\n")
        sys.exit(1)

    try:
        with open(token_path, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception as e:
        sys.stderr.write(f"错误：读取令牌文件失败：{e}\n")
        sys.exit(1)

    content = raw.strip()
    if not content:
        sys.stderr.write("错误：令牌文件为空\n")
        sys.exit(1)

    if content.startswith("{"):
        try:
            data = json.loads(content)
        except Exception as e:
            sys.stderr.write(f"错误：令牌文件 JSON 格式非法：{e}\n")
            sys.exit(1)

        if not isinstance(data, dict):
            sys.stderr.write("错误：令牌文件 JSON 顶层必须为对象/字典\n")
            sys.exit(1)

        jwt_val = data.get("jwt")
        if jwt_val is None and isinstance(data.get("result"), dict):
            jwt_val = data["result"].get("jwt")

        if not jwt_val or not isinstance(jwt_val, str) or not jwt_val.strip():
            sys.stderr.write("错误：JSON 中未找到有效的 'jwt' 字段\n")
            sys.exit(1)
        token = jwt_val.strip()
    else:
        token = content

    if not token:
        sys.stderr.write("错误：解析出的令牌为空\n")
        sys.exit(1)

    if any(c.isspace() for c in token):
        sys.stderr.write("错误：令牌格式非法（包含空白字符）\n")
        sys.exit(1)

    return token


def collect_files(root_dir, token_file_path):
    root_abs = os.path.abspath(root_dir)
    token_abs = os.path.abspath(token_file_path)
    files = {}

    for d, ds, fs in os.walk(root_abs):
        ds[:] = [x for x in ds if x not in ('.git', 'db')]
        for f in fs:
            p = os.path.join(d, f)
            if os.path.abspath(p) == token_abs:
                continue
            if f.endswith(('.tmp', '.swp', '~')):
                continue

            try:
                with open(p, 'rb') as fp:
                    content_bytes = fp.read()
            except Exception as e:
                sys.stderr.write(f"错误：读取文件失败 {p}：{e}\n")
                sys.exit(1)

            b = base64.b64encode(content_bytes).decode()
            ext = os.path.splitext(f)[1][1:]
            h = blake3.blake3((b + ext).encode()).hexdigest()[:32]
            rel_path = '/' + os.path.relpath(p, root_abs).replace('\\', '/')
            files[rel_path] = (h, p, b)

    return files


def check_response(resp, action_name="请求"):
    if resp.status_code in (401, 403):
        sys.stderr.write(f"错误：Cloudflare 令牌无效或已过期（HTTP {resp.status_code}）\n")
        sys.exit(1)
    if not resp.ok:
        sys.stderr.write(f"错误：Cloudflare API {action_name} 失败（HTTP {resp.status_code}）：{resp.text[:300]}\n")
        sys.exit(1)
    try:
        data = resp.json()
    except Exception:
        sys.stderr.write(f"错误：Cloudflare API {action_name} 返回非 JSON 数据（HTTP {resp.status_code}）\n")
        sys.exit(1)
    if not data.get("success", False):
        errors = data.get("errors", [])
        err_msg = "; ".join([f"[{e.get('code')}] {e.get('message')}" for e in errors if isinstance(e, dict)]) if errors else "未知错误"
        if any(isinstance(e, dict) and (e.get("code") in (10000, 10001) or "auth" in str(e).lower()) for e in errors):
            sys.stderr.write(f"错误：Cloudflare 令牌无效或已过期：{err_msg}\n")
        else:
            sys.stderr.write(f"错误：Cloudflare API {action_name} 失败：{err_msg}\n")
        sys.exit(1)
    return data


def main():
    args = parse_args()
    jwt_token = load_token(args.token_file)

    site_root = os.environ.get('SITE_ROOT')
    if not site_root:
        if os.path.exists('index.html'):
            site_root = '.'
        elif os.path.exists(os.path.join('..', 'index.html')):
            site_root = '..'
        else:
            site_root = '.'

    files = collect_files(site_root, args.token_file)

    if args.dry_run:
        print("[dry-run] 令牌解析成功。")
        print(f"[dry-run] 扫描到 {len(files)} 个待上传文件：")
        for path in sorted(files.keys()):
            h = files[path][0]
            print(f"  {path}: {h}")
        print(f"[dry-run] 共 {len(files)} 个文件，哈希计算完成（未调用网络）。")
        return

    headers = {'Authorization': 'Bearer ' + jwt_token}
    manifest = {k: v[0] for k, v in files.items()}

    manifest_dest = os.environ.get('MANIFEST')
    if not manifest_dest:
        manifest_dest = os.path.join(site_root, 'db', 'cf_manifest.json') if os.path.isdir(os.path.join(site_root, 'db')) else 'cf_manifest.json'

    with open(manifest_dest, 'w', encoding='utf-8') as f:
        json.dump(manifest, f)

    hashes = list({v[0] for v in files.values()})
    try:
        r = requests.post(API_BASE + 'check-missing', headers=headers, json={'hashes': hashes}, timeout=60)
    except requests.RequestException as e:
        sys.stderr.write(f"错误：连接 Cloudflare API 失败：{e}\n")
        sys.exit(1)

    data = check_response(r, "check-missing")
    miss = set(data.get('result', []))
    print(f"扫描到 {len(files)} 个文件，Cloudflare 需上传 {len(miss)} 个缺失文件。")

    byh = {v[0]: v for v in files.values()}
    batch = []
    size = 0

    def send(b):
        try:
            rr = requests.post(API_BASE + 'upload', headers=headers, json=b, timeout=300)
        except requests.RequestException as e:
            sys.stderr.write(f"错误：上传资源到 Cloudflare 失败：{e}\n")
            sys.exit(1)
        check_response(rr, "upload")

    for h in miss:
        _, p, b = byh[h]
        mime_type = mimetypes.guess_type(p)[0] or 'application/octet-stream'
        batch.append({
            'key': h,
            'value': b,
            'metadata': {'contentType': mime_type},
            'base64': True
        })
        size += len(b)
        if size > 30e6 or len(batch) >= 1000:
            send(batch)
            batch = []
            size = 0

    if batch:
        send(batch)

    if miss:
        print(f"成功上传 {len(miss)} 个文件。")

    try:
        resp = requests.post(API_BASE + 'upsert-hashes', headers=headers, json={'hashes': hashes}, timeout=60)
    except requests.RequestException as e:
        sys.stderr.write(f"错误：更新 Cloudflare 资源哈希失败：{e}\n")
        sys.exit(1)

    check_response(resp, "upsert-hashes")
    print("Cloudflare 资源哈希同步成功。")


if __name__ == '__main__':
    main()
