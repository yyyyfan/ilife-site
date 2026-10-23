"""给 song_videos 加「是否官方」标记与上传频道。

原来 song_videos 只有官方影像（MV / Lyric / Live / Dance / Other），
未音源化或有官方 MV 缺失的歌（Ride On!、Shout of Joy 等）在详情页只能看到「未找到官方影像」。
这次允许收录粉丝上传的现场影像，用 official=0 区分，前端做成可切换的两栏。

  python3 db/task032_video_official.py          # 迁移表结构（幂等）
"""
import os
import sqlite3

D = os.path.dirname(os.path.abspath(__file__))
c = sqlite3.connect(os.path.join(D, 'ilife.sqlite'))

cols = {r[1] for r in c.execute('PRAGMA table_info(song_videos)')}
if 'official' not in cols:
    c.execute('ALTER TABLE song_videos ADD COLUMN official INTEGER NOT NULL DEFAULT 1')
    print('+ song_videos.official')
if 'channel' not in cols:
    c.execute('ALTER TABLE song_videos ADD COLUMN channel TEXT')
    print('+ song_videos.channel')
c.commit()

n = c.execute('SELECT COUNT(*) FROM song_videos WHERE official=1').fetchone()[0]
m = c.execute('SELECT COUNT(*) FROM song_videos WHERE official=0').fetchone()[0]
print(f'官方 {n} 条 / 非官方 {m} 条')
