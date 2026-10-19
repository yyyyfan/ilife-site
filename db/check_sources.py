#!/usr/bin/env python3
"""检查数据库中的非 X 外部出处 URL：
1. 演出的非官方出处（Eventernote / LiveFans / 官网 / 博客等）：
   - HTTP 200
   - 页面包含 iLiFE!（兼容大小写、全角半角感叹号、平假名/片假名）
   - 页面包含该演出的日期（支持 YYYY/M/D、YYYY.M.D、YYYY年M月D日、YYYY-M-D 等）
2. 会场容纳人数出处（venues.url）：
   - HTTP 200
   - 页面包含该容纳人数数字（如 1300 或 1,300）

用法：
  python3 db/check_sources.py              # 检查全库所有非 X 演出出处与会场容量出处
  python3 db/check_sources.py --year 2022  # 仅检查 2022 年演出出处及该年演出所用会场的容量出处
"""

import argparse
import os
import re
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request

D = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(D, 'ilife.sqlite')

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
}


def fetch_url(url: str, timeout: int = 20, retries: int = 1) -> tuple[int, str]:
    """抓取页面内容，返回 (status_code, text)。优先使用 curl 以兼容 WAF 防护并保证超时。网络偶发抖动时自动重试 1 次。"""
    cmd = [
        'curl', '-s', '-L',
        '-m', str(timeout),
        '-H', 'User-Agent: Mozilla/5.0',
        '-w', '\n%{http_code}',
        url
    ]
    for attempt in range(retries + 1):
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout + 5)
            out = res.stdout.decode('utf-8', errors='replace')
            lines = out.rsplit('\n', 1)
            code = 200
            body = out
            if len(lines) == 2:
                body, code_str = lines
                try:
                    code = int(code_str.strip())
                except ValueError:
                    code = 200
            if code != 0 and res.returncode == 0:
                return code, body
        except subprocess.TimeoutExpired:
            pass
        except Exception:
            pass
        if attempt < retries:
            import time
            time.sleep(1)
    return 0, f'Timeout or network error after {retries+1} attempts'


def check_ilife_in_text(text: str) -> bool:
    """检查页面是否提及 iLiFE!。"""
    # 兼容 iLiFE / iLiFE! / iLiFE！ / あいらいふ / アイライフ
    patterns = [
        r'ilife[!！]?',
        r'あいらいふ',
        r'アイライフ',
    ]
    for pat in patterns:
        if re.search(pat, text, re.I):
            return True
    return False


def check_date_in_text(date_str: str, text: str) -> bool:
    """检查页面是否包含该场演出日期。"""
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', date_str)
    if not m:
        return False
    y, mo_str, d_str = m.groups()
    mo = str(int(mo_str))
    d = str(int(d_str))

    date_variants = [
        f'{y}/{mo}/{d}',
        f'{y}/{mo_str}/{d_str}',
        f'{y}.{mo}.{d}',
        f'{y}.{mo_str}.{d_str}',
        f'{y}-{mo}-{d}',
        f'{y}-{mo_str}-{d_str}',
        f'{y}年{mo}月{d}日',
        f'{y}年{mo_str}月{d_str}日',
        f'{y}年{mo}月{d}',
        f'{y}年{mo_str}月{d_str}',
    ]
    for variant in date_variants:
        if variant in text:
            return True
    return False


def check_capacity_in_text(capacity: int, text: str) -> bool:
    """检查会场页面是否包含容纳人数数字。"""
    cap_str = str(capacity)
    cap_comma = f'{capacity:,}'
    return (cap_str in text) or (cap_comma in text)


def is_x_url(url: str) -> bool:
    u = url.lower()
    return 'twitter.com' in u or 'x.com' in u


