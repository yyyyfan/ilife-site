"""016 验收修正脚本公用函数（幂等）。由 <组>-fixes.py 导入；与本文件同目录的 assets/ 存放修正用图片（已按规则转 webp，未裁剪、等比缩放到长边<=2048、<=1MB）。"""
import os, shutil, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KEY_ORDER = 'url,orig,date,post,text,category,local,source,w,h,review,review_note'
class Fixer:
    def __init__(self, argv):
        args = [a for a in argv[1:] if not a.startswith('--')]
        self.dry = '--dry-run' in argv
        self.db = os.path.abspath(args[0] if args else 'db/ilife.sqlite')
        self.root = os.path.dirname(os.path.dirname(self.db))
        self.c = sqlite3.connect(self.db); self.c.execute('PRAGMA foreign_keys=ON')
        self.n = {'DONE': 0, 'ALREADY': 0, 'SKIP': 0}
    def log(self, k, msg): self.n[k] += 1; print(f'{k:7} {msg}')
    def live_ok(self, lid, date, title_prefix):
        r = self.c.execute('SELECT date,title FROM lives WHERE id=?', (lid,)).fetchone()
        if not r or r[0] != date or not r[1].startswith(title_prefix):
            self.log('SKIP', f'live {lid} 不符（期望 {date} {title_prefix}，实际 {r}）'); return False
        return True
    def src_id(self, url):
        r = self.c.execute('SELECT id FROM sources WHERE url=?', (url,)).fetchone()
        return r[0] if r else None
    def era_for(self, date):
        r = self.c.execute('SELECT id FROM eras WHERE start<=? ORDER BY start DESC LIMIT 1', (date,)).fetchone()
        return r[0] if r else None
    def _refresh_cover(self, lid):
        cur = self.c.execute('SELECT cover_image_id FROM lives WHERE id=?', (lid,)).fetchone()[0]
        links = [r[0] for r in self.c.execute('SELECT image_id FROM image_lives WHERE live_id=? ORDER BY ord', (lid,))]
        if cur not in links:
            new = links[0] if links else None
            if not self.dry: self.c.execute('UPDATE lives SET cover_image_id=? WHERE id=?', (new, lid))
            print(f'        live {lid} cover {cur} -> {new}')
    def unbind(self, lid, img_url, why):
        r = self.c.execute('SELECT i.id FROM image_lives il JOIN images i ON i.id=il.image_id WHERE il.live_id=? AND i.url=?', (lid, img_url)).fetchone()
        if not r:
            if self.c.execute('SELECT 1 FROM images WHERE url=?', (img_url,)).fetchone(): self.log('ALREADY', f'unbind live {lid} x {img_url}')
            else: self.log('SKIP', f'unbind live {lid}: 找不到图片 {img_url}')
            return
        iid = r[0]
        if not self.dry: self.c.execute('DELETE FROM image_lives WHERE live_id=? AND image_id=?', (lid, iid))
        self.log('DONE', f'unbind live {lid} x img {iid}：{why}')
        self._refresh_cover(lid)
    def _place(self, asset, lid, year):
        dst_rel = f'img/live-{year}-{lid}-{asset.split(".")[0]}.webp'
        dst = os.path.join(self.root, dst_rel)
        if not self.dry and not os.path.isfile(dst): shutil.copyfile(os.path.join(HERE, 'assets', asset), dst)
        return dst_rel
    def add_image(self, spec):
        """spec: url, date, post(来源URL), text, source, asset, w, h, lid, year. 已存在同 url 的图片则复用。返回 image id。"""
        r = self.c.execute('SELECT id FROM images WHERE url=?', (spec['url'],)).fetchone()
        if r: self.log('ALREADY', f'image {spec["url"]} = {r[0]}'); return r[0]
        pid = self.src_id(spec['post'])
        if pid is None: self.log('SKIP', f'来源不在 sources: {spec["post"]}'); return None
        if self.dry: self.log('DONE', f'(dry) add image {spec["url"]}'); return None
        local = self._place(spec['asset'], spec['lid'], spec['year'])
        iid = self.c.execute('SELECT max(id)+1 FROM images').fetchone()[0]
        self.c.execute('INSERT INTO images(id,url,orig,date,post_id,text,category,local,source,w,h,key_order) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                       (iid, spec['url'], spec['url'], spec['date'], pid, spec['text'], 'official', local, spec['source'], spec['w'], spec['h'], KEY_ORDER))
        era = self.era_for(spec['date'])
        if era: self.c.execute('INSERT INTO image_eras VALUES(?,?)', (iid, era))
        self.log('DONE', f'add image {iid} {local} <- {spec["url"]}')
        return iid
    def replace_image(self, iid, old_url, spec):
        """016 新增行选错了同一原帖/原页面里的另一张图：原地改成正确的那张（只用于 id>=3998 的 016 新增行）。"""
        r = self.c.execute('SELECT url,local FROM images WHERE id=?', (iid,)).fetchone()
        if not r: self.log('SKIP', f'replace img {iid}: 不存在'); return
        if r[0] == spec['url']: self.log('ALREADY', f'replace img {iid}'); return
        if r[0] != old_url: self.log('SKIP', f'replace img {iid}: 当前 url {r[0]} 非预期'); return
        if self.dry: self.log('DONE', f'(dry) replace img {iid}'); return
        local = self._place(spec['asset'], spec['lid'], spec['year'])
        self.c.execute('UPDATE images SET url=?,orig=?,text=?,local=?,w=?,h=? WHERE id=?',
                       (spec['url'], spec['url'], spec['text'], local, spec['w'], spec['h'], iid))
        old = os.path.join(self.root, r[1])
        if r[1] != local and os.path.isfile(old) and not self.c.execute('SELECT 1 FROM images WHERE local=?', (r[1],)).fetchone():
            os.remove(old)
        self.log('DONE', f'replace img {iid}: {r[1]} -> {local}')
    def bind(self, lid, iid, cover=True):
        if iid is None: return
        if self.c.execute('SELECT 1 FROM image_lives WHERE live_id=? AND image_id=?', (lid, iid)).fetchone():
            self.log('ALREADY', f'bind live {lid} x img {iid}')
        else:
            if not self.dry:
                o = self.c.execute('SELECT coalesce(max(ord),0)+1 FROM image_lives WHERE live_id=?', (lid,)).fetchone()[0]
                self.c.execute('INSERT INTO image_lives VALUES(?,?,?)', (lid, iid, o))
            self.log('DONE', f'bind live {lid} x img {iid}')
        if cover and not self.dry:
            cur = self.c.execute('SELECT cover_image_id FROM lives WHERE id=?', (lid,)).fetchone()[0]
            if cur is None: self.c.execute('UPDATE lives SET cover_image_id=? WHERE id=?', (iid, lid)); print(f'        live {lid} cover None -> {iid}')
    def bind_existing(self, lid, img_url, cover=True):
        """按 url 绑定库里已有的图片（不新增图片行）。"""
        r = self.c.execute('SELECT id FROM images WHERE url=?', (img_url,)).fetchone()
        if not r: self.log('SKIP', f'bind live {lid}: 找不到图片 {img_url}'); return
        self.bind(lid, r[0], cover)
    def set_source_label(self, iid, old, new):
        """更正 016 新增图片的 images.source 显示文字（帖子 ID 不变，作者账号已改名/URL 写错账号）。"""
        r = self.c.execute('SELECT source FROM images WHERE id=?', (iid,)).fetchone()
        if not r: self.log('SKIP', f'label img {iid}: 不存在'); return
        if r[0] == new: self.log('ALREADY', f'label img {iid} = {new}'); return
        if r[0] != old or iid < 3998: self.log('SKIP', f'label img {iid}: 当前 {r[0]} 非预期'); return
        if not self.dry: self.c.execute('UPDATE images SET source=? WHERE id=?', (new, iid))
        self.log('DONE', f'label img {iid}: {old} -> {new}')
    def drop_new_image(self, iid, img_url, why):
        """删除 016 新增的图片行（只限 id>=3998、url 一致、且不再被其他演出/歌曲/成员/服装引用），连同 image_eras 与图片文件。"""
        r = self.c.execute('SELECT url,local FROM images WHERE id=?', (iid,)).fetchone()
        if not r:
            self.log('ALREADY', f'drop img {iid}'); return
        if iid < 3998 or r[0] != img_url: self.log('SKIP', f'drop img {iid}: 非 016 新增或 url 不符'); return
        for lid, in self.c.execute('SELECT live_id FROM image_lives WHERE image_id=?', (iid,)).fetchall():
            if not self.dry: self.c.execute('DELETE FROM image_lives WHERE live_id=? AND image_id=?', (lid, iid))
            self.log('DONE', f'unbind live {lid} x img {iid}：{why}')
            if not self.dry: self._refresh_cover(lid)
        refs = sum(self.c.execute(q, (iid,)).fetchone()[0] for q in (
            'SELECT count(*) FROM songs WHERE cover_image_id=?', 'SELECT count(*) FROM image_members WHERE image_id=?',
            'SELECT count(*) FROM costume_images WHERE image_id=?', 'SELECT count(*) FROM costumes WHERE image_id=?'))
        if refs: self.log('SKIP', f'drop img {iid}: 仍有其他引用 {refs}'); return
        if self.dry: self.log('DONE', f'(dry) drop img {iid}'); return
        self.c.execute('DELETE FROM image_eras WHERE image_id=?', (iid,))
        self.c.execute('DELETE FROM images WHERE id=?', (iid,))
        f = os.path.join(self.root, r[1])
        if os.path.isfile(f) and not self.c.execute('SELECT 1 FROM images WHERE local=?', (r[1],)).fetchone(): os.remove(f)
        self.log('DONE', f'drop img {iid} {r[1]}：{why}')
    def drop_orphan_source(self, url, min_id=4314):
        """删除 016 新增（id>=min_id；016 之前 sources 最大 id 为 4313）且已无任何引用的 sources 行。"""
        r = self.c.execute('SELECT id FROM sources WHERE url=?', (url,)).fetchone()
        if not r: self.log('ALREADY', f'drop source {url}'); return
        sid = r[0]
        if sid < min_id: self.log('SKIP', f'drop source {sid}: 016 之前的行，不动'); return
        refs = sum(self.c.execute(q, (sid,)).fetchone()[0] for q in (
            'SELECT count(*) FROM images WHERE post_id=?', 'SELECT count(*) FROM lives WHERE source_id=?', 'SELECT count(*) FROM songs WHERE source_id=?',
            'SELECT count(*) FROM members WHERE source_id=?', 'SELECT count(*) FROM member_fields_sources WHERE source_id=?',
            'SELECT count(*) FROM eras WHERE source_id=?', 'SELECT count(*) FROM costumes WHERE source_id=?'))
        if refs: self.log('SKIP', f'drop source {sid}: 仍有 {refs} 处引用'); return
        if not self.dry: self.c.execute('DELETE FROM sources WHERE id=?', (sid,))
        self.log('DONE', f'drop source {sid} {url}（无引用）')
    def finish(self):
        if not self.dry: self.c.commit()
        print('summary', self.n, '(dry-run)' if self.dry else '')
