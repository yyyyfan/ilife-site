#!/usr/bin/env python3
"""db/ilife.sqlite -> data/*.json（网站 app.js 读取的格式）。
用法：python3 db/export.py          校验并写出 data/*.json
      python3 db/export.py --rebuild-derived  先按日期重算 image_eras 再导出
      python3 db/export.py --check  校验并与现有 data/*.json 逐字节比较（不写文件）
任何完整性检查失败都会报错并以非零码退出，不会写出文件。"""
import json, os, re, sqlite3, sys, datetime
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
c = sqlite3.connect(os.path.join(D, 'ilife.sqlite')); c.row_factory = sqlite3.Row
c.execute('PRAGMA foreign_keys=ON')
Q = lambda sql, *a: c.execute(sql, a).fetchall()
if '--rebuild-derived' in sys.argv:   # 修改 eras 或图片日期后，按日期重算 image_eras
    c.execute('DELETE FROM image_eras')
    c.execute('''INSERT INTO image_eras SELECT i.id,(SELECT e.id FROM eras e WHERE e.start<=i.date ORDER BY e.start DESC LIMIT 1) FROM images i
                 WHERE EXISTS (SELECT 1 FROM eras e WHERE e.start<=i.date)'''); c.commit()
errs = []
def bad(msg): errs.append(msg)

# ---------- 完整性检查 ----------
for r in Q('PRAGMA foreign_key_check'): bad(f'外键失效: {tuple(r)}')
if Q('PRAGMA integrity_check')[0][0] != 'ok': bad('SQLite integrity_check 失败')
def isdate(s):
    try: datetime.date.fromisoformat(s); return True
    except Exception: return False
for t, col, key in [('eras','start','id'),('lives','date','id'),('images','date','id'),('timeline_marks','date','id'),
                    ('member_periods','date_from','id'),('member_periods','date_to','id')]:
    for r in Q(f'SELECT {key} k,{col} v FROM {t} WHERE {col} IS NOT NULL'):
        if not isdate(r['v']): bad(f'{t}.{col} 日期格式错误: id={r["k"]} {r["v"]!r}')
for r in Q('SELECT id,date_from,date_to FROM member_periods WHERE date_to IS NOT NULL AND date_to<date_from'):
    bad(f'member_periods 起止颠倒: {tuple(r)}')
prev = None
for r in Q('SELECT member_id,ord,date_from FROM member_periods ORDER BY member_id,ord'):
    if prev and prev[0] == r[0] and r[2] < prev[2]: bad(f'member_periods 顺序错误: member {r[0]} ord {r[1]}')
    prev = tuple(r)
es = [r['start'] for r in Q('SELECT start FROM eras ORDER BY sort')]
if es != sorted(es): bad(f'eras 开始日期未按顺序: {es}')
for t, cols in [('members','name'),('eras','name'),('images','url,post_id,local'),('venues','name,pref'),('sources','url')]:
    for r in Q(f'SELECT {cols},count(*) n FROM {t} GROUP BY {cols} HAVING n>1'): bad(f'{t} 重复 ({cols}): {tuple(r)}')
for r in Q('SELECT id,local FROM images WHERE local IS NOT NULL'):
    if not os.path.isfile(os.path.join(ROOT, r['local'])): bad(f'图片文件不存在: id={r["id"]} {r["local"]}')
for r in Q("SELECT id FROM images WHERE instr(key_order,'member')=0 AND id IN (SELECT image_id FROM image_members)"
           " UNION SELECT id FROM images WHERE instr(','||key_order||',',',member,')>0 AND id NOT IN (SELECT image_id FROM image_members)"):
    bad(f'image_members 与 images.key_order 不一致: id={r[0]}')
for r in Q('SELECT image_id,count(*) n FROM image_members GROUP BY image_id HAVING n>1'):
    bad(f'图片关联多名成员，images.json 只支持一名: id={r[0]}')
eras = Q('SELECT id,start FROM eras ORDER BY start')
cur = {r['image_id']: r['era_id'] for r in Q('SELECT * FROM image_eras')}
for r in Q('SELECT id,date FROM images'):
    want = ([e['id'] for e in eras if e['start'] <= r['date']] or [None])[-1]
    if cur.get(r['id']) != want: bad(f'image_eras 与日期不符: id={r["id"]} {cur.get(r["id"])} != {want}')
