# 人工复核数据（curation）

这里放的是**必须由人判断、以后还会不断增补**的结论，不是抓取结果。

抓取和推导逻辑在 `db/task*.py` 里；那些脚本只负责「找候选」和「算」，**结论一律从这里读**。
所以加一条数据不用碰代码，改错也不会悄悄跑成「什么都没匹配到」——`db/curation_check.py` 会拦。

| 文件 | 管什么 | 对应脚本 | 条目数（2026-10） |
|---|---|---|---|
| `videos.json` | 哪些粉丝影像算数（`song_videos.official=0`） | `task032_unofficial_scan.py` | keep 26 / reject 3 |
| `live_covers.json` | 哪些公演封面拿到了但不能用 | `task029_cover_backfill.py` | reject 10 |
| `live_members.json` | 出演成员推导的例外（整场辞退 / 单人缺场） | `task028_live_members.py` | 5 场 / 1 条 |
| `jackets.json` | 哪首歌用哪张配信 jacket | `task031_song_jacket_fill.py` | 作品 3 / 复用 1 |

> 这些文件是**输入**，数据库是**输出**。手工在 SQLite 里改 `live_members.status` 或
> `songs.cover_image_id` 会被下次重跑覆盖掉——要改就改这里。

---

## videos.json

```json
{"id": "lkWjBhI0H4o", "song": 4, "reason": "Sleeping face 未音源化…"}
```

| 字段 | 说明 |
|---|---|
| `id` | YouTube video_id，11 位 |
| `song` | 这首歌在 `songs.id` 里的编号（不是曲名，用编号才能防同名曲） |
| `reason` | 为什么留 / 为什么否，写给半年后的自己看 |

`keep` 是**白名单**：扫描脚本产出的候选，只有出现在这里才会入库。`reject` 是黑名单，
扫描时直接跳过，省得每次重扫都再人工过一遍同名曲。

## live_covers.json

| 字段 | 说明 |
|---|---|
| `live` | `lives.id` |
| `hint` | 当时的公演名，**只是给人看的**，改了不影响逻辑；和库里不一致会出警告 |
| `reason` | 为什么这张图不能当封面（分享卡 / 登录墙 / 别团 logo …） |

被否决的场次在 `--upload` 和 `--apply` 两个阶段都会跳过，所以图不会进 R2 也不会进库。

## live_members.json

```json
"no_show_lives": [{"live": 123, "reason": "2021-07 新冠自肃，整场辞退"}],
"overrides":     [{"live": 626, "member": "若葉のあ", "status": "休演", "reason": "官方 2024-11-10 告知"}]
```

- `no_show_lives`：整场辞退。成员在籍但当天没上台，会写成「未出演」而不是干脆不写行，
  这样前端能区分「没数据」和「确实没上」。
- `overrides`：单人缺场。`member` 必须写**全名**（`members.name`，不是昵称）；
  `status` 只能是 `出演 / 支援 / 非正式 / 休演 / 未出演`。

## jackets.json

- `albums`：`collection_id` 是 iTunes 的专辑 id（`itunes.apple.com/lookup?id=<id>` 能查到），
  脚本会拉 `1200x1200` 的封面。`songs` 是共用这张 jacket 的歌曲编号。
- `reuse`：库里已经有这张图（`image` 是 `images.id`），同作品的歌直接改指向，不重复下载。

一首歌只能出现在一个地方，重复了校验会报错（只有一个会生效）。

---

## 常见改动

**「这条粉丝视频其实是别的歌 / 不该收」**
把 `videos.json` 里对应的那条从 `keep` 移到 `reject`，补上 reason，然后
`python3 db/task032_unofficial_scan.py --apply`。注意 `--apply` 只增不删——
要从库里删掉已有行得手动 `DELETE FROM song_videos WHERE video_id='…'`。

**「新找到一条粉丝影像」**
先 `python3 db/task032_unofficial_scan.py --scan --ids=<歌曲编号>` 生成候选，
打开 `db/.cache_it/unofficial_videos_extra.json` 确认 video_id，再把它加进 `keep`，
最后 `--apply`。

**「这场公演的封面是错的 / 是主办方 logo」**
`live_covers.json` 的 `reject` 加一条（`live` 用 `lives.id`），再手动清掉已挂的封面：
`UPDATE lives SET cover_image_id=NULL WHERE id=…` 并删掉 `image_lives` 对应行。

**「这场其实有人没上」**
`live_members.json` 的 `overrides` 加一条，然后重跑 `python3 db/task028_live_members.py`
（会清空重建 `live_members`，幂等）。

**「这首歌的封面应该用某张 jacket」**
`jackets.json` 加进 `albums`（新作品）或 `reuse`（库里已有图），跑
`python3 db/task031_song_jacket_fill.py --fetch` → 上传 R2 → `db/r2_images.py add …` → `--apply`。

---

## 校验

```bash
python3 db/curation_check.py            # 有错误返回 1
python3 db/curation_check.py --strict   # 警告也算失败
```

查三类问题：

1. **结构** —— 字段齐不齐、video_id 是不是 11 位、有没有重复、`reason` 有没有写
   （字段名拼错也会被点名，否则数据会静默失效）
2. **引用** —— 指向的公演 / 成员 / 歌曲 / 图片在库里存不存在
3. **一致性** —— JSON 和数据库状态是否对得上。比如「库里有非官方影像但白名单里没有」
   「否决过的封面却又挂上了」「指定了 jacket 但库里封面还不是 jacket 图」

`--apply` 之前跑一遍，比事后翻日志快得多。

`added` 时间没单独存字段——什么时候加的看 `git log -p db/curation/xxx.json` 就行。
