#!/usr/bin/env python3
"""一次性迁移：data/*.json -> db/ilife.sqlite（零数据丢失，迁移后自动做往返校验）。"""
import json, os, re, sqlite3, sys, subprocess
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
DB = os.path.join(D, 'ilife.sqlite')
J = lambda n: json.load(open(os.path.join(ROOT, 'data', n + '.json'), encoding='utf-8'))
if os.path.exists(DB):
    if '--force' not in sys.argv: sys.exit('ilife.sqlite 已存在；如确需重新迁移请加 --force')
    os.remove(DB)
c = sqlite3.connect(DB); c.execute('PRAGMA foreign_keys=ON')
c.executescript(open(os.path.join(D, 'schema.sql'), encoding='utf-8').read())
src = {}
def S(u):
    if u is None: return None
    if u not in src:
        src[u] = c.execute('INSERT INTO sources(url) VALUES(?)', (u,)).lastrowid
    return src[u]
M, E, L, I, T = J('members'), J('eras'), J('lives'), J('images'), J('timeline')
MF = ['kana','birthday','color','hex','joined','note','status','romaji','role','x','x_status','catch','hex_note','support','left','color_source']
mid = {}
for k, m in enumerate(M):
    extra = set(m) - set(MF) - {'name', 'source', 'sources'}
    assert not extra, extra
    cols = {f: m.get(f) for f in MF}; cols['left_'] = cols.pop('left')
    mid[m['name']] = c.execute(
        f"INSERT INTO members(sort,name,source_id,key_order,{','.join(cols)}) VALUES(?,?,?,?{',?'*len(cols)})",
        (k, m['name'], S(m.get('source')), ','.join(m), *cols.values())).lastrowid
    for o, (f, u) in enumerate((m.get('sources') or {}).items()):
        c.execute('INSERT INTO member_fields_sources VALUES(?,?,?,?)', (mid[m['name']], f, S(u), o))
assert list(T) == ['source', 'note', 'members', 'marks'], list(T)
c.execute("INSERT INTO meta VALUES('timeline.source',?)", (T['source'],))
c.execute("INSERT INTO meta VALUES('timeline.note',?)", (T['note'],))
for k, tm in enumerate(T['members']):
    assert list(tm) == ['name', 'segments']
    c.execute('UPDATE members SET tl_sort=? WHERE id=?', (k, mid[tm['name']]))
    for o, s in enumerate(tm['segments']):
        assert set(s) <= {'from','to','type','label','color'}
        c.execute('INSERT INTO member_periods(member_id,ord,type,label,color,date_from,date_to,key_order) VALUES(?,?,?,?,?,?,?,?)',
                  (mid[tm['name']], o, s['type'], s['label'], s.get('color'), s['from'], s['to'], ','.join(s)))
for mk in T['marks']:
    assert list(mk) == ['date', 'label']; c.execute('INSERT INTO timeline_marks(date,label) VALUES(?,?)', (mk['date'], mk['label']))
for k, e in enumerate(E):
    assert list(e) == ['id','name','start','lineup','change','source']
    c.execute('INSERT INTO eras VALUES(?,?,?,?,?,?)', (e['id'], k, e['name'], e['start'], e['change'], S(e['source'])))
    for o, n in enumerate(e['lineup']):
        mm = re.fullmatch(r'(.+?)(?:\((.+)\))?', n)
        c.execute('INSERT INTO era_members VALUES(?,?,?,?)', (e['id'], mid[mm[1]], o, mm[2]))
vid = {}
for l in L:
    assert list(l) == ['id','date','title','venue','pref','source']
    v = (l['venue'], l['pref'])
    if v not in vid: vid[v] = c.execute('INSERT INTO venues(name,pref) VALUES(?,?)', v).lastrowid
    c.execute('INSERT INTO lives VALUES(?,?,?,?,?)', (l['id'], l['date'], l['title'], vid[v], S(l['source'])))
IF = ['url','orig','date','text','category','local','source','kind','era','w','h','match','crop_of','review','review_note','related','pending']
eras_sorted = sorted(E, key=lambda e: e['start'])
for k, i in enumerate(I, 1):
    extra = set(i) - set(IF) - {'post', 'member'}
    assert not extra, extra
    c.execute(f"INSERT INTO images(id,post_id,key_order,{','.join(IF)}) VALUES(?,?,?{',?'*len(IF)})",
              (k, S(i.get('post')), ','.join(i), *[i.get(f) for f in IF]))
    if 'member' in i: c.execute('INSERT INTO image_members VALUES(?,?)', (k, mid[i['member']]))
    ea = [e['id'] for e in eras_sorted if e['start'] <= i['date']]
    if ea: c.execute('INSERT INTO image_eras VALUES(?,?)', (k, ea[-1]))
c.commit()
for t in ['members','member_fields_sources','member_periods','timeline_marks','eras','era_members','venues','lives','images','image_members','image_eras','sources','songs','costumes']:
    print(f'{t:22s}', c.execute(f'SELECT count(*) FROM {t}').fetchone()[0])
c.close()
# 往返校验：导出到临时目录并与现有 data/*.json 逐字节比较
r = subprocess.run([sys.executable, os.path.join(D, 'export.py'), '--check'])
sys.exit(r.returncode)