for r in Q('SELECT i.id,i.era,e.era_id FROM images i LEFT JOIN image_eras e ON e.image_id=i.id WHERE i.era IS NOT NULL AND i.era IS NOT e.era_id'):
    bad(f'images.era 与日期推算时期不符: id={r[0]} {r[1]} != {r[2]}（时期起始日=新体制首批アー写或成员变动日）')
for r in Q('SELECT id,local,w,h FROM images'):
    if r['local'] and (r['w'] is None) != (r['h'] is None): bad(f'图片尺寸不完整: id={r["id"]}')
if errs:
    print('完整性检查失败（%d 项）：' % len(errs), file=sys.stderr)
    for e in errs[:200]: print('  -', e, file=sys.stderr)
    sys.exit(1)

# ---------- 生成 ----------
url = {r['id']: r['url'] for r in Q('SELECT * FROM sources')}
def obj(order, get):
    return {k: get(k) for k in order.split(',')} if order else {}
out = {}
fs = {}
for r in Q('SELECT * FROM member_fields_sources ORDER BY member_id,ord'): fs.setdefault(r['member_id'], {})[r['field']] = url[r['source_id']]
mname = {}
M = []
for r in Q('SELECT * FROM members ORDER BY sort'):
    mname[r['id']] = r['name']
    M.append(obj(r['key_order'], lambda k: url.get(r['source_id']) if k == 'source' else fs.get(r['id'], {}) if k == 'sources'
                 else r['left_'] if k == 'left' else r[k]))
out['members'] = M
lineup = {}
for r in Q('SELECT * FROM era_members ORDER BY era_id,ord'):
    lineup.setdefault(r['era_id'], []).append(mname[r['member_id']] + (f"({r['role']})" if r['role'] else ''))
out['eras'] = [{'id': r['id'], 'name': r['name'], 'start': r['start'], 'lineup': lineup.get(r['id'], []),
                'change': r['change'], 'source': url.get(r['source_id'])} for r in Q('SELECT * FROM eras ORDER BY sort')]
out['lives'] = [{'id': r['id'], 'date': r['date'], 'title': r['title'], 'venue': r['vn'], 'pref': r['pref'], 'source': url.get(r['source_id'])}
                for r in Q('SELECT l.*,v.name vn,v.pref FROM lives l JOIN venues v ON v.id=l.venue_id ORDER BY l.rowid')]
seg = {}
for r in Q('SELECT * FROM member_periods ORDER BY member_id,ord'):
    seg.setdefault(r['member_id'], []).append(obj(r['key_order'], lambda k: r[{'from': 'date_from', 'to': 'date_to'}.get(k, k)]))
meta = {r['key']: r['value'] for r in Q('SELECT * FROM meta')}
out['timeline'] = {'source': meta['timeline.source'], 'note': meta['timeline.note'],
                   'members': [{'name': r['name'], 'segments': seg.get(r['id'], [])} for r in Q('SELECT id,name FROM members WHERE tl_sort IS NOT NULL ORDER BY tl_sort')],
                   'marks': [{'date': r['date'], 'label': r['label']} for r in Q('SELECT * FROM timeline_marks ORDER BY id')]}
im = {r['image_id']: mname[r['member_id']] for r in Q('SELECT * FROM image_members')}
out['images'] = [obj(r['key_order'], lambda k: url.get(r['post_id']) if k == 'post' else im.get(r['id']) if k == 'member' else r[k])
                 for r in Q('SELECT * FROM images ORDER BY id')]

def dump(n, d):
    return json.dumps(d, ensure_ascii=False, separators=(',', ':')) if n == 'images' else json.dumps(d, ensure_ascii=False, indent=1)
check = '--check' in sys.argv; diff = 0
for n, d in out.items():
    p = os.path.join(ROOT, 'data', n + '.json'); s = dump(n, d)
    if check:
        old = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
        same = old == s; sem = same or (old and json.loads(old) == d)
        print(f'{n}.json: {"逐字节一致" if same else "语义一致（格式不同）" if sem else "不一致!"} ({len(s.encode())} bytes)')
        diff += not sem
    else:
        open(p, 'w', encoding='utf-8').write(s); print(f'写出 data/{n}.json ({len(d)} 条)')
sys.exit(1 if diff else 0)