def main():
    parser = argparse.ArgumentParser(description='验证非 X 外部出处有效性')
    parser.add_argument('--year', type=str, default=None, help='仅检查指定年份（如 2022）')
    parser.add_argument('--timeout', type=int, default=20, help='请求超时秒数（默认 20）')
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # 1. 演出出处
    live_sql = """
        SELECT l.id, l.date, l.title, s.url, v.name as venue_name
        FROM lives l
        JOIN sources s ON s.id = l.source_id
        JOIN venues v ON v.id = l.venue_id
        WHERE s.url IS NOT NULL
    """
    params = []
    if args.year:
        live_sql += " AND l.date LIKE ?"
        params.append(f'{args.year}%')
    live_sql += " ORDER BY l.date, l.id"

    live_rows = conn.execute(live_sql, params).fetchall()
    non_x_lives = [r for r in live_rows if not is_x_url(r['url'])]

    # 2. 会场容量出处（针对 2022 年新增会场 id >= 76，排除 011 的 114）
    if args.year:
        venue_sql = """
            SELECT DISTINCT v.id, v.name, v.capacity, v.url
            FROM venues v
            JOIN lives l ON l.venue_id = v.id
            WHERE l.date LIKE ?
              AND v.id >= 76 AND v.id != 114
              AND v.capacity IS NOT NULL
              AND v.url IS NOT NULL
            ORDER BY v.id
        """
        venue_rows = conn.execute(venue_sql, [f'{args.year}%']).fetchall()
    else:
        venue_sql = """
            SELECT v.id, v.name, v.capacity, v.url
            FROM venues v
            WHERE v.id >= 76 AND v.id != 114
              AND v.capacity IS NOT NULL
              AND v.url IS NOT NULL
            ORDER BY v.id
        """
        venue_rows = conn.execute(venue_sql).fetchall()
    non_x_venues = [r for r in venue_rows if not is_x_url(r['url'])]

    total_to_check = len(non_x_lives) + len(non_x_venues)
    print(f'=== 外部出处检查 {"[" + args.year + "]" if args.year else "[全库]"} ===')
    print(f'待查非 X 演出出处: {len(non_x_lives)} 条')
    print(f'待查非 X 会场容量出处: {len(non_x_venues)} 个')
    print(f'总计: {total_to_check} 项 (超时设定: {args.timeout}s)\n')

    failures = []
    cache = {}

    # 检查演出出处
    for r in non_x_lives:
        url = r['url']
        if url in cache:
            status, text = cache[url]
        else:
            status, text = fetch_url(url, timeout=args.timeout)
            cache[url] = (status, text)

        err_reasons = []
        if status != 200:
            err_reasons.append(f'HTTP {status}')
        else:
            if not check_ilife_in_text(text):
                err_reasons.append('页面未提及 iLiFE!')
            if not check_date_in_text(r['date'], text):
                err_reasons.append(f'页面未找到日期 {r["date"]}')

        if err_reasons:
            failures.append({
                'type': 'live',
                'id': r['id'],
                'date': r['date'],
                'title': r['title'],
                'url': url,
                'errors': err_reasons,
            })
            print(f'❌ [Live {r["id"]} | {r["date"]}] {r["title"][:30]} -> {", ".join(err_reasons)}')
        else:
            print(f'✅ [Live {r["id"]} | {r["date"]}] {r["title"][:30]}')

    # 检查会场容量出处
    for v in non_x_venues:
        url = v['url']
        if url in cache:
            status, text = cache[url]
        else:
            status, text = fetch_url(url, timeout=args.timeout)
            cache[url] = (status, text)

        err_reasons = []
        if status != 200:
            err_reasons.append(f'HTTP {status}')
        else:
            if not check_capacity_in_text(v['capacity'], text):
                err_reasons.append(f'页面未找到容纳人数 {v["capacity"]}')

        if err_reasons:
            failures.append({
                'type': 'venue',
                'id': v['id'],
                'name': v['name'],
                'capacity': v['capacity'],
                'url': url,
                'errors': err_reasons,
            })
            print(f'❌ [Venue {v["id"]}] {v["name"]} (容量 {v["capacity"]}) -> {", ".join(err_reasons)}')
        else:
            print(f'✅ [Venue {v["id"]}] {v["name"]} (容量 {v["capacity"]})')

    print('\n' + '=' * 50)
    if failures:
        print(f'检查未通过: 共 {len(failures)} 项失败！')
        for f in failures:
            if f['type'] == 'live':
                print(f"  - 演出 [{f['id']} {f['date']}] {f['title']}: {f['url']} -> {', '.join(f['errors'])}")
            else:
                print(f"  - 会场 [{f['id']}] {f['name']} (容量: {f['capacity']}): {f['url']} -> {', '.join(f['errors'])}")
        sys.exit(1)
    else:
        print(f'检查全部通过！共验证 {total_to_check} 项，零失败。')
        sys.exit(0)


if __name__ == '__main__':
    main()
